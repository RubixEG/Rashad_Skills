# RFP Authorship Assessment Schema

```text
AUTHORSHIP_ASSESSMENT {
  model: SINGLE_CLIENT_OWNER | INTERNAL_MULTI_FUNCTION_TEAM | EXTERNAL_ADVISORY_LED | HYBRID_COMPILED_PACKAGE | INSUFFICIENT_EVIDENCE
  confidence_0_100
  procurement_maturity_0_100
  evidence_dimensions[] {
    dimension_id
    score_0_5
    evidence_for[]
    evidence_against[]
    source_refs[]
    bid_implication
  }
  evidence_for_model[]
  counter_evidence[]
  proposal_implications[]
  clarification_implications[]
  pricing_implications[]
  council_owner
  approver
}
```

No named external author may be asserted without explicit source evidence.
