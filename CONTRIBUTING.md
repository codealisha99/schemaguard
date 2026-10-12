# Contributing to SchemaGuard

SchemaGuard uses FastAPI and Pydantic for deterministic JSON repair, with a vanilla HTML/CSS/JavaScript interface. Keep syntax repair conservative: do not guess values, relax schemas, execute input, or treat fallback as successful repair.

Declared project creator / primary author and maintainer: [Alisha Karma / codealisha99](https://github.com/codealisha99). Questions: [lishykarma99@gmail.com](mailto:lishykarma99@gmail.com). This describes the owner-supplied project identity; historical contributors and third-party ownership remain recorded in Git and the license notices.

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

## Commit identity

Use your own verified Git identity for contributions. Do not copy another contributor's identity or change historical commits to alter attribution. The intended maintainer identity is Alisha Karma / `codealisha99`; use a GitHub noreply address copied from that authenticated account's email settings for future maintainer commits. The public contact email above is not assumed to be a verified Git commit email. Existing local configuration remains unchanged until the correct address is verified.
