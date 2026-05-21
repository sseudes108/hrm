import streamlit as st

def draw_empty_element(size_px):
    """Cria um bloco vazio na tela com a altura exata em pixels."""
    st.markdown(f'<div style="height: {size_px}px; width: 100%;"></div>', unsafe_allow_html=True)


# def draw_empty_element():
#     """Cria o recuo perfeito baseado na altura definida no tema atual."""
#     st.markdown(
#         '<div style="height: var(--bk-header-h); width: 100%;"></div>', 
#         unsafe_allow_html=True
#     )