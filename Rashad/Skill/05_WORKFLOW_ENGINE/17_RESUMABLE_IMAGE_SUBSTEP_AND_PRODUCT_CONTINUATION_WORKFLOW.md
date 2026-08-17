# Resumable Image Sub-step & Product Continuation Workflow

`Prepare page → freeze content/concept → persist handoff → call image tool → return image → resume → asset QA → reconstruct/overlay → page QA → continue deck → export → release`.

Regression case `ORCH-IMG-001`: image tool returns a valid cover hero and ends the turn. Expected result: product remains `IN_PROGRESS`; next action is cover asset QA/composition; the same hero is reused.
