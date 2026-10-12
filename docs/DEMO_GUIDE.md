# SchemaGuard demo guide

## Setup

Python 3.13 is used by Docker/CI; this pass used Python 3.14. Use a modern browser. No external account or secret is needed.

```bash
git clone https://github.com/codealisha99/schemaguard.git
cd schemaguard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m app.run
```

Open http://localhost:8006/playground; keep the server running. In another terminal: `curl --fail http://localhost:8006/health` should return `{"status":"ok","service":"schemaguard"}`. Opening the HTML file directly will not work.

Reload: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8006 --reload --no-access-log`. Alternate port: `PORT=8007 python -m app.run` (update every URL). Stop with Ctrl+C. Windows PowerShell activation: `.venv\Scripts\Activate.ps1`; environment assignment uses `$env:PORT="8007"`.

## Main workflow

Select **User profile**, leave **Use sample fallback** off, and paste this deliberately malformed input:

```json
{ "name": "Sample user", "age": 30, "skills": ["Python"] }
```

| Step | Action                                                           | Expected result                                                                            |
| ---- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 1    | **Repair & validate**                                            | **Repaired input**, unchanged values, one comma repair; inspect the timeline               |
| 2    | Remove the comma; run                                            | **Valid input**, zero repairs                                                              |
| 3    | Change `age` to `"30"`; run                                      | **Validation failed**, integer issue, no valid output                                      |
| 4    | Enable fallback, inspect it; run                                 | **Fallback used**, explicit sample replaces input; original issue remains                  |
| 5    | Disable fallback; restore valid input; **Format JSON**, then run | Formatting confirmation, then **Valid input**; formatting alone does not validate          |
| 6    | **Copy JSON**, then **Reset playground**                         | Copy confirmation if permitted; reset restores the default fenced example and empty result |

Optional: select Product listing/Support ticket, choose **Trailing commas**, and run. Fields/contracts change together. Cmd/Ctrl+Enter executes validation.

## API demo

```bash
curl --fail-with-body http://localhost:8006/v1/validate \
  -H 'Content-Type: application/json' \
  --data '{"raw_output":"{\"name\":\"Sample user\",\"age\":30,\"skills\":[\"Python\"],}","schema_name":"UserProfile","max_retries":3}'
```

Expect `status: repaired`, one repair, and `output: {"name":"Sample user","age":30,"skills":["Python"]}`, plus actual trace/issues. HTTP 200 alone does not mean schema success; inspect `status`.

## 60-second pitch

“SchemaGuard helps developers handle structured output that looks like JSON but fails when their application tries to use it. Paste an output, choose one of three contracts, and see what happened. It can remove Markdown fences, convert single-quoted strings, and clean up trailing commas. Then it checks required fields and types and shows the exact repair trace. If a field is missing or wrong, it reports the issue instead of inventing a value. An optional fallback is clearly marked as a replacement, not a repair. The browser and API use the same pipeline. Everything runs locally without model calls, API keys, or a database, making the behavior repeatable and easy to demonstrate.”

Technical explanation: vanilla JS calls FastAPI; bounded parsing and deterministic repairs feed strict Pydantic models. Responses carry validated output, field issues, and request-local steps. Nothing is persisted.

## Troubleshooting

| Problem                                      | Recovery                                                                            |
| -------------------------------------------- | ----------------------------------------------------------------------------------- |
| Port busy / missing module                   | Use alternate port; activate venv and install requirements                          |
| Empty input / wrong schema / format rejected | Paste the sample, choose matching schema; repair malformed syntax before formatting |
| 429 / request failed                         | Wait 60 seconds for rate limits; check `/health`, terminal, and browser origin      |
| Clipboard unavailable                        | Select output and copy manually                                                     |
| Database probe 503                           | Expected without optional database; omit from core demo                             |
| Docs blank / ReDoc CSP warnings              | Check CDN/network; use `/openapi.json` or curl instead                              |

## Verification

2026-10-12: fresh isolated install/startup, **43 tests / 96.37% coverage**, `pip check`, static build/frontend checks, and **21 API cases** across all schemas passed. Native browser confirmed Markdown/trailing-comma repair and integer field-error output. Preview failures interrupted further controls; a complete browser sequence is not claimed. Hosted deployments/live database were not checked; Docker daemon is unavailable; existing TestClient warning remains. Run [README checks](../README.md#test-and-build) before presenting; no deployment is needed.
