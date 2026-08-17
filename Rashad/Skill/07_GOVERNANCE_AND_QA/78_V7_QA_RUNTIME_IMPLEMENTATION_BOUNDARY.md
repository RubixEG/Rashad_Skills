# V7 — QA Runtime Implementation Boundary

**STATUS: TRUTHFULNESS CONTRACT**

V7 specifies comprehensive QA behavior but does not claim the separate Streamlit/OpenAI/renderer/QA code already implements every detector. Each registry case is tagged `RUNTIME_REQUIRED` unless a deterministic Skill/package check can prove it statically.

During code conversion, build detector coverage from the registry and report `IMPLEMENTED / PARTIAL / NOT_IMPLEMENTED / NOT_APPLICABLE / NOT_EXECUTED`. Never translate an unimplemented detector into PASS.

## v7.0.1 clarification
Detector behavior is now fully specified at the Skill-contract level for all 233 cases, but `SPECIFIED_NOT_IMPLEMENTED` remains the default implementation state until code exists and measured evidence is produced. Code conversion must not invent a new detector semantic when a case already defines measurement/threshold/applicability; proposed deviations require Council/Red-Team review.
