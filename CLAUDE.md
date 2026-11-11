# CA Subsidy Research

Database of affordable multifamily subsidy sources (state, county, city, private) for
Brandon's target California counties. Source of truth is `data/programs.json`.

## Read first
- `data/SCHEMA.md`: field definitions, enums, and editing rules. Follow them on every record.
- `data/jurisdictions.json`: counties and priority cities in scope.

## Research passes
- Prompts in `research/prompts/`: 01 state, 02 county, 03 city, 04 private, 05 audit, 06 monthly
  deadline refresh (scheduled cloud routine; opens a PR with patch files, apply locally after merge).
- Site access routes for blocked agency sites: `research/site_access_notes.md`.
- Replace `{{COUNTY_NAME}}` and `{{CITY_NAME}}` before running a pass.
- New records must use the v2 schema: enum funding_type, enum application_cycle with detail in
  cycle_notes, lowercase string prevailing_wage_trigger, tag list in eligible_project_types
  with free text in eligible_project_detail.
- After every research pass run, in order:
  1. `python scripts/normalize_data.py`  (adds record_id, tags, deadline dates; safe to re-run)
  2. `python scripts/validate_schema.py`
  3. `python scripts/build_report.py`  (needs pandas and openpyxl)

## Audit
- Follow `research/prompts/05_audit.md`. Subagents write patch files only. Only
  `scripts/apply_audit.py` edits `data/programs.json` during an audit.
- Scripts: `link_check.py`, `make_worklist.py`, `apply_audit.py`.
- Review files and logs are in `data/review/`. Backups are in `data/backups/`. Never delete them.

## Hard rules
- Open and read each agency page. Never invent a source_url.
- `confidence: "verified"` only if the page was actually opened and read in that pass.
- Set prevailing_wage_trigger to true or false only with a cited rule in prevailing_wage_basis.
- Update existing records in place. No duplicates (record_id, or program_name plus jurisdiction).
- Keep closed or defunded programs, tagged `closed/inactive`.
- Do not hand-edit anything in `output/`. It is regenerated.
- Writing style for any report text: concise, direct, no em dashes, no exclamation points, no emojis.
