"""Conteúdo demonstrativo da rota de relatórios."""

from typing import Any
import streamlit as st
from bankai.pages.components.layout import filter_bar


def render(context: Any) -> None:
    """Posiciona filtros e conteúdo sem slots impostos pelo shell."""
    filter_bar.draw(context)
    with st.container(
        height=800,
        border=False,
        key=f"co_page_reports_content_{context.app_name}",
    ):
        st.subheader("Relatórios")
        st.write("Conteúdo próprio da rota de relatórios.")