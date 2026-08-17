# Proposal Workflow — Chat Mirror Context Contract

STATUS: ACTIVE CONTEXT MAP

## Principle
Reader-facing order is not authoring order. Use the current v2.5 parallel/dependency workflow rather than recreating the proposal in numeric section order.

## Core flow
RFP ingestion/evidence → compliance and bid strategy → scope/R-code plan → parallel proposal workstreams constrained by dependencies → section content → councils → Artifact Intelligence → native/deterministic production → QA/release.

## Late products
Executive Summary and CEO Letter remain late synthesis products even if they appear early in the final proposal.

## Context loading
For a requested section, load only:
- the section contract;
- its upstream dependencies;
- exact R-code prompts required by the approved plan;
- current evidence;
- relevant service-line/council modules;
- Artifact/brand/production authorities if an artifact is requested.

Never load all 388 prompt bodies by default.
