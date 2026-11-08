# Pass 4: Private and Philanthropic Sources

Run this once for the full region (all 12 counties), then again only if you expand into a new
region entirely. Most CDFIs and foundations active here operate regionally, not per-county.

## Task

Research CDFIs, foundation program-related investments (PRIs), and other private capital
sources active in affordable multifamily housing in Northern California / Bay Area / Sacramento
Valley / Central Valley. Read `data/SCHEMA.md` first.

Look for:

- **CDFIs active in the region**: e.g. Low Income Investment Fund (LIIF), Enterprise Community
  Loan Fund, Local Initiatives Support Corporation (LISC), Century Housing, California Community
  Reinvestment Corporation (CCRC), Housing Trust Silicon Valley (if footprint extends to San
  Mateo), Northern California Community Loan Fund
- **Foundation PRIs and grants specifically targeting affordable housing production** in this
  region, not general operating grants to nonprofits
- **Bank community reinvestment (CRA) linked debt or equity products**, where a lender has a
  named affordable housing production program with defined terms
- **Regional or statewide affordable housing equity funds** beyond LIHTC syndication, if any
  operate distinctly in this footprint

## Instructions

1. For each source, document typical deal size, whether they do debt, equity, or grants, and
   geographic footprint confirmation (some claim statewide but concentrate deals in specific
   metros, note that if you find it).
2. Fill every schema field. Use `level: "private"` and `county_tag: "regional"` unless a source
   is specific to one county.
3. `application_cycle` for private sources is often "rolling" but confirm rather than assume.
4. Append to `data/programs.json`, checking for duplicates first.
5. Run `python scripts/validate_schema.py` when done.

## Output check

Private capital sources are the easiest to overstate. Only include a source if you found a
live program page or recent (within ~2 years) deal announcement confirming they're actively
deploying in this region, not just a general national CDFI with no confirmed regional activity.
