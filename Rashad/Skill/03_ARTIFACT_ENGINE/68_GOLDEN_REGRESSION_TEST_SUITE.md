# Golden Regression Test Suite

STATUS: PERMANENT RENDERER REGRESSION CONTRACT — v2.6.4.2

## Purpose
Prevent a fix to one page class from silently breaking another.

## Representative difficult cases
The executable renderer implementation should maintain approved baselines for at least:
1. complex scope architecture;
2. large BOQ page;
3. scope-to-BOQ compression map;
4. Arabic timeline;
5. Arabic multi-stage journey;
6. mixed Arabic/English page;
7. complex team requirements table/architecture;
8. evaluation matrix/criteria-to-win artifact;
9. risk architecture/network;
10. governance operating model;
11. technical architecture;
12. integration diagram;
13. long Arabic title/body page;
14. dense evidence page;
15. cover;
16. Rubix | Client co-brand page;
17. chart page;
18. commercial/financial exposure page;
19. large table;
20. strategic clarification register;
21. bid decision cockpit.

## Build rule
Every renderer change reruns the full Golden Test Suite. If a change fixes one baseline but breaks another hard requirement, the build fails.

## Baseline policy
Golden baselines test geometry/structure/direction/brand behavior. They are not reusable client templates and do not override current RFP facts or current brand authorities.
