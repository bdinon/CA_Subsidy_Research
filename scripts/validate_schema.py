#!/usr/bin/env python3
"""
Validates data/programs.json against data/SCHEMA.md. Strict mode: enums are enforced.
Run after every research pass and after every audit apply.

Usage: python scripts/validate_schema.py
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRAMS_PATH = ROOT / "data" / "programs.json"

REQUIRED_FIELDS = [
    "record_id", "program_name", "administering_agency", "level", "jurisdiction",
    "funding_type", "application_cycle", "source_url", "date_researched",
    "confidence", "research_pass", "county_tag", "prevailing_wage_trigger",
]

VALID_LEVELS = {"state", "county", "city", "federal", "private"}
VALID_FUNDING = {"tax credit", "bond", "grant", "loan", "fee waiver", "tax abatement",
                 "density bonus", "rental assistance", "land", "zoning incentive",
                 "regulatory requirement", "policy/designation", "negative finding", "other"}
VALID_CYCLES = {"rolling", "annual NOFA", "biennial", "closed/inactive"}
VALID_CONFIDENCE = {"verified", "needs_confirmation"}
VALID_PASSES = {"1_state", "2_county", "3_city", "4_private", "5_audit"}
VALID_PW = {"true", "false", "unclear"}
VALID_DEADLINE_CHECK = {"future_date", "past_date", "no_date"}
VALID_TAGS = {"new construction", "acquisition-rehab", "preservation", "supportive housing",
              "mixed-income", "senior housing", "mixed-use", "adu", "homeownership",
              "predevelopment", "interim housing", "farmworker housing", "adaptive reuse",
              "rental assistance", "services/operations", "market-rate (compliance)", "other"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_programs():
    if not PROGRAMS_PATH.exists():
        print(f"ERROR: {PROGRAMS_PATH} does not exist.")
        sys.exit(1)
    try:
        return json.loads(PROGRAMS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: programs.json is not valid JSON: {e}")
        sys.exit(1)


def validate(programs):
    errors, warnings = [], []
    for i, r in enumerate(programs):
        label = f"#{i} {r.get('record_id','?')} ({str(r.get('program_name','UNNAMED'))[:50]} / {r.get('jurisdiction','?')})"

        for f in REQUIRED_FIELDS:
            if f not in r or r[f] in (None, ""):
                errors.append(f"{label}: missing required field '{f}'")

        def enum(field, allowed):
            v = r.get(field)
            if v not in (None, "") and v not in allowed:
                errors.append(f"{label}: invalid {field} '{str(v)[:60]}'")

        enum("level", VALID_LEVELS)
        enum("funding_type", VALID_FUNDING)
        enum("application_cycle", VALID_CYCLES)
        enum("confidence", VALID_CONFIDENCE)
        enum("research_pass", VALID_PASSES)
        enum("prevailing_wage_trigger", VALID_PW)
        if r.get("deadline_check") is not None:
            enum("deadline_check", VALID_DEADLINE_CHECK)

        tags = r.get("eligible_project_types")
        if not isinstance(tags, list) or not tags:
            errors.append(f"{label}: eligible_project_types must be a non-empty list of tags")
        else:
            for t in tags:
                if t not in VALID_TAGS:
                    errors.append(f"{label}: unknown project type tag '{t}'")

        nd = r.get("next_deadline_date")
        if nd is not None and not DATE_RE.match(str(nd)):
            errors.append(f"{label}: next_deadline_date must be YYYY-MM-DD or null, got '{nd}'")
        if not DATE_RE.match(str(r.get("date_researched", ""))):
            errors.append(f"{label}: date_researched must be YYYY-MM-DD")

        url = r.get("source_url", "")
        if url and not str(url).startswith("http"):
            errors.append(f"{label}: source_url is not a URL: '{url}'")

        if r.get("confidence") == "needs_confirmation" and r.get("research_pass") == "5_audit" and not r.get("audit_note"):
            warnings.append(f"{label}: audited but still needs_confirmation with no audit_note")

    ids = Counter(r.get("record_id") for r in programs)
    for k, c in ids.items():
        if c > 1:
            errors.append(f"duplicate record_id {k} appears {c} times")
    keys = Counter((r.get("program_name"), r.get("jurisdiction")) for r in programs)
    for k, c in keys.items():
        if c > 1:
            warnings.append(f"possible duplicate: '{str(k[0])[:60]}' / {k[1]} x{c}")
    if sum(1 for r in programs if r.get("funding_type") == "other"):
        warnings.append(f"{sum(1 for r in programs if r.get('funding_type') == 'other')} records still typed 'other'")
    return errors, warnings


def main():
    programs = load_programs()
    print(f"Loaded {len(programs)} records")
    errors, warnings = validate(programs)

    if warnings:
        print(f"\n{len(warnings)} WARNING(S):")
        for w in warnings[:40]:
            print(f"  - {w}")
        if len(warnings) > 40:
            print(f"  ... and {len(warnings) - 40} more")
    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors[:60]:
            print(f"  - {e}")
        if len(errors) > 60:
            print(f"  ... and {len(errors) - 60} more")
        print("\nFix these before proceeding.")
        sys.exit(1)

    print("\nSchema validation passed.")
    print("By level:", dict(Counter(r["level"] for r in programs)))
    print("By funding type:", dict(Counter(r["funding_type"] for r in programs)))
    print("By confidence:", dict(Counter(r["confidence"] for r in programs)))


if __name__ == "__main__":
    main()
