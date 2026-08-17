# Rashad OS — Final Brain + Artifact Production Upgrade

## Decision

Skill v7.0.2 remains the canonical/protected knowledge constitution. This upgrade changes execution behavior in the Brain/QA boundary, not the protected corpus.

## P0 fixed: content-to-PPTX bypass

The production composer is no longer allowed to accept a content pack directly. The canonical admission chain is:

`Brain Decision → Page Contract → Cognitive Packet → Artifact Intent → Semantic Graph → 5 Material Hypotheses → 5 Actual Render Hashes → Selected Draft Master → Brand Preflight → Claim-to-Visual Evidence Binding → Draft QA → Composer Admission`

`Brain/runtime/production_output_guard.py` returns `BLOCK_RENDER` when required evidence is absent.

### Output state machine

1. `CONTENT_DRAFT` — evidence-backed content exists; no visual-production claim.
2. `ARTIFACT_DRAFT` — real visual exploration/render evidence exists and draft QA passed. Live independent judging is not required.
3. `RELEASE_CANDIDATE` — independent judge + QA candidate + parity + proof index are complete.
4. `RELEASED` — only `RASHAD_BRAIN_RELEASE_CHAIR` may issue this state.

Missing live independent judging **cannot suppress Artifact Draft generation**. It only blocks escalation beyond Artifact Draft.

## Selective Consulting Brain additions

The following were added because they close real operating gaps:

- Knowledge readiness states: `AVAILABLE_VERIFIED`, `AVAILABLE_PARTIAL`, `STRUCTURE_ONLY`, `KNOWLEDGE_REQUIRED`.
- Missing-expertise routing without pretending that routing equals knowledge.
- Explicit actor ontology: SME, Executive Simulator, Evaluator Simulator, Governor, Producer, Challenger, Independent Judge, Release Chair.
- Governor vetoes for evidence, financial truth, artifact-pipeline bypass, independence and release authority.
- 16 cognitive functions as runtime jobs rather than generic "review this" personas.
- Bounded dynamic working councils (maximum 6 actors) that do not replace the 16 constitutional councils.
- First-class Technical Solution and Financial/Commercial reasoning pipelines.
- Confidence propagation: downstream conclusions cannot be more confident than their weakest required dependency.
- Visual-variety memory to detect immediate repeated structural grammar.
- Governed Firm Model foundation whose cells remain `KNOWLEDGE_REQUIRED` until approved internal evidence is supplied.

## Deliberate exclusions

The package does **not** claim 141 fully knowledgeable SMEs or populate dozens of empty knowledge packs for appearance. Long-tail specialists are routed when required, but high-stakes output is blocked if their knowledge pack is not ready.

Firm credentials, case studies, CV/capacity and rate cards are intentionally not invented from the RFP. They require an approved firm Data Room.

## Truthfulness boundary

Offline certification proves the runtime contracts and red-team behavior. It does not prove that a live provider, a real independent multimodal judge or the remaining final-production renderer mechanics executed for a specific engagement. Those are required before a proposal may reach `RELEASED`.
