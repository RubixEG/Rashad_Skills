# Image-Last Turn Orchestration Contract

1. Complete all non-image reasoning and persist state first.
2. The image call is the final tool action in the turn.
3. Persist `IMAGE_SLOT`, `IMAGE_BRIEF_HASH`, `EXPECTED_ASSET_QA`, `PRODUCT_STATUS=IN_PROGRESS`, `NEXT_STEP=ASSET_QA` before the call.
4. On the next user/continuation turn, bind the returned image to the slot and resume; do not regenerate unless QA rejects it.
5. Never interpret tool-level forced turn termination as Rashad product completion.
