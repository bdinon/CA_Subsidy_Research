# Deadline refresh 2026-11

Run date: November 11, 2026. Records: 24 (past 0, near 21, recheck 3). Results: 21 confirmed, 1 corrected, 2 unverifiable. Dry run: 0 rejected.

## Deadline changes
- aa68f3b18e CDBG, HOME and ESG entitlements, City of Stockton: "No open round as of November 10, 2026" to "No open round as of November 11, 2026". Removed stale hearing wording; the November 10 Council outcome on the substantial amendment (file 26-1157) is not yet published. No dated deadline changed on any other record.

## Upcoming deadlines confirmed
- 2026-11-13 4c38ec9433 Ready to Build technical assistance (Community Vision)
- 2026-11-19 64db10b2dc, a05f7f39f4, c6334d3f5e, e52ac0a3fc San Diego County NOFA 2026-03
- 2026-11-20 247db77da2 San Joaquin HHAP-6 local NOFA
- 2026-11-20 6e33f1967b Menlo Park BMR Housing Fund NOFA
- 2026-11-21 ce5d41a532 Manteca zoning update comment period (density bonus is a standing requirement)
- 2026-11-23 62fad77d98 Contra Costa technical questions due (application due December 7)
- 2026-12-07 13a9c2c042, 2dd6b23423, 4d562727d9, 50b4b2ad10, 62fad77d98, 86f8392c92, b4695738b3, cb26dce451, fbd2f7b0e8 Contra Costa FY 2027/28 NOFA and Consortium applications
- 2026-12-08 019fa873d8 Stockton Prohousing renewal hearing
- 2026-12-10 68e0dc751f Huntington Beach CDBG and HOME
- 2026-11-12 6f2b1a4e75 Fresno Section 108 Council item 26-1506 (still on final agenda)
- 2027-01-11 e323261aa8 Santa Ana RFP 26-004A (next proposal deadline)

## Unverifiable
- 580a6f688d: Sunnyvale Council November 10 vote on file 26-0862 not published; Legistar matter and calendar show no outcome or minutes.
- 46ca5946a2: Vallejo November 10 second reading outcome not found on an official source; project page PDF unreadable, guessed city paths returned 404, no Legistar client.

## Recheck soon
- 580a6f688d: check Sunnyvale Legistar file 26-0862 after the November 17 meeting or when November 10 minutes post.
- 46ca5946a2: find the Vallejo November 10 adoption result and effective date.
- aa68f3b18e: check Stockton file 26-1157 for passed status once November 10 minutes post.
- 6f2b1a4e75: record the Fresno Council result for the November 12 item.
- Contra Costa PLHA, in-lieu and Summer Lake (13a9c2c042, 50b4b2ad10, 86f8392c92): the NOFA, FAQs and Housing Guidelines name only CDBG-Housing, HOME and Measure X; confirm with DCD before December 7.
- Walnut Creek 4d562727d9: no walnutcreekca.gov page read (403); confirmed through Concord and Antioch Consortium pages only.
- Santa Ana e323261aa8: PlanetBids addenda unreadable (JavaScript portal), unchecked.
- Earlier items still open: Marin ADU waiver 3b88b743dc expiry December 31; Manteca hearing notice; Capitola; TRPA; Oxnard.

## Site access changes
- Contra Costa: /8695 redirects to /8695/Federal-Programs-Funds-HOME-and-CDBG. ca-contracostacounty3.civicplus.com works with curl and a Chrome user agent; DocumentCenter PDFs need an Accept: application/pdf header.
- Walnut Creek walnutcreekca.gov still 403.
- San Diego HCDS NOFA page: /content/sdc/sdhcd/community-development/di-nofa.html (curl with Chrome user agent).
- Manteca: ecode360.com/44092704 now 403; Title 17 page at manteca.gov/249/Zoning-Ordinance-Title-17.
- Stockton: stockton.legistar.com and webapi.legistar.com/v1/stockton work.
- Fresno Legistar API client fresno works with curl. Sunnyvale API client sunnyvaleca works via WebFetch but not curl.
- Vallejo: no Legistar client (cityofvallejo, vallejo not set up); long_range_planning and inclusionary_housing paths 404.
- Santa Ana PlanetBids portal returns no readable content.
- PyMuPDF would not import under python -I here; pdftotext worked for PDFs.
