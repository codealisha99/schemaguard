# Verification — 2026-10-08

## Automated backend checks

- `pytest`: **39 passed**, **96.72% coverage**, original 70% coverage threshold retained.
- Same suite in the production Docker image (Python 3.13): **39 passed**.
- Host environment: Python 3.14.4. `pip check`: no broken requirements.
- One non-failing upstream warning: Starlette deprecates its current httpx TestClient adapter. Tests still run correctly; production does not use TestClient.
- Tests assert exact successful repairs rather than accepting fallback as repair success. The original 100-input regression now requires repaired output for every sample. Its rate allowance is isolated for that test; dedicated tests exercise production rate rejection.
- Coverage includes all schemas, strict field paths/types, single quotes and escaped apostrophes, enclosing fences, trailing commas without changing string content, combined repairs, duplicate/non-finite/truncated/unsafe inputs, fallback validity, parallel request isolation, retry/body/input/depth/node limits, per-peer/global rate limits, formatting ambiguity, and HTML-like text.

## Container checks

- `docker build -t schemaguard:demo .`: passed with Python 3.13-slim.
- Ran image with `PORT=8016`; `/health` returned 200 and Docker reported `healthy`.
- Live container API request with a trailing comma returned `status: repaired`, the expected UserProfile, and parse → commas repair → parse → validation steps.
- Production image copies only runtime requirements and `app`; virtualenv, tests, credentials, and other projects are excluded. Runs as non-root.

## Browser checks (T3 Code native preview)

- Desktop **1280 × 800** and mobile **375 × 667**: no horizontal page overflow. Mobile editors stack vertically.
- Default Markdown example: repaired output and actual fence transformation timeline.
- Valid input: valid status, original object, no repair.
- Single quotes: repaired status, quoted-token repair step.
- Product listing trailing comma: repaired, correct product object.
- Support ticket fences: repaired, correct ticket object.
- Schema mismatch: failure, no output, required field and integer type messages.
- Explicit fallback: fallback status and validated sample, original errors retained.
- Empty input: actionable prompt to paste JSON or choose an example.
- Format: server-formatted input and confirmation.
- Copy: button confirmed `Copied` in native browser.
- Reset: default input and empty result restored.
- Loading: `Validating…` and disabled schema/actions during pending request.
- Simulated network error: request-failure state and no result.
- HTML-like subject containing an `onerror` payload: rendered as literal JSON text, no image node inserted, no script execution.
- `/docs`: Swagger UI loaded and displayed four API operations.

Native preview intermittently disconnected and some screenshot calls failed. Reopening restored automation; the checks above completed using native interaction and DOM evaluation. One desktop screenshot was inspected. No alternative browser was used.

## Deployment status

**No public deployment was performed or verified.** `railway whoami` reported expired OAuth credentials (`invalid_grant`); `railway status` reported no linked project. This workspace also has no Git repository. README.md contains exact GitHub-monorepo and existing-service CLI deployment steps, including the root directory, config-file path, health check, domain generation, and public verification commands.

No unrelated project files were edited. The local server is available at http://localhost:8006 while the development process is running.

## Premium UI refinement

The playground was redesigned with locally hosted Manrope and JetBrains Mono fonts, a focused dark editor workspace, safely highlighted JSON output, synchronized input line numbers, a sticky run control, keyboard execution, clearer status styling, and request round-trip timing. The service indicator uses `/health`; no demonstration metrics or results are fabricated.

Native preview checked desktop widths 1280/1440px and mobile widths 320/375px with no horizontal overflow. All six examples, three schemas, fallback, empty input, reset, safe formatting, and clipboard copy passed. Ctrl/Cmd+Enter executes validation; mobile results scroll into view; schema inspection dismisses on Escape and outside clicks. Syntax highlighting preserved the exact JSON text including quotes, backslashes, and HTML-like content, with no inserted HTML nodes or script execution. No browser JavaScript errors were observed. Screenshots of the desktop workspace, mobile layout, and developer section were reviewed. Secondary text contrast was increased during the review, and reduced-motion preferences are respected.

The API is unchanged by this UI refinement; its 39-test suite still passes with 96.72% host coverage. Font license notices are included under `app/static/fonts/`.
