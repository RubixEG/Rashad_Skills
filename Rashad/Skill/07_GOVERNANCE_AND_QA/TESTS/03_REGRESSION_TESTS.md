# Regression Tests

Compare v7.0 against preserved v6.5 for:
- section shell;
- generation order;
- summary completeness;
- logo and brand purity;
- Arabic RTL and numerals;
- overflow safety;
- artifact editability;
- compliance placement;
- dependency behavior;
- PowerPoint parity.

Any regression requires rollback or explicit authorized exception.

Additional v7.1 regression coverage:
- HTML/PDF renderer identity;
- fixed canvas dimensions;
- font embedding and fallback rejection;
- DOM bounds and collision detection;
- top-right start for diagonal Arabic sequences;
- top-to-bottom row progression;
- no rotated Arabic labels;
- no hidden overflow or mandatory ellipsis.


Additional v7.4 regression coverage:
- exact deck reading order remains unchanged;
- Section 3 is first produced only after the strategy gate;
- existing summary fields are preserved while adding user-specified extraction fields;
- historical proposal analysis cannot contaminate current brand or source truth;
- missing visual KB records cannot break analytical generation;
- AR-SEQ-001 and renderer parity remain unchanged.
