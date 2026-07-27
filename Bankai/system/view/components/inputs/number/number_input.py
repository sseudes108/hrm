import streamlit as st
from system.view.components.cards import card
from system.view.components._keys import scoped_key

def draw(
    context, label, 
    input_id, default=108, 
    step=1, min_v=1, max_v=1080, 
    in_card=False, hover=False, card_variant="surface", card_padding="normal",
):
    return card.draw(
        card.CardConfig(
            context=context,
            card_id=f"number_input_card_{input_id}",
            model="filter",
            hover=hover if in_card else False,
            variant=card_variant,
            show_card=in_card,
            padding=card_padding,
        ),
        card.CardRenderConfig(
            content=lambda: _draw_component(context, input_id, label, step, min_v, max_v, default)
        ),
    )


def _draw_component(
    context, input_id, label, step, min_v, max_v, default
):
    with st.container(key=scoped_key(context, "co_input_number", input_id)):
        n_input = st.number_input(
            label=label, step=step,
            min_value=min_v, max_value=max_v,
            value=default, key=scoped_key(context, "input_number", input_id)
        )

    # 3. Fallback blindado e elegante em uma única linha:
    # Se por qualquer motivo o Streamlit devolver None, ele engole e devolve o default.
    return n_input if n_input is not None else default
