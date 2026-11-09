#!/usr/bin/env python3
"""
Cleans data/programs.json. Safe to re-run (idempotent).

What it does:
  1. Adds a stable record_id to every record.
  2. Normalizes prevailing_wage_trigger to "true" | "false" | "unclear".
  3. Splits application_cycle into a clean enum (application_cycle) plus cycle_notes.
  4. Reclassifies funding_type "other" using keyword rules, writes a review CSV.
  5. Maps eligible_project_types to a fixed tag list; raw text moves to eligible_project_detail.
  6. Extracts next_deadline_date and deadline_check from the free-text next_deadline.

It never invents facts. Anything it cannot classify is left as-is and listed for the audit pass.

Usage:
  python scripts/normalize_data.py --dry-run     # report only, no write
  python scripts/normalize_data.py               # backs up, then writes
"""

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRAMS_PATH = ROOT / "data" / "programs.json"
BACKUP_DIR = ROOT / "data" / "backups"
REVIEW_DIR = ROOT / "data" / "review"

CYCLE_TYPES = ["closed/inactive", "annual NOFA", "biennial", "rolling"]

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}
DATE_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),?\s+(20\d{2})\b", re.I)
ISO_RE = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")

# Canonical project-type tags. Each raw string is mapped to zero or more tags by keyword.
# Raw text is kept in eligible_project_detail. Unmatched text becomes the tag "other".
TAG_ORDER = ["new construction", "acquisition-rehab", "preservation", "supportive housing",
             "mixed-income", "senior housing", "mixed-use", "adu", "homeownership",
             "predevelopment", "interim housing", "farmworker housing", "adaptive reuse",
             "rental assistance", "services/operations", "market-rate (compliance)", "other"]
TAG_RULES = [
    ("new construction", r"new construction|new development|ground-up|new multifamily|new affordable"),
    ("acquisition-rehab", r"(?<!land )(?<!site )acquisition|rehab"),
    ("preservation", r"preserv|recapitaliz|at-risk|expiring"),
    ("supportive housing", r"supportive|\bpsh\b|homeless|permanent housing"),
    ("mixed-income", r"mixed[- ]income"),
    ("senior housing", r"senior|older adult|elderly"),
    ("mixed-use", r"mixed[- ]use"),
    ("adu", r"\badus?\b|accessory dwelling"),
    ("homeownership", r"homeown|ownership|homebuyer|for-sale|first-time|condominium"),
    ("predevelopment", r"predevelopment|land acquisition|site acquisition"),
    ("interim housing", r"interim|shelter|navigation"),  # not "motel": motel conversions are usually permanent PSH
    ("farmworker housing", r"farmworker|farm worker|agricultural worker"),
    ("adaptive reuse", r"adaptive reuse|commercial[- ]to[- ]residential|office[- ]to[- ]residential"),
    ("rental assistance", r"rental assistance|rapid rehousing|voucher|\btbra\b"),
    ("services/operations", r"public services|^services|operations|public facilities"),
    ("market-rate (compliance)", r"market-rate|nonresidential|compliance"),
]


def derive_tags(raw_values):
    tags = set()
    for raw in raw_values:
        for tag, rx in TAG_RULES:
            if re.search(rx, raw, re.I):
                tags.add(tag)
    if not tags:
        tags.add("other")
    return [t for t in TAG_ORDER if t in tags]


# Ordered rules for funding_type == "other". First match wins.
# Each: (new_type, field, regex)  field is "name" or "award"
RULES = [
    ("negative finding", "award", r"^\s*(negative finding|no (standing|inclusionary|local|active|city|county|housing|known|dedicated)\b)"),
    ("regulatory requirement", "award", r"^\s*requirement\b"),
    ("zoning incentive", "name", r"overlay|streamlined|ministerial|by-right|density transfer|permit streamlining|expedited|combining district|additive zone"),
    ("policy/designation", "name", r"prohousing"),
    ("regulatory requirement", "name", r"inclusionary|linkage fee|housing impact fee|housing mitigation fee|workforce housing ordinance|below market rate housing program"),
    ("rental assistance", "name", r"project[- ]based voucher|\bpbv\b|section 811|continuum of care|\bcoc\b|rental assistance|\bhap\b|vash|mainstream voucher|tenant[- ]based"),
    ("land", "name", r"surplus land|city[- ]owned|county[- ]owned|publicly[ -]owned|town[- ]owned|land trust|land disposition|land bank|\bowned (land|sites?)\b"),
]

# Name-based rules below skip anything that looks like a fund. Funds can be real money
# sources, so they stay "other" and go to the audit pass for a human-level call.
NAME_RULES_SKIP_FUNDS = {"regulatory requirement", "land"}


def make_id(r):
    key = f"{r.get('level','')}|{r.get('jurisdiction','')}|{r.get('program_name','')}".lower()
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def norm_pw(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    s = str(v).strip().lower() if v is not None else ""
    if s in ("true", "yes", "y"):
        return "true"
    if s in ("false", "no", "n"):
        return "false"
    return "unclear"


def split_cycle(raw):
    """Return (enum, notes). Idempotent if raw is already an enum."""
    raw = (raw or "").strip()
    for t in CYCLE_TYPES:
        if raw.lower().startswith(t.lower()):
            rest = raw[len(t):].strip()
            if rest.startswith("(") and rest.endswith(")"):
                rest = rest[1:-1].strip()
            return t, rest
    return raw, ""


def reclass(r):
    name = r.get("program_name", "") or ""
    award = r.get("typical_award_size", "") or ""
    for new, field, rx in RULES:
        text = name if field == "name" else award
        if field == "name" and new in NAME_RULES_SKIP_FUNDS and re.search(r"\bfund\b", name, re.I):
            continue
        if re.search(rx, text, re.I):
            return new, f"{field}:{rx[:40]}"
    return None, None


def parse_dates(text):
    out = []
    for m in DATE_RE.finditer(text or ""):
        try:
            out.append(date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))))
        except ValueError:
            pass
    for m in ISO_RE.finditer(text or ""):
        try:
            out.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    return out


AS_OF_RE = re.compile(r"(?i)as of\s+(?:" + DATE_RE.pattern[2:] + r"|20\d{2}-\d{2}-\d{2})")


NO_ROUND_RE = re.compile(r"(?i)\s*no (open|fixed|standalone|nofa|application deadline)")


def deadline_fields(text, today):
    # "No open round as of <date>" records a check date, not a deadline. Ignore it.
    dates = parse_dates(AS_OF_RE.sub(" ", text or ""))
    if not dates:
        return None, "no_date"
    future = sorted(d for d in dates if d >= today)
    if future:
        return future[0].isoformat(), "future_date"
    # A statement that no round is open lists past dates only as history.
    if NO_ROUND_RE.match(text or ""):
        return None, "no_date"
    return max(dates).isoformat(), "past_date"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD, default is today")
    args = ap.parse_args()
    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()

    programs = json.loads(PROGRAMS_PATH.read_text(encoding="utf-8"))
    stats = Counter()
    reclass_rows, unmapped_types = [], Counter()

    for r in programs:
        # 1 record_id
        rid = make_id(r)
        if r.get("record_id") != rid:
            r["record_id"] = rid
            stats["record_id_added"] += 1

        # 2 prevailing wage
        new_pw = norm_pw(r.get("prevailing_wage_trigger"))
        if r.get("prevailing_wage_trigger") != new_pw:
            stats["prevailing_wage_changed"] += 1
        r["prevailing_wage_trigger"] = new_pw

        # 3 cycle split
        if "cycle_notes" not in r:
            cyc, notes = split_cycle(r.get("application_cycle"))
            if cyc != r.get("application_cycle"):
                stats["cycle_split"] += 1
            r["application_cycle"], r["cycle_notes"] = cyc, notes
        if r["application_cycle"] not in CYCLE_TYPES:
            stats["cycle_unrecognized"] += 1

        # 4 funding type
        if r.get("funding_type") == "other":
            new, rule = reclass(r)
            if new:
                reclass_rows.append([r["record_id"], r["level"], r.get("county_tag"), r["jurisdiction"],
                                     r["program_name"], "other", new, rule])
                r["funding_type"] = new
                stats["funding_reclassified"] += 1

        # 5 project types -> canonical tags, raw text kept in eligible_project_detail
        if "eligible_project_detail" not in r:
            raw = r.get("eligible_project_types") or []
            if isinstance(raw, str):
                raw = [t.strip() for t in raw.split(",") if t.strip()]
            r["eligible_project_detail"] = raw
            r["eligible_project_types"] = derive_tags(raw)
            stats["project_types_tagged"] += 1

        # 6 deadline
        d, status = deadline_fields(r.get("next_deadline") or "", today)
        r["next_deadline_date"], r["deadline_check"] = d, status
        stats[f"deadline_{status}"] += 1

    remaining_other = [r for r in programs if r.get("funding_type") == "other"]
    type_counts = Counter(t for r in programs for t in r["eligible_project_types"])
    other_types = [r for r in programs if r["eligible_project_types"] == ["other"]]

    print(f"Records: {len(programs)}   (as of {today})")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print("Funding types now:", dict(Counter(r["funding_type"] for r in programs)))
    print("Prevailing wage now:", dict(Counter(r["prevailing_wage_trigger"] for r in programs)))
    print("Cycle types now:", dict(Counter(r["application_cycle"] for r in programs)))
    print("Remaining 'other' funding types:", len(remaining_other))
    print("Project type tags:", dict(type_counts))
    print("Records with only tag 'other':", len(other_types))

    if args.dry_run:
        print("\nDry run. Nothing written.")
        return

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if any(v for k, v in stats.items() if not k.startswith("deadline_")):
        shutil.copy(PROGRAMS_PATH, BACKUP_DIR / f"programs_before_normalize_{stamp}.json")

    PROGRAMS_PATH.write_text(json.dumps(programs, indent=2, ensure_ascii=False), encoding="utf-8")

    if reclass_rows:  # only when something changed, so a re-run never wipes the log
        with open(REVIEW_DIR / f"funding_type_reclass_{stamp}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["record_id", "level", "county", "jurisdiction", "program_name", "old", "new", "rule"])
            w.writerows(reclass_rows)
    with open(REVIEW_DIR / "funding_type_other_remaining.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "level", "county", "jurisdiction", "program_name", "typical_award_size"])
        for r in remaining_other:
            w.writerow([r["record_id"], r["level"], r.get("county_tag"), r["jurisdiction"],
                        r["program_name"], (r.get("typical_award_size") or "")[:160]])
    with open(REVIEW_DIR / "project_types_unmapped.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "program_name", "eligible_project_detail"])
        for r in other_types:
            w.writerow([r["record_id"], r["program_name"], " | ".join(r["eligible_project_detail"])])

    print(f"\nWrote {PROGRAMS_PATH}")
    print(f"Review files in {REVIEW_DIR}")


if __name__ == "__main__":
    main()
