# Contributing to SchemaGuard

SchemaGuard uses FastAPI and Pydantic for deterministic JSON repair, with a vanilla HTML/CSS/JavaScript interface. Keep syntax repair conservative: do not guess values, relax schemas, execute input, or treat fallback as successful repair.

Primary maintainer: [Alisha Karma / codealisha99](https://github.com/codealisha99). Questions: [lishykarma99@gmail.com](mailto:lishykarma99@gmail.com). Historical contributors and third-party ownership remain recorded in Git and the license notices.

Follow the local setup in [README.md](README.md). Before submitting a change, run:

```bash
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
npm run build
npm run check:frontend
git diff --check
```

For interface changes, inspect `/`, `/playground`, `/docs`, `/redoc`, and browser 404 recovery at mobile, tablet, and desktop widths. Exercise all three schemas, repair and failure cases, opt-in fallback, formatting, copying, and keyboard controls. Use [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) for semantic tokens and component conventions.

Do not include submitted content, secrets, environment files, or private database URLs in logs, issues, or commits. Preserve third-party license files. No project-wide source license has been declared; third-party notices do not grant a license for the entire repository. Ask the maintainer before redistributing project code.
