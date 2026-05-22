import os
import streamlit as st
from system.view.layout.css.base import get_css_base
from system.view.layout.css.streamlit import get_css_settings
from system.view.layout.css.containers.index import get_css_containers
from system.view.layout.css.header.index import get_css_header
from system.view.layout.css.filters.index import get_css_filters
from system.view.layout.css.metrics.index import get_css_metrics

def init_theme(theme):
    """
    Injeta o mapa de variáveis no :root e carrega os blocos de CSS estruturais
    que agora consomem essas variáveis nativamente.
    """
    st.markdown(f"""
        <style>
            {get_css_settings()}
            
            /* 1. O base cria o :root dinâmico com o JSON */
            {get_css_base(theme)} 
            
            /* 2. Os demais agora são ESTÁTICOS e limpos, usam apenas var(--bk-*) */
            {get_css_header(theme)}

            {get_css_metrics()}
            {get_css_containers()}
            {get_css_filters()}
        </style>
    """, unsafe_allow_html=True)

    load_all_components_css()

def load_all_components_css():
    print("load_all_components_css()")
    """
    Varre recursivamente a pasta de componentes, lê todos os arquivos .css
    e os injeta combinados em um único bloco <style> dentro do Streamlit.
    """
    # Caminho relativo a partir da raiz do projeto Bankai
    components_dir = os.path.join("system", "view", "components")
    combined_css = []

    # Verifica se o diretório existe para evitar erros de inicialização
    if not os.path.exists(components_dir):
        st.warning(f"Diretório de componentes não encontrado em: {components_dir}")
        return

    # os.walk varre a pasta principal e todas as subpastas automaticamente
    for root, dirs, files in os.walk(components_dir):
        for file in files:
            if file.endswith(".css"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        css_content = f.read()
                        print(file_path)
                        print(css_content)
                        # Adiciona um comentário identificando a origem do CSS (ajuda no debug pelo F12)
                        combined_css.append(f"\n/* --- Componente: {file} --- */\n{css_content}")
                except Exception as e:
                    # Registra erro caso haja falha na leitura de algum arquivo específico
                    st.error(f"Erro ao carregar o arquivo CSS {file}: {e}")

    # Se encontrou algum CSS, junta tudo e injeta na tela de uma vez só
    if combined_css:
        full_style_block = "\n".join(combined_css)
        st.markdown(f"<style>{full_style_block}</style>", unsafe_allow_html=True)


# def init_theme(theme):
#     """
#     Injeta as configurações globais do Streamlit, o :root dinâmico com o tema,
#     e carrega de forma automatizada o CSS de todos os componentes isolados.
#     """
#     # 1. Injeta as configurações globais de tela e o :root de variáveis do tema
#     st.markdown(f"""
#         <style>
#             {get_css_settings()}
#             {get_css_base(theme)} 
#         </style>
#     """, unsafe_allow_html=True)
    
#     # 2. O grande pulo do gato: o carregador automático que você criou
#     # Ele vai varrer a pasta system/view/components, compilar os arquivos .css e injetar aqui
#     load_all_components_css()