import streamlit as st

def create_tabs(lista_abas, cor_destaque):
    """
    Cria abas com fundo transparente e uma faixa colorida na base da aba ativa.
    """
    st.markdown(f"""
        <style>
            /* Remove o fundo da barra e define transparência */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 20px;
                background-color: transparent;
                padding: 0px;
                border-bottom: 1px solid #E0E0E0; /* Linha sutil de separação */
            }}

            /* Estilo das abas individuais */
            .stTabs [data-baseweb="tab"] {{
                height: 45px;
                background-color: transparent;
                border: none;
                color: #2C3E50;
                font-weight: 500;
                transition: all 0.3s;
            }}

            /* Aba Selecionada: Fundo transparente + faixa na base */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {{
                background-color: transparent !important;
                color: {cor_destaque} !important;
                border-bottom: 3px solid {cor_destaque} !important;
            }}

            /* Remove a linha decorativa padrão do Streamlit que sobra */
            .stTabs [data-baseweb="tab-highlight"] {{
                display: none;
            }}
        </style>
    """, unsafe_allow_html=True)

    return st.tabs(lista_abas)