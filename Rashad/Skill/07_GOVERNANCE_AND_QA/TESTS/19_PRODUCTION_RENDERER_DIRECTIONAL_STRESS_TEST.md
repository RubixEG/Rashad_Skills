# Production Renderer Directional Stress Test — v2.6.4.2

STATUS: REQUIRED KNOWLEDGE/IMPLEMENTATION ACCEPTANCE SUITE

## Adversarial scenarios
1. Arabic page text is RTL but ordered cards start physically left → HARD FAIL.
2. Arabic timeline origin is left → HARD FAIL.
3. LTR API box inside RTL page → must remain LTR and bidi-safe.
4. Rubix | Client cluster mirrors under RTL → HARD FAIL.
5. 15 expected nodes, 14 rendered → HARD FAIL.
6. 23 expected edges, 22 rendered → HARD FAIL.
7. Edge clipped at artifact boundary → HARD FAIL.
8. Label detached from node/edge → HARD FAIL.
9. Long Arabic title overflows → repair/split/fail; never hide.
10. Dense BOQ forces tiny font → split/restructure within same artifact family.
11. Font silently substitutes and changes wrapping → HARD FAIL.
12. Client logo aspect ratio drifts → HARD FAIL.
13. System architecture becomes cards → HARD FAIL.
14. Responsive HTML reflows composition → HARD FAIL.
15. PDF line wrapping differs materially from approved geometry → parity FAIL.
16. PPTX shifts shapes/connectors → parity FAIL.
17. Chart is blindly mirrored → FAIL unless chart policy explicitly requires it.
18. Photograph is mirrored by page RTL → FAIL.
19. Footer leaves safe bounds → FAIL.
20. Table overlaps footer → FAIL.
21. technically safe page scores below ministry/consulting threshold → REDESIGN upstream.
22. renderer runtime unavailable but report says machine PASS → GOVERNANCE FAIL.

## Expected behavior
Every confirmed production defect must be mapped into the Bug-to-Regression policy.
