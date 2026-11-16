# Pass 7: Federal and National Sources

Run once. Re-run when a federal program changes materially. Federal money that reaches
developers only through the state, a county or a city (HOME, CDBG, National Housing Trust Fund,
HOME-ARP, CoC) is already recorded at that level; do not duplicate it here.

## Task

Research federal programs a developer applies to or uses directly for affordable multifamily
housing in California. Read `data/SCHEMA.md` first.

Starting points to check (confirm each one is current on the agency site; do not add a record
from this list alone):

- HUD Office of Multifamily Housing: FHA mortgage insurance for new construction and
  substantial rehab, and for refinance or acquisition of existing properties; Section 202
  Supportive Housing for the Elderly capital advances; Section 811 capital advances
- HUD Office of Recapitalization: Rental Assistance Demonstration and other conversion tools,
  and any current retrofit or preservation grant or loan program
- USDA Rural Development multifamily programs (direct and guaranteed rural rental housing, farm
  labor housing loans and grants, multifamily preservation). Record which target counties have
  eligible rural areas.
- CDFI Fund programs that reach housing developers through awardees (note who the awardees are
  in this footprint)
- Federal tax incentives other than LIHTC that apply to affordable multifamily (only if a current
  official source describes their use for this product)

## Instructions

1. Use the federal agency page or the Federal Register, not a secondary summary. Note any
   California field office or state office contact.
2. Fill every schema field. Use `level: "federal"`, `county_tag: "statewide"` (or the county for
   a county-specific eligibility map), `research_pass: "7_federal"`.
3. Prevailing wage: Davis-Bacon applicability depends on the program statute; cite the rule in
   `prevailing_wage_basis` or leave `unclear`.
4. In `layering_notes`, say how the program is combined with 4 percent and 9 percent credits,
   CDLAC bonds and state programs, and any known conflicts (for example rent or income rules
   that differ from CTCAC).
5. Append to `data/programs.json`, checking for duplicates first.
6. When done, run in order: `python scripts/normalize_data.py`, `python scripts/validate_schema.py`
   (fix anything it flags), `python scripts/build_report.py`.

## Output check

If a program is authorized but has no current funding or open window, record it with
`application_cycle: "closed/inactive"` and say so in `cycle_notes`, rather than leaving it out.
