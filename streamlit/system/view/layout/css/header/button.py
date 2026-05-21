"""
styles/header/button.py — Bankai 
CSS do botão de toggle de tema.
Utiliza color-mix() nativo do CSS para opacidades e injeta apenas o ícone em Base64.
"""
from system.view.components.helper import get_base64_icon

def get_button_css(theme: dict) -> str:
    # O ícone em Base64 ainda precisa ser lido via Python pois muda por tema
    icon = get_base64_icon(theme)
    
    return f"""
        [class*="st-key-toggle_theme_btn_container_"] {{
            z-index: 1001 !important;
            margin: 0 !important;      
            padding: 0 !important;     
            display: flex !important;
            align-items: center !important;
            
            /* MUDANÇA AQUI: Empurra o botão 100% para a extremidade direita da coluna */
            justify-content: flex-end !important; 
            
            height: 100% !important;
            width: 100% !important; /* Garante que o container ocupe toda a largura da coluna */
        }}

        [class*="st-key-toggle_theme_btn_container_"] button {{
            background: color-mix(in srgb, var(--bk-surface) 50%, transparent) !important;
            background-image: url('data:image/svg+xml;base64,{icon}') !important;
            background-repeat: no-repeat !important;
            background-position: center !important;

            border: 1px solid color-mix(in srgb, var(--bk-text) 30%, transparent) !important;
            border-radius: var(--bk-radius-full) !important;

            width: 40px;
            height: 40px;
            
            /* CORREÇÃO DE VAZAMENTO: Remove margens nativas do Streamlit que empurram o botão para baixo */
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }}

        [class*="st-key-toggle_theme_btn_container_"]:hover button {{
            border-color: color-mix(in srgb, var(--bk-border-focus) 40%, transparent) !important;
            transform: translateY(var(--bk-hover-y)) !important;
            box-shadow: var(--bk-shadow-md), var(--bk-glow-primary) !important;
        }}

        [class*="st-key-toggle_theme_btn_container_"]:active button {{
            transform: translateY(0) !important;
            box-shadow: var(--bk-shadow-sm) !important;
        }}

        /* Alinhamento global para os botões do cabeçalho */
        button {{
            transition: all 0.3s ease !important;
        }}
    """