# SchemaGuard design system

SchemaGuard is a developer tool for deterministic JSON repair and strict schema validation. Its visual direction is restrained and technical: readable typography, clear contracts, quiet surfaces, and a visible distinction between original input, repaired output, and explicit fallback.

## Tokens

`app/static/tokens.css` is the source of truth. `style.css` implements shared components and page layouts; `docs.css` adapts the generated API documentation.

| Role | HEX |
| --- | --- |
| Brand / hover | `#145C52` / `#0E463F` |
| Accent | `#99501A` |
| Primary / secondary / muted text | `#182724` / `#354743` / `#586A65` |
| Page / surface / selected surface | `#FFFFFF` / `#F5F8F7` / `#E7F1ED` |
| Divider / control border | `#DBE4DF` / `#74887E` |
| Focus | `#1769B3` |
| Success / surface | `#14634A` / `#E9F5EE` |
| Warning / surface | `#855009` / `#FFF4DF` |
| Error / surface | `#A02D3C` / `#FFF0F1` |
| Information / surface | `#225E99` / `#EDF4FC` |
| Code / elevated code | `#172B29` / `#203633` |
| Code text / muted text | `#E4EEEA` / `#AFC2B9` |
| Code key / string / number / literal | `#A9DBE7` / `#B5E0C2` / `#F6C887` / `#D4C5F0` |

Manrope provides headings, body text, navigation, and controls. JetBrains Mono provides code, field names, and traces. Both existing variable fonts are served locally with `font-display: swap` and system fallbacks. Body text is 15 px; helper text is 12–13 px. Headings and display text scale fluidly.

Spacing uses a 4 px base, with 8, 12, 16, 20, 24, 32, 40, 48, 64, and 80 px steps. Content is capped at 76 rem; gutters scale from 16 to 48 px. Radii are 6, 12, and 20 px. Transitions last 160 ms and respect reduced motion. The site uses a light theme with dark code surfaces.

## Shared patterns

- Header and footer preserve SchemaGuard identity and link to the existing playground, API documentation, source, and creator.
- Buttons expose focus, hover, disabled, and loading states. Run feedback separates valid, repaired, fallback, and failed results.
- Schema tabs use roving keyboard focus with arrow, Home, and End keys. On narrow screens three equal columns wrap labels without clipping.
- The input editor has visible limits, line numbers, validation guidance, and safe formatting. Output preserves selectable text and uses semantic syntax colors.
- Status messages use text and icons alongside color. Empty states explain the next action. Error details identify fields without exposing submitted values.
- Schema disclosure, fallback disclosure, trace, contract fields, and API examples retain real data and interactions.

`npm run build && npm run check:frontend` verifies JavaScript syntax, build outputs, asset paths, ARIA references, and 26 text contrast pairs. The minimum tested text ratio is 5.36:1. Run browser accessibility checks alongside these token checks; token ratios alone do not certify accessibility.
