# Deck Style Anchor & Continuity Batch Protocol

STATUS: HARD CONTINUITY AUTHORITY — v2.6.4.7

## Problem solved
When a deck exceeds 20 pages, generation cannot rely on chat memory or a single prompt. Every batch must inherit the same visual DNA, style anchors and previous-page lineage.

## Pre-generation setup
Before generating Page 1, lock:
- Deck Visual DNA;
- approved palette and accent discipline;
- cover anchor;
- analytical artifact anchor;
- dense-evidence anchor;
- technical/commercial anchor;
- optional decision/risk anchor;
- co-brand geometry;
- footer/page chrome geometry;
- typography and RTL behavior;
- image aspect ratio and resolution.

## Batch size
Generate in controlled batches of 4-6 pages. Do not ask for an entire 20-30-page visual deck in one generation pass.

## Every page prompt must include
- Deck Visual DNA;
- current section anchor;
- current page artifact brief;
- previous approved page reference unless page 1;
- page family and depth level;
- forbidden weak fallback family;
- output mode: `GOLDEN_VISUAL_MASTER_PAGE`.

## After every batch
Run:
- page-level visual QA;
- artifact-strength QA;
- RTL visual-flow QA;
- co-brand/cover geometry QA where relevant;
- visual rhythm audit;
- Deck Continuity Ledger update;
- regenerate outlier pages before moving to next batch.

## Continue command rule
If the user says continue, resume from the ledger, anchors and approved masters. Do not infer style from the chat transcript alone.
