# Required Instrumentation & No-Vacuous-Pass Contract

Each Page Spec declares applicable counts/classes before rendering, including as relevant:
`header_roles`, `nodes`, `edges`, `labels`, `owners`, `alignment_groups`, `spacing_groups`, `sequence_groups`, `dividers`, `tables`, `images`, `logos`, `sources`, `regions`.

Rule:
`required=true AND actual_test_count=0 -> FAIL_NOT_INSTRUMENTED`.

A page cannot claim PASS by omitting data attributes or by calling itself a SYSTEM/TIMELINE/MATRIX without measurable structure.
