# CA Subsidy Research

Database of affordable multifamily subsidy sources (state, county, city, private, federal) for
Brandon's target California counties. Source of truth is `data/programs.json`.

## Read first
- `data/SCHEMA.md`: field definitions, enums, and editing rules. Follow them on every record.
- `data/jurisdictions.json`: counties and priority cities in scope.

## Research passes
- Prompts in `research/prompts/`: 01 state, 02 county, 03 city, 04 private (per region), 05 audit,
  06 monthly deadline refresh (scheduled cloud routine; opens a PR with patch files, apply
  locally after merge), 07 federal and national.
- The monthly routine runs on the 1st from `main` on GitHub. Prompt or script changes take
  effect only after they are pushed to `main`.
- Site access routes for blocked agency sites: `research/site_access_notes.md`.
- Open recheck items live in `data/review/recheck.json` (record_id, due, check). The refresh
  worklist script reads it.
- Replace `{{COUNTY_NAME}}`, `{{CITY_NAME}}` and `{{REGION}}` before running a pass.
- New records must use the v2 schema: enum funding_type, enum application_cycle with detail in
  cycle_notes, lowercase string prevailing_wage_trigger, tag list in eligible_project_types
  with free text in eligible_project_detail.
- After every research pass run, in order:
  1. `python scripts/normalize_data.py`  (adds record_id to new records, tags, deadline dates; safe to re-run)
  2. `python scripts/validate_schema.py`
  3. `python scripts/build_report.py`  (needs pandas and openpyxl)
- After any script change, run `python scripts/backtest.py` (see `backtest.md`).

## Audit
- Follow `research/prompts/05_audit.md`. Batches go to the `audit-batch` subagent
  (`.claude/agents/audit-batch.md`), which writes patch files only. Only
  `scripts/apply_audit.py` edits `data/programs.json` during an audit.
- Scripts: `link_check.py`, `make_worklist.py`, `apply_audit.py`.
- Review files and logs are in `data/review/`. Backups are in `data/backups/`. Never delete them.

## Hard rules
- Open and read each agency page. Never invent a source_url.
- `confidence: "verified"` only if an official page was actually opened and read in that pass.
- Third-party code mirrors (zoneomics, gocodebook) are for finding text only. A record whose only
  readable source is a mirror stays `needs_confirmation`, with the blocked official hosts named in
  `audit_note`.
- Sending a normal browser user agent or Accept header to a public page is allowed. Do not solve,
  evade or script around Cloudflare challenges, CAPTCHAs or logins.
- Set prevailing_wage_trigger to true or false only with a cited rule in prevailing_wage_basis.
- Update existing records in place. No duplicates (record_id, or program_name plus jurisdiction).
- `record_id` never changes after it is assigned, including when a record is renamed.
- In `next_deadline`, write the submit-by date first. Start with "No open round as of <date>" or
  "No application deadline;" when there is none. Other dates go after it or in `cycle_notes`.
- Keep closed or defunded programs, tagged `closed/inactive`.
- Do not hand-edit anything in `output/`. It is regenerated.
- When answering a question about a live deal, give the record's `last_audited` date and open the
  source page before relying on award size, AMI, deadline or prevailing wage. Audited county
  records needed material corrections at about 26 percent, city records about 9 percent.
- Writing style for any report text: concise, direct, no em dashes, no exclamation points, no emojis.

## Changelog
- 2026-11-15. Review model: Fable 5.2. Implement model: Opus 5.5. Items applied (all 12 from the
  project review): deadline date takes the submit-by date and ignores "No open" text;
  refresh worklist adds `no_open_round` and reads `recheck.json`; record_id assigned once and
  never re-hashed; apply_audit rejects confirmed or corrected lines without sources and verified
  on mirror-only sources; mirror rule, validate warnings and `mirror_source` audit reason;
  prompts 01 to 04 updated for the v2 flow and regions; new prompt 07 federal and national;
  recheck items moved to `data/review/recheck.json`; matrix gets Record ID and Prevailing Wage
  Basis columns; dead validate warning fixed; `audit-batch` subagent; CLAUDE.md rules above;
  memory index shortened, `.json.old` batch files untracked, region label updated.
  Backup of the prior file: `CLAUDE.backup-2026-11-15.md`. Backtest: `backtest.md`.
