# SchemaGuard product audit — 2026-10-11

## Discovery and baseline

FastAPI / Python backend, strict Pydantic models, vanilla HTML/CSS/JavaScript frontend, Node static build, npm scripts, pip requirements. No login, user accounts, persistence workflow, migrations, or admin dashboard. Optional Neon connectivity is a read-only health probe. Vercel serves the static build and forwards API/docs to Railway. No new external integration is required.

Initial working tree: clean on `main`. Remote: `codealisha99/schemaguard`. Historical authors include `theabhijitam`; their commits and local Git identity will remain unchanged. No AGENTS.md found in this repository or its nearby parent directories.

Baseline executed: `npm run build`, `npm run check:frontend`, `.venv/bin/python -m pytest -q` (41 passed, 96.15% coverage), `.venv/bin/python -m pip check` (no broken requirements). Existing warning: deprecated Starlette/httpx test adapter.

## Route inventory before implementation

| Route                           | Purpose and components                                          | Findings / required improvement                                                     | States                                                                            | Initial status                          |
| ------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------- |
| `/`                             | Product overview, live editor, process explanation, API example | Refine visual identity and content hierarchy; clarify repair limits and attribution | Editor idle/loading/valid/repaired/failure/fallback; network and clipboard errors | Inspected                               |
| `/playground`                   | Focused editor, schema tabs, contract, trace                    | Stronger workflow hierarchy, accessible input errors, selected example accuracy     | Same as inline playground                                                         | Inspected                               |
| `/docs`                         | Swagger interactive API documentation                           | Consistent product chrome, reference navigation, clearer introduction               | Collapsed/expanded operations, request/response, errors                           | Inspected                               |
| `/redoc`                        | ReDoc API reference                                             | Consistent product chrome, interactive-docs link, improved reading surface          | Search, schema/operation navigation, mobile menu                                  | Inspected                               |
| Missing browser page (HTTP 404) | Default JSON response                                           | Branded recovery page; preserve API JSON errors and 404 status                      | Return home/open playground                                                       | Inspected                               |
| `/docs/oauth2-redirect`         | Framework callback compatibility helper                         | Preserve behavior; no product OAuth flow exists                                     | Framework-controlled callback                                                     | Inspected; exempt from product redesign |

API routes `/health`, `/health/database`, `/v1/schemas`, `/v1/validate`, `/v1/format`, and `/openapi.json` are not product pages. No fictional routes will be added.

Final implementation and verification results will be recorded here after checks run.

## Product and design outcome

Verified name: **SchemaGuard**. Purpose: conservatively repair JSON syntax and validate against UserProfile, ProductListing, or SupportTicket. Target users: developers testing structured model output and integrating the validation API. No model calls, keys, signup, or submitted-content persistence is required. Visual direction: technical field manual, with warm paper, forest-green actions, dark code panels, numbered stages, and visible repair evidence.

Creator identity supplied by the project owner: Alisha Karma. Intended primary maintainer: `codealisha99`. Footer and repository documentation use maintenance attribution, without making sole-authorship claims. Complete palette HEX values, font/spacing scales, components, and theme decision are recorded in [DESIGN_SYSTEM.md](../DESIGN_SYSTEM.md); [brand.md](../brand.md) records the direction.

## Final route checklist

All product routes progressed through inspection, design implementation, functionality testing, responsive checking, and local verification.

| Route                                           | Purpose                             | Design updated                                                        | Functionality tested                                                            | Responsive check                             | Status                                   |
| ----------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------- | ---------------------------------------- |
| `/`                                             | Overview and live inline validation | Yes: hierarchy, copy, palette, repair note, workspace, footer         | 21 schema/example/fallback cases plus editor/error/keyboard/clipboard checks    | 320, 375, 390, 430, 768, 1024, 1440, 1720 px | Verified locally                         |
| `/playground`                                   | Dedicated validation workspace      | Yes: workflow introduction, contracts, numbered editors, input errors | Same 21 cases and controls; actual mobile/tablet submission                     | Same eight widths                            | Verified locally                         |
| `/docs`                                         | Swagger API console                 | Yes: shared chrome, manual introduction, documentation views          | Live “Try it out” /health returned 200; operation expansion and view navigation | Same eight widths                            | Verified locally                         |
| `/redoc`                                        | Searchable API reference            | Yes: shared chrome, navigation, token-backed native theme             | Specification loaded, search and operation content checked                      | Same eight widths                            | Verified locally                         |
| Unmatched browser path (tested `/missing-page`) | HTTP 404 recovery                   | Yes: branded recovery with real links and HTTP 404                    | Home and playground recovery; API JSON errors preserved                         | Same eight widths                            | Verified locally                         |
| `/docs/oauth2-redirect`                         | Framework callback helper           | Preserved; not a product authentication page                          | Endpoint returns 200 in backend regression tests                                | Not applicable to callback helper            | Endpoint verified; no OAuth flow claimed |

There are no authenticated page blockers. APIs are excluded from the page count. No account, dashboard, legal, billing, or customer pages were invented.

## Ownership, content, and metadata

- Replaced obsolete package scope `@ai-infra` with `@codealisha99`; added repository and maintainer metadata without declaring a sole author.
- Changed “Built by” to “Maintained by,” added the supplied contact email and API-reference link, and replaced the ambiguous personal-looking playground sample with “Sample user.” Examples remain clearly demonstration data.
- Removed a machine-specific clone path from README. Current verification links point here, and prior deployment statements are explicitly historical rather than newly verified.
- Added `CONTRIBUTING.md`, `.github/CODEOWNERS`, and a check-only GitHub Actions workflow. Official checkout/setup-python/setup-node guidance was inspected for current action versions. Local equivalents ran; the remote workflow has not run.
- Added descriptive social metadata; retained product-specific identity and favicon. No unsupported canonical URL, social-preview image claim, or installable-app claim was added.
- Read-only `gh repo view codealisha99/schemaguard --json name,description,repositoryTopics,defaultBranchRef` succeeded: default branch `main`; description empty; topics unset. Remote metadata was not changed. Suggested description: “Deterministic JSON repair and strict schema validation with an inspectable trace.” Suggested topics: `json`, `json-schema`, `fastapi`, `pydantic`, `structured-output`.
- Existing Aceternity, Hugeicons/MIT, Manrope/OFL, and JetBrains Mono/OFL notices remain unchanged. No root project license was present; one was not invented. Historical audit/deployment records remain intact and labeled as prior evidence.
- Git history, author identities, Git configuration, remote URL, branch, and repository permissions remain unchanged. Initial tree was clean; final changes are local and uncommitted. No push or deployment occurred.

## Code and integration audit

Important changes: `app/static/tokens.css`, `style.css`, `index.html`, `app.js`, `docs.css`, new `docs-theme.js`, `app/pages.py`, `app/main.py`, new `app/error.html`, frontend build/check scripts, test suite, package metadata, and maintenance/brand/audit documentation.

Fixed stale example selection after formatting, UTF-16 character counting that disagreed with Python's input limit, missing invalid-input announcements, insufficient generic focus contrast on dark editor controls, and ReDoc response contrast on the revised background. Removed the unused hidden `schema-fields` element, its CSS, and its update code; removed duplicated mobile brand/hero rules and obsolete desktop-break markup styles. The custom favicon and header mark now match in color and radius.

A stylesheet-writing mistake introduced during implementation was caught by browser overflow checks, corrected before final verification, and is absent from the final diff. No tests were disabled. No runtime dependencies were changed. Playwright/axe and Prettier were temporary audit tools outside the project dependency graph.

Schemas, validation/format response contracts, repair algorithms, request/resource limits, optional database probe, trusted proxy configuration, and existing Railway/Vercel routing remain intact. Input-derived output continues to use text nodes rather than HTML; browser payload testing confirmed no injected image or script execution. New HTML 404 handling is conditional on browser Accept headers and leaves API/static errors machine-readable. Tests cover that distinction.

The existing documentation still relies on CDN-hosted Swagger/ReDoc bundles and its broader documentation-only CSP. The playground remains local-script/font-only. No new external integration, analytics, credentials, or storage was introduced; no secret values were included in reports. A conservative tracked-file credential-pattern scan matched only a deliberate fake-credential backend test fixture; no credential/environment files were tracked.

## Executed verification

| Check / command                       | Actual result                                                                                                                                                        |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `npm run build`                       | Passed; landing, playground, and 404 outputs generated                                                                                                               |
| `npm run check:frontend`              | Passed; syntax, outputs, assets, duplicate IDs, ARIA references, 26 AA text pairs (minimum 5.01:1), focus/control pairs                                              |
| `.venv/bin/python -m pytest -q`       | 43 passed; 96.37% coverage against unchanged 70% gate                                                                                                                |
| `.venv/bin/python -m pip check`       | No broken requirements                                                                                                                                               |
| `npx --yes prettier@3.6.2 --check …`  | Passed for HTML/CSS/JS/build/check/package/workflow formatting                                                                                                       |
| `git diff --check`                    | Passed; no whitespace errors                                                                                                                                         |
| `node /tmp/schemaguard-qa/verify.cjs` | Passed 46 recorded workflow groups; 42 schema/example/fallback cases, both locations' control checks, Swagger execution, and ReDoc search; no page JavaScript errors |
| Responsive browser layout             | Five page states × eight viewport widths; no page overflow or clipped header/button/tab labels                                                                       |
| Accessibility                         | axe WCAG 2 A/AA, 2.1 AA, and 2.2 AA at 390 and 1440 px: zero reported violations on all five page states after fixes                                                 |
| Clipboard                             | Real browser copy action and clipboard readback matched rendered JSON on both playground locations                                                                   |
| Network/loading                       | Intercepted aborted requests preserved input and restored controls; delayed real requests showed busy state and disabled conflicting controls                        |
| Additional mobile/keyboard pass       | Actual repair/reset/expand flows at 320, 390, and 768 px; skip-link focus, Unicode count, reduced-motion mode, and 404 recovery passed                               |
| Unsafe markup                         | HTML-like input stayed literal JSON; no injected nodes or code execution                                                                                             |
| External footer links                 | Personal site, GitHub profile, GitHub repository, and X returned HTTP 200; email delivery not tested                                                                 |
| `docker info`                         | Failed: Docker daemon socket unavailable; no container build performed                                                                                               |

The T3 native preview status/open tools explicitly reported no connected automation host. Browser verification used local headless Chromium with Playwright 1.64.0 and axe-core 4.13.0 after that confirmed limitation. Screenshots at 390, 768, and 1440 px were captured; representative landing, playground, and documentation screenshots were visually inspected. Browser evidence is in `/tmp/schemaguard-qa/` for this workspace.

## Known limits and remaining work

- Pre-existing Starlette/httpx TestClient deprecation warning remains; all backend tests pass.
- Automated accessibility reports have incomplete contrast judgments for decorative playground symbols/keyboard hints and overlapping ReDoc samples/schema decoration, plus upstream Swagger generic clipboard-wrapper ARIA judgments. These are incomplete checks, not reported violations or a complete accessibility certification.
- Physical devices and a full screen-reader audit were not tested. There is one deliberate light theme; no theme switching workflow exists.
- Docker build/runtime checks are blocked by the absent daemon. No production deploy or hosted rewrite/404 revalidation was performed.
- Current Vercel, Railway, and Neon account settings and live database connectivity were not inspected. The optional database check is covered with local unconfigured/error tests rather than live credentials.
- GitHub description/topics are empty. Applying remote metadata, selecting a project license, publishing, committing, or pushing remains for the owner to decide; none was performed.
- There is no configured type checker or formal lint task for this Python/vanilla-JavaScript repository. Syntax, formatting, frontend integrity, backend tests, and browser checks were used. No claim of a vulnerability scan is made.

No functional regressions remained in the checks that ran. This report describes local review readiness, not a verified production release.

## Subsequent publication authorization

After the local audit, the owner requested committing and pushing this redesign to `origin/main`. The local verification results above remain unchanged; hosted deployment behavior has not been revalidated. The authenticated GitHub account is `codealisha99`, but its token cannot read verified email addresses. Existing Git commit identity was retained; no email address or historical author was changed.
