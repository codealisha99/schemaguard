# SchemaGuard ownership and branding audit

Date: 2026-10-12. Scope: local authorship metadata, contributor provenance, repository settings, engineering documentation, and product logo consistency. This audit follows the previously authorized redesign commit `5cafb6f`; it does not rewrite that commit or its authorship.

## Canonical project identity

Owner-supplied creator, declared primary author, and intended maintainer: **Alisha Karma / codealisha99**. Profile: https://github.com/codealisha99. Website: https://alishakarma.com. Public contact: lishykarma99@gmail.com.

This is project-role metadata, not a claim that one person wrote every line. Historical Git authors and third-party implementations remain separately attributed. The product name remains **SchemaGuard**.

## Repository state and files inspected

The initial working tree was clean on `main`, at `5cafb6f1d63f3db69bb2cc53a20ec0796a9bf25b`. The existing remote remains `https://github.com/codealisha99/schemaguard.git`.

Inspected README, CONTRIBUTING, package metadata, CODEOWNERS, the Product checks workflow, design/brand documentation, PRD, historical audit/verification reports, source attribution and application chrome, logo/favicon, third-party notices and font/icon licenses, Python requirements, Docker/.dockerignore, Railway/Vercel configuration, environment-variable documentation, build/check scripts, tests, Git history/configuration, and accessible GitHub metadata. No pyproject.toml, Cargo.toml, pom.xml, root LICENSE, dedicated AUTHORS file, or release changelog was present.

## Safe changes made

| File                      | Change and reason                                                                                                                                                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `package.json`            | Added the declared primary author with the supplied name, website, and public contact; completed the existing single maintainer contact. No fictional contributor list or sole-authorship claim added.                       |
| `README.md`               | Clarified owner-supplied creator/primary-author/maintainer roles and historical provenance; corrected the old `06-schemaguard` Docker working-directory wording; added the actual product logo and architecture/audit links. |
| `CONTRIBUTING.md`         | Aligned project-role wording; documented using each contributor's own verified identity and distinguished the public support address from a verified Git commit email.                                                       |
| `Dockerfile`              | Added OCI product title, description, source repository, and declared primary-author labels. Runtime commands, worker settings, image base, and non-root user are unchanged.                                                 |
| `app/static/icon.svg`     | Refined the original JSON-brace/check motif with curved braces, balanced strokes, and a forest-green square. No unrelated logo or third-party mark was introduced.                                                           |
| `app/static/index.html`   | Replaced duplicated inline logo geometry with the canonical SVG image; favicon uses the same asset; added separate author metadata while preserving SchemaGuard product metadata and footer maintenance attribution.         |
| `brand.md`                | Documented creator/primary-author roles and logo geometry, minimum sizes, clear space, wordmark, and accessible usage.                                                                                                       |
| `DESIGN_SYSTEM.md`        | Recorded the single-source header/favicon logo convention. Existing palette and typography remain intact.                                                                                                                    |
| `docs/REDESIGN_AUDIT.md`  | Clarified that the original uncommitted state was historical and recorded the subsequently authorized `5cafb6f` commit/push. Earlier local verification is not presented as new deployment verification.                     |
| `docs/ARCHITECTURE.md`    | Added an actual code map, request/repair flow, static-build relationship, integration boundaries, limits, and dependency/check structure.                                                                                    |
| `docs/OWNERSHIP_AUDIT.md` | Recorded findings, changes, verification, settings, and unresolved items without exposing private account data.                                                                                                              |

No runtime or test dependencies changed. No new functionality, contributors, metrics, testimonials, or copyright claims were fabricated. Existing non-obvious parser/security comments remain intact; no broad code reorganization was justified by this metadata pass.

## Contributor and third-party attribution

`git shortlog -sn HEAD` and GitHub's contributors endpoint both identified `theabhijitam` (9 commits) and `codealisha99` (7 commits). These are recorded attribution facts, not estimates of effort or ownership. Neither contributor was removed, renamed, squashed, or reattributed.

Aceternity/Manu Arora adaptation credits, Hugeicons MIT attribution, Manrope OFL notices, and JetBrains Mono OFL notices are preserved. Required license files and original icon paths remain untouched. Service names such as FastAPI, Swagger, ReDoc, Railway, Vercel, and Neon identify intentional dependencies/integrations rather than unrelated template ownership.

No project-wide source LICENSE was present. A license was not invented or copied from a dependency; the owner must choose one if a project license is desired.

## Git identity status

The authenticated GitHub login is `codealisha99`, but `gh api user/emails` is unavailable with the current token's scopes. A verified GitHub noreply address could not be retrieved from authenticated email settings. No address was guessed, and the public contact email was not assumed to be verified for commits.

Existing local Git name/email configuration remains unchanged. Its configured name is `theabhijitam`, which differs from the intended maintainer identity. Configuring future maintainer commits as Alisha Karma remains pending verification of the correct account email. Historical commit metadata, timestamps, branch, remotes, and repository permissions are unchanged. This audit creates local changes only; no new commit or push was performed.

## GitHub settings inspected

| Setting                       | Observed result                                                                                            |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Owner / authenticated account | `codealisha99`                                                                                             |
| Visibility                    | Public                                                                                                     |
| Default branch                | `main`                                                                                                     |
| Description / topics          | Empty / unset                                                                                              |
| Main branch protection        | API reports branch not protected                                                                           |
| Repository rulesets           | Empty list                                                                                                 |
| Collaborators                 | `codealisha99` with admin role                                                                             |
| Contributors                  | Existing two GitHub contributor identities listed above                                                    |
| Latest Product checks CI      | Passed for `5cafb6f`; [run evidence](https://github.com/codealisha99/schemaguard/actions/runs/38141145154) |

No remote setting was changed. Proposed description: “Deterministic JSON repair and strict schema validation with an inspectable trace.” Proposed topics: `json`, `json-schema`, `fastapi`, `pydantic`, `structured-output`. Any branch protection or permission change requires separate explicit authorization; contributor history should remain untouched.

## Verification actually executed

- Baseline and final `.venv/bin/python -m pytest -q`: **43 passed**, **96.37% coverage**, unchanged 70% gate.
- `.venv/bin/python -m pip check`: no broken requirements.
- `npm run build`: passed; landing, dedicated playground, 404, and static assets generated.
- `npm run check:frontend`: passed; JavaScript syntax, outputs/assets, duplicate IDs, ARIA references, 26 AA text-contrast pairs (minimum 5.01:1), and focus/control contrast checks.
- Prettier 3.6.2 checked changed HTML, manifest, and Markdown. The SVG used the explicit HTML parser because Prettier does not infer an SVG parser automatically.
- `git diff --check`: passed.
- Native T3 browser inspected the refined logo and canonical footer on `/`, `/playground`, `/docs`, `/redoc`, and browser 404 recovery. Header and favicon resolve to the same product-mark asset.
- Native browser checks on `/` and `/playground` at 320, 768, and 1440 px: logo loaded, canonical home-link label, expected maintenance attribution, and no horizontal page overflow. `/docs`, `/redoc`, and the 404 page passed the same logo/overflow checks at 320 px. Further documentation viewport changes were interrupted by preview disconnections/timeouts and are not claimed as verified in this pass.
- The mobile landing screenshot was visually inspected. An attempted playground browser submission was interrupted by preview loss; no successful browser workflow result is claimed from that attempt. The backend regression suite and direct local repair request verify the repair behavior independently.
- SVG XML/safe-element inspection, manifest author/maintainer consistency, local documentation links, a direct HTTP trailing-comma repair, and a conservative tracked-file credential-pattern scan were run. The only credential-pattern match was a deliberate fake-credential test fixture; no private account information or secret values are recorded here.
- Docker CLI is installed, but the daemon is unavailable. The metadata-only Dockerfile change was inspected; no container build is claimed.

## Remaining inconsistencies and limits

1. Future-commit Git identity still needs the actual verified GitHub noreply email. No history rewrite is appropriate.
2. GitHub description/topics remain empty; proposed values are above. Main has no protection/rulesets. Remote corrections were not applied.
3. A root project license is absent; selecting one is an owner decision.
4. Pre-existing Starlette/httpx TestClient deprecation warning remains. There is no configured TypeScript checker or formal lint task; existing syntax, formatting, build, and test tools were used.
5. Docker build, hosted deployment verification, full screen-reader testing, and uninterrupted documentation checks at all sizes were not performed. Browser automation was intermittent. No vulnerability-scan claim is made.

All initial user changes were preserved: the tree was clean before this audit, and only the listed task files were changed. No commit, push, deployment, domain/DNS change, repository transfer, visibility/access change, or history manipulation was performed during this audit.

## Subsequent commit and push authorization

After this local audit, the owner explicitly requested committing and pushing the reviewed ownership, documentation, and logo changes to `origin/main`. The unchanged Git identity is retained because a verified account email is still unavailable. The verification results above describe the local audit; this authorization does not establish hosted deployment verification.
