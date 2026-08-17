# V6.1 Page Execution Dossier Contract

For each critical analytical page create:

```text
pages/<page_id>/
  content_pack.json
  relationship_graph.json
  artifact_truth.json
  exhibit_hypotheses.json
  exhibit_selection.json
  evidence_pack.json
  visual_search/manifest.json
  visual_search/candidate_01.png
  visual_search/candidate_02.png
  visual_search/candidate_03.png
  ceqs.json
  final_page_master.png
  qa/html_report.json
  qa/repair_safety.json        # required when a repair occurred
  state_transitions.json
```

The product root creates `proof_index.json` enumerating every released page dossier.

Critical analytical pages require exactly five exhibit hypotheses and at least three actual rendered candidates. **No page-family exemption may reduce either count for a critical analytical page.** Non-critical covers/dividers or explicitly non-analytical page families may use a documented Page Spec exception, but it cannot waive evidence, applicable QA, truthfulness, or final-master requirements.

The external Unified QA Runtime validates this contract. The Skill never self-certifies it.
