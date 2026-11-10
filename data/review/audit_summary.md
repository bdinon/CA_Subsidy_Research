# Audit Summary (Pass 5)

Date: November 8, 2026. Database: 852 records. Records audited: 465.

## Results by tier

| Tier | Scope | Records | Confirmed | Corrected | Unverifiable |
|---|---|---|---|---|---|
| 1 | needs_confirmation, dead or moved links, funding_type other, ambiguous reclass | 195 | 18 | 124 | 53 |
| 2 | Past deadlines on live money programs | 106 | 0 | 96 | 10 |
| 3 | Prevailing wage unclear on live money programs | 77 | 0 | 28 | 49 |
| 4 | Spot check of records marked verified | 87 | 73 | 12 | 2 |

No patch lines were rejected in any tier.

Database after the audit:

- Confidence: 787 verified, 65 needs_confirmation (was 730 and 122 before Tier 1).
- Funding type "other": 7 records, each with a note that nothing is deployable (was 41).
- Past deadlines: 56 records (was 182 before the audit).
- Prevailing wage: 361 true, 335 false, 156 unclear.

## Spot-check correction rate

12 of 85 readable records needed a material correction: **14 percent**. Two records could not be read and are excluded.

| Level | Corrected | Checked |
|---|---|---|
| County | 7 | 23 |
| Private | 3 | 24 |
| State | 1 | 11 |
| City | 1 | 29 |

Kinds of error found:

- **Prevailing wage only (3 records):** Alameda Continuum of Care, Mendocino surplus land and Orange County MHSA capital. Without these, the rate is 9 of 85, or 10.6 percent.
- **Income limits or set-asides (5 records):** state TOD program (60 percent AMI instead of 80), San Mateo County PLHA (an owner-occupied set-aside that does not exist), Capital Impact Partners (an AMI test the lender does not state), SLO Housing Trust Fund (set-aside described as extremely low income instead of special needs), and Anaheim (record said no inclusionary ordinance; one exists).
- **Award or availability (3 records):** San Joaquin HHAP local amounts overstated about four times, Fresno County HOME-ARP capital shown as available when fully committed, and El Dorado welfare exemption cap misstated.
- **Eligibility (1 record):** Community Vision lends to social enterprises as well as nonprofits.

County records had the highest error rate. City code records, mostly density bonus and inclusionary ordinances, were the most reliable.

## Where corrections clustered (all tiers)

- By level: 126 county, 107 city, 19 state, 8 private.
- By county, the most corrected records: San Diego 16, Santa Clara 15, Orange 14, Monterey 13, San Benito 12, San Joaquin 11, Ventura 11, Fresno 10, Sacramento 10. Statewide and regional records had 19.

## Known gaps

- **Missing prevailing wage citations:** 634 records have prevailing wage true or false with no cited rule. No tier covered them. Several spot checks found true values that rest only on the general Labor Code 1720(b) definition, which the Tier 3 rule treats as unclear.
- **Blocked city sites:** about 40 Tier 1 records stay needs_confirmation because the city site blocks automated access.
- **Fields patches cannot change:** program_name and administering_agency. Records needing a manual edit include the Manteca and Richmond names, Nevada County Assessor phone, South Lake Tahoe and Roseville contacts, and the Sonoma County density bonus phone.
- **Sources that are mirrors or news:**
  - **Code mirrors:** some verified records rest on third-party code mirrors (zoneomics, gocodebook) because the official code host blocks access. Examples are Irvine, Corona and Los Banos.
  - **News only:** one verified record, the Ventura County inclusionary postponement, rests on a news article.
- **Possible new records:** Anaheim inclusionary ordinance (Chapter 17.40) and the San Joaquin County HHAP-6 NOFA of October 27, 2026.

## Tier 4 round 2 (November 9, 2026)

Sample: 130 verified records not audited before, county records at 50 percent and city at 25 percent (`make_worklist.py --sample-rate 0.25 --county-weight 2 --fresh`). State and private records were all checked in round 1.

| Result | Records |
|---|---|
| Confirmed | 109 |
| Corrected | 19 |
| Unverifiable | 2 |

Correction rate: 19 of 128, **15 percent**. Two corrections were prevailing wage only (OCHA and San Mateo PBVs, false to true under 24 CFR 983.153(c)); without them, 13 percent.

| Level | Corrected | Checked |
|---|---|---|
| County | 12 | 65 |
| City | 7 | 63 |

Both rounds combined: 31 of 213, **14.6 percent**. County 19 of 88 (22 percent), city 8 of 92 (9 percent).

Most material round 2 corrections: Hayward inclusionary terms (2023 amendment), Contra Costa HOME per-unit limits and PLHA five-year amount, Nevada County Homekey+ and Prohousing Incentive Program reopened, Orange County PLHA uses (no rental development), San Diego inclusionary thresholds, SJRHF per-unit caps, Sunnyvale CDBG cycle, Santa Clara fee fund balance (about $5.5M uncommitted, not $10.4M), Thousand Oaks density bonus incentive scope.

Other changes:

- 22 records dropped from verified to needs_confirmation, most because only a code mirror could be read (source-quality rule added for round 2).
- Normalizer bug fixed: "motel" no longer maps to the interim housing tag. Nine records corrected by patch FIX_motel_tag (not counted in the rate).
- Database now: 765 verified, 87 needs_confirmation; 53 past deadlines; prevailing wage 364 true, 333 false, 155 unclear; 616 true or false values still have no cited basis.

## Tier 4 round 3: all remaining county records (November 9, 2026)

Scope: the 65 county-level verified records no tier had touched (`make_worklist.py --fresh --levels county --sample-rate 1.0`). Every county-level verified record has now been audited.

| Result | Records |
|---|---|
| Confirmed | 44 |
| Corrected | 21 |
| Unverifiable | 0 |

Correction rate: 21 of 65, **32 percent**. Of the 21, 2 were prevailing wage only (HACA and HACCC PBVs, false to true under 24 CFR 983.153(c)) and 4 were project type tags only. Excluding both: 15 of 65, 23 percent.

County records across all three Tier 4 rounds: 40 of 153, **26 percent**. All Tier 4 rounds: 52 of 278, 18.7 percent.

Repeat error patterns:

- **Welfare exemption $20M cap** misdescribed as a cap on limited partnership projects (Rev. and Tax. Code 214(g)(1)(C) caps claims that qualify only on the 90 percent occupancy test). Fixed in Contra Costa, Orange, San Mateo, Santa Clara and Yolo. Alameda (ab54448b8d) and Marin (bca5bdb76f) still carry the old wording but were marked confirmed; they need the same fix.
- **PBV prevailing wage false** where new construction is eligible. Fixed in Alameda, Contra Costa, Orange and San Mateo. Nine other PBV records (Sacramento County, Solano County, Marin, Fairfield, Vacaville, Vallejo, Suisun City, Roseville) are still false without a 983.153 analysis.
- **Density bonus records tagged homeownership only** when the ordinance covers rental (Fresno, San Benito, Santa Cruz).
- **Award figures from older documents**: Riverside gap loan range, Solano trust fund (Tabor Commons approved at different terms), Santa Cruz PBV scoring.

Database now: 762 verified, 90 needs_confirmation; prevailing wage 365 true, 331 false, 156 unclear; 604 true or false values have no cited basis.

## Prevailing wage citation pass and targeted fixes (November 9, 2026)

Every record with prevailing wage true or false now cites a rule. 607 patch lines applied, 0 rejected (change log `audit_changes_20261109_101436.csv`).

| Value change | Records |
|---|---|
| true to unclear | 175 |
| false to unclear | 14 |
| false to true | 8 (PBV records under 24 CFR 983.153(c)) |
| true to false | 6 (CoC and HHAP or BHSA spent on operations only) |
| unchanged, rule now cited | about 400 |

How values were set:

- **Mechanical, by program type (247 records):** density bonus, inclusionary and other requirements (false, Labor Code 1720(a)(1): no public funds); HOME and CDBG (true at 12+ HOME units or 8+ CDBG units); welfare exemption (false, pays no construction cost).
- **Researched (349 records):** program NOFA, guidelines, ordinances and federal or state rules by name.
- **Rules applied consistently:** PLHA formula, BHSA, LHTF match, Surplus Land Act and housing successor funds state no wage rule of their own, so they are unclear unless a local rule exists. Fee waivers and deferrals are unclear (1720(b)(4)). Density bonus records stay false with any SB 35 or AB 2011 streamlining path stated as a condition. Private lender capital is false. Federal and state LIHTC are false (Duncan, 2008; DIR PW 2006-001).
- **Programs with their own rule (true):** MHP and programs using its 7316(e), Homekey and Homekey+, IIG (infrastructure only), Oakland, Berkeley and Hayward loan programs, San Diego County NOFA 2026-03, Santa Clara County loan funds, Fresno Section 108.

Targeted fixes: Alameda and Marin welfare exemption cap wording corrected; eight PBV records set to true under 983.153(c) (Roseville kept true by user decision; its awards are usually 8 units, below the threshold).

Database now: prevailing wage 192 true, 315 false, 345 unclear. No true or false value lacks a basis. 91 unclear values have no basis text.

Follow-ups from this pass:

- Santa Clara County "true" values rest on the County wage policy as quoted in a 2017 Housing Trust Silicon Valley document; County pages are blocked.
- Santa Ana housing funds may carry a Community Workforce Agreement; official text could not be read.
- Marin, Fremont and Walnut Creek trust funds went to unclear only because their sites block access.
- HACSM and HACSJ development funds are true on 42 U.S.C. 1437j(a), applied by the agent without a HUD document confirming it.

## Recommendation

The wider sample did not bring the rate down: 14.6 percent across 213 records, so round 1 was not a small-sample fluke. City code records are near the 10 percent line; county program records are about 22 percent. Before relying on the database for deal screening:

1. County audit, welfare exemption fixes, PBV values and the prevailing wage citation pass are done.
2. Before relying on a "true" or "unclear" prevailing wage value for a live deal, read the program's current NOFA or loan terms; most "unclear" values turn on 1720(c)(5)(E) and project facts.
3. For any program that matters to a live deal, open the source page before relying on award size, AMI or deadline.

## Prevailing wage basis completion and layering fixes (November 9, 2026, afternoon)

Closed two follow-ups: the 91 unclear values with no basis text, and layering notes that said public funds always trigger prevailing wage. 164 patch lines applied, 0 rejected (change logs `audit_changes_20261109_135652.csv` and `audit_changes_20261109_135722.csv`).

| Batch | Scope | Result |
|---|---|---|
| PWM_1 | 57 fee waiver, density bonus, mandate, negative finding and designation records | 28 set false under the rules already applied to those types (1720(a)(1)); 29 kept unclear with a 1720(b)(4) fee basis |
| PWB_1 to 3 | 34 loan, grant, land, bond and rental assistance records, source pages read | 24 confirmed unclear, 8 corrected, 2 unverifiable (CalHFA SNHP, Madera BHSA) |
| PWL_1 | 69 layering notes in 15 counties | Flat "public funds trigger prevailing wage" sentences replaced with the rule, its 1720(c) exemptions and a pointer to prevailing_wage_basis |
| PWC_1 | 4 records | Old 1720(c)(6)(E) numbering updated to (c)(5)(E) |

Value changes from the source reading:

- **True:**
  - Oakland Jobs/Housing Impact Fee. Spent through City loans, which carry the City's own wage requirement.
  - Santa Cruz HACSC PBV. 983.153(c), 9 or more units.
- **False:**
  - Conduit bonds in Napa and Yolo. DIR PW 2006-001 and 2006-020.
  - LISC PLUS. Private capital.
  - Nevada BHSA. No capital use.
  - Roseville land sale. Sold at appraised fair market value.
  - Napa ADU loan. 1720(c)(1).

Fixes outside the prevailing wage fields: MIP and Sonoma CFH layering notes now cite 1720(c)(5)(E), and the Roseville affordability_requirement now reflects the recorded covenant (15 percent lower income for 55 years).

Database now: prevailing wage 194 true, 349 false, 309 unclear. Every record has a basis.

Follow-ups from this pass:

- Napa ADU loan false rests on the County, not the Housing Authority, signing the loan agreement; if the Housing Authority signs, 1720(c)(1) does not apply.
- Sonoma LMIHAF record says the fund is not offered for development, but the FY 2024-25 report shows $3.84 million of development spending.
- Placer Launchpad NOFA LP-002 link returns 404.

## Possible new records follow-up (November 9, 2026, evening)

Of seven candidates, three were already in the database: Riverside County Revolving Loan Fund (4ed0b28b41), Clovis fee deferral (8bc997e0a1), and Yolo Section 18, which sits inside the Yolo County Housing partnerships record (f708a2e83d).

- **Added:**
  - Anaheim Inclusionary Housing Ordinance, Chapter 17.40, with the Resolution 2024-126 in-lieu fee of $10.00 per leasable square foot. Prevailing wage false.
  - Placer County BHSA Integrated Plan FY 2026-29. Housing Interventions total $25.8M over three years, with $6.0M of capital committed to Carriage Court Studios. Prevailing wage unclear.
- **Confirmed:** San Joaquin HHAP-6 (247db77da2). The "October 27 NOFA" is the October 19 NOFA re-saved under a new file name; the deadline of November 20, 2026 is unchanged.
- **Corrected:** Marin 83146f5922. The County's only adopted development fee waiver is for ADUs and JADUs (Board letter of March 11, 2025, through December 31, 2026). The record was renamed by hand to match, and the multifamily negative finding is kept in layering_notes.

Database: 854 records, 765 verified, 89 needs_confirmation. Backup before the merge: `data/backups/programs_before_newrecords_20261109.json`.

Follow-ups:

- **Anaheim:** confirm that the $10 per square foot in-lieu fee has not been updated since 2024.
- **Placer:** find the Board agenda item for the plan certification signed June 25, 2026.
- **Marin:** the official text of the ADU resolution and of the Chapter 22.22 fee reduction was not read.

## City records full spot check (November 9, 2026, night)

Scope: every verified city record that no earlier Tier 4 round had checked, 338 records in 21 batches (`data/review/batches/T4C_*.json`). With the 93 city records sampled earlier, every verified city record has now been spot checked. 338 patch lines applied, 0 rejected (change log `audit_changes_20261109_234409.csv`; one follow-up fix in `audit_changes_20261109_234424.csv`).

| Result | Records |
|---|---|
| Confirmed | 286 |
| Corrected | 47 (13.9 percent) |
| Unverifiable, moved to needs_confirmation | 5 |

Correction rate by batch: highest in San Joaquin (5 of 10), Santa Clara 2 (6 of 13), San Diego (5 of 18) and Alameda 2 (3 of 11). Contra Costa, Fresno, Sacramento and Madera, and San Mateo and El Dorado had none.

What the corrections were:

- **Stale deadlines:** NOFAs described as expected or pending that never opened (San Jose, Stockton, Garden Grove, Manteca, Mountain View and Stockton PIP Round 4).
- **Outdated dollar figures:** fund balances and allocations replaced with FY 2025-26 or adopted-plan figures (Napa funds, Santa Clara CDBG and HOME, San Jose HOME reservation, Corona HOME-ARP, Mountain View Lot 12, Anaheim LMIHAF).
- **Wrong income or code terms:**
  - Oakland Measure U loan cap and 60 percent AMI limit
  - Sunnyvale inclusionary thresholds
  - Petaluma income split
  - San Diego Complete Communities and ADU bonus terms
  - Carlsbad rent cap
  - Capitola in-lieu fee ($25 per square foot, not $10)
  - Tracy density bonus tables
  - Novato 99-year term
  - Thousand Oaks off-site rules
- **Reclassified:** the Davis, Woodland and West Sacramento inclusionary ordinances changed from density bonus to regulatory requirement.

Unverifiable because the source is blocked or gone:

- Anaheim HOME, PLHA and CDBG gap financing (853d7e7f96)
- San Leandro RFP (dec8aca3c5)
- City of Monterey inclusionary (998e609da7)
- Oxnard density bonus (e7e38bd9b1) and Oxnard affordable housing zones (3fedd621ce)

Manual fixes after the apply:

- Renamed Santa Rosa CFF pilot (1a4482981d), Paso Robles fee deferral (bad1e3bae2) and Tracy density bonus (ccd43a5158).
- Moved the Manteca density bonus source to official ecode360.

Database now: 854 records, 760 verified, 94 needs_confirmation.

Follow-ups:

- **San Diego IB 538 expedite (0efcc39e93):** expedite fees are waived for 100 percent affordable projects, so the prevailing wage basis (no fee waiver) should be revisited under 1720(b)(4).
- **Chula Vista Housing Authority bonds (183596192c):** the Otay Ranch II TEFRA example (Res. 2026-092) was a CMFA issuance, not Housing Authority bonds.
- **Nevada City 17.80.220 (f36356c385):** the record says 30 percent of homes at 1,500 square feet or smaller, but the 2025 APR describes 20 percent lower income units. Reconcile.
- **Napa density bonus (d09a3c4ecd):** move source_url to official ecode360.
- **Anaheim gap financing (853d7e7f96):** retry with the anaheim.net browser-header method in the site access notes.
- **Elk Grove (8fd8dede09):** the outcome of the September 23, 2026 fee hearing is still unconfirmed.

### Follow-ups resolved (November 10, 2026)

All six applied through `scripts/apply_audit.py` (patch `FU_city_spotcheck_20261110.jsonl`, change log `audit_changes_20261110_005035.csv`): 5 corrected, 1 confirmed, 0 rejected. Database now 761 verified, 93 needs_confirmation.

- **San Diego IB 538 (0efcc39e93):** IB 538 Section IV.B waives expedite fees for 100 percent affordable projects. The November 9 note saying all fees are paid was wrong. Prevailing wage changed from false to unclear, citing 1720(b)(4) with the 1720(c)(3) de minimis test.
- **Chula Vista (183596192c):** CTCAC staff report CA-25-798 names CMFA as issuer for Otay Ranch II (270 units, $31.22M bond allocation, Dec 10, 2025). Removed it as an Authority example, and the layering note now says JPA issuance still occurs.
- **Nevada City (f36356c385):** the APR treats the 30 percent / 1,500 square foot rule as Housing Element Program 5 and separately cites 17.80.220 as requiring 20 percent lower income units. The record now states both. Code text is still not available (zoneomics has no section text, gocodebook 403).
- **Napa (d09a3c4ecd):** source moved to official ecode360 (17.52.130 at ecode360.com/43397951; Napa's code is client NA4976). Terms confirmed.
- **Anaheim (853d7e7f96):** the A-LHTF Guidelines PDF opens at anaheim.net/DocumentCenter/View/66427 with a Chrome user agent and confirms the HOME, PLHA, $4.6M and $6M figures. Restored to verified. Miraflores and Center of Hope details are flagged in layering_notes as not reopened.
- **Elk Grove (8fd8dede09):** Resolution 2026-202 (Sept 23, 2026) adopted the staff-recommended per square foot fees, and Ordinance 09-2026 passed its second reading Oct 14, 2026. Effective Jan 1, 2027: $3.59 single-unit, $3.29 owner multi-unit, $1.46 rental multi-unit, $2.29 office, $2.15 retail, $0.39 industrial, $1,146.75 per hotel room. Fund uses now include moderate income, and the ordinance adds a local preference authority (16.88.080). Council attachment PDFs open at elkgrove.gov/.../council-meetings/attachments/2026/MM-DD-YY-N-N.pdf even though HTML pages 403.

## Files

- Change logs: `data/review/audit_changes_*.csv` (one per tier).
- Applied patches: `data/review/audit_patches/applied/`.
- Backups before each tier: `data/backups/programs_before_audit_*.json`.
