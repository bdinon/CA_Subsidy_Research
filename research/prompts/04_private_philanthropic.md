# Pass 4: Private and Philanthropic Sources

Run once per region in `data/jurisdictions.json`, then again when a new region is added. Most
CDFIs and foundations operate regionally, not per county.

## Target region for this run

`{{REGION}}`: replace before handing off. The first run (November 8, 2026) covered mainly the
Bay Area and Northern California. Regions with few or no private records as of November 15, 2026:
Southern California and Inland Empire (Orange, San Diego, Riverside, Ventura), Central Coast
(Monterey, San Benito, Santa Cruz, San Luis Obispo), Central Valley (Fresno, Madera, Merced,
San Joaquin), North Coast and Sierra Foothills (Mendocino, Nevada, El Dorado, Placer).

## Task

Research CDFIs, foundation program-related investments (PRIs), and other private capital
sources active in affordable multifamily housing in `{{REGION}}`. Read `data/SCHEMA.md` first.
Check the existing `level: "private"` records before adding; a lender already in the database
gets its footprint updated in place, not a second record.

Look for:

- **CDFIs active in the region**, including regional loan funds and housing trusts specific to
  the target counties, and statewide CDFIs already in the database whose footprint covers it
- **Foundation PRIs and grants specifically targeting affordable housing production** in this
  region, not general operating grants to nonprofits
- **Health system community investment** (hospital systems with housing loan funds)
- **Bank community reinvestment (CRA) linked debt or equity products**, where a lender has a
  named affordable housing production program with defined terms
- **Regional affordable housing equity or acquisition funds** beyond LIHTC syndication

## Instructions

1. For each source, document typical deal size, whether they do debt, equity, or grants, and
   geographic footprint confirmation (some claim statewide but concentrate deals in specific
   metros, note that if you find it).
2. Fill every schema field. Use `level: "private"` and `county_tag: "regional"` unless a source
   is specific to one county.
3. `application_cycle` for private sources is often "rolling" but confirm rather than assume.
4. Append to `data/programs.json`, checking for duplicates first.
5. When done, run in order: `python scripts/normalize_data.py`, `python scripts/validate_schema.py`
   (fix anything it flags), `python scripts/build_report.py`.

## Output check

Private capital sources are the easiest to overstate. Only include a source if you found a
live program page or recent (within about 2 years) deal announcement confirming they are
actively deploying in this region, not just a national CDFI with no confirmed regional activity.
