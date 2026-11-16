# CA Subsidy Research

See CLAUDE.md for rules. Counties in scope are listed in data/jurisdictions.json.

Run order: 01_state_level (once), 02_county_level (per county), 03_city_level (per city),
04_private_philanthropic (per region), 07_federal_national (once). After each pass run
normalize_data.py, validate_schema.py and build_report.py.

Add a county later: add it to data/jurisdictions.json, run passes 02 and 03 for it only, run
04 if it is in a new region, then re-run the three scripts.

Check script behavior after any script change: `python scripts/backtest.py` (see backtest.md).
