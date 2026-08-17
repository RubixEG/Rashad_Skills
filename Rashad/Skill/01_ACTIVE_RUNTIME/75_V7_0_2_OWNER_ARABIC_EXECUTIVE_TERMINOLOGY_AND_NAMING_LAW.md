# v7.0.2 — Owner Arabic Executive Terminology & Naming Law

**STATUS: CURRENT OWNER LANGUAGE AUTHORITY**  
**SCOPE:** Arabic visible executive RFP Summary/product language and any prompt/instruction capable of generating it.  
**COMPATIBILITY:** Preserve stable internal IDs such as `COMMERCIAL_EXPOSURE`. Do not mutate protected 388 R-code prompts, 96 scopes, 96 mappings, or immutable protected corpus.

## 1. Executive naming law
The Arabic word **«التعرّض»** and the unvocalized form **«التعرض»** are prohibited in final visible executive titles, subsection headings, callouts, management questions, decision labels, and artifact labels unless the owner explicitly approves a specific engagement exception.

Preferred language states the business implication directly: `التزام`، `مخاطرة`، `أثر مالي`، `أثر تجاري`، `أثر على الربحية`، `أثر على التدفق النقدي`، `أثر تعاقدي`. Do not use abstract finance jargon when a direct Arabic expression is available.

The prohibition applies to final visible product language, not stable internal IDs, historical archives, exact source quotations, filenames, debugging, or regression attack strings. Those exceptions must never be promoted automatically into visible executive labels.

## 2. Role 16 canonical default
Internal identity: `COMMERCIAL_EXPOSURE` — **retain**.  
Default visible Arabic title: **الالتزامات والمخاطر التجارية والمالية**.

Evidence-adaptive alternatives:
- **الالتزامات المالية والتجارية وأثرها على الربحية** — only when profitability/margin implications are genuinely supported.
- **الالتزامات المالية والتجارية وأثرها على التدفق النقدي والربحية** — only when both cash-flow and profitability implications are genuinely supported.
- **الأثر المالي والتجاري** — only when the surrounding context already makes the exact decision issue sufficiently specific.

## 3. Contextual replacement law
Do not apply a one-phrase global replacement. Interpret the management question first. Examples of approved direct language include:
- `مصادر المخاطر والالتزامات المالية`
- `حجم الالتزامات والمخاطر التجارية`
- `أثر شروط الدفع على التدفق النقدي`
- `الالتزامات المالية المرتبطة بالضمانات`
- `المخاطر والالتزامات التعاقدية`

## 4. CFO language test
For every commercial/financial page, the naming system must let a CFO immediately understand:
1. what Rubix must pay or commit;
2. what may affect margin;
3. what may affect cash flow;
4. what guarantees are required;
5. which payment terms create risk;
6. what penalties exist;
7. what assumptions may change price.

If the title uses an abstract financial label without naming the decision issue, REVISE or BLOCK. Do not mention الربحية or التدفق النقدي unless supported by source evidence or defensible analysis.

## 5. Visible-title generation
`Visible Executive Title = Canonical Role + RFP Topic + Management Question + Primary Executive Audience`

The canonical registry title is the safe default. Topic adaptation is encouraged when it makes the management question clearer, but must not invent implications. Every visible title passes the Executive Naming Council: Consulting Partner, CEO/GM, CFO where commercial, COO where execution, Government Evaluator, Bid Director, Information Design Director, Arabic Editorial Director.

## 6. Runtime-visible term policy
Reusable runtime rule:
- normalize Arabic diacritics/tatweel before checking;
- prohibited normalized term: `التعرض`;
- block visible text unless explicitly marked as an exact source quotation/historical-source exception;
- internal IDs and non-visible metadata are out of scope;
- source quotation exceptions must never be reused automatically as title/subtitle/callout/decision/artifact labels.

## 7. Permanent red-team attacks
The following strings are attack fixtures, **not approved output**:
1. visible title `التعرّض التجاري والمالي` → BLOCK
2. visible subsection `مصادر التعرّض` → BLOCK
3. visible callout `التعرّض المالي مرتفع` → BLOCK / REVISE
4. internal ID `COMMERCIAL_EXPOSURE` → PASS internally
5. exact source quotation containing `التعرّض` → may remain as quotation; must not become a visible title
6. `الالتزامات والمخاطر التجارية والمالية` → PASS
7. `الالتزامات المالية والتجارية وأثرها على الربحية` → PASS only with evidence-supported profitability implications
8. `الأثر المالي والتجاري` → PASS only when context is sufficiently specific

## 8. Release condition
`VISIBLE_EXECUTIVE_OCCURRENCES = 0` for the prohibited Arabic term variants unless an explicit owner-approved engagement exception exists. A release scan must enumerate every remaining occurrence with file, line, classification, `visible_to_user`, action, and justification.
