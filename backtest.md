# Backtest set

Created 2026-11-15 by the project review (review model: Fable 5.2). Keep this file. Re-run it at
each model release or setup change and compare scores.

All six tasks have answers already recorded in this repo, so they can be scored without new
research. Tasks 1 to 6 are deterministic (script behavior). None of them measures how well a model
researches a live agency page; the Tier 4 spot-check rate in `data/review/audit_summary.md`
(14.6 percent overall, 26 percent county) remains the measure for that.

Run it with `python scripts/backtest.py` (exit code 1 if any task fails). BT2 needs
`data/backups/`, which is not in git, so it is skipped on a fresh clone.

## Tasks and known answers

### BT1 Deadline date extraction
Input: `next_deadline` text of 12 records, evaluated as of 2026-11-11.
Expected `next_deadline_date` (the date an applicant must submit by, or null):

| record_id | Expected | Source of the known answer |
|---|---|---|
| 62fad77d98 | 2026-12-07 | deadline_refresh_2026-11.md (Nov 23 is the question deadline) |
| e323261aa8 | 2027-01-11 | deadline_refresh_2026-11.md (Nov 30 is a question deadline) |
| c4c3170fac | 2027-01-15 | audit_summary.md, Deadline refresh 2026-11-10 |
| 247db77da2 | 2026-11-20 | deadline_refresh_2026-11.md |
| 64db10b2dc | 2026-11-19 | deadline_refresh_2026-11.md |
| 68e0dc751f | 2026-12-10 | deadline_refresh_2026-11.md |
| 6e33f1967b | 2026-11-20 | deadline_refresh_2026-11.md |
| 155974291b | null | text starts "No open local round" |
| a4e3ed5aee | null | text starts "No open developer or sponsor round" |
| 1bd8f7ea7f | null | text starts "No open round" |
| 019fa873d8 | null | text starts "No open City round"; Dec 8 is a hearing |
| ce5d41a532 | null | text starts "No application deadline"; Nov 21 is a comment period |

### BT2 record_id survives a rename
Input: the three records renamed by hand on 2026-11-10 (aec15a86fe, 343b5d5dac, 23bd3a2dd9), taken
from `data/backups/programs_before_manual_edits_20261110_082639.json`, with the new names applied.
Expected: record_id unchanged after normalize (SCHEMA.md calls it stable).

### BT3 Patch gate
Input: every line in `data/review/audit_patches/applied/` (2,012 lines).
Expected: a `confirmed` or `corrected` line with no `sources_checked` is rejected
(05_audit.md: "confirmed and corrected both require sources_checked"). There are 9 such lines.

### BT4 Refresh worklist covers programs with no open round
Input: `data/programs.json`, worklist built as of 2026-12-01.
Expected: the 15 live state records whose next_deadline starts "No open round" (CTCAC 9 percent
and 4 percent, state credits, CDLAC QRRP, MIP, MHP, Super NOFA, IIG, VHHP, Joe Serna, NHTF, AHSC,
TCC) are on the worklist, so a newly posted 2027 schedule is picked up.

### BT5 New record flow
Input: one valid v2 record with no record_id appended to a scratch copy of programs.json.
Expected: the steps written in the pass prompt end with validation passing.

### BT6 Find a cited record in the Excel matrix
Input: the 25 record_ids cited in `data/review/deadline_refresh_2026-11.md`.
Expected: each can be found in `output/subsidy_matrix.xlsx`.

## Results, 2026-11-15

| Task | Current setup | With proposed fixes |
|---|---|---|
| BT1 | 5 of 12 | 12 of 12 (14 of 854 records change; all 14 reviewed, none worse) |
| BT2 | 0 of 3 ids kept | 3 of 3 |
| BT3 | 0 of 9 caught | 9 of 9 |
| BT4 | 0 of 15 covered, worklist 19 records | 15 of 15 covered, worklist 36 records |
| BT5 | validate fails: missing required field record_id | passes |
| BT6 | 0 of 25 (no record_id column) | 25 of 25 |

Instruction tokens read per monthly routine run: about 14,100 now. About 8,500 of that is
`audit_summary.md`, read only for its "Recheck soon" list. A structured recheck file would cut the
total to about 6,000. The larger BT4 worklist adds research work (17 more records on December 1).

Correction to the BT4 worklist sizes above: Phase 1 held the 45-day window at November 11. On a
rolling window, the December 1 worklist is 31 records under the old setup and 48 with the new
rules, plus 8 due recheck items: 56 in total.

## Results, 2026-11-15, after implementation (Opus 5.5, `scripts/backtest.py`)

| Task | Score |
|---|---|
| BT1 | 12 of 12 |
| BT2 | 3 of 3 |
| BT3 | 9 of 9 |
| BT4 | 15 of 15 (worklist 56 on 2026-12-01) |
| BT5 | 1 of 1 |
| BT6 | 25 of 25 |

No task fell below the Phase 1 "after" score.

## Not covered by this backtest
- Wording changes to prompts 01 to 04 and any new federal or Southern California private pass.
  These need a live research run to score.
- The Sonnet monthly run. The scheduled Opus check on 2026-12-02 scores that.
