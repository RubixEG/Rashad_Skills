# V7.2.1 — Exact Artifact Handoff Lock

**STATUS: CURRENT V7.2.1 GLOBAL HANDOFF AUTHORITY**

## Incident closed
`I16 / INCIDENT_P0_WRONG_ARTIFACT_HANDOFF_20260817`: the file delivered to the user was a 14-slide generic deck, while the QA/delivery dossier described a different 24-page artifact and a different SHA-256. This is a P0 delivery-integrity failure.

## Non-negotiable law
The artifact the user receives must be the **same bytes** that passed product inspection, actual-pixel QA and the delivery dossier.

Before any PPTX/PDF/bundle link is surfaced, Rashad must execute the exact handoff guard and obtain `CERTIFIED_FOR_HANDOFF`.

Required PPTX identity:

```text
DELIVERED_PPTX_SHA
= DELIVERY_DOSSIER.output_file_sha256
= DELIVERY_DOSSIER.deck_pixel_review.deck_sha256
= DELIVERY_DOSSIER.product_inspection.pptx_sha256
```

Required count identity:

```text
actual PPTX slide count
= dossier page count
= PASS page-pixel-review count
= production-page-render count
```

Any mismatch is `BLOCK_HANDOFF`.

## Product-truth law
- `IMAGE_LED` requires a real image on the corresponding final slide.
- One picture repeated across most pages is treated as likely logo/chrome and cannot satisfy image-led evidence.
- Product-inspection blockers remain handoff blockers; a later file copy/rebuild cannot inherit an earlier QA PASS.
- A shape-only/card-grid/structurally repetitive analytical deck cannot be handed off as a valid Artifact output.

## Trace law
The final trace must describe the actual delivered file. Planned-state traces have zero handoff authority. If a trace says 24 pages and the file has 14 slides, handoff is blocked.

## Handoff certificate
The final certificate is generated only from the delivered bytes after all production work is complete. The certificate records exact SHA-256, byte size, slide count, dossier count, production-render count, pixel-review count and product-inspection status.

`QA_CANDIDATE_PASS` or `DELIVERY_ALLOWED` without an exact handoff certificate is insufficient for user-facing file delivery.
