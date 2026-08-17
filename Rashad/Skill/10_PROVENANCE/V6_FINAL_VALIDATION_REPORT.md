# V6 Final Validation Report

```json
{
  "baseline_files_ex_manifest": 1204,
  "v6_files_ex_manifest": 1242,
  "unchanged": 1198,
  "modified": 6,
  "added": 34,
  "removed": 0,
  "protected_checked": 591,
  "protected_changed": 0,
  "startup_routing": true,
  "missing_v6_paths": [],
  "skill_frontmatter": true,
  "qa_compile": true,
  "qa_regression": "PASS",
  "qa_regression_count": "19/19",
  "artifact_stress": {
    "runs": 500,
    "crashes": 0,
    "passes": 498,
    "pass_winner_budget_violations": 0,
    "graphs_per_sec": 324.1,
    "status": "PASS"
  },
  "html_stress": {
    "id": "C9_STRESS",
    "name": "Metamorphic robustness + fault-injection stress",
    "required": true,
    "executed": true,
    "test_count": 12,
    "status": "PASS",
    "violations": [],
    "measured": {
      "robustness_modes": [
        "ARABIC_INDIC_NUMERALS",
        "ARABIC_TEXT_GROWTH_120",
        "FIVE_DIGIT_BADGE",
        "FONT_SCALE_108",
        "FONT_SCALE_110",
        "LINE_HEIGHT_108",
        "LOGO_CANVAS_PADDING",
        "LONG_SOURCE_LINE"
      ],
      "fault_injection_modes": [
        "FONT_FALLBACK",
        "LONG_LATIN_TOKEN",
        "NODE_GROWTH",
        "TITLE_THREE_LINES"
      ]
    }
  },
  "parity": "PASS",
  "release_positive": "RELEASED",
  "release_negative": "BLOCKED"
}
```
