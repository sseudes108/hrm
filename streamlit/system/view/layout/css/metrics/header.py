from system.control.config import hex_to_rgba

def get_css_header(theme):
    colors = theme["colors"]
    typography = theme["typography"]
    borders = theme["borders"]
    effects = theme["effects"]
    dark = theme["meta"]["base"] == "dark"

    # if dark:
    #     bg_normal    = "rgba(255, 255, 255, 0.05)"
    #     bg_hover     = "rgba(255, 255, 255, 0.08)"
    #     border       = "1px solid rgba(255, 255, 255, 0.08)"
    #     border_hover = f"1px solid {hex_to_rgba(colors['primary'], 0.4)}"
    #     shadow       = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
    #     shadow_hover = "0 12px 40px 0 rgba(0, 0, 0, 0.5)"
    #     backdrop     = "backdrop-filter: blur(10px) !important; -webkit-backdrop-filter: blur(10px) !important;"
    #     text_primary = "rgba(255, 255, 255, 0.95)"
    #     text_muted   = "rgba(255, 255, 255, 0.35)"
    # else:
    #     bg_normal    = colors["surface"]
    #     bg_hover     = colors["surface_2"]
    #     border       = f"1px solid {colors['border']}"
    #     border_hover = f"1px solid {colors['border_focus']}"
    #     shadow       = borders["shadow_sm"]
    #     shadow_hover = borders["shadow_md"]
    #     backdrop     = ""
    #     text_primary = colors["text"]
    #     text_muted   = colors["text_muted"]
    border_hover = f"1px solid {colors['border_focus']}"

    return f"""
        /* O PAI (Container Externo) */
        [class*="st-key-metric_card_"] {{            
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: stretch !important;
            justify-content: flex-start !important;
            
            min-height: 120px;
            max-height: 120px;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
            /* Importante: overflow visible para o tooltip vazar para cima */
            overflow: visible !important; 
            position: relative !important;
        }}

        /* Reduz o gap entre os elementos filhos do card */
        [class*="st-key-metric_card_"] > div {{
            gap: 0 !important;
            row-gap: 0 !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}

        /* O FILHO (Cabeçalho Vermelho) */
        [class*="st-key-metric_header_"] {{
            width: 100% !important;
            padding: 8px 12px !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            min-height: 35px !important;
            overflow: visible !important;
            transform: translateY(-15px) !important;
        }}

                
        [class*="st-key-metric_header_"] > div {{
            overflow: visible !important;
            width: 100% !important;
        }}



        [class*="st-key-metric_header_"] .mcard-titulo {{
            font-size: 1rem !important;
            color: white !important;
            text-transform: uppercase !important;
            font-weight: bold !important;
        }}

        [class*="st-key-metric_header_"] .mcard-icon {{
            display: flex !important;
            align-items: center !important;    /* Centraliza o conteúdo (texto/emoji) verticalmente */
            justify-content: center !important; /* Centraliza o conteúdo horizontalmente dentro de si */

            width: 1em;
            height: 1em;
        }}

        /* ─── 4. INFO & TOOLTIP (CORREÇÃO DE LAYOUT) ───────────────────── */
        /* 1. Forçar o container do Streamlit a permitir que o tooltip "vaze" */
        [data-testid="stVerticalBlock"]:has(> [class*="st-key-metric_card_"]) {{
            overflow: visible !important;
        }}

        /* Tooltip corrigido */
        .mcard-tooltip {{
            visibility: hidden;
            opacity: 0;
            position: absolute;
            z-index: 999999 !important; 
            bottom: 110%; /* Sobe um pouco mais */
            right: 10px;
            background: #1a1a1a;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 10px;
            border-radius: 5px;
            pointer-events: none;
            transition: all 0.3s ease;
            transform: translateY(5px);
        }}

        /* Seta do Tooltip (opcional, mas fica elegante) */
        .mcard-tooltip::after {{
            content: "";
            position: absolute;
            top: 100%;
            right: 10px;
            border-width: 6px;
            border-style: solid;
            border-color: rgba(255, 255, 255, 0.1) transparent transparent transparent;
        }}

        .mcard-info {{
            position: relative !important;
            overflow: visible !important;
            z-index: 101 !important;
        }}

        .mcard-info:hover .mcard-tooltip {{
            visibility: visible !important;
            opacity: 1 !important;
            transform: translateY(0) !important;
        }}
    """