"""
styles/header/index.py — Bankai
Unificador do CSS do cabeçalho superior.
Consome as subfunções de título, botão e ticker de forma estática.
"""
from system.view.layout.css.header.title import get_title_css
from system.view.layout.css.header.tiker import get_tiker_css
from system.view.layout.css.header.button import get_button_css

def get_css_header(theme) -> str:
    return f"""
        /* ─────────────────────────────────────────────────────────────────
           BLOCO 1 — HEADER PRINCIPAL (barra superior + título)
        ───────────────────────────────────────────────────────────────── */
        {get_title_css()}

        /* ─────────────────────────────────────────────────────────────────
           BLOCO 2 — BOTÃO DE TOGGLE DE TEMA
        ───────────────────────────────────────────────────────────────── */
        {get_button_css(theme)}

        /* ─────────────────────────────────────────────────────────────────
           BLOCO 3 — TICKER (faixa de notícias animada)
        ───────────────────────────────────────────────────────────────── */
        {get_tiker_css()}
    """