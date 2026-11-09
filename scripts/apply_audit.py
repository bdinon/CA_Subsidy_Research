#!/usr/bin/env python3
"""
Merges audit patches into data/programs.json. Subagents write patches, only this script edits the database.

Patch file: data/review/audit_patches/<batch_id>.jsonl, one JSON object per line:
  {"record_id": "ab12cd34ef",
   "result": "confirmed" | "corrected" | "unverifiable",
   "set": {"typical_award_size": "...", "confidence": "verified"},
   "reason": "short why",
   "sources_checked": ["https://..."]}

Rules enforced here:
  - only whitelisted fields may be set, enums are checked
  - confidence=verified needs at least one sources_checked URL
  - prevailing_wage_trigger true/false (from unclear) needs set.prevailing_wage_basis
  - next_deadline_date and deadline_check are recomputed, never patched
  - changed source_url clears link_status (it needs a new link check)
Bad lines go to data/review/audit_patches/rejected.jsonl with the reason.

Usage: python scripts/apply_audit.py [--dry-run]
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_schema as vs  # noqa: E402

ALLOWED = {
    "source_url", "typical_award_size", "per_unit_cap", "affordability_requirement",
    "eligible_project_types", "eligible_project_detail", "application_cycle", "cycle_notes",
    "next_deadline", "funding_type", "prevailing_wage_trigger", "prevailing_wage_basis",
    "layering_notes", "confidence", "audit_note",
}
RESULTS = {"confirmed", "corrected", "unverifiable"}


def check_patch(p, rec):
    if rec is None:
        return "unknown record_id"
    if p.get("result") not in RESULTS:
        return "result must be confirmed, corrected or unverifiable"
    s = p.get("set") or {}
    if not isinstance(s, dict):
        return "set must be an object"
    bad = set(s) - ALLOWED
    if bad:
        return f"fields not allowed: {sorted(bad)}"
    if "funding_type" in s and s["funding_type"] not in vs.VALID_FUNDING:
        return f"bad funding_type {s['funding_type']}"
    if "application_cycle" in s and s["application_cycle"] not in vs.VALID_CYCLES:
        return f"bad application_cycle {s['application_cycle']}"
    if "confidence" in s and s["confidence"] not in vs.VALID_CONFIDENCE:
        return f"bad confidence {s['confidence']}"
    if "prevailing_wage_trigger" in s and s["prevailing_wage_trigger"] not in vs.VALID_PW:
        return "prevailing_wage_trigger must be the string true, false or unclear"
    if "eligible_project_types" in s:
        t = s["eligible_project_types"]
        if not isinstance(t, list) or not t or any(x not in vs.VALID_TAGS for x in t):
            return "eligible_project_types must be a list of valid tags"
    if "source_url" in s and not str(s["source_url"]).startswith("http"):
        return "source_url must be http(s)"
    if s.get("confidence") == "verified":
        src = p.get("sources_checked") or []
        if not src or not all(str(u).startswith("http") for u in src):
            return "verified requires sources_checked URLs"
    new_pw = s.get("prevailing_wage_trigger")
    if new_pw in ("true", "false") and rec.get("prevailing_wage_trigger") == "unclear":
        if not (s.get("prevailing_wage_basis") or "").strip():
            return "setting prevailing wage from unclear needs prevailing_wage_basis"
    if p.get("result") == "unverifiable" and s.get("confidence") == "verified":
        return "unverifiable cannot be set to verified"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--programs", default=str(ROOT / "data" / "programs.json"))
    ap.add_argument("--patches-dir", default=str(ROOT / "data" / "review" / "audit_patches"))
    args = ap.parse_args()

    programs_path = Path(args.programs)
    patches_dir = Path(args.patches_dir)
    files = sorted(patches_dir.glob("*.jsonl"))
    files = [f for f in files if f.name != "rejected.jsonl"]
    if not files:
        print("No patch files found.")
        return

    programs = json.loads(programs_path.read_text(encoding="utf-8"))
    by_id = {r["record_id"]: r for r in programs}
    today = date.today().isoformat()
    log, rejected, tally = [], [], Counter()

    for f in files:
        tier = f.stem.split("_")[0]
        for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                p = json.loads(line)
            except json.JSONDecodeError:
                rejected.append({"file": f.name, "line": ln, "error": "invalid JSON", "raw": line[:200]})
                continue
            rec = by_id.get(p.get("record_id"))
            err = check_patch(p, rec)
            if err:
                rejected.append({"file": f.name, "line": ln, "error": err, "patch": p})
                continue
            for field, new in (p.get("set") or {}).items():
                old = rec.get(field)
                if old != new:
                    log.append([rec["record_id"], rec["program_name"][:70], field, json.dumps(old, ensure_ascii=False)[:200],
                                json.dumps(new, ensure_ascii=False)[:200], p.get("reason", ""), "; ".join(p.get("sources_checked") or []), f.name])
                    rec[field] = new
                    if field == "source_url":
                        rec.pop("link_status", None)
            rec["last_audited"] = today
            if p.get("reason") and "audit_note" not in (p.get("set") or {}) and p["result"] == "unverifiable":
                rec["audit_note"] = p["reason"][:300]
            tally[(tier, p["result"])] += 1

    print(f"Patch files: {len(files)}   applied: {sum(tally.values())}   rejected: {len(rejected)}   field changes: {len(log)}")
    for (tier, res), n in sorted(tally.items()):
        print(f"  {tier} {res}: {n}")
    t4 = tally[("T4", "confirmed")] + tally[("T4", "corrected")]
    if t4:
        print(f"Spot-check correction rate: {tally[('T4', 'corrected')]}/{t4} = {tally[('T4', 'corrected')] / t4:.0%}")

    if args.dry_run:
        print("Dry run. Nothing written.")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backups = programs_path.parent / "backups"
    backups.mkdir(exist_ok=True)
    shutil.copy(programs_path, backups / f"programs_before_audit_{stamp}.json")
    programs_path.write_text(json.dumps(programs, indent=2, ensure_ascii=False), encoding="utf-8")

    review = programs_path.parent / "review"
    review.mkdir(exist_ok=True)
    with open(review / f"audit_changes_{stamp}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["record_id", "program", "field", "old", "new", "reason", "sources_checked", "patch_file"])
        w.writerows(log)
    if rejected:
        with open(patches_dir / "rejected.jsonl", "a", encoding="utf-8") as fh:
            for x in rejected:
                fh.write(json.dumps(x, ensure_ascii=False) + "\n")
        print(f"Rejected lines appended to {patches_dir / 'rejected.jsonl'}. Send them back for redo.")

    applied_dir = patches_dir / "applied"
    applied_dir.mkdir(exist_ok=True)
    for f in files:
        f.rename(applied_dir / f"{stamp}_{f.name}")

    if programs_path == ROOT / "data" / "programs.json":
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "normalize_data.py")], check=False)
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "validate_schema.py")], check=False)


if __name__ == "__main__":
    main()
