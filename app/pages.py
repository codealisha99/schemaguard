"""Shared product chrome, API documentation, and browser error pages."""

from pathlib import Path

from fastapi.responses import HTMLResponse


STATIC = Path(__file__).parent / "static"


def product_chrome() -> tuple[str, str]:
    template = (STATIC / "index.html").read_text()
    header = template[
        template.index("<header"):template.index("</header>") + len("</header>")
    ]
    footer = template[
        template.index("<footer>"):template.index("</footer>") + len("</footer>")
    ]
    return header, footer


def not_found_page() -> HTMLResponse:
    header, footer = product_chrome()
    template = (STATIC.parent / "error.html").read_text()
    return HTMLResponse(template.replace("{{header}}", header).replace("{{footer}}", footer), status_code=404)


def documentation_page(page: HTMLResponse, reference: bool = False) -> HTMLResponse:
    header, footer = product_chrome()
    header = header.replace('class="nav-docs"', 'class="nav-docs" aria-current="page"')
    active = 'aria-current="page"'
    docs_navigation = (
        '<section class="docs-intro" aria-label="Documentation navigation">'
        '<div><span class="kicker">Developer manual / API v2</span>'
        '<p class="docs-title">' + ("Read the contract." if reference else "Test the contract.") + '</p>'
        '<p>Three strict schemas. Conservative syntax repair. No API key required.</p></div>'
        '<nav aria-label="Documentation views">'
        f'<a href="/docs" {"" if reference else active}>Interactive docs</a>'
        f'<a href="/redoc" {active if reference else ""}>API reference</a>'
        '<a href="/openapi.json">OpenAPI JSON</a></nav></section>'
        '<noscript><p class="docs-noscript">This documentation viewer needs JavaScript. '
        'You can still <a href="/openapi.json">read the OpenAPI specification</a>.</p></noscript>'
    )
    styles = (
        '<link rel="stylesheet" href="/static/tokens.css">'
        '<link rel="stylesheet" href="/static/style.css">'
        '<link rel="stylesheet" href="/static/docs.css">'
    )
    html = page.body.decode().replace("<html>", '<html lang="en">')
    if reference:
        # Set token-backed options before Redoc's bundle initializes its HTML element.
        html = html.replace('</redoc>', '</redoc><script src="/static/docs-theme.js"></script>')
    html = html.replace("</head>", '<meta name="description" content="SchemaGuard API: strict JSON validation, syntax repairs, and explicit fallback with an inspectable trace.">' + styles + "</head>")
    html = html.replace(
        "<body>",
        '<body data-page="docs"><a class="skip-link" href="#main">'
        "Skip to API documentation</a>" + header
        + '<main id="main" tabindex="-1" class="docs-main">' + docs_navigation,
    )
    html = html.replace("</body>", "</main>" + footer + "</body>")
    return HTMLResponse(html)
