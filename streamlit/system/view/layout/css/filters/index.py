"""
styles/filters/index.py — Bankai 
Unificador do CSS dos filtros e componentes de seleção do dashboard.
"""
from system.view.layout.css.filters.select import get_css_select

def get_css_filters() -> str:
    return f"""
        /* ─────────────────────────────────────────────────────────────────
            BLOCO 1 — SELECT
        ───────────────────────────────────────────────────────────────── */
        {get_css_select()}
    """