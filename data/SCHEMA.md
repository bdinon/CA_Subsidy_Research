# Program Record Schema (v2, after cleanup)

Every entry in `programs.json` is an object. Enums are enforced by `scripts/validate_schema.py`.
Use `null` for anything genuinely unknown after a good-faith search. Do not guess.

## Fields

| Field | Rule |
|---|---|
| record_id | Required. Stable 10 char hash. Created by `normalize_data.py`. Never hand-edit. New records get one when normalize is run. |
| program_name | Required string |
| administering_agency | Required string |
| level | `state` `county` `city` `federal` `private` |
| jurisdiction | Required, e.g. `Sacramento County`, `City of Davis`, `Statewide` |
| county_tag | Required. County name, `statewide`, or `regional` |
| funding_type | One of: `tax credit` `bond` `grant` `loan` `fee waiver` `tax abatement` `density bonus` `rental assistance` `land` `zoning incentive` `regulatory requirement` `policy/designation` `negative finding` `other` |
| typical_award_size | String. Dollar figures where published |
| per_unit_cap | String or null |
| affordability_requirement | String, e.g. `20% at 50% AMI` |
| eligible_project_types | List of tags only: `new construction` `acquisition-rehab` `preservation` `supportive housing` `mixed-income` `senior housing` `mixed-use` `adu` `homeownership` `predevelopment` `interim housing` `farmworker housing` `adaptive reuse` `rental assistance` `services/operations` `market-rate (compliance)` `other` |
| eligible_project_detail | List of original free text strings behind the tags. Free text lives here only |
| application_cycle | Exactly one of: `rolling` `annual NOFA` `biennial` `closed/inactive` |
| cycle_notes | Free text detail for the cycle (round dates, program year, conditions) |
| next_deadline | Free text as found |
| next_deadline_date | `YYYY-MM-DD` or null. Earliest future explicit date, else latest past date |
| deadline_check | `future_date` `past_date` `no_date`. Set by script. `past_date` means the audit should look for the next round |
| prevailing_wage_trigger | `true` `false` `unclear` (lowercase strings, never booleans) |
| layering_notes | String. Stacking, compatibility, timing |
| source_url | Required. Real agency page that was opened. Never invented |
| date_researched | `YYYY-MM-DD` |
| confidence | `verified` (page opened and read) or `needs_confirmation` |
| research_pass | `1_state` `2_county` `3_city` `4_private` `5_audit` |
| prevailing_wage_basis | Required when prevailing_wage_trigger is set to true or false by the audit. Names the rule and URL that supports it |
| link_status | Optional. `ok` `redirected` `blocked` `dead` `error`. Set by link_check.py |
| last_audited | Optional `YYYY-MM-DD`. Set by apply_audit.py |
| audit_note | Optional. Why a record is still unconfirmed, or what changed |

## Meaning of funding_type values

- Money or value to the project: `tax credit` `bond` `grant` `loan` `rental assistance` `land` `tax abatement` `fee waiver`
- Entitlement value: `density bonus` `zoning incentive`
- Not a subsidy, kept for context: `regulatory requirement` (inclusionary, linkage fees), `policy/designation` (Prohousing), `negative finding` (searched, nothing exists)
- `other`: unresolved, audit must reclassify

## Rules for any agent editing the database

1. Never fabricate a `source_url`. If no live agency page exists, mark `needs_confirmation` and say why in `audit_note`.
2. State programs are entered once with `county_tag: "statewide"`.
3. Separate records per jurisdiction when terms differ.
4. Keep closed or defunded programs as `closed/inactive`.
5. Check `record_id` or program_name plus jurisdiction before adding. Update in place.
6. `verified` means the source page was opened and read in that pass. Do not mark it from memory or from a search snippet.
7. Do not set `prevailing_wage_trigger` to true or false without a cited rule in the source or in the funding source's published requirements. Otherwise leave `unclear`.
8. After any change run `python scripts/normalize_data.py` then `python scripts/validate_schema.py`.
