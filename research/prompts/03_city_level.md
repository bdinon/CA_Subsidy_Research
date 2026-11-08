# Pass 3: City-Level Subsidy Sources

Run this once per city. Use the `priority_cities` list in `data/jurisdictions.json` for each
county to decide which cities to cover. You don't need to cover every incorporated city in a
county. Focus on where deal volume is realistic (the priority list already reflects that).

## Target city for this run

`{{CITY_NAME}}`, `{{COUNTY_NAME}}` County: replace before handing off.

## Task

Research and document city-level subsidy, financing, fee, and zoning-based incentive programs
for affordable multifamily housing in `{{CITY_NAME}}`. Read `data/SCHEMA.md` first.

Look for:

- **Local housing trust fund**, if the city has its own separate from the county's
- **Density bonus ordinance**: local implementation of state density bonus law, check for any
  local enhancements beyond the state minimum
- **Fee waiver or fee deferral programs** for affordable units: building permit fees, impact
  fees, park fees, school fees
- **Local property tax abatement structures**: e.g. city-specific JPA bond structures, welfare
  exemption processing quirks
- **Inclusionary housing in-lieu fee fund**, if the city collects and redeploys these locally
  rather than through the county
- **ADU or missing-middle specific incentive programs** if relevant to your product type
- **Redevelopment successor agency residual funds**: some California cities still have legacy
  RDA successor housing funds being deployed
- **Local NOFA cycles or annual competitive rounds** run directly by the city rather than
  through the county

## Instructions

1. Start at the city's planning department and housing division pages, then check the city
   council's most recent housing element or annual progress report. These often list active
   incentive programs.
2. Fill every schema field. Use `county_tag: "{{COUNTY_NAME}}"`, `level: "city"`, and put the
   city name in `jurisdiction`.
3. Cross-reference against the county-level record for the same fee/program type. Note in
   `layering_notes` if this city's program duplicates, supplements, or conflicts with the
   county program.
4. Append to `data/programs.json`, checking for duplicates first.
5. Run `python scripts/validate_schema.py` when done.

## Output check

If a city has essentially nothing beyond state-mandated density bonus, record that explicitly
as a record with `application_cycle: "closed/inactive"` or a note, rather than silently
skipping the city. That tells you where a market lacks tools other markets have.
