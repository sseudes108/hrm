"""Conteúdo da rota inicial do Bankai."""
from typing import Any

import streamlit as st

def render(context: Any) -> None:
    st.subheader("Início")
    st.write("Conteúdo da rota inicial. O header pertence ao shell do Bankai.")


def render_sidebar(context: Any) -> None:
    """Exemplo de conteúdo pertencente ao slot lateral desta rota."""
    st.caption("PAINEL LATERAL")
    st.write("Este bloco permanece abaixo do header durante a rolagem.")
    st.radio(
        "Visualização",
        options=["Resumo", "Detalhes"],
        key="bankai_home_sidebar_view",
    )
