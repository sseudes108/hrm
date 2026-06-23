import os, base64
from pathlib import Path
import streamlit as st

from system.core.managers.view import css

def init_theme(theme):
    """
    Injeta o mapa de variáveis no :root e carrega os blocos de CSS estruturais.
    Faz apenas UMA injeção para evitar a criação de múltiplos containers vazios.
    """
    components_css = _get_all_components_css()
    
    full_style = f"""
        <style>
            {css.reset_st_base()}
            {css.set_bankai_base(theme)}
            {components_css}
        </style>
    """
    
    st.html(full_style)

def _get_all_components_css() -> str:
    """
    Varre recursivamente pastas predefinidas, lê todos os arquivos .css.
    Usa cache para ler o disco apenas na primeira vez que o app abrir.
    """
    
    # 1. Defina suas pastas hardcoded diretamente nesta lista
    directories = [
        os.path.join("system", "view", "components"),
        os.path.join("apps"),
    ]

    combined_css = []

    # 2. Itera sobre a lista de diretórios
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Aviso: Diretório de CSS não encontrado em: {directory}")
            continue  # Pula para a próxima pasta em vez de parar a execução

        # 3. Varre os arquivos da pasta atual
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".css"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            css_content = f.read()
                            # Comentário com o caminho para facilitar o debug depois
                            combined_css.append(f"\n/* --- Origem: {file_path} --- */\n{css_content}")
                    except Exception as e:
                        print(f"Erro ao carregar o arquivo CSS {file_path}: {e}")
                        
    return "\n".join(combined_css)

def _get_image_base64(img_path: str) -> str:
    """Lê um arquivo de imagem local e converte para base64."""
    path = Path(img_path)
    if not path.is_file():
        print(f"Aviso: Imagem de fundo não encontrada no caminho: {img_path}")
        return ""
    
    with open(path, "rb") as f:
        data = f.read()
        b64_encoded = base64.b64encode(data).decode("utf-8")
        
    # Identifica o tipo do arquivo para montar o formato correto
    ext = path.suffix.lower().replace(".", "")
    mime_type = "jpeg" if ext in ["jpg", "jpeg"] else ext
    
    return f"data:image/{mime_type};base64,{b64_encoded}"


def set_page_background(context):
    """
    Injeta o CSS específico da página lendo a imagem do tema atual.
    Suporta tanto URLs web (http) quanto arquivos locais (.png, .jpg).
    """
    img_source = context.theme.get("assets", {}).get("background_image", "")

    if not img_source:
        return # Sai silenciosamente se não houver imagem configurada

    # Checa se é um link da web ou um arquivo local
    if img_source.startswith("http://") or img_source.startswith("https://"):
        img_css_url = img_source
    else:
        # Converte o arquivo local para base64
        img_css_url = _get_image_base64(img_source)

    # Só injeta se a URL (ou o base64) for válido
    if img_css_url:
        custom_bg_style = f"""
            <style>
                :root {{
                    --bk-bg-image: url('{img_css_url}') !important;
                }}
            </style>
        """
        
        st.html(custom_bg_style)