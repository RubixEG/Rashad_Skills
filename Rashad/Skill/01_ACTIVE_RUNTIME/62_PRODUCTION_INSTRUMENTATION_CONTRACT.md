# 62 — Production Instrumentation Contract

**Status:** CURRENT — mandatory for every client-facing page
**Owner:** Instrumentation Contract Owner (C8 #57), blocking, NO-WAIVER
**Gate:** `G00_INSTRUMENTATION`

---

## 62.0 Why this module is the highest-leverage fix in v5.2

The v5.1 QA harness implements 24 render gates. When run against the three
actually-delivered MWAN artifacts, this is what happened:

| Observation on the delivered deck | Count |
|---|---|
| `data-*` attributes present in the source | **0** |
| Gates that returned `FAIL_NOT_INSTRUMENTED` | 8 per slide |
| Gates that returned **PASS on zero measured objects** | up to 12 per slide |
| Slides with semantic node instrumentation | 0 / 19 |

Both failure modes come from the same root cause: **the producer and the
inspector never agreed on a contract.** QA was written expecting instrumentation
that production was never told to emit.

The result is the worst of both worlds — the QA appears thorough, and the pages
it clears are unmeasured.

This module is the treaty. Production emits it. QA consumes it. Neither side
gets to assume.

---

## 62.1 The page container contract

```html
<section class="slide"
         data-page-id="P07"
         data-page-mode="ARTIFACT_LED"        <!-- COVER | DIVIDER | NARRATIVE | ARTIFACT_LED | HYBRID | DENSE_EVIDENCE -->
         data-page-family="ANALYTICAL"
         data-canvas="1600x900"
         data-complexity-band="AC-3"
         data-artifact-expression="HUB ⊕ BAND ⊕ GAUGE ⊕ LOOP"
         dir="rtl" lang="ar">
```

**Rule I-01.** The QA page selector is `[data-page-id]`. It is **not** a CSS class.
In the delivered MWAN artifacts the class `.page` was the *page-number label*
while the actual page container was `.slide` — pointing the harness at the
documented default selector produced a meaningless BLOCKED. Selector-by-class is
banned; selector-by-contract is mandatory.

**Rule I-02.** `data-canvas` declares the authoring canvas. It must be one of the
approved authoring sizes and must match the 16:9 aspect. Master export resolution
is enforced separately at parity.

---

## 62.2 Required attribute set

### Structure and semantics

| Attribute | On | Purpose | Gate |
|---|---|---|---|
| `data-page-id` | page container | page identity, ordering | G00, deck continuity |
| `data-page-mode` | page container | drives which gates are required | G18, G32 |
| `data-node-id` | every semantic node | topology truth | G15, G32 |
| `data-node-type` | every semantic node | `ACTOR\|CAPABILITY\|PROCESS\|ASSET\|OUTCOME\|CONSTRAINT\|MEASURE\|DECISION\|RISK\|EVIDENCE` | AI2 |
| `data-edge-id` | every connector | relationship identity | G16 |
| `data-source` / `data-target` | connector | endpoints | G16 |
| `data-relation` | connector | one of the 14 closed relations | AI2, G32 |
| `data-directionality` | connector | `DIRECTED\|UNDIRECTED\|ISOLATED` | G16, G27 |
| `data-label-for` | every label | which node it belongs to | G17 |
| `data-owner-id` + `data-anchor` | badges, KPIs, icons, chips, footnote marks | containment | G11 |

### Layout discipline

| Attribute | Purpose | Gate |
|---|---|---|
| `data-align-group` + `data-align-axis` | declared alignment intent | G08 |
| `data-spacing-group` | declared rhythm intent | G09 |
| `data-seq-group` + `data-seq` | ordered sequences — the RTL truth source | G14 |
| `data-divider-id` | rules and separators | G12 |
| `data-layer-id` + `data-layer-order` | stacking intent | G07 |
| `data-region-id` | composite region (`DOMINANT\|SUPPORTING\|RAIL\|BAND\|SOURCE`) | G32, AI2 |
| `data-area-budget` | declared share of live area for the region | AI2-P01 |
| `data-overlap-policy` | `ALLOW` only where intentional | G06 |

### Content and truth

| Attribute | Purpose | Gate |
|---|---|---|
| `data-content-slot` | `question\|thesis\|evidence\|interpretation\|implication\|source` | G30 |
| `data-source` on a claim | evidence ledger ID | G31 |
| `data-confidence` | `HIGH\|MEDIUM\|LOW` | G31 |
| `data-asset-id` | approved asset logical ID | G29 |
| `data-header-role` | `EYEBROW\|TITLE\|SUBTITLE\|ACCENT\|ARTIFACT_START` | G02 |
| `data-table-role` | dense evidence identity | G21 |
| `data-stress-grow` | opt-in for text-growth stress | stress |

**Rule I-03.** `data-stress-grow` must be present on every text element that
carries variable-length content. In v2.5 the text-growth mutation silently did
nothing on pages that did not opt in — a stress test that tests nothing reports
PASS. v2.6 treats a page with zero `data-stress-grow` elements and >40 words as
`FAIL_NOT_INSTRUMENTED` for the stress gate.

---

## 62.3 Worked example

```html
<section class="slide" data-page-id="P07" data-page-mode="ARTIFACT_LED"
         data-canvas="1600x900" data-complexity-band="AC-3" dir="rtl" lang="ar">

  <h2 data-header-role="TITLE" data-content-slot="thesis" data-stress-grow>
    المركز يطلب قدرة تشغيلية للشراكات لا مجموعة وثائق منفصلة
  </h2>

  <div data-region-id="DOMINANT" data-area-budget="0.55">
    <div data-node-id="N-CORE" data-node-type="CAPABILITY"
         data-align-group="core" data-align-axis="CENTER_Y">
      قدرة مؤسسية مستمرة لإدارة الشراكات
    </div>

    <div data-node-id="N-01" data-node-type="PROCESS"
         data-seq-group="lifecycle" data-seq="1">فهم البيئة وأصحاب المصلحة</div>
    <span data-owner-id="N-01" data-anchor="TOP_RIGHT">١</span>

    <svg><path data-edge-id="E-01" data-source="N-01" data-target="N-CORE"
               data-relation="ENABLES" data-directionality="DIRECTED"
               marker-end="url(#arrow)"/></svg>
  </div>

  <aside data-region-id="RAIL" data-area-budget="0.20">
    <p data-content-slot="implication" data-stress-grow>
      المطلوب تأسيس قدرة مؤسسية تخطط وتقيس وتتابع وتضبط الامتثال
    </p>
  </aside>

  <footer data-region-id="SOURCE">
    <span data-content-slot="source" data-source="EV-0042" data-confidence="HIGH">
      المصدر: ملف التأهيل — دراسة الشروط
    </span>
    <span class="page-number" dir="ltr">٠٤</span>
  </footer>
</section>
```

---

## 62.4 Sequence and RTL — the rule that must not be softened

`data-seq` carries **semantic** order (1, 2, 3, 4). Physical geometry is derived,
not authored:

```
dir=rtl  ⇒  physical x descends as seq ascends
            item 1 sits at the RIGHT edge
            arrows point leftward
            connectors are computed AFTER direction resolution
```

`G14_RTL_BIDI` verifies this by measuring rendered x positions against `data-seq`.
Without `data-seq-group`, the gate has nothing to measure. In v2.5 that produced
a silent PASS on every slide of an Arabic-first deck. In v2.6 it is a hard
`FAIL_NOT_INSTRUMENTED` whenever the page contains Arabic.

---

## 62.5 Conformance levels

| Level | Requirement | Permitted use |
|---|---|---|
| `L0` none | — | internal drafts only, never client-facing |
| `L1` structural | page container + header roles + regions | covers, dividers |
| `L2` analytical | L1 + nodes, edges, relations, labels, owners, sequences | every analytical page |
| `L3` full | L2 + content slots, evidence IDs, area budgets, stress-grow | **required for release** |

**Rule I-04.** Client-facing release requires `L3` on every page. `L2` pages may
be reviewed but not released. `L0`/`L1` analytical pages are rejected at
`G00_INSTRUMENTATION`.

---

## 62.6 Migration path for existing decks

1. Add `data-page-id` and `data-page-mode` to every page container. *(unblocks the
   selector problem immediately)*
2. Add `data-header-role` to title stacks. *(unblocks G02)*
3. Add `data-seq-group`/`data-seq` to every numbered sequence. *(unblocks G14 —
   highest priority for Arabic)*
4. Add `data-node-id`/`data-node-type` to the analytical objects. *(unblocks G15,
   G32 — this is where artifact strength starts moving)*
5. Replace decorative div chains with real SVG connectors carrying
   `data-edge-id`/`data-source`/`data-target`/`data-relation`. *(unblocks G16 and
   the relationship-truth score, which is 20 of the 100 points)*
6. Add `data-content-slot` and `data-source`. *(unblocks G30, G31)*
7. Add `data-region-id`/`data-area-budget`. *(unblocks composite verification)*

Steps 1–3 are mechanical and can be done on the existing deck in an afternoon.
Steps 4–5 require the Artifact Intelligence Engine v2 pipeline, because they
presuppose that the relationships were modelled at all.
