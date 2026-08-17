# V4 Root Cause & Architecture Decision

## Trigger
Version 3 still produced pages with overflow/collision risk, detached or weakly connected nodes, card-dominant composition, weak whole-page harmony, and insufficient executable inspection of fonts/layers/dividers/geometry.

## Root cause
Rules existed but the runtime did not expose enough semantic instrumentation and the QA stack did not inspect the complete rendered object graph and pixels. Safety checks could therefore miss or fail to prove element placement, topology and visual integrity.

## Decision
Version 4 makes whole-page visual thinking/GVM the design truth, semantic reconstruction the execution layer, instrumentation mandatory, and an executable DOM+pixel QA harness mandatory before release.
