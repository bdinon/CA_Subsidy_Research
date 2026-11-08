# Pass 1: State-Level Subsidy Sources (California, statewide)

Run this once. It does not need to be repeated when new counties are added, since these
programs apply statewide.

## Task

Research and document every California state-level subsidy, financing, or incentive program
available for affordable multifamily housing development. Read `data/SCHEMA.md` first for the
exact record format, then append validated records to `data/programs.json`.

Cover, at minimum, these known program families, and search for others you find while
researching each agency's site:

- **CTCAC (California Tax Credit Allocation Committee)**: 9% and 4% Low-Income Housing Tax
  Credits, State LIHTC. Get current per-unit caps, scoring criteria highlights, and application
  round dates.
- **CDLAC (California Debt Limit Allocation Committee)**: private activity bond allocation for
  4% deal pairing.
- **HCD (Department of Housing and Community Development)**: Affordable Housing and
  Sustainable Communities (AHSC), Infill Infrastructure Grant (IIG), Multifamily Housing Program
  (MHP), Veterans Housing and Homelessness Prevention (VHHP), Housing for a Healthy California,
  Portfolio Reinvestment Program, Homekey (if still active for multifamily-eligible product).
- **CalHFA**: Mixed-Income Program (MIP), Special Needs Housing Program, permanent and
  construction/perm loan products usable alongside tax credits.
- **Strategic Growth Council**: Affordable Housing and Sustainable Communities if not already
  captured under HCD, Transformative Climate Communities if it touches housing.
- **CalHFA/CDLAC/CTCAC coordination programs**: anything specifically designed to layer with
  9%/4% deals (e.g. state tax credit "gap" programs).
- Any statewide property tax related benefit relevant to affordable housing ownership
  structures (e.g. the Welfare Exemption for low-income housing, and how it's administered
  even though the county assessor executes it).

## Instructions

1. For each program, go to the actual agency page (HCD, CTCAC, CDLAC, CalHFA), not a
   secondary summary site. Pull current NOFA/QAP cycle dates if published.
2. Fill out every field in the schema. Use `county_tag: "statewide"`.
3. Note in `layering_notes` which programs are commonly stacked together (e.g. 4% credits +
   CDLAC bonds + AHSC + MIP is a common capital stack) and which have mutually exclusive
   eligibility.
4. Flag prevailing wage triggers accurately. This matters a lot for underwriting.
5. Append records to `data/programs.json`. Do not overwrite existing unrelated records.
6. When done, run `python scripts/validate_schema.py` and fix anything it flags.

## Output check

Before finishing, confirm you have distinct records (not one combined blob) for at least:
CTCAC 9%, CTCAC 4%, CDLAC bonds, HCD AHSC, HCD IIG, HCD MHP, HCD VHHP, CalHFA MIP.
