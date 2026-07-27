import streamlit as st
from system.view.components.cards import card
from system.view.components._keys import scoped_key

def draw(
    context, 
    label, input_id,
    default="",
    in_card=False, hover=False, card_variant="surface", card_padding="normal",
):
    return card.draw(
        card.CardConfig(
            context=context,
            card_id=f"text_input_card_{input_id}",
            model="filter",
            hover=hover if in_card else False,
            variant=card_variant,
            show_card=in_card,
            padding=card_padding,
        ),
        card.CardRenderConfig(content=lambda: _draw_component(context, input_id, label, default)),
    )

def _draw_component(
    context, input_id, label, default
):
    with st.container(key=scoped_key(context, "co_input_text", input_id)):
        txt_input = st.text_input(
            label=label, value=default, key=scoped_key(context, "input_text", input_id)
        )

    return txt_input
