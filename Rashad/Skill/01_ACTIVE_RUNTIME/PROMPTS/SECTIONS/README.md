MODULE: SECTION_PROMPT_INDEX
STATUS: INDEX_ONLY
LOAD WHEN: A proposal node has `READINESS=READY` and canonical `STATE=NOT_STARTED` or `STATE=STALE` for controlled regeneration.
DEPENDS ON: `07_PROPOSAL_WORKFLOW.md`; `08_FINAL_PROPOSAL_SKELETON.md`; `SECTION_DEPENDENCIES.md`; CRAFT index.
DO NOT APPLY TO: Drafting blocked sections or replacing exact section/R-code prompts with summaries.
SUPERSEDES: One-size-fits-all proposal drafting prompts.

# Section prompt routing

For each section:

1. confirm dependency status and Section Contract;
2. load only current RFP evidence for that section;
3. retrieve the relevant exact CRAFT block and R-codes;
4. execute routed verified councils;
5. create content before artifact/render work;
6. update engagement state and recommend the next dependency-ready section.
