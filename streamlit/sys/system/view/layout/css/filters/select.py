# from system.control.config import hex_to_rgba
# def get_css_select(colors, typography, borders):
#     return f"""
#         /* 1. O CONTAINER PRINCIPAL */
#         [class*="st-key-container_filter_bar_"] {{            
#             position: relative !important;
#             left: 0 !important;
#             padding: 0em !important;
#             cursor: pointer;
#         }}

#         /* 2. A LABEL (Efeito Floating) */
#         /* Miramos no p para a cor e no widgetLabel para o fundo que corta a borda */
#         [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {{
#             position: absolute !important;
#             top: -0.6rem !important; /* Ajuste fino para sentar na borda */
#             left: 1.2rem !important;
#             z-index: 10 !important;
#             background-color: {colors['background']} !important; 
#             padding: 0 8px !important;
#             width: auto !important;
#             min-width: 10px !important;
#             display: flex !important;
#             align-items: center !important;
#             justify-content: center !important;
#         }}

#         [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] p {{           
#             color: {colors['text_muted']} !important;
#             font-size: 0.85rem !important;
#             font-weight: {typography['weight_bold']} !important;
#             margin: 0 !important;
#         }}

#         /* 3. A BORDA DO CAMPO (Selectbox) */
#         [class*="st-key-container_filter_bar_"] [data-baseweb="select"] > div {{
#             border: 1px solid {colors['border']} !important;
#             background-color: transparent !important;
#             border-radius: {borders['radius_md']} !important;
#             transition: all 0.3s ease;
#         }}
        
#         /* Texto do valor SELECIONADO (dentro do campo) */
#         [class*="st-key-container_filter_bar_"] [data-baseweb="select"] div {{
#             color: {colors['text']} !important;
#         }}

#         [data-testid="stSelectboxVirtualDropdown"] {{
#             border: {colors['border']} !important;
#             padding: 4px !important;
#         }}
#         /* 1. REMOVE A COR E BORDA INTERNA (A caixa escura/laranja que aparece no hover/selected) */
#         [data-testid="stSelectboxVirtualDropdown"] li div[class*="e1d7a4qp0"] {{
#             background-color: transparent !important;
#             border: none !important;
#         }}

#         /* 2. CONSOLIDAÇÃO DO ITEM DA LISTA (LI) */
#         [data-testid="stSelectboxVirtualDropdown"] li {{
#             background-color: transparent !important;
#             transition: all 0.2s ease-in-out !important;
#             border-radius: 12px !important;
#             margin: 4px !important;
#             padding: 4px !important;
#             border: none !important; /* Remove bordas internas */
#         }}

#         /* Hover no item - APENAS UMA CAMADA */
#         [data-testid="stSelectboxVirtualDropdown"] li:hover {{
#             background-color: {hex_to_rgba(colors['primary'], 0.1)} !important;
#         }}

#         /* Selecionado - APENAS UMA CAMADA */
#         [data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] {{
#             background-color: {hex_to_rgba(colors['primary'], 0.2)} !important;
#             border: none !important;
#         }}

#         /* 6. SCROLLBAR */
#         [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar {{
#             width: 4px !important;
#         }}
        
#         [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar-thumb {{
#             background: {colors['border']} !important;
#             border-radius: 10px !important;
#         }}
#     """



"""
styles/filters/select.py — Bankai 
CSS customizado para Selectbox com efeito de Floating Label e dropdown limpo.
Totalmente estático e acoplado ao Design System global.
"""

def get_css_select() -> str:
    return """
        /* 1. O CONTAINER PRINCIPAL */
        [class*="st-key-container_filter_bar_"] {            
            position: relative !important;
            left: 0 !important;
            padding: 0em !important;
            cursor: pointer;
        }

        /* 2. A LABEL (Efeito Floating) */
        [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {
            position: absolute !important;
            top: -0.6rem !important; /* Sentar exatamente no topo da borda */
            left: 1.2rem !important;
            z-index: 10 !important;
            
            /* Herda dinamicamente o fundo do app ativo (Dark ou Light) */
            background-color: var(--bk-bg) !important; 
            padding: 0 8px !important;
            width: auto !important;
            min-width: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] p {           
            color: var(--bk-text-muted) !important;
            font-family: var(--bk-font) !important;
            font-size: 0.85rem !important;
            font-weight: var(--bk-w-bold) !important;
            margin: 0 !important;
        }

        /* 3. A BORDA DO CAMPO (Selectbox) */
        [class*="st-key-container_filter_bar_"] [data-baseweb="select"] > div {
            border: var(--bk-border-w) solid var(--bk-border) !important;
            background-color: transparent !important;
            border-radius: var(--bk-radius-md) !important;
            transition: all 0.3s ease;
        }
        
        /* Texto do valor SELECIONADO (dentro do campo) */
        [class*="st-key-container_filter_bar_"] [data-baseweb="select"] div {
            color: var(--bk-text) !important;
            font-family: var(--bk-font) !important;
        }

        /* 4. O DROPDOWN SUSPENSO (Virtual Dropdown) */
        [data-testid="stSelectboxVirtualDropdown"] {
            background-color: var(--bk-surface) !important;
            border: var(--bk-border-w) solid var(--bk-border) !important;
            border-radius: var(--bk-radius-md) !important;
            box-shadow: var(--bk-shadow-md) !important;
            padding: 4px !important;
        }
        
        /* Remove a caixa escura/laranja nativa do Streamlit no hover/selected */
        [data-testid="stSelectboxVirtualDropdown"] li div[class*="e1d7a4qp0"] {
            background-color: transparent !important;
            border: none !important;
        }

        /* CONSOLIDAÇÃO DO ITEM DA LISTA (LI) */
        [data-testid="stSelectboxVirtualDropdown"] li {
            background-color: transparent !important;
            color: var(--bk-text) !important;
            font-family: var(--bk-font) !important;
            font-size: var(--bk-base) !important;
            transition: all 0.2s ease-in-out !important;
            border-radius: var(--bk-radius-md) !important;
            margin: 4px !important;
            padding: 6px 12px !important;
            border: none !important; 
        }

        /* Hover no item — Substituição do hex_to_rgba pelo color-mix nativo */
        [data-testid="stSelectboxVirtualDropdown"] li:hover {
            background-color: color-mix(in srgb, var(--bk-primary) 12%, transparent) !important;
            color: var(--bk-text) !important;
        }

        /* Selecionado — Aplica uma camada de destaque um pouco mais forte */
        [data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] {
            background-color: color-mix(in srgb, var(--bk-primary) 22%, transparent) !important;
            color: var(--bk-text) !important;
            font-weight: var(--bk-w-medium) !important;
            border: none !important;
        }

        /* 5. SCROLLBAR DO DROPDOWN */
        [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar {
            width: 4px !important;
        }
        
        [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar-thumb {
            background: var(--bk-border) !important;
            border-radius: var(--bk-radius-full) !important;
        }
        
        [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar-thumb:hover {
            background: var(--bk-primary) !important;
        }
    """