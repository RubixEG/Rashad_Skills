# Test 24 — Image Tool Turn Boundary / Product Continuation

1. Start RFP Summary product.
2. Persist state before cover generation.
3. Simulate image tool returning one asset and ending the turn.
4. Reload product state.
5. Assert `status != RELEASED/DONE`.
6. Assert returned asset is bound to the same cover asset ID.
7. Assert `NEXT_STEP = ASSET_QA | COVER_COMPOSITION`.
8. Continue pilot pages and exports without re-ingesting the RFP.

PASS only with evidence of the state transition.
