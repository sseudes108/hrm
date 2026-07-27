import base64
from pathlib import Path
import streamlit as st

from system.core.managers.view import css


STYLE_DIRECTORY = Path(__file__).resolve().parents[3] / "view" / "styles"

def init_theme(theme):
    """
    Injeta o mapa de variáveis no :root e carrega os blocos de CSS estruturais.
    Faz apenas UMA injeção para evitar a criação de múltiplos containers vazios.
    """
    stylesheet = _get_system_styles()
    
    full_style = f"""
        <style>
            {css.render_theme_tokens(theme)}
            {stylesheet}
        </style>
    """
    
    st.html(full_style)

def _get_system_styles() -> str:
    """Carrega somente a árvore oficial de estilos, invalidando por alteração."""
    files = tuple(sorted(STYLE_DIRECTORY.rglob("*.css")))
    signature = tuple((str(path), path.stat().st_mtime_ns) for path in files)
    return _read_styles(signature)


@st.cache_data(show_spinner=False)
def _read_styles(signature: tuple[tuple[str, int], ...]) -> str:
    blocks = []
    for file_path, _ in signature:
        path = Path(file_path)
        blocks.append(f"\n/* --- Origem: {path.relative_to(STYLE_DIRECTORY)} --- */\n{path.read_text(encoding='utf-8')}")
    return "\n".join(blocks)

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
                    --ui-assets-background-image: url('{img_css_url}') !important;
                }}
            </style>
        """
        
        st.html(custom_bg_style)
