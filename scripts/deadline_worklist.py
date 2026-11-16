#!/usr/bin/env python3
"""
Builds the worklist for a deadline refresh (research/prompts/06_deadline_refresh.md).

Selects records that are not closed/inactive and match one of:
  - deadline_past   deadline_check == past_date
  - deadline_near   a deadline within the next --days days (default 45)
  - no_open_round   a live annual NOFA or biennial money program whose next_deadline starts
                    "No open ..." or "No NOFA ...", so a newly posted round is picked up.
                    State and private records: every run. Others: when the "as of" date in the
                    text is --stale-days old or more (default 85), oldest first, at most --cap
                    records (default 25).
  - recheck         an item in data/review/recheck.json whose due date has arrived. If the record
                    is already on the list for another reason, the recheck note is attached.

Run scripts/normalize_data.py first so deadline_check is current as of today.
Writes data/review/deadline_worklist.json
(a list of {record_id, audit_reason, county_tag, recheck_note?, record}).

Usage: python scripts/deadline_worklist.py [--days 45] [--stale-days 85] [--cap 25] [--today YYYY-MM-DD]
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalize_data as nd  # noqa: E402

MONEY = {"tax credit", "bond", "grant", "loan", "rental assistance", "land", "tax abatement", "fee waiver"}
NO_OPEN_RE = re.compile(r"(?i)\s*no (open|nofa)\b")
AS_OF_DATE_RE = re.compile(r"(?i)as of\s+(" + nd.DATE_RE.pattern[2:] + r"|20\d{2}-\d{2}-\d{2})")


def as_of_date(r):
    m = AS_OF_DATE_RE.search(r.get("next_deadline") or "")
    if m:
        ds = nd.parse_dates(m.group(1))
        if ds:
            return ds[0]
    # No "as of" date in the text: fall back to the last time anyone looked.
    for f in ("last_audited", "date_researched"):
        try:
            return datetime.strptime(r.get(f) or "", "%Y-%m-%d").date()
        except ValueError:
            continue
    return date(2000, 1, 1)


def load_rechecks(path=ROOT / "data" / "review" / "recheck.json"):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def build_worklist(records, today, days=45, stale_days=85, cap=25, rechecks=()):
    horizon = (today + timedelta(days=days)).isoformat()
    out, stale = {}, []

    def add(r, reason):
        out[r["record_id"]] = {"record_id": r["record_id"], "audit_reason": reason,
                               "county_tag": r.get("county_tag"), "record": r}

    for r in records:
        if r.get("application_cycle") == "closed/inactive":
            continue
        d, dc = nd.deadline_fields(r.get("next_deadline") or "", today)
        if dc == "past_date":
            add(r, "deadline_past")
        elif dc == "future_date" and d <= horizon:
            add(r, "deadline_near")
        elif (dc == "no_date" and r.get("funding_type") in MONEY
              and r.get("application_cycle") in ("annual NOFA", "biennial")
              and NO_OPEN_RE.match(r.get("next_deadline") or "")):
            if r.get("level") in ("state", "private"):
                add(r, "no_open_round")
            elif (today - as_of_date(r)).days >= stale_days:
                stale.append(r)
    for r in sorted(stale, key=as_of_date)[:cap]:
        add(r, "no_open_round")

    by_id = {r["record_id"]: r for r in records}
    for item in rechecks:
        if (item.get("due") or "9999") > today.isoformat():
            continue
        rid = item.get("record_id")
        if rid in out:
            out[rid]["recheck_note"] = item.get("check", "")
        elif rid in by_id:
            add(by_id[rid], "recheck")
            out[rid]["recheck_note"] = item.get("check", "")
        else:
            print(f"WARNING: recheck.json names unknown record_id {rid}")

    return sorted(out.values(), key=lambda x: (x["county_tag"] or "", x["record_id"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=45)
    ap.add_argument("--stale-days", type=int, default=85)
    ap.add_argument("--cap", type=int, default=25)
    ap.add_argument("--today", default=None, help="YYYY-MM-DD, default is today")
    args = ap.parse_args()
    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()

    records = json.loads((ROOT / "data" / "programs.json").read_text(encoding="utf-8"))
    out = build_worklist(records, today, args.days, args.stale_days, args.cap, load_rechecks())

    path = ROOT / "data" / "review" / "deadline_worklist.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Today {today.isoformat()}, horizon {(today + timedelta(days=args.days)).isoformat()}")
    print(f"Records: {len(out)}  {dict(Counter(x['audit_reason'] for x in out))}")
    print(f"With a recheck note: {sum(1 for x in out if x.get('recheck_note'))}")
    print(f"By county: {dict(Counter(x['county_tag'] for x in out))}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
