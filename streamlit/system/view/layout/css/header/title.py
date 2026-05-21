"""
styles/header/title.py — Bankai
CSS do título do cabeçalho principal.
Consome de forma estática as variáveis definidas no :root.
"""

def get_title_css() -> str:
    return """
        [class*="st-key-container_header_"] .custom-header {
            margin-top: 0.4em !important; /* Corrigido o posicionamento do !important */
        }

        [class*="st-key-container_header_"] .header-title {
            margin: 0 !important;      
            padding: 0 !important;     
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            /* Consumo das variáveis globais do :root */
            color: var(--bk-text) !important;
            font-size: var(--bk-title) !important;
            font-family: var(--bk-font) !important;
            font-weight: var(--bk-w-bold) !important;

            line-height: 1 !important;
        }
    """