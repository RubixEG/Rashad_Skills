# Test 23 — QA Harness v1.2 Integration Regression

STATUS: SPECIFICATION / FORWARD TEST

Required cases:
1. Cover with no sequence → G05 = N_A, not blocker.
2. Golden Master page without frozen master SHA → compiler BLOCK.
3. Golden Master topology with no DOM nodes but valid hashed sidecar → G11 sidecar PASS; no fake hidden DOM nodes.
4. Sidecar missing required edge ID → G11 FAIL.
5. Master `scaleX(-1)` / clip / filter / aspect-ratio drift → G14 FAIL.
6. Rubix/client visible-height mismatch >2% → G09 FAIL.
7. alpha padding below 5% does not distort optical logo measurement.
8. Montserrat requested but runtime substitutes another font → G07 FAIL.
9. browser blocked → structured NOT_EXECUTED/BLOCKED evidence; exit code 2.
10. clean HTML gates all pass → `HTML_PREEXPORT_PASS`, never `RELEASED`.
11. actual PDF raster equals approved reference within thresholds → `PDF_PARITY_PASS`.
12. actual PPTX raster equals approved reference within thresholds → `PPTX_PARITY_PASS`.
13. long-deck ledger/master/anchor regression passes → `DECK_CONTINUITY_PASS`.
14. final aggregator missing any of the four required verdicts → BLOCKED.
15. all four machine verdicts present + applicable Rashad council PASS → eligible for final `RELEASED`.
