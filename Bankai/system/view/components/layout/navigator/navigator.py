import streamlit as st
import system.control.managers.hash as hash_man

from dataclasses import dataclass
from typing import Optional


VALID_MODELS = {"in_header", "no_bg"}

@dataclass
class NavigatorConfig:
    app_name: str
    model: str
    nav_pages: list
    title: Optional[str] = None
    has_card: bool = True
    hover: bool = False

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            st.error(f"Navigator — model inválido: '{self.model}'. Escolha entre: {VALID_MODELS}")
            raise ValueError(f"model inválido: '{self.model}'")

        if not self.nav_pages:
            st.error("Navigator — 'nav_pages' não pode ser vazio.")
            raise ValueError("nav_pages não pode ser vazio")

def draw(nav_config: NavigatorConfig):
    if nav_config is None:
        return

    key = hash_man.get_hash_key(nav_config.app_name, f"navigator_{nav_config.model}")

    if nav_config.model == "no_bg":
        st.markdown(
            '<div class="co-navigator-no_bg"></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="co-navigator-bg"></div>',
            unsafe_allow_html=True
        )

    with st.container(key=f"co_navigator_{nav_config.model}_{key}"):
        return st.tabs(nav_config.nav_pages)