# Pass 5: Audit and Re-verification

Run after any batch of research passes. Goal: turn unverified records into verified ones,
fix stale data, resolve unclear fields, and measure how accurate the verified records are.

Read `CLAUDE.md` and `data/SCHEMA.md` first.

## Step 0: Prepare (run these yourself, in order)

1. `python scripts/normalize_data.py`
2. `python scripts/link_check.py --apply`   (about 3 to 5 minutes, needs internet)
3. `python scripts/make_worklist.py`
4. Read `data/review/audit_worklist.json` and tell me the batch counts per tier.

Link statuses `blocked` and `error` are not proof a page is dead. Many agency sites block
scripts. Treat those as "open it yourself with the fetch tool".

## Tiers (work in order, report after each tier, wait for my go-ahead before the next)

| Tier | What | Batch files |
|---|---|---|
| 1 | needs_confirmation, dead or moved links, funding_type "other", ambiguous reclass | `data/review/batches/T1_*.json` |
| 2 | past deadlines on live money programs | `T2_*.json` |
| 3 | prevailing wage "unclear" on live money programs | `T3_*.json` |
| 4 | spot-check sample of records currently marked verified | `T4_*.json` |

## How to run a tier

Spawn one subagent per batch file, at most 4 running at once. Give each subagent the
"Per-record checks" and "Patch format" sections below plus its batch file path.

Subagents must NOT edit `data/programs.json`. Each writes exactly one file:
`data/review/audit_patches/<batch_id>.jsonl`, one JSON line per record in its batch.
A record with no patch line is treated as not audited.

When all batches in the tier are done:
1. `python scripts/apply_audit.py --dry-run` and read the summary.
2. `python scripts/apply_audit.py` (applies, backs up, logs changes, re-normalizes, re-validates).
3. If `data/review/audit_patches/rejected.jsonl` has lines, send those records back to a
   subagent to redo with the rejection reason.
4. `python scripts/build_report.py`
5. Reply with: records audited, how many became verified, how many stayed unverified and
   why, the 5 most material corrections (program, field, old, new), and anything odd.

## Per-record checks

Open `record.source_url` with the fetch tool and read the page. If the page is dead, moved,
or blocked, find the current official page on the same agency domain with search and use
that. Never use an aggregator, news article, or PDF copy of unknown origin as the only
source for `verified`.

Look at `audit_reasons` and do the matching work:

- **needs_confirmation**: check `typical_award_size`, `affordability_requirement`,
  `application_cycle`, `next_deadline`, and `eligible_project_types` against the page. If the
  page supports them, set `confidence: "verified"` and list the URLs you read in
  `sources_checked`. If the page is unreachable or does not support the record, leave it
  `needs_confirmation`, set `result: "unverifiable"`, and give the reason.
- **link_dead, link_soft_404, link_redirected**: find the correct page, set `source_url`, and
  re-check the facts on it.
- **funding_type_other, reclass_ambiguous**: choose the best `funding_type` from the enum
  using the meanings in `SCHEMA.md`. Trust funds and housing successor funds that deploy
  loans are `loan`, grants are `grant`. A fund that only collects fees and has nothing
  deployable stays `other` with an `audit_note`. Behavioral Health Services Act records:
  `grant` if the plan funds housing capital or rental subsidy for housing, otherwise
  `other`. Say which in `layering_notes`.
- **deadline_past**: find the next round, or confirm none is open. Write `next_deadline` as
  plain text with explicit dates written as "Month D, YYYY" (the date is extracted from this
  text by script). If no round is open, write "No open round as of <today's date>" and add
  the expected timing if the agency states it. If the program ended, set
  `application_cycle` to `closed/inactive`. Update `cycle_notes` to match.
- **prevailing_wage_unclear**: set `true` or `false` only if the program guidelines, NOFA,
  or an authoritative rule (HCD, DIR, HUD, the statute) states it, and name the rule and
  URL in `prevailing_wage_basis`. If you cannot find a stated rule, leave it `unclear`,
  return `result: "unverifiable"`, and put what you searched in `reason`. Do not infer from
  the funding type alone.
- **spot_check**: these are currently marked verified. Re-read the page and compare award
  size, AMI, cycle, deadline, and prevailing wage. All match: `result: "confirmed"`,
  `set: {}`. Any material difference: `result: "corrected"` with the fix in `set`. A
  material difference means a dollar figure, AMI level, eligibility, or deadline that would
  change a screening decision. Wording differences do not count. Be strict: this tier
  measures how reliable the verified records are.

Rules for every record:
- `confirmed` and `corrected` both require `sources_checked` with the URLs you opened.
- Never mark `verified` from memory, from a search snippet, or from a page you could not read.
- Write plain text. No em dashes, no exclamation points, no emojis.
- Keep `reason` to one sentence.

## Patch format

One JSON object per line:

```
{"record_id": "ab12cd34ef",
 "result": "confirmed",
 "set": {},
 "reason": "Page matches on award, AMI and cycle.",
 "sources_checked": ["https://agency.example.gov/housing"]}
```

`result` is `confirmed`, `corrected`, or `unverifiable`.
`set` may contain only: source_url, typical_award_size, per_unit_cap,
affordability_requirement, eligible_project_types (list of valid tags), eligible_project_detail,
application_cycle (rolling, annual NOFA, biennial, closed/inactive), cycle_notes,
next_deadline, funding_type, prevailing_wage_trigger ("true", "false" or "unclear" as strings),
prevailing_wage_basis, layering_notes, confidence, audit_note.
Do not set `next_deadline_date` or `deadline_check`. The scripts compute them.

## Final report (after tier 4)

Write `data/review/audit_summary.md` with: counts by tier and result, the spot-check
correction rate, which counties or levels had the most corrections, and a recommendation.
If the spot-check correction rate is above 10 percent, recommend widening the sample
(`python scripts/make_worklist.py --sample-rate 0.25`) before relying on the database for
deal screening.
