# Final Release Evidence Aggregation Gate

STATUS: FINAL MACHINE-EVIDENCE AGGREGATOR — v2.6.4.6

The external final-release aggregator may emit `RELEASED` only when it receives evidence IDs containing all required stage verdicts:
1. `HTML_PREEXPORT_PASS`;
2. `PDF_PARITY_PASS`;
3. `PPTX_PARITY_PASS`;
4. `DECK_CONTINUITY_PASS`.

This machine aggregation does not waive Consulting Visual Excellence, evidence/compliance, Artifact Council, brand, or Release Council requirements. Any active Rashad hard blocker still prevents final delivery.

## Multi-page deck aggregation
Per-page HTML reports must be aggregated across the full deck. `HTML_PREEXPORT_PASS` for a deck is valid only when every required page report is `HTML_PREEXPORT_PASS`; one passed page cannot stand in for the deck.
