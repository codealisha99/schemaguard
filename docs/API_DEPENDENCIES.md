# API dependencies and configuration

**Core playground/API needs no external API, model provider, database, account, or API key.** Browser calls are same-origin `/health`, `/v1/schemas`, `/v1/validate`, and `/v1/format`. Examples are fixtures; responses are real, not mocked.

## Core libraries — local, not services

[FastAPI](https://fastapi.tiangolo.com/)/[Starlette](https://www.starlette.io/) route/guard requests; [Uvicorn](https://www.uvicorn.org/) serves them; [Pydantic](https://docs.pydantic.dev/latest/) validates schemas. All are required at startup, with no credentials. [psycopg binary](https://www.psycopg.org/psycopg3/docs/) must also be installed because it is imported at startup, even with the database disabled. Direct requirements are pinned; transitive dependencies are not fully locked.

## Optional runtime features

| Service / status                                | Purpose; failure impact                                                                                        | Configuration / credentials                                                                                                                          | Official docs                                                                                                                                                                                    |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PostgreSQL; recorded host Neon. Wired, optional | `/health/database` runs `SELECT 1`; unavailable/unconfigured → 503. Core validation and `/health` continue     | Server-only `DATABASE_URL`; obtain connection string from database administrator or existing [Neon console](https://console.neon.tech) Connect panel | [Connection guide](https://neon.com/docs/connect/connect-from-any-app), [PostgreSQL](https://www.postgresql.org/docs/current/)                                                                   |
| jsDelivr + Swagger UI 5/ReDoc 2. Active         | CDN JS/CSS power `/docs` and `/redoc`; unavailable → viewers fail, while playground/OpenAPI remain local       | None; no account/key                                                                                                                                 | [jsDelivr](https://www.jsdelivr.com/documentation), [Swagger](https://swagger.io/docs/open-source-tools/swagger-ui/usage/installation/), [ReDoc](https://redocly.com/docs/redoc/deployment/html) |
| ReDoc `cdn.redoc.ly` logo. Attempted, blocked   | Existing CSP blocks remote branding image and a blob search worker; reference loads, search not fully verified | None                                                                                                                                                 | [Configuration](https://redocly.com/docs/redoc/config)                                                                                                                                           |

FastAPI uses major-version CDN URLs (`swagger-ui-dist@5`, `redoc@2`), not exact release pins. Playground scripts/fonts/icons are local. Hugeicons/Aceternity/font credits are attribution, not network integrations.

## Deployment — optional locally, recorded configuration

Live account/deployment state was not checked.

| Service        | Role / failure impact                                                                   | Variables and credentials                                                                            | Official docs                                                                                          |
| -------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Vercel         | Static `dist` host; proxies API/docs/health to Railway. Outage affects hosted frontend  | No build secrets; authorized project/team account and Git integration. Upstream URL in `vercel.json` | [Git](https://vercel.com/docs/git), [environment](https://vercel.com/docs/environment-variables)       |
| Railway        | Docker FastAPI backend; outage breaks hosted API and forwarded docs                     | Injected `PORT`, optional settings below; authorized project account/Git integration                 | [Variables](https://docs.railway.com/variables), [Docker](https://docs.railway.com/guides/dockerfiles) |
| GitHub/Actions | Source and CI; outage affects cloning/checks/autodeploy triggers, not running local app | Write/settings access needs GitHub account; CI uses automatic `GITHUB_TOKEN`, no app secrets         | [Actions](https://docs.github.com/en/actions)                                                          |

CLI credentials/linkage are tooling-only (`.vercel/`, `.railway/` ignored by Git). No deploy is needed for the demo. Pushes may trigger recorded autodeploys.

## Development/install tools

| Tool                    | Use / absence impact                                                       | Credentials and docs                                                                                                             |
| ----------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Python/pip/PyPI         | Package installation; unavailable registry blocks clean installs           | Public requirements need no key; [pip](https://pip.pypa.io/en/stable/), [PyPI](https://pypi.org/)                                |
| Node/npm                | Static build/checks only; server still works without Node                  | No account or `npm install`; [Node](https://nodejs.org/en/download), [npm](https://docs.npmjs.com/)                              |
| pytest/pytest-cov/httpx | Test-only requirements; absent → tests cannot run                          | None; [pytest](https://docs.pytest.org/), [coverage](https://pytest-cov.readthedocs.io/), [httpx](https://www.python-httpx.org/) |
| Docker/Docker Hub       | Optional container build; needs daemon and public `python:3.13-slim` image | No app/private-registry secret; [Docker](https://docs.docker.com/), [base image](https://hub.docker.com/_/python)                |

## Environment

None is mandatory locally. Export process variables before startup or set them in host settings; `.env` is **not automatically loaded**. Keep connection strings server-side and out of Git/logs.

| Variable                       | Default     | Purpose                                                           |
| ------------------------------ | ----------- | ----------------------------------------------------------------- |
| `PORT`                         | `8006`      | HTTP port; Railway supplies its own                               |
| `RATE_LIMIT_PER_MINUTE`        | `60`        | Positive integer POST allowance/peer/rolling minute               |
| `RATE_LIMIT_GLOBAL_PER_MINUTE` | `180`       | Positive integer global POST allowance/rolling minute             |
| `TRUSTED_PROXY_IPS`            | `127.0.0.1` | Trusted proxy addresses/CIDRs; trust only verified infrastructure |
| `DATABASE_URL`                 | Unset       | Secret PostgreSQL URL; optional database probe only               |

Docker fixes `PYTHONDONTWRITEBYTECODE=1` / `PYTHONUNBUFFERED=1`; no user setup needed. `LLM_PROVIDER` is unused. No OpenAI/Anthropic, auth provider, analytics, payment, email-sending, or webhook integration exists. Footer links are navigation; `/docs/oauth2-redirect` is a framework helper, not login.

## Verified general cost models — 2026-10-12

| Service        | Model / official source                                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| jsDelivr       | [Free public open-source CDN](https://www.jsdelivr.com/)                                                                                                                |
| Neon           | Free allowance; paid compute CU-hours/storage GB-months: [pricing](https://neon.com/pricing)                                                                            |
| Railway        | Plan subscription/included usage plus excess resource usage: [plans](https://docs.railway.com/pricing/plans)                                                            |
| Vercel         | Free Hobby limits; paid plans/allowances and usage charges: [pricing](https://vercel.com/pricing)                                                                       |
| GitHub Actions | Standard hosted runners free for public repos; other runner/storage use may cost: [billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) |

Project plans/bills, Docker subscription terms, and other tool pricing were not verified. No paid resources were provisioned. Live database connectivity is unverified; local missing/error behavior is tested.
