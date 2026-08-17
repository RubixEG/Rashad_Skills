MODULE:
CERTIFICATION_INDEX

STATUS:
REUSABLE_RUBIX_EVIDENCE inventory; validity review required at each bid date

LOAD WHEN:
Eligibility / company documents matching; appendix official-docs selection; Summary evidence-readiness; A0/A3 validity checks.

DEPENDS ON:
EVIDENCE_INDEX
17_APPENDIX_AND_EVIDENCE
CURRENT_RFP mandatory document list

DO NOT APPLY TO:
Claiming current validity from scan presence alone; silently including or excluding the extra media-license asset without review.

SUPERSEDES:
“Certificates folder exists ⇒ eligible.”

CLASSIFICATION:
**Reusable Rubix company-document index.** Not current RFP truth. Mandatory document lists come from the active tender pack.

---

# Certification and Company Documents Index

## Source

| Field | Value |
|---|---|
| Document pages | `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` pages 46–55 (standard 10-document deck list) |
| Raster assets (as indexed) | `appendix/images/certs/p114.png` … `p124.png` |
| Inventory authority | `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` |

## Ordered document list

| Order | Page | Title | Asset | Status |
|---|---:|---|---|---|
| 1 | 46 | السجل التجاري | `appendix/images/certs/p114.png` | VALIDITY_REVIEW_REQUIRED |
| 2 | 47 | شهادة/رمز السجل التجاري QR | `appendix/images/certs/p115.png` | VALIDITY_REVIEW_REQUIRED |
| EXTRA | — | ترخيص إعلامي | `appendix/images/certs/p116.png` | NOT_INCLUDED_IN_10_DOCUMENT_DECK_LIST_REVIEW_REQUIRED |
| 3 | 48 | شهادة الزكاة | `appendix/images/certs/p117.png` | VALIDITY_REVIEW_REQUIRED |
| 4 | 49 | شهادة تسجيل ضريبة القيمة المضافة | `appendix/images/certs/p118.png` | VALIDITY_REVIEW_REQUIRED |
| 5 | 50 | شهادة التأمينات الاجتماعية | `appendix/images/certs/p119.png` | VALIDITY_REVIEW_REQUIRED |
| 6 | 51 | شهادة اشتراك الغرفة التجارية | `appendix/images/certs/p120.png` | VALIDITY_REVIEW_REQUIRED |
| 7 | 52 | شهادة السعودة/التوطين | `appendix/images/certs/p121.png` | VALIDITY_REVIEW_REQUIRED |
| 8 | 53 | شهادة منشآت صغيرة ومتوسطة | `appendix/images/certs/p122.png` | VALIDITY_REVIEW_REQUIRED |
| 9 | 54 | رقم/بيانات المنشأة | `appendix/images/certs/p123.png` | VALIDITY_REVIEW_REQUIRED |
| 10 | 55 | شهادة المحتوى المحلي | `appendix/images/certs/p124.png` | VALIDITY_REVIEW_REQUIRED |

## Validity honesty

```text
Presence is not proof of current validity.
Recheck expiry and authenticity at each bid date.
expired_required_documents = 0 required for A3 when docs are mandatory.
```

Official documents in the appendix must remain **unmodified** scans/exports. Do not regenerate seals, QR codes, or certificates via image models (KF-006 / image policy).

## Count conflict (must stay visible)

- Certificate asset folder contains **11** assets.  
- Rendered appendix document lists **10** documents.  
- Extra media license (`p116`) is flagged `NOT_INCLUDED_IN_10_DOCUMENT_DECK_LIST_REVIEW_REQUIRED`.  
- Resolve via Corporate Documents curator + user decision; do not invent a 11th “standard” slot or drop the asset silently.

## Matching vs current RFP

1. Read mandatory/eligibility docs from **current RFP**.  
2. Map to rows above.  
3. Mark MATCHED / PARTIAL / MISSING / VALIDITY_REVIEW_REQUIRED.  
4. Disclose gaps in Summary readiness — never fabricate missing certificates.

## Selective loading

Load only documents required by the active pack (plus conflict notes). Do not attach all cert PNGs to every Summary request.

## Source paths

| Path | Role |
|---|---|
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` | Company documents table + restrictions |
| `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` | Validity / authenticity reviewer |
| `runtime\appendix\appendix_engine.json` | may_contain certificates/licenses |
| `PROJECT_INSTRUCTIONS.md` | No invented certificates; images must not fake seals |
| `_forensic_work\master_prompt_extract.txt` (§46) | Evidence engine |
