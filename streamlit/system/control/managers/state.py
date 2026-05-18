import streamlit as st
from system.control.config import set_theme

def init_session_state(overrides: dict = None):
    defaults = {
        "app": "bankai",
        "themes":[
            "bankai_dark",
            "bankai_light"
        ]
    }

    if overrides:
        # Extrai o primeiro tema da lista antes do merge
        if "themes" in overrides:
            overrides["theme_name"] = overrides["themes"][0]
        defaults.update(overrides)

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    set_theme(st.session_state.theme_name)