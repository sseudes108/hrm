import streamlit as st
import system.control.managers.hash as hash_man
from system.view.components.cards import draw_card

## EXEMPLO
# navi_config = {
#     "app_name": "lakshmi",
#     "model": "in_header",
#     "has_card": True,
#     "hover": True,
#     "title": "lak_navigator",
#     "nav_pages":[
#         "Adi",
#         "Dhana",
#         "Vidya",
#         "Veera",
#         "Gaja",
#         "Santana",
#         "Dhanya",
#         "Vijaya"
#     ]
# }

def draw(nav_config: dict):
    key = hash_man.get_hash_key(nav_config["app_name"], f"navigator_{nav_config["model"]}")

    # Card vazio — só visual, sem conteúdo
    if nav_config["model"] == "no_bg":
        st.markdown(
            f'<div class="co-navigator-no_bg"></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="co-navigator-bg"></div>',
            unsafe_allow_html=True
        )

    # Tabs fora do card, sobem via CSS
    with st.container(key=f"co_navigator_{nav_config["model"]}_{key}"):
        return st.tabs(nav_config["nav_pages"])