import streamlit as st
from system.view.components.cards import card

def draw(
    context, input_id,
    label, options,
    in_card=False, hover=False
):
    if in_card:
        return card.draw(
            card.CardConfig(
                context=context, card_id=f"multiselect_input_card_{context.app_name}_{label}_{input_id}", hover=hover
            ), card.CardRenderConfig(
                content=lambda: _draw_component(
                    context.app_name, input_id, label, options
                )
            )
        )
    else:
        return _draw_component(
            context.app_name, input_id, label, options
        )

def _draw_component(
    app_name, input_id, label, options
):
    with st.container(key=f"co_input_select_multi_{app_name}_{input_id}"):
        selecteds = st.multiselect(
            label=label, options=options, key=input_id
        )

    return selecteds