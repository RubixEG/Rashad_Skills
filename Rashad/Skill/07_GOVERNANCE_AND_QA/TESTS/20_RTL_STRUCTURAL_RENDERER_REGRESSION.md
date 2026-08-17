# RTL Structural Renderer Regression — v2.6.4.2

STATUS: HARD DIRECTIONAL REGRESSION SUITE

Required assertions:
- Arabic horizontal semantic item 1 is physically rightmost unless explicitly excepted.
- Process progression direction is right-to-left where Arabic reading logic governs.
- Timeline origin is right for Arabic ordered timelines.
- Connector endpoints are recalculated after directional geometry.
- Latin acronyms/API identifiers remain LTR islands.
- Logos are never mirrored.
- Rubix | Client remains physically left and in the approved order.
- charts/maps/photos follow their component-specific preserve policy.
- no whole-canvas flip is used as a substitute for semantic direction resolution.

Any regression is release-blocking.
