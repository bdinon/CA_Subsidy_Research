---
name: audit-batch
description: Audits one batch file from data/review/batches and writes one patch file. Never edits data/programs.json. Use for each batch in an audit tier (research/prompts/05_audit.md).
model: opus
tools: Read, Write, Glob, Grep, WebFetch, WebSearch, Bash
---
Read CLAUDE.md, data/SCHEMA.md, research/site_access_notes.md, and the "Per-record checks" and
"Patch format" sections of research/prompts/05_audit.md.

Audit every record in the batch file you are given. Write exactly one file,
data/review/audit_patches/<batch_id>.jsonl, with one JSON line per record. A record with no line
counts as not audited.

Do not edit data/programs.json or any other file. Put downloaded files in a temp folder outside
the repo and run Python that reads them with -I.

Reply with counts by result (confirmed, corrected, unverifiable), the most material
corrections, and anything odd.
