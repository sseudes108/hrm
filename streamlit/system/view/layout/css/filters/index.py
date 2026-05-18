from system.view.layout.css.filters.select import get_css_select


def get_css_filters(theme):
    colors = theme["colors"]
    typography = theme['typography']
    borders = theme["borders"]
    return f"""
        /* ─────────────────────────────────────────────────────────────────
            BLOCO 1 — SELECT
        ───────────────────────────────────────────────────────────────── */
        {get_css_select(colors, typography, borders)}
    """