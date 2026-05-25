import streamlit as st

# EXEMPLO
# card_config = {
#     "model": "header",
#     "has_title": False,
#     "header":{
#         "title": "title",
#         "subtitle": "subtitle",
#     },
#     "hover": False,
#     "key": "hash_man.get_hash_key(app_name, title)"
# }

def draw_card(card_config: dict, render_content=None, *args, **kwargs):
    if render_content is None:
        st.error("Render Content is None")
        return

    key   = card_config["key"]
    model = card_config["model"]
    hover_y = "--bk-hover-y" if card_config["hover"] else "0"

    # Injeta o estilo FORA do container (escopo global da página)
    unique_style = f"""
        <style>
            [class*="st-key-co_card_{model}_{key}"]:hover {{
                transform: translateY(var({hover_y})) !important;
            }}
        </style>
    """
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    # Container só com o conteúdo
    with st.container(key=f"co_card_{model}_{key}"):
        response = render_content(*args, **kwargs)

    return response