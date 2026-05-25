import streamlit as st

from system.control.contexts import AppContext
import system.control.managers.layout as layout_man

def get_context(app_name: str) -> AppContext:
    """Garante a existência e retorna a instância da classe de contexto na sessão"""
    session_key = f"filter_context_{app_name}"
    theme_setting = layout_man.get_theme(app_name)
    if session_key not in st.session_state:
        st.session_state[session_key] = AppContext(app_name, theme_setting)

    return st.session_state[session_key]