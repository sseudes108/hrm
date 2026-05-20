# import streamlit as st
# import uuid

# def draw_select_filter(title, options, theme, label_width="5"):
#     key = f"f_select_{hash(title) if title else uuid.uuid4().hex[:6]}"

#     unique_style = f"""
#         <style>
#             [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {{
#                 width:{label_width}rem !important;
#                 min-width: 5rem !important;
#             }}

#             /* Hover no campo */
#             [class*="st-key-container_filter_bar_{key}"]:hover [data-baseweb="select"] > div {{
#                 border-color: {theme['colors']['primary']} !important;
#             }}
#         </style>
#     """
    
#     st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

#     with st.container(key=f"container_filter_bar_{key}"):
#         selected = st.selectbox(
#             label=title,
#             options=options,
#             key=key
#         )

#     return selected

import hashlib
import streamlit as st

def draw_select_filter(title, options, theme, label_width="5", allow_all=True):
    """
    Componente de filtro customizado com suporte a 'Selecionar Todos'.
    """
    # 1. Correção do Hash estável (Python puro muda o hash() a cada restart do app)
    title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()[:6] if title else "default"
    key = f"f_select_{title_hash}"

    # 2. Injeta a opção "Todos" no início da lista, se permitido
    modified_options = list(options)
    if allow_all and "Todos" not in modified_options:
        modified_options.insert(0, "Todos")

    unique_style = f"""
        <style>
            [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {{
                width:{label_width}rem !important;
                min-width: 5rem !important;
            }}

            /* Hover no campo */
            [class*="st-key-container_filter_bar_{key}"]:hover [data-baseweb="select"] > div {{
                border-color: {theme['colors']['primary']} !important;
            }}
        </style>
    """
    
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    with st.container(key=f"container_filter_bar_{key}"):
        selected = st.selectbox(
            label=title,
            options=modified_options,
            key=key
        )

    return selected