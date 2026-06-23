import streamlit as st
from system.view.components.cards import card

def draw(
    context, label, 
    input_id, default=108, 
    step=1, min_v=1, max_v=1080, 
    in_card=False, hover=False
):
    if in_card:
        return card.draw(
            card.CardConfig(
                context=context, card_id=f"number_input_card_{context.app_name}_{label}_{input_id}", hover=hover
            ), card.CardRenderConfig(
                content=lambda: _draw_component(
                    context.app_name, input_id, label, step, min_v, max_v, default
                )
            )
        )
    else:
        return _draw_component(
            context.app_name, input_id, label, step, min_v, max_v, default
        )


def _draw_component(
    app_name, input_id, label, step, min_v, max_v, default
):
    with st.container(key=f"co_input_number_{app_name}_{input_id}"):
        n_input = st.number_input(
            label=label, step=step,
            min_value=min_v, max_value=max_v,
            value=default, key=input_id
        )

    # 3. Fallback blindado e elegante em uma única linha:
    # Se por qualquer motivo o Streamlit devolver None, ele engole e devolve o default.
    return n_input if n_input is not None else default