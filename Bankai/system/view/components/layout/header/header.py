import streamlit as st
from system.view.components.cards import card
import system.control.managers.hash as hash_man

from system.view.components.layout.header import HeaderConfig
from system.view.components.layout.header import slim

def draw(header_config: HeaderConfig):
    if header_config is None:
        return

    key = f"{header_config.app_name}_{hash_man.get_hash(header_config.app_name)}"

    card_config = card.CardConfig(
        model="header",
        key=key,
    )

    if header_config.has_card:
        card.draw_card(
            card_config,
            render_content=lambda: get_component(header_config)
        )
    else:
        get_component(header_config)

def get_component(header_config: HeaderConfig):
    if header_config is None:
        return

    if header_config.model == "slim":
        slim.get_component(header_config)
    elif header_config.model == "nav":
        pass  # nav_header.get_nav_component(header_config)
    elif header_config.model == "ticker":
        pass  # ticker_header.get_component(header_config)
    else:
        st.error(f"Componente não implementado para model='{header_config.model}'")