# Program Record Schema

Every entry in `programs.json` is an object with these fields. Required fields are marked.
Use `null` for anything genuinely unknown after a good-faith search, don't guess.

```json
{
  "program_name": "string, required",
  "administering_agency": "string, required",
  "level": "state | county | city | federal | private, required",
  "jurisdiction": "string, required, e.g. 'Sacramento County', 'City of Davis', 'Statewide'",
  "funding_type": "tax credit | bond | grant | loan | fee waiver | tax abatement | density bonus | other, required",
  "typical_award_size": "string, e.g. '$500K-$3M per project' or '$50,000/unit cap'",
  "per_unit_cap": "string or null",
  "affordability_requirement": "string, e.g. '20% at 50% AMI' or '100% at 60% AMI'",
  "eligible_project_types": ["new construction", "acquisition-rehab", "preservation", "adu", "supportive housing"],
  "application_cycle": "rolling | annual NOFA | biennial | closed/inactive, required",
  "next_deadline": "string date or 'unknown, verify with agency'",
  "prevailing_wage_trigger": "true | false | unclear",
  "layering_notes": "string: known compatibility/incompatibility with other programs, timing conflicts, gap-funding order",
  "source_url": "string, required, must be the actual agency page, not a secondary aggregator",
  "date_researched": "YYYY-MM-DD, required",
  "confidence": "verified | needs_confirmation (verified means source_url was actually opened and read this pass)",
  "research_pass": "1_state | 2_county | 3_city | 4_private",
  "county_tag": "string or null, which county in jurisdictions.json this applies to, for filtering. Use 'statewide' for Pass 1 records."
}
```

## Rules for the researching agent

1. Never fabricate a `source_url`. If you can't find a live, working agency page for a program, mark `confidence: "needs_confirmation"` and note why in `layering_notes`.
2. Don't duplicate state-level programs (TCAC, CDLAC, HCD, CalHFA) once per county. They get `county_tag: "statewide"` and are entered once in Pass 1.
3. If a program has separate NOFAs or terms per county/city, create a separate record per jurisdiction rather than one record with a combined note.
4. Programs that are closed, defunded, or fully allocated with no new rounds expected should still be recorded with `application_cycle: "closed/inactive"`. Useful negative information, don't just omit them.
5. Before appending, check for an existing record with the same `program_name` + `jurisdiction` and update it in place instead of creating a duplicate.
