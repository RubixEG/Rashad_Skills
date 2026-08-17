# Bug-to-Regression Policy

STATUS: ACTIVE PRODUCTION ENGINEERING POLICY — v2.6.4.2

## Rule
Every confirmed production defect must become a permanent regression test before the defect is considered closed.

Examples:
- Arabic timeline begins on left → add `test_arabic_timeline_origin_is_right`.
- connector disappears → add edge-preservation/topology test.
- PDF clips footer → add footer-boundary regression.
- Rubix logo mirrors → add co-brand no-mirror test.
- font fallback causes overflow → add font-preflight regression.
- PPTX shifts nodes → add PPTX geometry/topology regression.

## Closure conditions
A defect is closed only when:
1. root cause identified;
2. renderer/contract fix defined;
3. regression test added;
4. test fails against defective behavior;
5. test passes after fix;
6. full Golden Regression suite still passes.

A solved defect must not silently return.
