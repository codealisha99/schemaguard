# SchemaGuard

<img src="app/static/icon.svg" alt="SchemaGuard logo" width="48" height="48" />

Repair common JSON syntax errors in LLM-style output, validate three strict schemas, and inspect every repair. FastAPI + vanilla HTML/CSS/JavaScript. No model calls, API keys, signup, or database are required for the playground.

## Quick start

Python 3.13 is used by Docker/CI; local verification used Python 3.14. Node.js 24/npm are needed only for static build checks.

```bash
git clone https://github.com/codealisha99/schemaguard.git
cd schemaguard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m app.run
```

Open http://localhost:8006/playground. Overview: `/`; interactive API docs: `/docs`; reference: `/redoc`. No environment setup is required. Optional settings and credentials are in [API dependencies](docs/API_DEPENDENCIES.md). The app does not automatically load `.env` files.

## Test and build

From the repository root, with the virtual environment activated:

```bash
python -m pip check
python -m pytest -q
npm run build
npm run check:frontend
git diff --check
```

No `npm install` is needed: build scripts use Node built-ins. Runtime-only installs can use `requirements.txt` instead of `requirements-dev.txt`.

## Guides

- [Project guide](docs/PROJECT_GUIDE.md): features, architecture, API contracts, status, and limits.
- [Demo guide](docs/DEMO_GUIDE.md): setup, sample workflow, pitch, and troubleshooting.
- [API dependencies](docs/API_DEPENDENCIES.md): actual services, configuration, credentials, and billing sources.

Declared creator/primary author and maintainer: [Alisha Karma / codealisha99](https://github.com/codealisha99) · [website](https://alishakarma.com) · [contact](mailto:lishykarma99@gmail.com). Historical contributions remain attributed. See [CONTRIBUTING.md](CONTRIBUTING.md) and [third-party notices](THIRD_PARTY_NOTICES.md).
