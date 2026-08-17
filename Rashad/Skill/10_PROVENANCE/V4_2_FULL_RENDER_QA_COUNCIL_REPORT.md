# Rashad v4.2 — Full Render QA Council Report

## Council verdict
**GO — non-breaking architecture/QA hardening release.**

The council rejects the earlier assumption that overflow/collision checks alone are sufficient. v4.2 governs every applicable rendered object through geometry, rendered line fragments, ownership, anchors, spacing, layer order, transforms, topology, assets, stress mutation and export parity.

## Root problems closed
1. Arabic title/subtitle overlap can no longer hide behind container-level overflow PASS.
2. Required gates cannot PASS with zero testable objects.
3. Number badges/KPIs/icons/markers must remain attached to declared owners/anchors.
4. `data-artifact-type=system` cannot spoof a higher-order artifact.
5. Scale/mirror/clip/opacity/z-index defects are explicit failure surfaces.
6. Tables/dense evidence and asset geometry are governed.
7. 1080p screenshot masters are not production authority; final masters are 4K minimum, with 6K target for critical dense pages.
8. PDF and PPTX Visual Mirror must derive from the exact same final page master hashes.
9. Image generation is the final tool action in the turn; product state is saved before the call and resumed on the next turn.
10. Stress QA now uses mutation families rather than repeating only the same weak detectors.

## Executable evidence from QA Harness v2.5
- Regression: 12/12 expected outcomes.
- Clean stress mutations: 6/6 PASS.
- v4.1 pilot back-test: 6/6 pages blocked, proving the previous 6/6 PASS is no longer trusted.

## Non-regression
- Baseline files: 1160
- Added: 18
- Modified: 6
- Removed: 0
- Byte-for-byte unchanged: 1154/1160 (99.48%)
- Protected checked: 591
- Protected changed: 0
