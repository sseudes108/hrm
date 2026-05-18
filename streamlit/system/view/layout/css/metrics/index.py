from system.view.layout.css.metrics.header import get_css_header
from system.view.layout.css.metrics.body import get_css_body

def get_css_metrics(theme):
    colors = theme["colors"]
    typography = theme['typography']
    borders = theme["borders"]
    return f"""
        /* ─────────────────────────────────────────────────────────────────
            BLOCO 1 — Header - Icone, Titulo e "?"
        ───────────────────────────────────────────────────────────────── */
        {get_css_header(theme)}

        /* ─────────────────────────────────────────────────────────────────
            BLOCO 1 — Body
        ───────────────────────────────────────────────────────────────── */
        {get_css_body(theme)}
    """