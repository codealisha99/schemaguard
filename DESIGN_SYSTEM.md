# SchemaGuard design system

SchemaGuard is a deterministic JSON repair and strict validation tool for developers working with structured model output. Its direction is a technical field manual: warm paper, forest-green controls, compact monospaced labels, numbered input/output panels, and readable repair evidence. Product identity remains SchemaGuard. Maintenance attribution uses Alisha Karma / codealisha99 without changing historical authorship.

## Semantic palette

`app/static/tokens.css` is the source of truth. Shared layout and components live in `style.css`; generated API documentation uses `docs.css` and token-backed `docs-theme.js`.

| Role                                 | HEX                                           |
| ------------------------------------ | --------------------------------------------- |
| Brand / hover                        | `#224F3E` / `#163C2E`                         |
| Secondary accent                     | `#925520`                                     |
| Primary / secondary / muted text     | `#202A23` / `#3E4B40` / `#5E685E`             |
| Page / surface / elevated surface    | `#F7F6F0` / `#EEEFE7` / `#FFFFFF`             |
| Selected surface / on-brand text     | `#E4EBDF` / `#FFFFFF`                         |
| Divider / control border             | `#D4DACF` / `#788475`                         |
| Focus / code focus                   | `#1769B3` / `#A9DBE7`                         |
| Success / surface                    | `#14634A` / `#E9F5EE`                         |
| Warning / surface                    | `#855009` / `#FFF4DF`                         |
| Error / surface                      | `#A02D3C` / `#FFF0F1`                         |
| Information / surface                | `#225E99` / `#EDF4FC`                         |
| Code / elevated code / border        | `#1C2923` / `#29372E` / `#53685A`             |
| Code text / muted text               | `#E4EEEA` / `#AFC2B9`                         |
| Code key / string / number / literal | `#A9DBE7` / `#B5E0C2` / `#F6C887` / `#D4C5F0` |
| Code success / surface               | `#B5E0C2` / `#24483B`                         |
| Code warning / surface               | `#F6D393` / `#493B22`                         |
| Code error / surface                 | `#FFC0C6` / `#4C2C33`                         |

The interface intentionally uses one light theme with dark editor surfaces; no theme switch is offered. Informational borders differ from interactive control borders. Focus on dark editors uses a separate contrast-safe token. Status text, icons, and messages accompany semantic colors.

## Typography and layout

Existing local variable fonts remain: Manrope for interface text and headings; JetBrains Mono for JSON, contracts, and protocol labels. Both use `font-display: swap` and system fallbacks. The landing page preloads Manrope; no Google font request is required.

| Token                              | Scale                                                          |
| ---------------------------------- | -------------------------------------------------------------- |
| Helper / small / body / lead       | 12 / 14 / 16 / 18 px                                           |
| Section heading                    | Fluid 28–40 px                                                 |
| Display heading                    | Fluid 38–68 px                                                 |
| Body line height                   | 1.65                                                           |
| Code line height                   | 1.85; mobile editor 1.7                                        |
| Spacing                            | 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80 px                    |
| Content width / gutter             | 76 rem / fluid 16–48 px                                        |
| Control / panel / workspace radius | 4 / 8 / 12 px                                                  |
| Border                             | 1 px; process dividers 2 px                                    |
| Motion                             | 160 ms default; reduced motion disables nonessential animation |
| Layers                             | Disclosure 10; skip link 20                                    |

The only elevated shadow belongs to schema disclosure. Editors stack at 650 px; supporting layouts collapse at 850 px. Category and secondary workspace hints disappear below 1100 px. The mobile textarea stays at 16 px for readable input without automatic iOS zoom.

## Shared components and behavior

- Product header, active navigation, footer, maintenance/contact links, and matching favicon.
- Primary/secondary actions with hover, focus, disabled, busy, success, fallback, and failure feedback.
- Keyboard schema tabs with roving focus, arrows, Home, End, and a shared selected surface.
- Schema contracts generated from the API, native schema/fallback disclosures, and Escape dismissal for schema inspection.
- Numbered input/output panels, editable line-numbered input, character limit, expand/compact controls, and selectable syntax-highlighted output.
- Accurate example selection after formatting; Unicode character counts consistent with Python limits.
- Input errors with `aria-invalid`, linked guidance, focus recovery for empty/oversized submissions, and preserved input on request failure.
- Explicit fallback disclosure, field issues, actual transformation chips, and repair timeline.
- Documentation view navigation, token-backed ReDoc theme, and a JavaScript-disabled specification link.
- Browser 404 recovery with retained HTTP 404 status; machine-readable API errors stay JSON.

ReDoc's theme attribute follows its [official HTML configuration](https://redocly.com/docs/redoc/deployment/html#theme-configuration); colors and fonts are read from CSS tokens before its existing bundle initializes. Third-party attribution remains in `THIRD_PARTY_NOTICES.md` and local font/icon license files.

## Verification boundaries

`npm run build && npm run check:frontend` checks JavaScript syntax, three static outputs, asset paths, duplicate IDs, ARIA references, and 26 text contrast pairs (minimum observed 5.01:1), plus focus/control contrast pairs. Browser checks supplement these token checks; neither alone certifies full accessibility. Current route results and incomplete accessibility checks are recorded in [docs/REDESIGN_AUDIT.md](docs/REDESIGN_AUDIT.md).
