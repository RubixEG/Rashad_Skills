MODULE:
CASE_STUDY_INDEX

STATUS:
REUSABLE_RUBIX_EVIDENCE inventory; statuses preserved honestly

LOAD WHEN:
Experience matching; SEC-12; appendix case selection; Summary evidence-readiness for prior experience.

DEPENDS ON:
EVIDENCE_INDEX
17_APPENDIX_AND_EVIDENCE
CURRENT_RFP experience requirements

DO NOT APPLY TO:
Inventing client names for NOT_EXTRACTED rows; using templated case text as verified proof; treating BAD/historical proposal pages as Rubix case evidence.

SUPERSEDES:
Claims of “26 verified cases” without source-page verification.

CLASSIFICATION:
**Reusable Rubix case library index.** Not current RFP truth. Relevance must be re-matched per engagement.

---

# Case Study Index

## Sources

| Source | Role |
|---|---|
| `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` (case pages) | Primary textual/source pages |
| `EXTERNAL_APPENDIX_PACKAGE/CASE_STUDY_SOURCE` | Visual case-study source |
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` | Inventory authority |

## Inventory

| Page | ID | Client | Project | Status |
|---:|---|---|---|---|
| 3 | 01 | وزارة الثقافة - هيئة الأدب والنشر والترجمة | تصميم وتفعيل نموذج ممارسة الرعايات المؤسسية | VERIFIED_SOURCE_PAGE |
| 4 | 02 | بنك المنشآت الصغيرة والمتوسطة | تطوير إدارة الشراكات الاستراتيجية | VERIFIED_SOURCE_PAGE |
| 5 | 03 | هيئة تطوير منطقة المدينة المنورة | دعم وتشغيل مكتب إدارة المشاريع والمدن الذكية | VERIFIED_SOURCE_PAGE |
| 6 | 04A | NOT_EXTRACTED | تطوير إطار عمل شامل لإدارة الموردين | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 6 | 04B | NOT_EXTRACTED | تطوير السياسات والإجراءات وسير العمل | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 7 | 05A | NOT_EXTRACTED | تقييم أعمال الموارد البشرية | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 7 | 05B | NOT_EXTRACTED | مراجعة آلية طباعة الكتب المدرسية | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 8 | 06A | NOT_EXTRACTED | دعم ممارسات كفاءة الإنفاق - المسار الأول | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 8 | 06B | NOT_EXTRACTED | دعم ممارسات كفاءة الإنفاق - المسار الأول | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 9 | 07A | NOT_EXTRACTED | بناء وتشغيل أعمال مكتب الإنجاز لقطاع مشغلي المدن والامتثال | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 9 | 07B | NOT_EXTRACTED | بناء وتشغيل وتسليم أعمال مكتب التحول الرقمي | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 10 | 08A | NOT_EXTRACTED | تشغيل أعمال مكتب مشاريع المدن الذكية | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 10 | 08B | NOT_EXTRACTED | بناء وتشغيل أعمال مكتب إدارة المشاريع | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 11 | 09A | NOT_EXTRACTED | تطوير النماذج والقوالب القياسية وإعداد كراسات الشروط والمواصفات | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 11 | 09B | NOT_EXTRACTED | تطوير منصة استطلاعات الرأي | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 12 | 10A | NOT_EXTRACTED | دعم أعمال مركز البيانات البلدية ودعم القرار | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 12 | 10B | NOT_EXTRACTED | تطوير منصة مستودع البيانات ومؤشرات الأداء | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 13 | 11A | NOT_EXTRACTED | تطوير البنية التحتية لتقنية المعلومات بمستشفيات المنطقة الجنوبية | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |
| 13 | 11B | NOT_EXTRACTED | تطوير استراتيجية التحول الرقمي البلدي | SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED |

## Status rules

| Status | Allowed use |
|---|---|
| VERIFIED_SOURCE_PAGE | May be shortlisted; still require relevance fit + confidentiality review |
| SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED | May cite project theme only with review; **do not invent client**; flag in A1 gaps if RFP needs named references |
| TEMPLATED_NOT_EVIDENCE | Forbidden — includes unverified templated expansions beyond source pages |

## Honesty constraints

- Do not upgrade NOT_EXTRACTED clients to named clients without source extraction + review.  
- Source claims of 26 cases with templated content are **not** evidence; this index lists source-backed rows only.  
- Historical proposal corpora (other clients) are never case-study proof for Rubix unless separately verified in this library.  
- Selective loading: retrieve only cases matched to the active RFP theme/requirement — not the full table narrative into every prompt.

## Source paths

| Path | Role |
|---|---|
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` | Case inventory |
| `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` | Case curator gate |
| `_forensic_work\master_prompt_extract.txt` (§46–§47) | Evidence + historical example classes |
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::SOURCE_INVENTORY_AND_FILE_GUIDE.md` | Historical corpus is external / not factual authority |
