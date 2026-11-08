# Pass 2: County-Level Subsidy Sources

Run this once per county. When a new county gets added to `data/jurisdictions.json`, re-run
this pass scoped to just that county. Existing counties don't need to be redone.

## Target county for this run

`{{COUNTY_NAME}}`: replace with the specific county before handing this off. Pull the
county's `county_housing_authority` and `notes` fields from `data/jurisdictions.json` for
context before starting.

## Task

Research and document every county-level (not city, not state) subsidy, financing, or
incentive program available for affordable multifamily housing in `{{COUNTY_NAME}}` County.
Read `data/SCHEMA.md` first for the exact record format.

Look for:

- **County housing trust fund or affordable housing fund**, if one exists, including how it's
  capitalized (inclusionary in-lieu fees, real estate transfer tax, general fund allocation)
- **HOME Investment Partnerships Program and CDBG** allocations administered directly by the
  county (some counties are direct HUD entitlement recipients, others go through the state,
  check which applies)
- **County-issued mortgage revenue bonds or multifamily housing bonds**
- **County housing authority programs**: project-based vouchers, HAP contracts usable in
  underwriting, county-specific rental assistance that can support debt service
- **County density bonus or fee reduction ordinances** that apply countywide (distinct from
  individual city ordinances, covered in Pass 3)
- **County property tax related programs**, e.g. how the Welfare Exemption is processed by
  this specific county assessor, any local property tax abatement joint powers authority
- **Regional/county-level continuum of care or homelessness funding** if it extends to
  permanent supportive multifamily housing
- Any county-specific NOFA calendar or annual action plan (check the county's HUD-mandated
  Annual Action Plan / Consolidated Plan, these documents list every federal pass-through
  program the county runs)

## Instructions

1. Start at the county housing authority / community development department website named in
   `jurisdictions.json`.
2. Pull the most recent Consolidated Plan or Annual Action Plan PDF if available. These are
   the single best index of what a county actually funds each year.
3. Fill every schema field. Use `county_tag: "{{COUNTY_NAME}}"` and `level: "county"`.
4. Note in `layering_notes` how each county program is typically combined with state 9%/4%
   deals in this market.
5. Append to `data/programs.json`, checking for existing duplicate records first per the rule
   in `SCHEMA.md`.
6. Run `python scripts/validate_schema.py` when done.

## Output check

If you find zero county-administered programs beyond pass-through HOME/CDBG, say so
explicitly in a summary note rather than leaving the county thin without explanation. That is
a real and useful finding, not a failed search.
