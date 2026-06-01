import streamlit as st

from system.control.contexts import AppContext
import system.control.managers.layout as layout_man

@st.cache_data
def get_mode(app_name: str) -> str:
    d = "dark"
    l = "light"

    lights  = [
        "bankai","lakshmi"
    ]

    if app_name in lights:
        return l
    else:
        return d

@st.cache_resource
def get_context(app_name: str) -> AppContext:
    """Garante a existência e retorna a instância da classe de contexto na sessão"""
    session_key = f"app_context_{app_name}"
    mode = get_mode(app_name)
    theme_setting = layout_man.get_theme(app_name, mode)
    if session_key not in st.session_state:
        st.session_state[session_key] = AppContext(app_name, theme_setting, mode)

    return st.session_state[session_key]