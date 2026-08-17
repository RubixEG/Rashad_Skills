MODULE:
EVIDENCE_INDEX

STATUS:
AUTHORITATIVE index map (reusable library); not current RFP factual authority

LOAD WHEN:
Any evidence search, appendix planning, Summary evidence-readiness, Compliance evidence mapping, or A0–A3 gates.

DEPENDS ON:
17_APPENDIX_AND_EVIDENCE
TEAM_INDEX
CASE_STUDY_INDEX
CERTIFICATION_INDEX
CURRENT_RFP_SOURCES (for matching only)

DO NOT APPLY TO:
Treating this index as proof that the current RFP’s mandatory evidence is satisfied.

SUPERSEDES:
Unindexed dumping of CVs/cases/certs into prompts.

CLASSIFICATION:
**Reusable Rubix evidence map.** Current RFP truth lives only in the active engagement pack.

---

# Evidence Index

## Honesty protocol

```text
Presence in this index ≠ bid compliance
Presence ≠ current validity
Match candidate → verify strength → disclose gaps → never fabricate
```

Use statuses from `09_APPENDIX_EVIDENCE/17_APPENDIX_AND_EVIDENCE.md`. Prefer MISSING over invention.

## Primary sources

| Source file | Bytes (index) | Role | Classification |
|---|---:|---|---|
| `EXTERNAL_APPENDIX_PACKAGE/CV_SOURCE` | 1701313 | Expanded CV library | REUSABLE_RUBIX_EVIDENCE |
| `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` | 4125111 | Cases, profile, company docs, selected CVs | REUSABLE_RUBIX_EVIDENCE |
| `EXTERNAL_APPENDIX_PACKAGE/CASE_STUDY_SOURCE` | 813590 | Case-study visual source | REUSABLE_RUBIX_EVIDENCE |

Canonical inventory:

`EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md`

## Sub-indexes

| Index | Path | Contents |
|---|---|---|
| Team / CVs | `09_APPENDIX_EVIDENCE/EVIDENCE/TEAM_INDEX.md` | People, roles, language, conflicts |
| Case studies | `09_APPENDIX_EVIDENCE/EVIDENCE/CASE_STUDY_INDEX.md` | Case IDs, clients, statuses |
| Certifications / company docs | `09_APPENDIX_EVIDENCE/EVIDENCE/CERTIFICATION_INDEX.md` | Ordered docs, assets, validity flags |

## Company profile page map (reusable narrative)

| Pages (`EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE`) | Category |
|---|---|
| 14–20 | Company identity |
| 21–25 | Consulting services |
| 26–29 | Solutions |
| 30–33 | Innovation / capability platforms |
| 34–37 | Communications |
| 38–44 | Engagement and collaboration |

These pages are Rubix self-description — not current RFP requirements.

## Selective retrieval caps

For a typical Summary / readiness request:

- do **not** load all CVs, cases, and certs
- retrieve requirement-matched candidates only (runtime historically capped ~8–10 appendix hits for a sample Summary assembly)
- always return gap list for unmatched mandatory requirements

## Critical library restrictions (carry forward)

1. CV role labels differ across `EXTERNAL_APPENDIX_PACKAGE/CV_SOURCE` and `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` for some people.  
2. Arwa Ajarem AR/EN duplicate versions — deduplicate.  
3. Templated case content (e.g. from `data.py` claiming 26 cases) is **not** evidence.  
4. Cert asset folder count (11) vs rendered 10-document list — review required.  
5. Recheck validity/expiry at each bid date.

## Matching workflow (A1)

```text
CURRENT_RFP requirement
  → search TEAM / CASE / CERT indexes
  → candidate list with source locators
  → strength / conflict / validity flags
  → MATCHED | PARTIAL | MISSING | CONFLICT
  → disclose in Summary / readiness register
```

## What is not in this package

All appendix binaries live outside the portable core and are supplied at runtime. This Markdown package indexes them; it does not replace the binaries. Attach current bid-date verified assets at engagement time.

## Source paths

| Path | Role |
|---|---|
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` | Master inventory |
| `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` | Gates |
| `runtime\appendix\appendix_engine.json` | Engine contract |
| `10_PROVENANCE/PHASE_2_3_REPORT.md` | Capped evidence retrieval example |
| `_forensic_work\master_prompt_extract.txt` (§46) | Evidence engine mandate |
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::SOURCE_INVENTORY_AND_FILE_GUIDE.md` | Attachment policy |
