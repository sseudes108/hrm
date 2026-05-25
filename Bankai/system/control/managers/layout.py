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

def get_theme(app_name: str, mode: str = "dark") -> dict:
    """
    Busca o arquivo JSON do tema estruturado dentro do diretório do app específico.
    Caminho real: ROOT / apps / <categoria> / {app_name} / themes / {mode}.json
    """
    # 1. Encontra o diretório atual onde este script está rodando
    current_path = Path(__file__).resolve()
    
    # 2. Sobe na árvore de diretórios até encontrar a raiz real 'Bankai'
    # Isso evita ficar adivinhando quantos ".parent" usar
    root_path = None
    for parent in current_path.parents:
        if parent.name.lower() == "bankai":
            root_path = parent
            break
            
    # Se não achar a pasta 'Bankai' pelo nome, usa o fallback clássico de subir 3 níveis
    if not root_path:
        root_path = current_path.parent.parent.parent

    # 3. Agora sim, miramos na pasta 'apps' que está na raiz do projeto
    apps_root = root_path / "apps"

    # 4. Busca usando curinga para a categoria (ex: dashboards, engines, etc.)
    # O '*' substitui 'dashboards' ou qualquer outra pasta que venha antes do app
    theme_pattern = f"*/{app_name}/themes/{mode}.json"
    theme_files = list(apps_root.glob(theme_pattern))
    
    # 5. Se encontrou o arquivo real do app, carrega e retorna
    if theme_files:
        path = theme_files[0]
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    # 6. Se não encontrou (ex: o app específico não tem pasta de temas), 
    # busca o tema padrão na pasta 'bankai' independente de onde ela esteja
    fallback_files = list(apps_root.glob(f"*/bankai/themes/{mode}.json"))
    if fallback_files:
        with open(fallback_files[0], "r", encoding="utf-8") as f:
            return json.load(f)
            
    raise FileNotFoundError(
        f"Tema '{mode}.json' para o módulo '{app_name}' (e nem o fallback da Bankai) "
        f"foi encontrado dentro de '{apps_root}'."
    )

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg(img_path:str):
    img_base64 = get_base64_of_bin_file(img_path)

    # 3. Montar o CSS (Note que as chaves do Streamlit/stApp estão duplicadas {{}} para não bugar o f-string)
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