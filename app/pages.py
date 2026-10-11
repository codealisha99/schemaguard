"""Product chrome for the generated API documentation."""

from pathlib import Path

from fastapi.responses import HTMLResponse


STATIC = Path(__file__).parent / "static"


def documentation_page(page: HTMLResponse) -> HTMLResponse:
    template = (STATIC / "index.html").read_text()
    header = template[
        template.index("<header"):template.index("</header>") + len("</header>")
    ]
    footer = template[
        template.index("<footer>"):template.index("</footer>") + len("</footer>")
    ]
    header = header.replace('class="nav-docs"', 'class="nav-docs" aria-current="page"')
    styles = (
        '<link rel="stylesheet" href="/static/tokens.css">'
        '<link rel="stylesheet" href="/static/style.css">'
        '<link rel="stylesheet" href="/static/docs.css">'
    )
    html = page.body.decode().replace("<html>", '<html lang="en">')
    html = html.replace("</head>", styles + "</head>")
    html = html.replace(
        "<body>",
        '<body data-page="docs"><a class="skip-link" href="#main">'
        "Skip to API documentation</a>" + header
        + '<main id="main" tabindex="-1" class="docs-main">',
    )
    html = html.replace("</body>", "</main>" + footer + "</body>")
    return HTMLResponse(html)
