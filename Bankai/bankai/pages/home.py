"""Conteúdo da rota inicial do Bankai."""
from typing import Any

import streamlit as st
from bankai.pages.components.layout import filter_bar
from system.view.components import button


def render(context: Any) -> None:
    """Monta livremente sidebar e conteúdo da página inicial."""
    sidebar_column, content_column = st.columns([1, 3], gap="small")

    with sidebar_column:
        filter_bar.draw(context)

    with content_column:
        with st.container(
            height=800,
            border=False,
            key=f"co_page_home_content_{context.app_name}",
        ):
            button.draw(
                context=context,
                label="Salvar",
                button_id="save_report",
                icon=":material/save:",
                width="stretch",
            )
