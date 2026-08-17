# Layout Budget and Collision Engine

## Principle
A page is not valid because it looks correct in one preview. It is valid only when every critical element fits within the fixed canvas in HTML and PDF.

## Safe zones
Default fixed-slide safe zones:
- left: 48px;
- right: 48px plus approved brand rail;
- top: 38px;
- bottom: 42px;
- logo inset: normally at least 72px from trim;
- footer content must remain inside its reserved band.

## Vertical page budget
Every page contract must reserve explicit bands for:
- header/logo area;
- section label;
- title;
- subtitle/thesis;
- primary artifact;
- insight/source/footer area.

No component may borrow space from the footer or another band without a page-contract revision.

## DOM preflight
Before PDF creation, measure every critical element using `getBoundingClientRect()`.

Reject when:
- `left < safe_left`;
- `right > slide_width - safe_right`;
- `top < safe_top`;
- `bottom > slide_height - safe_bottom`;
- `scrollWidth > clientWidth`;
- `scrollHeight > clientHeight`;
- mandatory text is ellipsized;
- two critical text/component rectangles overlap unexpectedly;
- a footer rectangle intersects body content;
- a logo or source note exceeds its zone.

Decorative elements may exceed the content safe zone only when explicitly tagged and clipped by a dedicated decorative mask. Critical content may never be clipped.

## Collision classes
Hard-fail collisions include:
- text over text;
- title over subtitle;
- text behind a card or shape;
- number badge over body copy;
- footer over content;
- source note over page number;
- logo over title or rail;
- chart labels outside plot bounds.

## Overflow resolution order
1. select a better artifact/component;
2. shorten supporting copy without losing mandatory facts;
3. increase page count;
4. adjust approved internal spacing;
5. reduce font size only within approved minimums.

Never resolve overflow by clipping or scaling the full page.
