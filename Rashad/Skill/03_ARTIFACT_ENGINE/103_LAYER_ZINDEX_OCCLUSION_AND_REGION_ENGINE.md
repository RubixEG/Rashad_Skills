# Layer, Z-Index, Occlusion & Region Engine

Validate:
- layer order is explicit and consistent with `data-layer-order`;
- labels/text are not hidden behind opaque surfaces;
- connectors do not cross above text unless intended;
- region children remain inside their governed region;
- overlays do not cover titles, sources, page numbers, legends or evidence;
- background/hero layers cannot unexpectedly intercept foreground content.

Use rendered hit-testing (`elementFromPoint`) and computed z-index, not source order alone.
