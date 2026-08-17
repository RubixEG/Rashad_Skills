# Visual Asset Service

## Role in the proposal system
The Visual Asset Service is called by the Artifact Engine after the page thesis and information relationship are known. It cannot decide the proposal claim, evidence, commitment, or section ownership.

## Decision questions
1. Does a visual asset improve comprehension, emotion, sector relevance, or narrative transition?
2. Is the page better served by a precise native diagram instead?
3. Is the asset primary, supporting, background, or decorative?
4. Does it need to be editable or merely replaceable?
5. What is the safest production mode?

## Asset roles
- `PRIMARY_HERO` — visual focal point for cover/opener/vision.
- `SUPPORTING_EDITORIAL` — reinforces thesis while text remains primary.
- `CONCEPTUAL_EXPLANATORY` — illustrates a system or future state beneath editable labels.
- `BACKGROUND_ATMOSPHERE` — subtle, low-contrast backdrop.
- `NAVIGATION_ICON` — repeated semantic marker.
- `ACCENT_MOTIF` — small branded or sector cue.

## Generation decision matrix
### Strong generation candidates
- cover and section-opening hero imagery;
- beneficiary/customer experience scenes;
- future-state transformation concepts;
- sustainability and circular-economy imagery;
- public/private partnership scenes;
- AI/data conceptual illustrations;
- events and activation contexts;
- abstract institutional backgrounds.

### Hybrid candidates
- stakeholder ecosystems;
- operating model concepts;
- change journeys;
- data ecosystems;
- innovation portfolios.

Generate the illustration layer, then add labels, connectors, evidence, and decision logic as editable overlays.

### Native-only candidates
- compliance, BOQ, evaluation scoring;
- detailed architecture and integration;
- financial models;
- roadmaps with commitments;
- RACI, governance rights, acceptance gates;
- risk, security, or SLA matrices.

## Failure handling
If generation produces text, logos, watermarks, unclear hands/faces, incorrect cultural signals, irrelevant symbolism, or poor composition:
- reject the asset;
- retry once with a corrected brief;
- then use native-vector fallback or an approved asset.

## Page-level asset budget
A page should normally have one primary visual system. Do not combine hero photography, complex illustration, multiple icon packs, and a dense diagram on the same page.
