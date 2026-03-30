import streamlit as st
from Control.Managers import image_manager as ImageMan
from Control.Managers import style_manager as StyleMan

def init_layout(cliente):
    cliente_id = cliente
    if cliente == "Itau":
        cliente = "Itaú"

    st.set_page_config(
        page_title=cliente,
        page_icon="📣",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    StyleMan.carregar_css(cliente_id)
    remove_sidebar()

def remove_sidebar():
    st.markdown(
        """
        <style>
            /* Remove o botão de abrir/fechar a barra lateral */
            [data-testid="stSidebarNav"] {display: none;}
            
            /* Remove a área da barra lateral propriamente dita */
            section[data-testid="stSidebar"] {
                display: none;
            }

            /* Ajusta a margem do conteúdo principal para ocupar o espaço vazio */
            .main .block-container {
                margin-left: auto;
                margin-right: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def draw_logo():
    logo_b64 = ImageMan.image_to_base64("source/imagens/untitled.PNG")
    st.markdown(
        f'<img src="{logo_b64}" width="100" style="border: 2px solid black;">', 
        unsafe_allow_html=True
    )