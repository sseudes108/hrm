"""Emissão do bloco CSS de tema compartilhado."""

from collections.abc import Mapping
from typing import Any

from .theme_tokens import compile_css_variables


def render_theme_tokens(theme: Mapping[str, Any]) -> str:
    """Compila fontes opcionais e tokens JSON em um único bloco ``:root``."""
    font_url = theme["typography"].get("font_url", "")
    import_font = f"@import url('{font_url}');" if font_url else ""

    return f"""
        {import_font}
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        :root {{
            {compile_css_variables(theme)}
        }}
    """
