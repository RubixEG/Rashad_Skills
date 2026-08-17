# Font, Glyph, Typography & BiDi Engine

Validate the actual rendered typography, not requested CSS declarations.

Required checks:
- required font face is loaded for the actual string;
- no silent fallback for governed text styles;
- minimum body/source/label font sizes;
- title/subtitle/body hierarchy;
- controlled line-height and line count;
- Arabic shaping and mixed LTR island policy;
- URLs/API/ISO/technical IDs preserve LTR logical order;
- no Unicode replacement characters or known tofu/square leakage in visible source text;
- Arabic numbers follow active numeral policy unless technical-token exception applies.

Typography failure that changes legibility or meaning is HARD FAIL.
