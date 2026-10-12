# SchemaGuard architecture

SchemaGuard is a deterministic JSON repair and validation service with a public playground. FastAPI serves the API and local interface; Node copies the static assets into production build output. The application does not call a language model or persist submitted content.

## Code map

| Location                               | Responsibility                                                                                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `app/main.py`                          | Strict Pydantic schemas; bounded parsing, conservative repair, safe formatting, request limits, security headers, health probes, and page routes |
| `app/pages.py`                         | Shared product header/footer, generated API documentation chrome, browser 404 response                                                           |
| `app/error.html`                       | Browser error template, also used by the static build                                                                                            |
| `app/run.py`                           | One-worker Uvicorn entrypoint and trusted proxy configuration                                                                                    |
| `app/static/index.html`                | Shared overview/playground template and canonical product chrome                                                                                 |
| `app/static/app.js`                    | Schema examples, input/output, fallback, actual repair trace, network and clipboard handling                                                     |
| `app/static/components.js`             | Keyboard schema tabs and stateful validation-button feedback                                                                                     |
| `app/static/tokens.css`, `style.css`   | Semantic design tokens, typography, components, responsive layout, reduced motion                                                                |
| `app/static/docs.css`, `docs-theme.js` | Swagger presentation and token-backed ReDoc configuration                                                                                        |
| `app/static/icon.svg`                  | Shared original SchemaGuard logo: JSON braces and a check                                                                                        |
| `scripts/build-frontend.mjs`           | Copies assets; emits `index.html`, `playground.html`, and `404.html`                                                                             |
| `scripts/check-frontend.mjs`           | Syntax, built assets, IDs/ARIA references, and semantic color-contrast checks                                                                    |
| `tests/test_app.py`                    | API contracts, repair boundaries, resource limits, isolation, safe errors, health, documentation, and 404 regression coverage                    |

## Request flow

The playground sends same-origin requests to `/v1/validate`. The server bounds the request body and rate, then attempts strict parsing and schema validation. If syntax is invalid, it can remove a complete enclosing Markdown fence, convert bounded single-quoted string tokens, and remove trailing commas outside strings. Each changed candidate is parsed and validated before the next step. A successfully parsed object with wrong fields or types stops syntax repair.

Fallback is explicit and validated against the same schema. A fallback result is reported separately from valid or repaired input. Response aliases remain available for existing API clients. The frontend renders input-derived content as text nodes, preserving literal JSON without executing HTML.

Resource limits and error status codes are documented in [README.md](../README.md). Rate counters are bounded, in-memory, per-process values; they are not distributed across replicas. No database migrations or authentication system exists. `DATABASE_URL` is optional and used only by the explicit `/health/database` read-only connectivity probe.

## Local and recorded production layouts

Locally, FastAPI serves product pages, `/static`, documentation, and the API on port 8006 by default. The recorded production configuration serves Node-built static output on Vercel and forwards API, documentation, and health routes to the Railway FastAPI service. These recorded configurations do not prove the current hosted account/deployment state.

The overview and dedicated playground share a template and use `data-page` to select their layout. API docs and browser 404 pages extract the same header/footer. When changing product chrome, keep the header/footer structure compatible with both the Python renderer and Node build; exercise all page routes after changes.

## Dependencies and checks

Runtime requirements are pinned in `requirements.txt`; test requirements are pinned in `requirements-dev.txt`. Node scripts use built-in modules and do not need an npm dependency installation. There is no configured TypeScript checker or formal lint task. CI runs the existing dependency, backend, build, and frontend integrity checks. It has read-only repository access and does not publish or deploy.

## Project identity

The owner-supplied creator and primary-author identity is Alisha Karma / `codealisha99`; historical commits independently record contribution provenance. Product branding remains SchemaGuard. Required third-party credits live in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) and local font/icon license files.
