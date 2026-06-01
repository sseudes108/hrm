import os
import json
import streamlit as st
from pathlib import Path
import base64

from system.view.layout import css

def init_theme(theme):
    """
    Injeta o mapa de variáveis no :root e carrega os blocos de CSS estruturais
    que agora consomem essas variáveis nativamente.
    """
    st.markdown(f"""
        <style>
            {css.hide_streamlit_features()}
            
            /* 1. O base cria o :root dinâmico com o JSON */
            {css.create_base_css(theme)} 
            
        </style>
    """, unsafe_allow_html=True)

    load_all_components_css()

def load_all_components_css():
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
                        # Adiciona um comentário identificando a origem do CSS (ajuda no debug pelo F12)
                        combined_css.append(f"\n/* --- Componente: {file} --- */\n{css_content}")
                except Exception as e:
                    # Registra erro caso haja falha na leitura de algum arquivo específico
                    st.error(f"Erro ao carregar o arquivo CSS {file}: {e}")

    # Se encontrou algum CSS, junta tudo e injeta na tela de uma vez só
    if combined_css:
        full_style_block = "\n".join(combined_css)
        st.markdown(f"<style>{full_style_block}</style>", unsafe_allow_html=True)

def _deep_merge(base: dict, override: dict) -> dict:
    """
    Merge recursivo — override sobrescreve folhas do base,
    mas preserva chaves do base que não existem no override.
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result

@st.cache_data 
def get_theme(app_name: str, mode: str = "dark") -> dict:
    current_path = Path(__file__).resolve()

    # Encontra a raiz do projeto (Bankai)
    root_path = None
    for parent in current_path.parents:
        if parent.name.lower() == "bankai":
            root_path = parent
            break
            
    if not root_path:
        root_path = current_path.parent.parent.parent

    def _load_search(target_app: str, file_name: str) -> dict | None:
        """
        Usa busca recursiva (rglob) para encontrar o arquivo de tema, 
        independentemente de estar em books, dashboards, engines ou sandbox.
        """
        # Procura em qualquer lugar por: <target_app>/themes/<file_name>
        pattern = f"**/{target_app}/themes/{file_name}"
        
        # O rglob vasculha a partir do root_path
        files = list(root_path.rglob(pattern))
        
        if files:
            with open(files[0], "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    # Tenta carregar base e mode do app específico, com fallback para bankai
    base  = _load_search(app_name, "base.json")  or _load_search("bankai", "base.json")
    theme = _load_search(app_name, f"{mode}.json") or _load_search("bankai", f"{mode}.json")

    if not base:
        raise FileNotFoundError(f"base.json não encontrado para '{app_name}' nem no fallback.")
    if not theme:
        raise FileNotFoundError(f"'{mode}.json' não encontrado para '{app_name}' nem no fallback.")

    return _deep_merge(base, theme)

@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg(img_path:str):
    img_base64 = get_base64_of_bin_file(img_path)

    page_bg_img = f'''
    <style>
        /* O .stApp é a classe principal que engloba toda a tela do Streamlit */
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Caso queira escurecer um pouco o fundo para os cards brilharem mais (Opcional) */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(11, 13, 20, 0.4); /* Ajuste a opacidade se precisar */
            z-index: -1;
        }}
    </style>
    '''

    # 4. Injetar o CSS no app
    st.markdown(page_bg_img, unsafe_allow_html=True)