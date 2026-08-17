# Test 24 — Image-Based Golden Deck Regression

STATUS: SPECIFICATION TEST — v2.6.4.7

Required scenarios:
1. MWAN-style cover generated with left imagery and right title zone -> PASS if co-brand and title zones match reference grammar.
2. Client logo visually weaker because transparent padding was scaled incorrectly -> FAIL.
3. Rubix and client logos not on same optical baseline -> FAIL.
4. Full-page Golden Visual Master accepted but no SHA recorded -> FAIL.
5. Visual-Mirror PPTX slide uses a different or compressed image -> FAIL.
6. Golden PDF page differs from approved master -> FAIL.
7. HTML rebuilds page as responsive cards instead of preserving the master -> FAIL for visual-fidelity mode.
8. Three consecutive analytical pages use generic equal-card grammar without meaningful relationship -> FAIL visual rhythm.
9. Page contains Saudi flag/screen/person as relevant visual context -> ALLOWED, not automatically rejected.
10. Page contains fake generated logo/official value treated as fact -> FAIL.
11. More than six pages generated without continuity ledger update -> FAIL.
12. Continue command without style anchors/previous page/ledger -> FAIL.
