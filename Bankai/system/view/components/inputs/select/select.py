import streamlit as st
from system.view.components.cards import card
from system.view.components._keys import scoped_key

def draw(
    context, input_id,
    label, options,
    in_card=False, hover=False, card_variant="surface", card_padding="normal",
):
    return card.draw(
        card.CardConfig(
            context=context,
            card_id=f"select_input_card_{input_id}",
            model="filter",
            hover=hover if in_card else False,
            variant=card_variant,
            show_card=in_card,
            padding=card_padding,
        ),
        card.CardRenderConfig(content=lambda: _draw_component(context, input_id, label, options)),
    )

def _draw_component(
    context, input_id, label, options
):
    with st.container(key=scoped_key(context, "co_input_select", input_id)):
        selecteds = st.selectbox(
            label=label, options=options, key=scoped_key(context, "input_select", input_id)
        )

    return selecteds
