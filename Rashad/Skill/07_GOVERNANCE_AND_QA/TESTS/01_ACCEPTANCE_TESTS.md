# Acceptance Tests

1. Uploading files does not automatically generate sections.
2. First generated output is RFP Understanding Summary.
3. Summary includes full available RFP coverage.
4. Exact deck shell is preserved.
5. Executive Summary and CEO Letter are generated late.
6. Compliance Matrix is Section 0 after TOC.
7. Arabic ordered sequences satisfy AR-SEQ-001: horizontal starts right, vertical starts top, diagonal starts top-right, and wrapped rows restart right.
8. Arabic client-facing numerals use the approved form.
9. No old or generated logo can pass.
10. No production slide is a flattened AI image.
11. No text overlap, hidden text, clipping, or overflow.
12. Every page answers an evaluator question.
13. Every material claim has evidence and confidence.
14. Every section has a contract and distinct ownership.
15. Changes propagate and mark dependent pages stale.
16. Every critical technical page passes a relevant service-line review.
17. Vendor pages state business outcome, capability, criteria, integration, security, and exit assumptions.
18. Government digital/cyber references are retrieved from current official sources when applicable.
19. Critical pages score 92+ and overall scores 90+.
20. PowerPoint maps approved artifacts without independent rewriting.
21. Production PDF is generated from the same pinned Chromium engine used for HTML review.
22. WeasyPrint cannot be used for slide-like production artifacts.
23. No mandatory content relies on `overflow:hidden` or ellipsis.
24. Arabic diagonal paths start at top-right and progress down-left.
25. Arabic multi-row grids restart each row from the right.
26. No Arabic text is rotated or vertically written.
27. All critical DOM rectangles fit within the fixed page safe zone.
28. PDFium and Poppler renders are materially equivalent.
29. HTML golden screenshot and PDF raster pass parity comparison.
30. No Arabic ordered artifact begins at the left or bottom.
31. No Arabic ordered artifact progresses bottom-to-top.
32. Sequence contract and explicit visual-slot map exist for every numbered artifact.
33. HTML, PDF, and PowerPoint object coordinates preserve the same sequence.

34. RFP-SUM-001 searches annexes semantically and does not depend on fixed page numbers.
35. Summary extracts identity/logo, dates, duration, location, phase content/outputs, BOQ, training, evaluation, and team when present.
36. Source phase order and analytical dependency order remain separate.
37. SEC-DEP-001 blocks Section 3 until the Bid Strategy Gate is approved.
38. Reading, production, and finalization orders are stored separately.
39. Compliance Register v0 begins early and final Section 0 closes late.
40. Executive Summary Strategy Skeleton begins early and final Section 2 closes late.
41. VIS-KB-001 references cannot enter production before scoring, council review, and promotion.
42. The three v7.4 tracks pass non-interference tests.
