# CA Subsidy Research

See CLAUDE.md for rules. Counties in scope are listed in data/jurisdictions.json.

Run order: 01_state_level (once), 02_county_level (per county), 03_city_level (per city),
04_private_philanthropic (once). Validate after each pass. Build outputs when done.

Add a county later: add it to data/jurisdictions.json, run passes 02 and 03 for it only,
then re-run scripts/build_report.py.
