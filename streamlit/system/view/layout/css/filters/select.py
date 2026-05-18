from system.control.config import hex_to_rgba
def get_css_select(colors, typography, borders):
    return f"""
        /* 1. O CONTAINER PRINCIPAL */
        [class*="st-key-container_filter_bar_"] {{            
            position: relative !important;
            left: 0 !important;
            padding: 0em !important;
            cursor: pointer;
        }}

        /* 2. A LABEL (Efeito Floating) */
        /* Miramos no p para a cor e no widgetLabel para o fundo que corta a borda */
        [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {{
            position: absolute !important;
            top: -0.6rem !important; /* Ajuste fino para sentar na borda */
            left: 1.2rem !important;
            z-index: 10 !important;
            background-color: {colors['background']} !important; 
            padding: 0 8px !important;
            width: auto !important;
            min-width: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] p {{           
            color: {colors['text_muted']} !important;
            font-size: 0.85rem !important;
            font-weight: {typography['weight_bold']} !important;
            margin: 0 !important;
        }}

        /* 3. A BORDA DO CAMPO (Selectbox) */
        [class*="st-key-container_filter_bar_"] [data-baseweb="select"] > div {{
            border: 1px solid {colors['border']} !important;
            background-color: transparent !important;
            border-radius: {borders['radius_md']} !important;
            transition: all 0.3s ease;
        }}
        
        /* Texto do valor SELECIONADO (dentro do campo) */
        [class*="st-key-container_filter_bar_"] [data-baseweb="select"] div {{
            color: {colors['text']} !important;
        }}

        [data-testid="stSelectboxVirtualDropdown"] {{
            border: {colors['border']} !important;
            padding: 4px !important;
        }}
        /* 1. REMOVE A COR E BORDA INTERNA (A caixa escura/laranja que aparece no hover/selected) */
        [data-testid="stSelectboxVirtualDropdown"] li div[class*="e1d7a4qp0"] {{
            background-color: transparent !important;
            border: none !important;
        }}

        /* 2. CONSOLIDAÇÃO DO ITEM DA LISTA (LI) */
        [data-testid="stSelectboxVirtualDropdown"] li {{
            background-color: transparent !important;
            transition: all 0.2s ease-in-out !important;
            border-radius: 12px !important;
            margin: 4px !important;
            padding: 4px !important;
            border: none !important; /* Remove bordas internas */
        }}

        /* Hover no item - APENAS UMA CAMADA */
        [data-testid="stSelectboxVirtualDropdown"] li:hover {{
            background-color: {hex_to_rgba(colors['primary'], 0.1)} !important;
        }}

        /* Selecionado - APENAS UMA CAMADA */
        [data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] {{
            background-color: {hex_to_rgba(colors['primary'], 0.2)} !important;
            border: none !important;
        }}

        /* 6. SCROLLBAR */
        [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar {{
            width: 4px !important;
        }}
        
        [data-testid="stSelectboxVirtualDropdown"] > div::-webkit-scrollbar-thumb {{
            background: {colors['border']} !important;
            border-radius: 10px !important;
        }}
    """