# SchemaGuard

Turn messy LLM output into validated JSON. A public playground and API served together by FastAPI, with vanilla HTML/CSS/JavaScript and three strict Pydantic schemas. No database, API key, LLM, or paid model call is required.

The playground includes editable input, six examples per schema, readable output, validation issues, an actual repair timeline, an opt-in sample fallback, copy, safe formatting, and reset. Submitted content stays in request memory; application logs do not contain it. External infrastructure may have its own logging policy.

## Run locally

Python 3.13 is used by Docker; Python 3.12–3.14 work locally.

```bash
cd /Users/abhijitam/Developer/Archive/ai-projects/06-schemaguard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m app.run
```

Open http://localhost:8006. Interactive API docs: http://localhost:8006/docs.

For development with automatic reload:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8006 --reload --no-access-log
```

Run tests with `pytest`. The existing 70% coverage gate is retained. Runtime dependencies live in `requirements.txt`; test dependencies live in `requirements-dev.txt`.

## Docker

Run from **06-schemaguard**, so other projects are outside the build context:

```bash
docker build -t schemaguard .
docker run --rm -p 8006:8006 -e PORT=8006 schemaguard
```

The image runs as a non-root user, copies only the application and runtime requirements, and checks `/health` using the actual `PORT`. There is one Uvicorn worker. No volume is needed.

## API

- `GET /health`: service readiness.
- `GET /v1/schemas`: schema names and JSON Schema definitions.
- `POST /v1/validate`: parse, conservatively repair, and validate.
- `POST /v1/format`: safely format valid JSON without requiring a business schema. Duplicate keys and non-finite numbers are rejected.

```bash
curl -X POST http://localhost:8006/v1/validate \
  -H 'Content-Type: application/json' \
  -d '{"raw_output":"{\"name\":\"Alisha\",\"age\":30,\"skills\":[\"Python\"],}","schema_name":"UserProfile","max_retries":3}'
```

`schema_name` defaults to `UserProfile`. Alternatives are `ProductListing` and `SupportTicket`. Inspect definitions at `/v1/schemas` or in the playground. Optional `fallback` is an explicit object, validated against the same schema. The UI always exposes the sample fallback before use.

The result includes:

- `status`: `valid`, `repaired`, `fallback`, or `failure`.
- `output`: schema-valid object or `null`.
- `validation_errors`: field path, message, expected schema/type, and `input` or `fallback` source. Submitted field values are excluded.
- `repair_steps`: request-local stage, outcome, message, and zero-based repair attempt. Attempt zero is the original input; every changed candidate is parsed and validated.
- Compatibility aliases: `success`, `data`, `retries`, `fallback`, `repair_log`, and `error`. As before, `success` is false for fallback results, even when the fallback itself is valid. `retries` now accurately counts transformations actually applied.

Schema failures return HTTP 200 with a `failure` result. Invalid request fields/limits return 422, unknown schema returns 404, oversized bodies return 413, slow body reads return 408, and rate limits return 429 with `Retry-After: 60`. Request error responses omit submitted values.

Compatibility intentionally tightened: no coercion of strings into numbers, no extra fields, no guessed closing brackets, no extraction from surrounding prose, and no unvalidated fallback output. UserProfile retains its `name`, `age`, and `skills` fields, with reasonable length/age constraints. Shared repair logs have been removed.

## Repair boundaries and resource limits

The parser first tries strict JSON. If parsing fails, it tries, in order: remove a complete enclosing Markdown fence; convert single-quoted string tokens; remove trailing commas outside strings. It never executes submitted expressions. `ast.literal_eval` is used only to decode a bounded, isolated single-quoted string token, never an object or expression. Unsupported escapes are rejected.

Repairs are deterministic syntax transformations. They do not fill missing fields, coerce business types, guess delimiters, or guarantee recovery. A successful parse with schema errors stops syntax repair immediately. Duplicate keys, non-finite numbers, truncated input, and arbitrary prose remain failures.

Server-enforced limits:

- Input: 16,384 characters; entire request body: 64 KiB, including fallback.
- Nesting: 32 levels; parsed JSON: 4,096 values (including containers).
- Repair budget: integer `max_retries` from 0 to 3, default 3.
- Request body: 10-second timeout per incoming chunk; Uvicorn: 64 concurrent connections/tasks.
- All POST endpoints: rolling 60-second rate windows, 60 requests per peer IP and 180 globally by default. At most 2,048 active peer buckets; new peers are rejected if full. GET requests and health checks remain available.

Rate counters contain only peer addresses and timestamps and expire in memory. No submitted content is stored. Limits reset on restart and are per process/replica: run one worker and one Railway replica for this demo. This is not a distributed abuse-prevention system.

The playground uses `textContent` for input-derived output, errors, and traces, plus a restrictive Content Security Policy. API docs permit Swagger's CDN scripts and initialization; the playground loads no remote scripts/fonts.

## Environment variables

No required user-provided variables or secrets.

| Variable | Default | Purpose |
| --- | --- | --- |
| `PORT` | `8006` | HTTP port; Railway injects this automatically. |
| `RATE_LIMIT_PER_MINUTE` | `60` | Requests per peer IP per rolling minute. Use a positive integer. |
| `RATE_LIMIT_GLOBAL_PER_MINUTE` | `180` | Requests per instance per rolling minute. Use a positive integer. |
| `TRUSTED_PROXY_IPS` | `127.0.0.1` | Uvicorn's trusted proxy addresses/CIDRs. Only verified proxies should be trusted. |

Without a trusted proxy configuration, visitors behind the same proxy share its per-IP allowance. Arbitrary forwarded headers are ignored. Configure `TRUSTED_PROXY_IPS` only with verified infrastructure addresses; do not set `*` on an app that can receive direct untrusted traffic. The global limit applies regardless of forwarded headers. `LLM_PROVIDER` is unused and unnecessary.

## Railway deployment from the monorepo

1. Publish the monorepo to a GitHub repository if it is not already hosted. This workspace has no `.git` repository; do not initialize or push unrelated projects just to deploy this service.
2. In Railway, create a project/service from that repository and select the intended branch.
3. In service **Settings → Source**, set **Root Directory** to `/06-schemaguard`.
4. Set **Railway Config File** to `/06-schemaguard/railway.json`. This path is relative to the repository root, not the service root. The config selects the Dockerfile and `/health` health check. Keep the default Docker start command; no override is needed.
5. Keep one replica. No database, secrets, or model keys are required. Railway supplies `PORT`; optional variables are listed above. Initially the safe proxy default may pool visitors into a shared IP allowance; the separate global cap still applies.
6. Deploy. Confirm the deployment passes `/health`, then choose **Settings → Networking → Generate Domain**. Use its HTTPS URL.
7. Verify the public deployment, replacing the example hostname:

```bash
curl --fail https://YOUR-DOMAIN.up.railway.app/health
curl --fail https://YOUR-DOMAIN.up.railway.app/v1/schemas
curl --fail https://YOUR-DOMAIN.up.railway.app/v1/validate \
  -H 'Content-Type: application/json' \
  -d '{"raw_output":"{\"name\":\"Alisha\",\"age\":30,\"skills\":[\"Python\"],}"}'
```

The last response must show `status: "repaired"`, the validated object, and a `commas` repair step. Open the HTTPS page on desktop/mobile and run schema mismatch both with and without fallback before sharing it.

For an already-created Railway service, `railway login`, `railway link`, then `railway up` from this directory can upload just this application. Link the intended new service explicitly; do not reuse another project's service. Configure `/health` and generate a domain as above.

Official reference: [monorepo roots and config paths](https://docs.railway.com/deployments/monorepo), [Dockerfile builds](https://docs.railway.com/builds/dockerfiles), [PORT and health checks](https://docs.railway.com/deployments/healthchecks).

No public deployment has been verified in this workspace: the saved Railway login is expired and no project is linked. Local verification results are recorded in `VERIFICATION.md`.
