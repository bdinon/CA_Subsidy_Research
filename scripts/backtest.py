#!/usr/bin/env python3
"""
Runs the backtest set in backtest.md against the current scripts and data. Read-only: it never
writes to data/ or output/ (BT5 and BT6 use a temp copy).

Usage: python scripts/backtest.py
Exit code 1 if any task scores below its pass mark.
"""

import glob
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_audit as aa  # noqa: E402
import deadline_worklist as dw  # noqa: E402
import normalize_data as nd  # noqa: E402

P = json.loads((ROOT / "data" / "programs.json").read_text(encoding="utf-8"))
BY = {r["record_id"]: r for r in P}
results = []


def score(task, got, total, note=""):
    results.append((task, got, total))
    print(f"{task}: {got} of {total}  {'PASS' if got == total else 'FAIL'}  {note}")


# BT1 deadline extraction, evaluated as of the 2026-11 refresh run
KNOWN = {"62fad77d98": "2026-12-07", "e323261aa8": "2027-01-11", "c4c3170fac": "2027-01-15",
         "247db77da2": "2026-11-20", "64db10b2dc": "2026-11-19", "68e0dc751f": "2026-12-10",
         "6e33f1967b": "2026-11-20", "155974291b": None, "a4e3ed5aee": None, "1bd8f7ea7f": None,
         "019fa873d8": None, "ce5d41a532": None}
ok, missing = 0, []
for rid, want in KNOWN.items():
    if rid not in BY:
        missing.append(rid)
        continue
    got = nd.deadline_fields(BY[rid].get("next_deadline") or "", date(2026, 11, 11))[0]
    ok += got == want
    if got != want:
        print(f"  BT1 {rid}: want {want}, got {got}")
score("BT1 deadline extraction", ok, len(KNOWN), f"(records since edited: {missing})" if missing else "")
# Note: once a refresh rewrites these texts the answers may legitimately change; update KNOWN then.

# BT2 record_id survives a rename (normalize's own loop logic on a renamed copy)
bk = sorted(glob.glob(str(ROOT / "data" / "backups" / "programs_before_manual_edits_*.json")))
if bk:
    old = {r["record_id"]: r for r in json.loads(Path(bk[0]).read_text(encoding="utf-8"))}
    kept = 0
    ids = ["aec15a86fe", "343b5d5dac", "23bd3a2dd9"]
    for rid in ids:
        rec = dict(old[rid], program_name=old[rid]["program_name"] + " (renamed)")
        tmp = Path(tempfile.mkdtemp()) / "p.json"
        tmp.write_text(json.dumps([rec]), encoding="utf-8")
        # run the real normalize on a one-record file
        code = (f"import sys,json; sys.path.insert(0,{str(ROOT / 'scripts')!r}); import normalize_data as nd;"
                f"from pathlib import Path; nd.PROGRAMS_PATH=Path({str(tmp)!r}); nd.BACKUP_DIR=Path({str(tmp.parent)!r});"
                f"nd.REVIEW_DIR=Path({str(tmp.parent)!r}); sys.argv=['x']; nd.main()")
        subprocess.run([sys.executable, "-c", code], capture_output=True)
        kept += json.loads(tmp.read_text(encoding="utf-8"))[0]["record_id"] == rid
        shutil.rmtree(tmp.parent, ignore_errors=True)
    score("BT2 record_id kept on rename", kept, len(ids))
else:
    print("BT2 skipped: data/backups is not present (backups are not in git)")

# BT3 patch gate: sourceless confirmed or corrected lines are rejected
caught = total = 0
for f in glob.glob(str(ROOT / "data" / "review" / "audit_patches" / "applied" / "*.jsonl")):
    for line in open(f, encoding="utf-8"):
        try:
            p = json.loads(line)
        except json.JSONDecodeError:
            continue
        rec = BY.get(p.get("record_id"))
        if rec and p.get("result") in ("confirmed", "corrected") and not p.get("sources_checked"):
            total += 1
            caught += aa.check_patch(p, rec) is not None
score("BT3 sourceless patch lines rejected", caught, total)

# BT4 state 'No open round' programs on the 2026-12-01 worklist
state = [r for r in P if r["level"] == "state" and r["application_cycle"] != "closed/inactive"
         and re.match(r"(?i)\s*no open", r.get("next_deadline") or "")]
wl = dw.build_worklist(P, date(2026, 12, 1), rechecks=dw.load_rechecks())
on = {x["record_id"] for x in wl}
score("BT4 state no-open-round programs covered", sum(1 for r in state if r["record_id"] in on), len(state),
      f"(worklist size {len(wl)})")

# BT5 and BT6 in a temp copy of the repo
work = Path(tempfile.mkdtemp())
try:
    shutil.copytree(ROOT / "scripts", work / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    (work / "data").mkdir()
    shutil.copy(ROOT / "data" / "jurisdictions.json", work / "data")
    new = {"program_name": "BACKTEST Example City Housing Trust Fund", "administering_agency": "City of Example",
           "level": "city", "jurisdiction": "City of Example", "county_tag": "Sacramento", "funding_type": "loan",
           "typical_award_size": "Up to $1,000,000", "per_unit_cap": None, "affordability_requirement": "60% AMI",
           "eligible_project_types": ["new construction"], "eligible_project_detail": ["New construction rental"],
           "application_cycle": "annual NOFA", "cycle_notes": "", "next_deadline": "Applications due March 1, 2027",
           "prevailing_wage_trigger": "unclear", "layering_notes": "", "source_url": "https://example.gov/htf",
           "date_researched": "2026-11-15", "confidence": "needs_confirmation", "research_pass": "3_city"}
    (work / "data" / "programs.json").write_text(json.dumps(P + [new], ensure_ascii=False), encoding="utf-8")

    def run(script):
        return subprocess.run([sys.executable, str(work / "scripts" / script)], capture_output=True,
                              text=True, encoding="utf-8", errors="replace").returncode

    ok5 = run("normalize_data.py") == 0 and run("validate_schema.py") == 0
    score("BT5 new record normalizes and validates", int(ok5), 1)

    if run("build_report.py") == 0:
        from openpyxl import load_workbook
        ws = load_workbook(work / "output" / "subsidy_matrix.xlsx", read_only=True)["All Programs"]
        hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        col = hdr.index("Record ID") if "Record ID" in hdr else None
        found = set()
        if col is not None:
            found = {row[col] for row in ws.iter_rows(min_row=2, values_only=True)}
        cited = sorted(set(re.findall(r"\b[0-9a-f]{10}\b",
                                      (ROOT / "data" / "review" / "deadline_refresh_2026-11.md").read_text(encoding="utf-8"))))
        score("BT6 cited ids findable in matrix", sum(1 for i in cited if i in found), len(cited))
    else:
        score("BT6 cited ids findable in matrix", 0, 1, "(build_report failed)")
finally:
    shutil.rmtree(work, ignore_errors=True)

failed = [t for t, g, n in results if g != n]
print(f"\n{len(results) - len(failed)} of {len(results)} tasks pass.")
sys.exit(1 if failed else 0)
