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

## Needs_confirmation sweep (November 10, 2026)

All 93 needs_confirmation records audited in 8 county-grouped batches (`data/review/batches/NC_1.json` to `NC_8.json`), applied through `scripts/apply_audit.py` (change log `audit_changes_20261110_012016.csv`): 93 applied, 0 rejected, 297 field changes. 54 corrected (42 upgraded to verified, 12 corrected but left needs_confirmation), 39 unverifiable. Database now 803 verified, 51 needs_confirmation (36 city, 14 county, 1 state).

Why the 51 remain: almost all are blocked official hosts. Municipal code hosts (codepublishing, ecode360, municode, amlegal) and many city sites (anaheim.net, carlsbadca.gov, cityofventura.ca.gov, cityoftracy.org, rocklin.ca.gov, walnutcreekca.gov, countyofmonterey.gov, maderacounty.com, countyofmerced.com, napacounty.gov) returned 403 or Cloudflare challenges. Where only a mirror (zoneomics, gocodebook) had the code text, the record stayed needs_confirmation.

Most material corrections:

- **Fremont impact fee reduction (b548893b8a):** the 50 percent cut applies only to Parkland, Park Facilities and Traffic fees, per deed-restricted unit up to moderate income. Capital and Fire Facilities fees are paid in full.
- **City of Napa fee reduction (3ae88136e6):** pilot adopted Sept 15, 2026 (R2026-111, R2026-112) rescinds R2021-119. Building permit fees cut 100/75/50 percent by income tier, impact fees 100/75 percent for very low/low (250 unit caps), permits July 1, 2026 to Dec 31, 2028. Terms read from the staff draft resolutions; adoption confirmed in Legistar matter history.
- **Lincoln density bonus (12573fd176):** Lincoln has a local chapter, 18.59 (Ord. 881B), cited in the Housing Element. The record said there was none.
- **Oceanside inclusionary and density bonus (7de4d4240b, 04ff5fbbd4):** Coastal Commission approval Feb 5, 2026; Council adoption June 17, 2026, citywide, 7+ units, 15 percent, 55 years.
- **Burlingame fees (b6113a572d):** Ordinance 2046 (March 2, 2026) rates added: rental $17/$21/$31 psf by density, for-sale $36, commercial $7 to $26.
- **Thousand Oaks trust fund and fee deferral (c39bce1dcb, 7dc729615f):** in-lieu fees $25.70/$14.60/$16.80 psf; deferral is open to any development, city fees only, and may have lapsed.
- **Fairfield PBVs (867ada565c):** HUD found a HAP shortfall over $200,000 in December 2025; voucher issuance halted.
- **City of Madera housing successor (547f70b1e1):** FY 2024-25 ACFR fund balance $3,458,285.
- **San Joaquin County land (ca36da736a):** French Camp Veterans Village is not on County land; Homekey+ authorization was July 29, 2025.

Accepted with partial mirror reliance (core facts on official sources, one detail mirror-only, noted in audit_note): Lincoln 12573fd176 (chapter text), Thousand Oaks 8c520e2130 (Article 7), Napa County 1dc55ae94f (90-day refund), Petaluma a3627a554c (amendment history), Burlingame b6113a572d (25.44 exemptions).

Follow-ups:

- **Alameda County boomerang funds (777c6b9680):** tagged closed/inactive, but achcd.org shows HCD still administers Boomerang. Decide whether to reopen.
- **Manual name edits (not settable by patch):** South Lake Tahoe aec15a86fe "adopted December 2024" conflicts with the March 2024 fee schedule; Richmond 343b5d5dac should become a pointer record; City of Santa Cruz 23bd3a2dd9 says "reduced" childcare fee where 100 percent affordable projects may be exempt. RESOLVED Nov 10, 2026 (log `audit_changes_20261110_082639_manual.csv`): SLT date dropped from name; Richmond renamed to a pointer record with County agencies and links to 62fad77d98 and 7b49041303; Santa Cruz renamed to Part 3 density bonus plus Part 4 fee deferrals, childcare claim removed from name and PW basis and flagged in layering notes.
- **Possible new records:** Hollister Housing Trust Guidelines and $300,000 to the HOME revolving loan fund (June 22, 2026); Ventura Chapter 4.240 impact fee deferral (Sept 2024 snippet only). RESOLVED Nov 10, 2026 as updates to existing records, not new records (patch `20261110_followups.jsonl`, logs `audit_changes_20261110_084720.csv` and `_084721_manual.csv`): Hollister a28971818e, Council adopted the guidelines and $300,000 transfer to HOME RLF 809 on June 22, 2026 (5-0, minutes opened), pending HCD review, guideline PDF unreadable; Ventura fc3dd4f637 renamed to Chapter 4.240 Development Impact Fee Deferral Program (adopted October 2024 per Ojai Valley News), details from search excerpts of blocked city PDFs, stays needs_confirmation.
- **Davis Measure W:** certification due Dec 3, 2026; then update 286b3332af and d3c111e44a.
- **Madera County PLHA (19afbbe608):** HCD dashboard shows the housing element not compliant, which bars PLHA awards.

## Older prevailing wage items (Nov 10, 2026)

Three parallel agents, patches `20261110_pw_A/B/C.jsonl`, 16 records corrected, 0 rejected, 44 field changes (log `audit_changes_20261110_085912.csv`). One trigger changed.

- **Santa Clara County (b9423ec8a0, bb49c3e13d, 45a29b9c03, a5cbf8c30d, 9248240ed5, 1ac0881658, 2fe81f006d):** bases now cite Supportive Housing Development Program Guidelines V7 (Board Nov 16, 2021, BOS-2021-168; still applied in the Sept 15, 2026 North 40 Phase II report): State prevailing wage when County funds pay for construction unless otherwise exempt, higher of State and Davis-Bacon with federal funds. Triggers unchanged. HTSV Supportive Housing Fund layering note no longer says unclear. County land stays unclear (V7 silent on conveyances).
- **HACSM and HACSJ (d65d39c7f5, 6d68d56e51, ab0e64f2f1):** HACSM MTW development cites PIH 2011-45 (Davis-Bacon on all MTW-funded development, no unit floor); HACSJ PBVs cite 24 CFR 983.153(c) and 983.4 (nine or more contract units, not existing housing); repositioning cites 1437j(a) for public housing development. RAD supplemental notice URL 404, not checked.
- **Santa Ana (e323261aa8, fb9539f944, c5b437d4e2):** the Community Workforce Agreement (LA/OC Building Trades, effective June 6, 2023) printed as RFP 26-004A Exhibit V covers "any Affordable Housing projects that receive City funds" (Sec. 2.2.4), with prevailing wage (Sec. 5.1), union hiring halls and 30 percent local or targeted hire. LMIHAF fb9539f944 changed unclear to true on the CWA. CWA pages are scans read as images; the Exhibit II sample commitment leaves the Labor Code 1720 call to the developer, noted in the basis.
- **Napa ADU loan (fb882ab07a):** stays false. Loan Agreement, Deed of Trust, Note and Regulatory Agreement run to the County of Napa (guidelines V2, matter 26-308, March 10, 2026); the Housing Authority is not a party, so 1720(c)(1) holds.
- **Sonoma LMIHAF (8b40a193d2):** "not offered for development" removed. FY 2024-25 development spending $3,837,187 (FY 2023-24 $1,316,702); balance $2,509,338 at June 30, 2025, of which $1,509,338 excess surplus; loans receivable $31,242,980. PW stays unclear; housing successor is the CDC, parent of the Housing Authority, so 1720(c)(1) should not be assumed. No FY 2025-26 report posted. funding_type grant may deserve review given the loan portfolio.
- **Placer Launchpad (1d1bc18543):** LP-001 and LP-002 NOFA PDFs removed from the County site; program page kept as source. LP-002 posted Feb 6, 2026, 12 applications, 55 units, $10.55 million requested, four reserved projects $3.25 million. No open round; guideline revisions expected later in 2026.

Follow-ups: Napa ADU layering_notes still cite 2023 search-result terms; Sonoma LMIHAF funding_type; CWA Article 21 term not printed in the RFP.

## Sacramento-area city items (Nov 10, 2026)

Two agents, patches `20261110_sac_city.jsonl` and `20261110_sac_suburbs.jsonl`: 5 corrected, 1 unverifiable (log `audit_changes_20261110_184254.csv`).

- **City of Sacramento HTF linkage fee (77c3590bb3):** FY 2026-27 rates effective July 1, 2026: office $3.35, hotel $3.19, commercial $2.69, manufacturing $2.09, warehouse $0.92 psf (0.49 percent index adjustment). Notice is attached to the City Fees and Charges ArcGIS record (fee ID 3798); the HTF web page still links FY25-26.
- **Housing Impact Fee (7a03511fb5):** FY27 $3.58 / $0.00 / $1.55 confirmed.
- **SHRA lending and bonds (dc4482720d, 3038f76416):** proposed 2027 schedule (Exhibit B, 2027 SHRA budget, SHRC Nov 4, 2026): Round 1 pre-app Jan 4, full app Mar 1, Board/Council June 29, 2027; Round 2 pre-app July 1, full app Sept 1, 2027. Council and Board adoption not confirmed; no 2027 funds-available notice yet. Recheck in December 2026.
- **Folsom AHL (94239692fe):** no NOFA or new loan. Fund 238 used for a $1.55 million Leidesdorff Street site purchase (Res. 11659, 2026) and a $615,000 transfer for Habitat at 300 Persifer (Res. 11467). Fund 238 about $23.85 million projected June 30, 2026.
- **Folsom HTF commercial fee (b5e8f6c802):** $2.13 psf from July 1, 2026 (Res. 11601, 2.43 percent index); Fund 221 about $858,000 projected.
- **Rancho Cordova HTF fee (f0fe655a96):** still needs_confirmation; city site and code host blocked. 2021 KMA County report shows rates matched the pre-2022 County schedule. The Liora (250 affordable units, Anatolia Drive) noted.

Follow-ups: confirm SHRA 2027 schedule adoption and funds-available notice in December 2026; Folsom FY 2026-27 fund tables.

## Files

- Change logs: `data/review/audit_changes_*.csv` (one per tier).
- Applied patches: `data/review/audit_patches/applied/`.
- Backups before each tier: `data/backups/programs_before_audit_*.json`.

## Small cleanups (2026-11-10)

- Napa ADU Forgivable Loan fb882ab07a: layering_notes rewritten from the ADU Guidelines V2 and loan documents (Legistar matter 26-308). Covers escrow disbursement, other financing (Loan Agreement 3(g)), senior liens, due on sale, eligibility limits. The guidelines do not name the funding source.
- Sonoma LMIHAF 8b40a193d2: funding_type grant to loan. FY 2024-25 development spending $3,837,187 vs services $173,658; Note 4 calls the $31,242,980 receivable loans receivable; excess surplus plan names homeownership loans and rental development. Instrument per expenditure not stated, so loan is an inference. Tags now new construction, preservation, homeownership, supportive housing.

## Madera housing element compliance (2026-11-10)

Source: HCD Housing Element Compliance Report on data.ca.gov (CSV updated November 6, 2026). The accountability.ca.gov dashboard (data last updated February 26, 2026) is not a reliable status source; use the HCD CSV.

- Madera County: adopted 6th cycle element received October 20, 2025, found in compliance December 16, 2025. Earlier "not compliant" notes were wrong. Corrected PLHA 19afbbe608 (compliance no longer blocks payment; plan still unfound, stays needs_confirmation) and density bonus 720cc72cc0 (rezones adopted with the element, parcels not identified).
- City of Madera: adopted element received February 6, 2026, reviewed April 7, 2026, Out. Added to PLHA 7523df22f7 (2024-2028 NOFA pays only once compliant) and density bonus af9dcb340f (Builder's Remedy exposure, state fund eligibility).

## Deadline refresh (2026-11-10)

Scope: 76 records (43 open records with past deadlines, 33 with deadlines through December 31, 2026), 8 parallel agents by county, patch files deadline_b1 to b8. Result: 20 confirmed, 56 corrected, 0 unverifiable, 0 rejected. After apply: 0 open records with past deadlines (5 past dates remain, all closed/inactive), 102 future dates.

Main finding: most past deadlines were not missed rounds. About 40 regulatory or incentive records (inclusionary, density bonus, fee schedules, Prohousing) had an ordinance adoption, effective, hearing or reporting date in next_deadline, which the script read as a deadline. These now start "No application deadline" with the dates moved to cycle_notes. Use that wording for standing requirements going forward.

Material corrections:
- San Diego HACSD PBVs e72e35e00b: not offered in NOFA 2026-03; no open round.
- City of San Diego CDBG FY2028 c4c3170fac: December 7, 2026 is the RFP release; proposals due January 15, 2027, RFQ-qualified applicants only.
- Fresno HOME AHD NOFA c254cd9aed: December 14, 2026 was the HUD CPD release; AHD round closed August 31, 2026.
- Fresno Downtown RLF 3af88382e6: December 31, 2026 was a commitment expiry; no Round 3.
- Fresno Infill fee waiver 17ad4295f7: form sunset June 30, 2026; may need closed/inactive if the ordinance also sunset (amlegal 403).
- Santa Rosa density bonus 9d7bdebf03: Chapter 20-31 last amended by Ord. 2025-011, not 2023-006.
- San Rafael Prohousing 1f99eae749: HCD PIP Round 5 open through March 31, 2027.
- Sunnyvale BMR 580a6f688d: effective 30 days after adoption, not 60; proposed $93 psf.
- Fort Bragg 6838c762fe: Council directed a $350,000 MOU (June 22, 2026); ARPA deadline December 31, 2026 stands.
- Santa Cruz BHSA 6de784df42: source now the final FY 2026-29 plan.
- Huntington Beach 5c54e31538: HCD found the adopted element out of compliance August 18, 2026.

Recheck soon: Sunnyvale 580a6f688d and Vallejo 46ca5946a2 Council votes November 10, 2026; Fresno Section 108 6f2b1a4e75 November 12; Stockton CDBG amendment aa68f3b18e; Contra Costa NOFA records December 7 (PLHA, in-lieu and Summer Lake not named in the FY 2027/28 NOFA PDF); Marin ADU waiver 3b88b743dc expiry December 31; Manteca zoning update comment period November 21; Capitola Chapter 18.03 Coastal certification; TRPA Phase 3 vote early 2027; Oxnard inclusionary update (site blocked).
