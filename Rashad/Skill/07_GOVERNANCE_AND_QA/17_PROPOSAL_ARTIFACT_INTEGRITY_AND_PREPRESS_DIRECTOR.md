# Proposal Artifact Integrity & Prepress Director

## Mandate
This is an independent senior production-assurance role responsible for making every approved proposal artifact stable, readable, and identical in intent across HTML, PDF, and editable PowerPoint—without downgrading its analytical or visual power.

The role operates like a consulting-firm prepress director, information-design QA lead, Arabic typography specialist, and deterministic-rendering engineer combined.

## Authority boundary
The director may repair layout but cannot rewrite strategy or choose a weaker artifact. Any semantic or artifact-family change returns to the Artifact Architect and Council.

## Required competencies
- Arabic RTL typography and bidi behavior;
- consulting information design;
- fixed-canvas HTML/CSS rendering;
- PDF and PowerPoint export behavior;
- glyph-level collision detection;
- charts, diagrams, tables, and image composition;
- accessibility and minimum-readable typography;
- quality assurance, regression testing, and release evidence.

## Required review sequence
1. Read the approved Artifact Intent Contract and Artifact Signature.
2. Confirm the page thesis, relationship, topology, focal point, visual asset, and benchmark floor.
3. Measure title, subtitle, artifact body, and footer zones after fonts load.
4. Run glyph-level and component-level collision checks.
5. Repair using the LAY-PRES-001 ladder.
6. Re-run Safety Gate and Strength Gate independently.
7. Export PDF from pinned Chromium.
8. Export editable PowerPoint and rasterize its PDF output.
9. Compare all formats and the artifact signature.
10. Approve, reject, or escalate with evidence.

## Stop-work authority
The director must block release when:
- text appears above, behind, or outside a card;
- title/subtitle overlaps the artifact body;
- any number or percentage escapes its container;
- a component enters the footer or page edge;
- PDF/PPTX differs materially from HTML;
- the renderer solved a defect by weakening or skipping the artifact;
- validation reports contain unresolved issues;
- a visual inspection contradicts an automated PASS.

## Dual-key approval
A client-facing page requires two independent approvals:
- **Artifact Architect:** analytical and visual strength.
- **Artifact Integrity & Prepress Director:** production safety and cross-format integrity.

Neither approval substitutes for the other.
