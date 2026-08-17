# AR-SEQ-001 Hard-Gate Test Suite

## Purpose
Prevent recurrence of Arabic ordered artifacts that begin on the left or bottom, reverse in later rows, or change order between HTML, PDF, and PowerPoint.

## Required positive fixtures
1. Four-stage horizontal flow: `١` rightmost.
2. Four-step vertical flow: `١` topmost.
3. Seven-item wrapped grid: `١` right of row one and `٥` right of row two.
4. Four-step diagonal/staircase: `١` top-right, final item bottom-left.
5. Radial process: `١` in upper-right quadrant with explicit connectors.

## Required negative fixtures
1. Item `١` on the left.
2. Item `١` at the bottom.
3. Bottom-to-top staircase.
4. First row correct, second row reversed.
5. Correct number positions but arrows pointing the opposite way.
6. Western sequence numerals in Arabic output.
7. Numbers baked into an AI-generated raster image.
8. HTML correct but PDF reversed.
9. HTML/PDF correct but PowerPoint objects reversed.
10. Numbered artifact with no sequence contract.

## Assertions
- blueprint schema passes;
- logical indices are unique and contiguous;
- visual slots are unique;
- DOM coordinate invariants pass;
- PDF raster coordinate invariants pass;
- PowerPoint shape coordinate invariants pass;
- connector vectors match the declared path;
- labels use Arabic-Indic numerals;
- no waiver exists without explicit user approval.

## Release result
Any failed assertion returns:

```text
REJECTED — AR-SEQ-001 ORDERED-FLOW VIOLATION — REBUILD REQUIRED
```
