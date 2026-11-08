# CA Subsidy Research

Database of affordable multifamily subsidy sources (state, county, city, private) for
Brandon's target California counties. Source of truth is `data/programs.json`.

## Read first
- `data/SCHEMA.md`: field definitions and research rules. Follow them on every record.
- `data/jurisdictions.json`: counties and priority cities in scope.

## How work is run
- Prompts live in `research/prompts/` (01 state, 02 county, 03 city, 04 private).
- Replace `{{COUNTY_NAME}}` and `{{CITY_NAME}}` before running a pass.
- After every pass, run `python scripts/validate_schema.py` and fix all errors.
- Regenerate outputs with `python scripts/build_report.py` (needs pandas and openpyxl).

## Hard rules
- Open and read each agency page. Never invent a source_url.
- Mark `confidence: "verified"` only if the page was actually opened this pass.
- Update existing records in place. No duplicates (program_name + jurisdiction).
- Keep closed or defunded programs, tagged `closed/inactive`.
- Do not hand-edit anything in `output/`. It is regenerated.
- Writing style for any report text: concise, direct, no em dashes, no exclamation points, no emojis.
