# Pass 6: Monthly deadline refresh

Runs once a month, usually as a scheduled cloud agent from `main`. Goal: keep `next_deadline`
current for programs with a past deadline or a deadline in the next 45 days, catch newly posted
rounds for programs with no open round, and work the due items in `data/review/recheck.json`.
The run proposes changes as patch files in a pull request. It never edits `data/programs.json`.
The owner reviews the PR, merges it, and runs `scripts/apply_audit.py` locally.

## Read first

- `CLAUDE.md`, `data/SCHEMA.md`
- `research/prompts/05_audit.md`, sections "Per-record checks" (deadline_past) and "Patch format"
- `research/site_access_notes.md` (alternate routes for blocked agency sites)
- `data/review/recheck.json` (open recheck items; do not read `audit_summary.md` for this)

## Steps

1. Set up: `pip install pymupdf pandas openpyxl` if missing. If PyMuPDF will not import,
   use `pdftotext -layout` for PDFs. Create a branch
   `deadline-refresh-YYYY-MM` from `main` (use the run month).
   Preflight: try `git push --dry-run origin HEAD` and fetch two agency hosts from the
   worklist (for example a county site and a Legistar site). If the push is refused or both
   hosts fail with DNS or proxy errors, stop. Do not write patches. Reply with the exact
   errors and that the environment needs full network access and GitHub access for this repo.
2. `python scripts/normalize_data.py` so deadline_check reflects today. Do not commit the
   resulting programs.json or output/ changes; restore them with `git checkout -- data/programs.json output/`
   after step 3.
3. `python scripts/deadline_worklist.py` (writes `data/review/deadline_worklist.json`). It
   already includes due recheck items (audit_reason `recheck`, or a `recheck_note` on a record
   listed for another reason) and `no_open_round` records.
4. Check every record (see "Per record" below). Write one patch line per record to
   `data/review/audit_patches/deadline_YYYY-MM.jsonl`.
5. Validate: every line parses, has record_id, result, set, reason, sources_checked, and
   uses only allowed `set` fields. Then run `python scripts/apply_audit.py --dry-run` and
   confirm 0 rejected. Do NOT run apply_audit without `--dry-run`.
6. Update `data/review/recheck.json`: remove items this run resolved, move the `due` date of
   unresolved items to when the answer should exist, and add new items (record_id, due,
   added, check). Every item needs a record_id that exists in `data/programs.json`.
7. Write `data/review/deadline_refresh_YYYY-MM.md` (format below).
8. Commit only the patch file, the summary file, `data/review/recheck.json` and
   `data/review/deadline_worklist.json`.
   Push the branch and open a pull request against `main` titled
   "Deadline refresh YYYY-MM: N records". Paste the summary into the PR body.
   If a PR cannot be opened, push the branch and say so in the final reply.

## Per record

- `deadline_past`: the deadline has passed. Find the next round, or confirm none is open. If
  the program ended, set `application_cycle` to `closed/inactive`.
- `deadline_near`: confirm the date still stands (extensions, addenda, cancellations). If the
  date is today or earlier, treat it as deadline_past.
- `no_open_round`: the record says no round is open. Check the agency page for a newly posted
  NOFA, schedule or round. If one is posted, write its submit-by date (`corrected`). If not,
  return `confirmed` with `set` containing only `next_deadline`, with the "as of" date moved to
  today and the rest of the text kept. The script uses that date to decide when to check again.
- `recheck`, or any record with a `recheck_note`: do what the note asks (for example, record a
  Council vote result), then update `recheck.json` (step 6).

Writing `next_deadline`:
- Write the submit-by date first. A script takes the first date written as the deadline when it
  is in the future. Release dates, question deadlines, hearings and plan terms come after it or
  go in `cycle_notes`.
- Explicit dates as "Month D, YYYY". A script extracts the date from this text.
- Nothing open: "No open round as of <Month D, YYYY>." plus expected timing only if the agency
  states it.
- Standing requirements (inclusionary, density bonus, fee schedules, Prohousing, ordinances):
  start with "No application deadline;" and keep adoption, effective or hearing dates in
  `cycle_notes`, never in next_deadline. Most past dates found in earlier runs were this case.
- Separate release dates, question deadlines, RFQ deadlines and proposal due dates. Record
  the date an applicant must submit by.
- Update `cycle_notes` to match.

Other fields: change award sizes, AMI levels or eligibility only if the page you read shows
they changed. Leave `confidence` as is, except a needs_confirmation record may become
`verified` if you read an official page that supports it. Do not change
`prevailing_wage_trigger`.

`audit_note`: copy the existing text and append "Deadline refresh <Month D, YYYY>: ...". If it
is null, write just the new sentence.

## Hard rules

- Open and read each page. Never invent a URL. Never mark anything verified from a search
  snippet or memory.
- `confirmed` and `corrected` need `sources_checked` with URLs you actually opened. If no
  official source could be reached, use `unverifiable` with only an `audit_note` in `set`, and
  say what you tried in `reason`.
- Prefer official agency pages, agenda portals (Legistar, Granicus, iqm2, eScribe, CivicClerk,
  PrimeGov) and NOFA PDFs. Sending a normal browser user agent or Accept header to a public page
  is allowed. Do not solve, evade or script around Cloudflare challenges, CAPTCHAs or logins.
- Third-party code mirrors (zoneomics, gocodebook) can help find text but are never the only
  source for `confirmed`, `corrected` or `verified`.
- Put downloaded files in a temp folder outside the repo. Run Python that reads them with `-I`.
- Plain text. No em dashes, no exclamation points, no emojis. `reason` is one sentence.

## Summary file format

```
# Deadline refresh YYYY-MM

Run date: <date>. Records: N (past P, near Q, recheck R). Results: C confirmed, X corrected, U unverifiable. Dry run: 0 rejected.

## Deadline changes
- <record_id> <program_name>: <old next_deadline date or text> to <new>. <one-line why>

## Upcoming deadlines confirmed
- <date> <record_id> <program_name>

## Unverifiable
- <record_id>: <what was tried>

## Recheck soon
- <record_id>: <what to check and when> (same items as the recheck.json changes in this PR)

## Site access changes
- <new working routes or newly blocked sites, for research/site_access_notes.md>
```

## After merge (owner, local)

```
python scripts/apply_audit.py --dry-run
python scripts/apply_audit.py
python scripts/normalize_data.py
python scripts/validate_schema.py
python scripts/build_report.py
```
Then copy the "Site access changes" items into `research/site_access_notes.md` and commit.
Recheck items arrive through `data/review/recheck.json` in the PR; no copying needed.
