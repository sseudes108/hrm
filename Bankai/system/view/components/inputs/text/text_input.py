import streamlit as st
from system.view.components.cards import card

def draw(
    context, 
    label, input_id,
    default="",
    in_card=False, hover=False
):
    if in_card:
        return card.draw(
            card.CardConfig(
                context=context, card_id=f"text_input_card_{context.app_name}_{label}_{input_id}", hover=hover
            ), card.CardRenderConfig(
                content=lambda: _draw_component(
                    context.app_name, input_id, label, default
                )
            )
        )
    else:
        return _draw_component(
            context.app_name, input_id, label, default
        )

def _draw_component(
    app_name, input_id, label, default
):
    with st.container(key=f"co_input_text_{app_name}_{input_id}"):
        txt_input = st.text_input(
            label=label, value=default, key=f"{input_id}"
        )

    return txt_input