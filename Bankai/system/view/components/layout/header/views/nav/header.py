import streamlit as st

from system.view.components.layout.navigator import navigator
from system.view.components.layout.header.views import brand, helper

def draw_title(header_config, context):
    brand.draw(context, header_config)

def get_component(header_config, context):
    # Adicionamos vertical_alignment="bottom" para garantir que o Streamlit 
    # jogue tudo das 3 colunas para a linha de base
    header_cols = st.columns([2, 5, 0.5], gap='xxsmall', vertical_alignment="bottom")

    with header_cols[0]:
        draw_title(header_config, context)

    with header_cols[1]:
        navigator.draw(
            context=context,
            model="header_nav",
            items=header_config.nav_items,
            active_route=header_config.active_route,
            on_navigate=header_config.on_navigate,
        )

    with header_cols[2]:
        helper.draw_tools(context)
