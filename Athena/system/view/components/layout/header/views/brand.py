"""Marca compartilhada pelos modelos de header."""

from html import escape
from typing import Any

import streamlit as st

from system.view.components.cards import card


def draw(context: Any, header_config: Any) -> None:
    """Renderiza logo, título e subtítulo sem depender do modelo de navegação."""
    title = escape(header_config.title.upper())
    subtitle = escape((header_config.subtitle or "").upper())
    logo_size = int(context.theme["layout"]["logo_size"])
    logo_path = context.theme.get("layout", {}).get("logo_png")

    if logo_path:
        ratios = [0.2, 0.8] if logo_size < 80 else [0.3, 0.6]
        logo_column, title_column = st.columns(
            ratios, gap="small", vertical_alignment="bottom"
        )
        with logo_column:
            card.draw(
                card.CardConfig(
                    card_id="header_logo",
                    context=context,
                    show_card=header_config.logo_card,
                    hover=False,
                    model="wrapper",
                    padding="none",
                ),
                card.CardRenderConfig(
                    content=lambda: st.image(logo_path, width=logo_size)
                ),
            )
    else:
        title_column = st.container()

    with title_column:
        subtitle_html = (
            f'<p class="header-brand-subtitle">{subtitle}</p>' if subtitle else ""
        )
        card.draw(
            card.CardConfig(
                card_id="header_title_text",
                context=context,
                show_card=False,
                hover=False,
                model="wrapper",
                padding="none",
            ),
            card.CardRenderConfig(
                content=lambda: st.html(
                    '<div class="header-brand"><div class="header-brand-text">'
                    f'<p class="header-brand-title">{title}</p>{subtitle_html}'
                    "</div></div>"
                )
            ),
        )
