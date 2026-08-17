# Rashad Unified QA Runtime v4.0 FINAL — Code Handoff

Use this package as the QA baseline when converting Rashad Skill + QA to code. Do not rebuild the taxonomy or lower thresholds. Wire real producers to the measurement/judge/source evidence contracts, then call `release-product-v4` as the only final product-release route.

Core integration surfaces:
- `rashad_qa.py` — CLI/orchestrator
- `qa_v4/detector_registry.py` — 233-case implementation/provenance enforcement
- `qa_v4/stress_runner_final.py` — exact v7 20-mutation runner
- `validation/execution_dossier_v4.py` — page-chain + judge/render/diversity/master/state checks
- `validation/proof_integrity_v4.py` — product proof checks
- `validation/skill_binding_v4.py` — v7.0.1 authority binding
- `qa/parity_qa.py` — PDF/PPTX parity
- `qa/unified_html_qa.py` — browser/DOM/pixel QA

Never interpret `FINAL` as permission to bypass per-product evidence.
