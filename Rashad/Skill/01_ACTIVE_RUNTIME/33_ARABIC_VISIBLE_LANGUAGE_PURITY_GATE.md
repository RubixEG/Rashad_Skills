MODULE: 33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE
STATUS: BLOCKING — v2.4
LOAD WHEN: Any Arabic Summary/proposal/artifact/table/page.

# Arabic Visible-Language Purity Gate

## Root problem fixed

Internal canonical role IDs such as `COMPETITION_NARRATIVE`, `OPPORTUNITY_SNAPSHOT`, `KEY_DATES`, or English workstream labels must **never leak into visible Arabic output**.

## Two-layer naming model

- `internal_role_id`: machine/internal identifier; may be English.
- `visible_label`: client/user-visible label; must follow engagement language.

For Arabic engagements, visible headings/subheadings/labels/callouts/table headers/process labels/footer labels are Arabic.

## Arabic visible-label map for RFP Summary

| Internal role | Required Arabic visible label |
|---|---|
| COVER | الغلاف |
| COMPETITION_NARRATIVE | ماذا تشتري الجهة فعليًا؟ |
| TABLE_OF_CONTENTS | خريطة الملخص التنفيذي |
| OPPORTUNITY_SNAPSHOT | صورة الفرصة في دقيقة واحدة |
| KEY_DATES | الجدول الزمني وضغط التقديم |
| SOURCE_COVERAGE | اكتمال مستندات المنافسة وما يحتاج إلى حسم |
| CLIENT_NEED | أهداف المشروع والنتائج التي تتوقعها الجهة |
| STRATEGIC_READING | القراءة الاستراتيجية للفرصة |
| SCOPE_ARCHITECTURE | نطاق المشروع ومجالات العمل |
| DELIVERY_JOURNEY | كيف سينتقل المشروع من التأسيس إلى التشغيل؟ |
| BOQ_INTELLIGENCE | المخرجات والكميات: ما الذي سنلتزم بتسليمه فعليًا؟ |
| TECHNICAL_REQUIREMENTS | متطلبات الحل التقني والبيانات والتكامل |
| TEAM_CAPACITY | القدرات المطلوبة لتنفيذ المشروع |
| EVALUATION_WIN | كيف سيُقيَّم العرض وما الذي يصنع التفوق؟ |
| QUALIFICATION_READINESS | جاهزية التأهيل والأدلة الداعمة |
| EVIDENCE_READINESS (legacy alias) | جاهزية التأهيل والأدلة الداعمة |
| COMMERCIAL_EXPOSURE | الالتزامات والمخاطر التجارية والمالية |
| PROPOSAL_STRATEGY | استراتيجية الاستجابة للمنافسة |
| PROPOSAL_GANTT | خطة إعداد العرض حتى التقديم |
| CONTRACT_GANTT | تصور تنفيذ المشروع بعد الترسية |
| DELIVERY_GANTT (legacy alias) | تصور تنفيذ المشروع بعد الترسية |
| RISKS | ما الذي قد يهدد الفوز أو التنفيذ؟ |
| CLARIFICATIONS | الاستفسارات التي يجب حسمها قبل التقديم |
| ASSUMPTIONS_GAPS | الافتراضات والفجوات المؤثرة على القرار |
| ASSUMPTIONS (legacy alias) | الافتراضات والفجوات المؤثرة على القرار |
| AUTHORSHIP_MATURITY | ماذا تكشف طريقة إعداد المنافسة عن عملية الشراء؟ |
| BID_DECISION | قرار الدخول وشروط النجاح |

## English admission rule in Arabic output

English is allowed only when at least one is true:
- official product/standard/proper name;
- acronym/technical token whose Arabic translation would reduce precision (`AI`, `POC`, `API`, `SLA`, `UAT`, `UI/UX`, etc.);
- code/identifier/URL/email/version string;
- exact source term that must be preserved.

On first meaningful occurrence, prefer Arabic term followed by the acronym where natural, e.g. `نموذج إثبات مفهوم (POC)`.

Do not use English for stylistic headings such as `Opportunity Snapshot`, `Strategic Reading`, `Win Strategy`, `Critical Finding`, `Council Observation`, `Management Conclusion`, `Workstream`, `Treatment`, `Gate`, `High`, `Medium`, `Low` when a natural Arabic label exists.

## Blocking QA

Release target for Arabic visible output:
- `english_heading_leakage = 0`
- `english_subtitle_leakage = 0`
- `avoidable_english_label_leakage = 0`

Technical tokens are not leakage when allowed by the admission rule.


## v7.0 monolingual reinforcement
Execute `70_V7_MONOLINGUAL_OUTPUT_AND_NAMING_AUTHORITY.md`. Arabic product means Arabic visible headings/labels throughout except narrow precision-required technical/proper-name islands. English product means English visible product. Decorative bilingual headings are blocking defects.


## v7.0.2 Owner Arabic Executive Terminology Lock

Execute `75_V7_0_2_OWNER_ARABIC_EXECUTIVE_TERMINOLOGY_AND_NAMING_LAW.md`.

- Arabic visible executive product language must use direct business implications rather than abstract exposure jargon.
- The stable internal ID `COMMERCIAL_EXPOSURE` remains valid and invisible.
- The default visible Arabic title for role 16 is **الالتزامات والمخاطر التجارية والمالية**.
- A title mentioning الربحية or التدفق النقدي is allowed only when supported by the RFP evidence/analysis.
- Source quotations may preserve original wording, but the quoted wording must not be promoted automatically into a title, subsection, callout, management question, decision label, or artifact label.
