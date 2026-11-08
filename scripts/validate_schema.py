#!/usr/bin/env python3
"""
Validates data/programs.json against the schema in data/SCHEMA.md.
Run after every research pass, before moving on to the next one.

Usage: python scripts/validate_schema.py
"""

import json
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
PROGRAMS_PATH = ROOT / "data" / "programs.json"

REQUIRED_FIELDS = [
    "program_name",
    "administering_agency",
    "level",
    "jurisdiction",
    "funding_type",
    "application_cycle",
    "source_url",
    "date_researched",
    "confidence",
    "research_pass",
    "county_tag",
]

VALID_LEVELS = {"state", "county", "city", "federal", "private"}
VALID_CYCLES_PREFIX = {"rolling", "annual NOFA", "biennial", "closed/inactive"}
VALID_CONFIDENCE = {"verified", "needs_confirmation"}
VALID_PASSES = {"1_state", "2_county", "3_city", "4_private"}


def load_programs():
    if not PROGRAMS_PATH.exists():
        print(f"ERROR: {PROGRAMS_PATH} does not exist.")
        sys.exit(1)
    with open(PROGRAMS_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: programs.json is not valid JSON: {e}")
            sys.exit(1)


def validate(programs):
    errors = []
    warnings = []

    for i, record in enumerate(programs):
        label = f"record #{i} ({record.get('program_name', 'UNNAMED')} / {record.get('jurisdiction', 'NO JURISDICTION')})"

        for field in REQUIRED_FIELDS:
            if field not in record or record[field] in (None, ""):
                errors.append(f"{label}: missing required field '{field}'")

        if record.get("level") and record["level"] not in VALID_LEVELS:
            errors.append(f"{label}: invalid level '{record['level']}'")

        cycle = record.get("application_cycle", "")
        if cycle and not any(cycle.startswith(v) for v in VALID_CYCLES_PREFIX):
            warnings.append(f"{label}: unusual application_cycle value '{cycle}'")

        if record.get("confidence") and record["confidence"] not in VALID_CONFIDENCE:
            errors.append(f"{label}: invalid confidence value '{record['confidence']}'")

        if record.get("research_pass") and record["research_pass"] not in VALID_PASSES:
            errors.append(f"{label}: invalid research_pass value '{record['research_pass']}'")

        url = record.get("source_url", "")
        if url and not url.startswith("http"):
            errors.append(f"{label}: source_url doesn't look like a URL: '{url}'")

    keys = [(r.get("program_name"), r.get("jurisdiction")) for r in programs]
    counts = Counter(keys)
    for k, count in counts.items():
        if count > 1:
            warnings.append(f"Possible duplicate record: program_name='{k[0]}', jurisdiction='{k[1]}' appears {count} times")

    return errors, warnings


def main():
    programs = load_programs()
    print(f"Loaded {len(programs)} records from {PROGRAMS_PATH}")

    errors, warnings = validate(programs)

    if warnings:
        print(f"\n{len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors:
            print(f"  - {e}")
        print("\nFix these before proceeding to the next research pass.")
        sys.exit(1)

    print("\nSchema validation passed.")

    by_level = Counter(r.get("level") for r in programs)
    by_county = Counter(r.get("county_tag") for r in programs)
    print("\nRecords by level:", dict(by_level))
    print("Records by county_tag:", dict(by_county))


if __name__ == "__main__":
    main()
