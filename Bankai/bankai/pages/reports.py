"""Conteúdo demonstrativo da rota de relatórios."""

from typing import Any

import streamlit as st


def render(context: Any) -> None:
    st.subheader("Relatórios")
    st.write("Esta rota reutiliza o header sticky do shell, mas possui conteúdo próprio.")
