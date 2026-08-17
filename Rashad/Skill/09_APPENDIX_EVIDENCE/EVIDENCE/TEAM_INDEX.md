MODULE:
TEAM_INDEX

STATUS:
REUSABLE_RUBIX_EVIDENCE inventory; conflicts preserved

LOAD WHEN:
Team requirements matching; SEC-08; appendix CV selection; Summary team-readiness; role-fit conflicts review.

DEPENDS ON:
EVIDENCE_INDEX
17_APPENDIX_AND_EVIDENCE
CURRENT_RFP team specification

DO NOT APPLY TO:
Auto-staffing a proposal without A1 fit checks; hiding ROLE_CONFLICT rows.

SUPERSEDES:
Single-source CV role assumptions when conflicts exist.

CLASSIFICATION:
**Reusable Rubix CV library index.** Not current RFP truth. RFP minimum years/roles come only from the active pack.

---

# Team Index (CVs)

## Source

| Field | Value |
|---|---|
| Primary expanded CV source | `EXTERNAL_APPENDIX_PACKAGE/CV_SOURCE` |
| Secondary / appendix CV overlap | `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` (selected CVs; role labels may conflict) |
| Inventory authority | `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` |

## Inventory

| Page (`EXTERNAL_APPENDIX_PACKAGE/CV_SOURCE`) | Name | Source role (as indexed) | Language | Status |
|---:|---|---|---|---|
| 1 | عبدالله المصطفى | شريك مؤسس ومدير تنفيذي | ar | SOURCE_PAGE_AVAILABLE |
| 2 | هشام درويش | مدير تنفيذي لتطوير الأعمال | ar | ROLE_CONFLICT_WITH_APPENDICES_P58 |
| 3 | محمد راتب | خبير الخدمات المالية والعقود | ar | SOURCE_PAGE_AVAILABLE |
| 4 | أحمد النمر | مدير تنفيذي - التقنيات الناشئة وخدمات المدن الذكية | ar | SOURCE_PAGE_AVAILABLE |
| 5 | إيهاب طبارة | مدير نمو الأعمال والابتكار | ar | SOURCE_PAGE_AVAILABLE |
| 6 | بدر القثامي | استشاري موجه | ar | ROLE_CONFLICT_WITH_APPENDICES_P63 |
| 7 | مؤيد الشيباني | استشاري - تطوير تنظيمي | ar | SOURCE_PAGE_AVAILABLE |
| 8 | خالد الايراني | مستشار أول | ar | SOURCE_PAGE_AVAILABLE |
| 9 | محمد القيسي | مستشار | ar | SOURCE_PAGE_AVAILABLE |
| 10 | أروى عجارم | استشاري | ar | DUPLICATE_LANGUAGE_VERSION |
| 11 | أحمد موسى | خبير الشراكات وتطوير الأعمال | ar | SOURCE_PAGE_AVAILABLE |
| 12 | د. جابر الإسماعيل | خبير استثمار واقتصاد | ar | SOURCE_PAGE_AVAILABLE |
| 13 | غيث توفيق | مدير تنفيذي - قطاع تحليل البيانات | ar | SOURCE_PAGE_AVAILABLE |
| 14 | د. عادل علي | خبير ومستشار قانوني | ar | SOURCE_PAGE_AVAILABLE |
| 15 | محمد العبيدي | مستشار - محلل أعمال | ar | SOURCE_PAGE_AVAILABLE |
| 16 | بلال منيمنة | مدير تنفيذي للتسويق والإعلان | ar | ROLE_CONFLICT_WITH_APPENDICES_P61 |
| 17 | Moatasim Ibrahim | Senior Manager | en | SOURCE_PAGE_AVAILABLE |
| 18 | Abedlatif Al-Omar | Transformation Consultant | en | SOURCE_PAGE_AVAILABLE |
| 19 | Arwa Ajarem | Senior Consultant | en | DUPLICATE_LANGUAGE_VERSION |

## Conflict and dedupe rules

1. **ROLE_CONFLICT** rows (هشام درويش, بدر القثامي, بلال منيمنة): do not pick a role label silently. Resolve via Appendix Gap/Substitution + user/bid decision; keep conflict visible until resolved (`unresolved_role_fit_conflicts = 0` required for A3).  
2. **Arwa Ajarem / أروى عجارم**: Arabic and English versions of the same person — select one language version per proposal language; never present as two people.  
3. Role titles in this index are **library labels**, not proof that the person meets the current RFP’s mandatory years/qualifications.  
4. When RFP experience years are unspecified, show `Not specified` for the requirement and keep any advisory staffing clearly separated from RFP mandates.

## Selection loading rule

Load only shortlisted candidates for the active role matrix. Never load all 19 CV pages into context by default.

## Source paths

| Path | Role |
|---|---|
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` | CV inventory table |
| `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` | Curator / conflict gates |
| `01_ACTIVE_RUNTIME/22_RFP_SUMMARY_FINAL_PRODUCT_CONTRACT.md` | Team years / Not specified rules |
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::SOURCE_INVENTORY_AND_FILE_GUIDE.md` | MWAN team file is engagement-test only, not this library |
