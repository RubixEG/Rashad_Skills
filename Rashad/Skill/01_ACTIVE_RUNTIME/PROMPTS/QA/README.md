MODULE: QA_PROMPT_INDEX
STATUS: INDEX_ONLY
LOAD WHEN: Running content, source, artifact, language, brand, geometry, prepress, or release review.
DEPENDS ON: `16_QA_AND_RELEASE_GATES.md`; relevant product module; current engagement evidence.
DO NOT APPLY TO: Self-grading generation, exposing internal reasoning, or claiming blocked render tests ran.
SUPERSEDES: Unstructured “review this” prompts without hard gates and evidence.

# QA retrieval

Use current QA contracts under:

- `03_ARTIFACT_ENGINE/20_ARTIFACT_STRENGTH_NON_REGRESSION_AUTHORITY.md`

Generation and evaluation contexts remain isolated. Human baseline scores belong only to independent evaluation after the final candidate; benchmark leakage blocks the request.
