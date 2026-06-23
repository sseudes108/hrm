import streamlit as st

from apps.engines.athena.pages import espada
from system.view.components.cards import card
from system.view.components.layout import header
from system.view.components.renderers import page

PAGES = {
    1: espada,
    # 2: escudo, 
    # 3: visao, 
}

def get_page(context):
    return PAGES.get(context.current_page or 1, espada)

def draw_header(context):
    card.draw(
        card.CardConfig(
            card_id="header_wrapper_athena", context=context, 
            hover=False, model="wrapper"
        ), card.CardRenderConfig(
            content=lambda: header.draw(
                title="Athena", subtitle="Calculadora de Capacity",
                context=context, model="nav", nav_pages=[
                    "Espada", "Escudo", "Visão"
                ], logo_card=True
            )
        )
    )

def main(context):
    draw_header(context)
    page_to_render = get_page(context)
    layout_cols = st.columns([0.015, 0.98, 0.015], gap="xxsmall")
    with layout_cols[1]:
        page.render(page_to_render, context)