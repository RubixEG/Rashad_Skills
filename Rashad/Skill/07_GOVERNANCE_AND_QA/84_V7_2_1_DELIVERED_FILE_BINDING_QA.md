# V7.2.1 — Delivered-File Binding QA

**STATUS: CURRENT V7.2.1 GLOBAL QA / DELIVERY AUTHORITY**

## Mandatory last-mile gate
Immediately before any user-visible artifact link, execute:

`Rashad/Brain/runtime/exact_artifact_handoff_guard.py`

or the equivalent runtime call to `brain.exact_handoff.issue_exact_handoff_certificate`.

The only successful terminal state is:

```text
CERTIFIED_FOR_HANDOFF
```

Anything else is `BLOCK_HANDOFF`.

## Required attack coverage
The final verifier must prove that Rashad blocks:
- delivered-file SHA mismatch;
- deck pixel-review SHA mismatch;
- product-inspection SHA mismatch;
- slide-count mismatch;
- production-render-count mismatch;
- page pixel-review-count mismatch;
- final trace describing another artifact;
- `IMAGE_LED` with logo-only media;
- product-inspection/card-grid/shape-only failures;
- reuse of a handoff certificate for different bytes.

## Permanent real incident regression
The actual 2026-08-17 14-slide delivered deck and a minimized copy of its 24-page dossier are preserved under the incident fixtures. They must always return `BLOCK_HANDOFF` with the known mismatch blockers.
