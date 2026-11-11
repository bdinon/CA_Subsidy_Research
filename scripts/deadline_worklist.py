#!/usr/bin/env python3
"""
Builds the worklist for a deadline refresh (research/prompts/06_deadline_refresh.md).

Selects records that are not closed/inactive and either
  - have a past deadline (deadline_check == past_date), or
  - have a deadline within the next --days days (default 45).

Run scripts/normalize_data.py first so deadline_check is current as of today.
Writes data/review/deadline_worklist.json (a list of {record_id, audit_reason, county_tag, record}).

Usage: python scripts/deadline_worklist.py [--days 45]
"""

import argparse
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=45)
    args = ap.parse_args()
    today = date.today()
    horizon = (today + timedelta(days=args.days)).isoformat()

    records = json.loads((ROOT / "data" / "programs.json").read_text(encoding="utf-8"))
    out = []
    for r in records:
        if r.get("application_cycle") == "closed/inactive":
            continue
        dc = r.get("deadline_check")
        d = r.get("next_deadline_date")
        if dc == "past_date":
            out.append({"record_id": r["record_id"], "audit_reason": "deadline_past",
                        "county_tag": r.get("county_tag"), "record": r})
        elif dc == "future_date" and d and d <= horizon:
            out.append({"record_id": r["record_id"], "audit_reason": "deadline_near",
                        "county_tag": r.get("county_tag"), "record": r})
    out.sort(key=lambda x: (x["county_tag"] or "", x["record_id"]))

    path = ROOT / "data" / "review" / "deadline_worklist.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Today {today.isoformat()}, horizon {horizon}")
    print(f"Records: {len(out)}  {dict(Counter(x['audit_reason'] for x in out))}")
    print(f"By county: {dict(Counter(x['county_tag'] for x in out))}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
