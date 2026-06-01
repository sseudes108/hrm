import streamlit as st
from system.control.contexts import AppContext
from system.view.components.cards import card, CardConfig

from system.view.components.layout.header import HeaderConfig
from system.view.components.layout.header.views import slim, nav

def _get_component(header_config: HeaderConfig, context:AppContext):
    if header_config.model == "slim":
        slim.get_component(header_config, context)

    elif header_config.model == "nav":
        nav.get_component(header_config, context)

    elif header_config.model == "ticker":
        pass  # ticker_header.get_component(header_config)

    else:
        st.error(f"Componente não implementado para model='{header_config.model}'")

def draw(
        title:str, subtitle:str, context:AppContext,
        show_card:bool = True, hover:bool = False, 
        model:str = "slim", nav_pages=[]
    ):

    card.draw(
        CardConfig(
            context.app_name, card_id=f"{context.app_name}_main_header",
            hover=hover, show_card=show_card, model="header"
        ),  render_content=lambda: 
            _get_component(
                HeaderConfig(
                    app_name=context.app_name, model=model, 
                    title=title, subtitle=subtitle, hover=hover, nav_pages=nav_pages
                ),
        context)
    )