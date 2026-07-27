"""Sincronização mínima entre widgets Streamlit e estado da aplicação."""

import streamlit as st


def sync_widget_value(key: str, value: object) -> None:
    """Atualiza a memória do widget apenas quando o estado externo mudou."""
    if key in st.session_state and st.session_state[key] != value:
        st.session_state[key] = value
