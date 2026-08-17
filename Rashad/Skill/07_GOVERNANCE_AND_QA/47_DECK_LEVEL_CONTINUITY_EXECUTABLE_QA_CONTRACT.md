# Deck-Level Continuity Executable QA Contract

STATUS: HARD LONG-DECK REGRESSION CONTRACT — v2.6.4.6

Per-page QA is insufficient for a 20–40 page Golden Visual Master deck. The companion continuity checker consumes the Deck Continuity Ledger and verifies at minimum:
- every master exists and matches its frozen SHA;
- previous-page adjacency links are coherent;
- each page is checked against its approved Style Anchor / page-family anchor when available;
- material lightness, visual-density/edge-density and coarse color-histogram drift stay inside calibrated tolerances.

This executable fingerprint is a regression detector, not a substitute for the Deck Continuity & Consulting Visual Council. Final release requires both applicable human/AI council approval and executable `DECK_CONTINUITY_PASS`.
