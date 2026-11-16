# Site access notes

Collected across research passes. Many agency sites block scripts. Sending a normal browser user agent or Accept header to a public page is allowed; do not solve, evade or script around Cloudflare challenges, CAPTCHAs or logins. Use the alternate routes below. Extract PDFs locally with PyMuPDF, or `pdftotext -layout` if PyMuPDF will not import. curl with a full Chrome user agent often works when a fetch tool fails, and the reverse.

Code mirrors (zoneomics, gocodebook) listed below help find text. They are never the only source for a verified record.

- HCD listing 403s, use /funding/ short URLs
- napacounty.gov Cloudflare-blocked, use services.napacounty.gov agenda PDFs
- Solano via solano.legistar.com
- Contra Costa via ca-contracostacounty3.civicplus.com and the Legistar web API
- Orange County sites open directly
- Alameda via achcd.org and alamedacountyca.gov Board PDFs
- San Mateo via smcgov.org and Legistar API 'sanmateocounty'
- Marin Cloudflare-blocked, use marin.granicus.com and GovDelivery PDFs
- El Dorado sites open, Legistar API client 'eldorado'
- San Diego via curl (WebFetch times out) and Legistar API client 'sdcounty'
- Yolo via public.destinyhosted.com yolocdocs PDFs and ych.ca.gov (yolocounty.gov 403)
- Placer Cloudflare-blocked, use content.govdelivery.com CAPLACER attachments and Legistar 'placerca' (placerca events before July 2026 hold test items only; public.govdelivery.com topics page needs JavaScript)
- Santa Clara santaclaracounty.gov 403, use sccgov.iqm2.com Detail_LegiFile pages and FileOpen attachments plus scchousingauthority.org
- San Joaquin via sjchsa.org documents, sanjoaquincountyca.iqm2.com (&Print=Yes for attachments), hacsj.org and sjcog.org
- San Mateo cities: redwoodcity.org 403 (use meetings.redwoodcity.org and zoneomics), SSF Legistar client ci-ssf-ca, burlingame.org numbered pages, codepublishing 403
- Riverside rivcohws.org and harivco.org 403, use riversidecountyca.iqm2.com (&Print=Yes) and media.rivcocob.org proceedings PDFs
- Fresno via fresnocountyca.gov, Legistar API client fresnocounty (Versions then Texts/{key}) and fresnohousing.org
- San Benito county sites 403, use cosb.granicus.com AgendaViewer and cloudfront packet PDFs
- extract PDFs locally with PyMuPDF
- Nevada via nevadacountyca.gov DocumentCenter and Legistar 'nevco' attachments (docx staff reports)
- SLO slocounty.ca.gov opens but 429s on bursts, no Legistar API
- Monterey and Mendocino Legistar API clients 'monterey' and 'mendocino'
- Merced, Madera, Ventura and Monterey county sites blocked
- Anaheim: anaheim.net DocumentCenter PDFs open with curl using a full Chrome user agent plus Accept: application/pdf, and records.anaheim.net Laserfiche text via POST DocumentService.aspx/GetTextHtmlForPage (repoName CITYOFANAHEIM)
- Sacramento cities: elkgrove.gov PDFs only (council attachments at /council-meetings/attachments/YYYY/MM-DD-YY-N-N.pdf open), Rancho Cordova and Folsom 403 (Folsom via mccmeetingspublic blob PDFs), zoneomics for zoning codes
- City of Napa official code on ecode360 client NA4976 (Title 17 at ecode360.com/43396077)
- Fresno city Legistar API client fresno
- Sunnyvale Legistar client sunnyvaleca
- Fort Bragg Legistar client cityfortbragg
- Thousand Oaks agendas at toaks.primegov.com Portal/Meeting?meetingTemplateId=
- cityofventura.ca.gov/AgendaCenter opens
- Rocklin meetings on rocklin-ca.granicus.com (no Legistar API)
- Roseville affordable housing funds page at roseville.ca.gov/departments/affordable_housing/affordable_housing_funds.php
- Oxnard site, amlegal and municode Cloudflare-blocked; agendas, packets and minutes on CivicClerk (oxnardca.portal.civicclerk.com), public API oxnardca.api.civicclerk.com/v1/Events (OData $filter, 15 per page with $skip) and /v1/Meetings/{id}
- Menlo Park opens via WebFetch but 403 to curl
- housing element compliance from the HCD CSV on data.ca.gov (housing-element-compliance-report)

## Added from deadline refresh 2026-11
- Contra Costa: /8695 redirects to /8695/Federal-Programs-Funds-HOME-and-CDBG; ca-contracostacounty3.civicplus.com works with curl and a Chrome user agent; DocumentCenter PDFs need an Accept: application/pdf header
- Walnut Creek walnutcreekca.gov 403 (Akamai); Council agendas and staff reports open on walnutcreek.granicus.com (ViewPublisher.php?view_id=12, documents via MetaViewer.php); no Legistar client; Concord and Antioch Consortium pages for the NOFA
- San Diego HCDS NOFA page at /content/sdc/sdhcd/community-development/di-nofa.html (curl with Chrome user agent)
- Manteca: ecode360.com/44092704 opens again with curl and a Chrome user agent (was 403 November 10); Title 17 page at manteca.gov/249/Zoning-Ordinance-Title-17; notices at /505; agendas on manteca-ca.granicus.com (view_id=2)
- Stockton: stockton.legistar.com and webapi.legistar.com/v1/stockton work
- Sunnyvale Legistar API client sunnyvaleca works via WebFetch but not curl
- Vallejo has no Legistar API client; long_range_planning and inclusionary_housing paths 404
- Santa Ana PlanetBids portal is JavaScript only, addenda unreadable
- Cloud environment: PyMuPDF may not import; pdftotext is installed and works for PDFs

## Added from recheck 2026-11-15
- Vallejo agendas and minutes are on CivicClerk (vallejoca.portal.civicclerk.com); the public API at vallejoca.api.civicclerk.com/v1/Events and /v1/Meetings/{id} returns agenda, packet and minutes files
- Legistar web API eventitems with AgendaNote=1&MinutesNote=1 can show a passed action and resolution number while the public meeting page still shows "Not available" (draft minutes); cite the API URL
- Contra Costa: www.contracosta.ca.gov/8702 returned 200 to curl with a Chrome user agent on November 15, 2026
- Anaheim: anaheim.gov returns 403 to curl, the same pages on anaheim.net open; Council agendas as HTML at anaheim.granicus.com/AgendaViewer.php?view_id=2&clip_id=N; no Legistar client
- Fresno city Legistar has no 2021 Council matters from about mid-April to October (Ordinance 2021-029 not there); legistar2.granicus.com attachments download with curl
- Community Vision (Ready to Build): FAQ and RFI PDFs are Google Drive links, download via drive.google.com/uc?export=download&id=...
