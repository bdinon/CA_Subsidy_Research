#!/usr/bin/env python3
"""
Builds the audit worklist and batch files from data/programs.json.

Tiers (work them in order, stop whenever you like):
  1  needs_confirmation, dead/soft_404/redirected links, funding_type 'other', ambiguous reclass
  2  expired or past deadlines on live money programs
  3  prevailing wage 'unclear' on live money programs
  4  spot-check sample of verified records (all state and private, plus ~8% of the rest, min 2 per county)
  (link_status 'blocked' or 'error' goes to tier 1 only if the record is also in another tier or unverified)

Output: data/review/batches/T{tier}_{county}_{n}.json  (full records plus audit reasons)
        data/review/audit_worklist.json                (index)

Usage: python scripts/make_worklist.py [--batch-size 15] [--sample-rate 0.08] [--seed 7]
"""

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalize_data as nd  # noqa: E402

PROGRAMS_PATH = ROOT / "data" / "programs.json"
REVIEW_DIR = ROOT / "data" / "review"
BATCH_DIR = REVIEW_DIR / "batches"

MONEY = {"tax credit", "bond", "grant", "loan", "rental assistance", "land", "tax abatement", "fee waiver"}


def ambiguous_reclass(r):
    """True if the program name matches rules for 2+ different funding types."""
    hits = set()
    name = r.get("program_name", "")
    for new, field, rx in nd.RULES:
        if field == "name" and re.search(rx, name, re.I):
            hits.add(new)
    return len(hits) >= 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-size", type=int, default=15)
    ap.add_argument("--sample-rate", type=float, default=0.08)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--fresh", action="store_true", help="tier 4: skip records that already have last_audited")
    ap.add_argument("--levels", default="", help="tier 4: comma list of levels to sample (default all)")
    ap.add_argument("--county-weight", type=float, default=1.0, help="tier 4: multiply the sample rate for county-level records")
    args = ap.parse_args()

    programs = json.loads(PROGRAMS_PATH.read_text(encoding="utf-8"))
    rng = random.Random(args.seed)
    tiers = defaultdict(dict)  # tier -> record_id -> (record, [reasons])

    def add(tier, r, reason):
        rid = r["record_id"]
        for t in range(1, tier):  # already handled in a better tier
            if rid in tiers[t]:
                tiers[t][rid][1].append(reason)
                return
        tiers[tier].setdefault(rid, (r, []))[1].append(reason)

    for r in programs:
        live = r["application_cycle"] != "closed/inactive"
        money = r["funding_type"] in MONEY
        ls = r.get("link_status")
        if r["confidence"] == "needs_confirmation":
            add(1, r, "needs_confirmation")
        if ls in ("dead", "soft_404", "redirected"):
            add(1, r, f"link_{ls}")
        if ls in ("blocked", "error") and r["confidence"] == "needs_confirmation":
            add(1, r, f"link_{ls}")
        if r["funding_type"] == "other":
            add(1, r, "funding_type_other")
        if ambiguous_reclass(r):
            add(1, r, "reclass_ambiguous")
        if r.get("deadline_check") == "past_date" and live and money:
            add(2, r, "deadline_past")
        if r["prevailing_wage_trigger"] == "unclear" and live and money:
            add(3, r, "prevailing_wage_unclear")

    claimed = {rid for t in tiers.values() for rid in t}
    verified = [r for r in programs if r["confidence"] == "verified" and r["record_id"] not in claimed]
    if args.fresh:
        verified = [r for r in verified if not r.get("last_audited")]
    if args.levels:
        keep = {x.strip() for x in args.levels.split(",")}
        verified = [r for r in verified if r["level"] in keep]
    sample = {r["record_id"] for r in verified if r["level"] in ("state", "private")}
    by_group = defaultdict(list)
    for r in verified:
        if r["record_id"] not in sample:
            by_group[(r["county_tag"], r["level"] == "county")].append(r)
    for (county, is_county), rows in sorted(by_group.items()):
        rate = args.sample_rate * (args.county_weight if is_county else 1.0)
        k = max(1, round(len(rows) * min(rate, 1.0)))
        for r in rng.sample(rows, min(k, len(rows))):
            sample.add(r["record_id"])
    for r in verified:
        if r["record_id"] in sample:
            add(4, r, "spot_check")

    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    for old in BATCH_DIR.glob("T*.json"):
        old.replace(old.with_suffix(".json.old"))  # keep, never delete
    index = []
    for tier in sorted(tiers):
        grouped = defaultdict(list)
        for rid, (r, reasons) in tiers[tier].items():
            grouped[r["county_tag"]].append((r, reasons))
        for county in sorted(grouped):
            rows = grouped[county]
            for n in range(0, len(rows), args.batch_size):
                chunk = rows[n:n + args.batch_size]
                bid = f"T{tier}_{re.sub(r'[^A-Za-z0-9]+', '', county)}_{n // args.batch_size + 1}"
                payload = [{"audit_reasons": reasons, "record": r} for r, reasons in chunk]
                (BATCH_DIR / f"{bid}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
                index.append({"batch_id": bid, "tier": tier, "county": county, "records": len(chunk)})
    (REVIEW_DIR / "audit_worklist.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

    print("Records per tier:", {t: len(v) for t, v in sorted(tiers.items())})
    print("Batches per tier:", dict(Counter(b["tier"] for b in index)))
    print("Total batches:", len(index), "  total records:", sum(len(v) for v in tiers.values()))
    reasons = Counter(x for t in tiers.values() for _, rs in t.values() for x in rs)
    print("Reasons:", dict(reasons))


if __name__ == "__main__":
    main()
