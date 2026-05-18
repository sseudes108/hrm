from system.control.config import hex_to_rgba

def get_css_body(theme):
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
        /* Container que envolve as colunas */
        [class*="st-key-metric_body_"] {{
            flex-grow: 1 !important; /* Ocupa todo o resto do card */
            display: flex !important;
            flex-direction: column !important;
            width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
            margin-top: 0 !important;
            flex-grow: 1 !important;
        }}

        /* A estrutura de colunas do Streamlit */
        [class*="st-key-metric_body_"] > div[data-testid="stHorizontalBlock"] {{
            height: 100% !important;
            flex-grow: 1 !important;
            gap: 0 !important; /* Cola uma coluna na outra */
        }}

        /* Cada coluna individual */
        [class*="st-key-metric_body_"] div[data-testid="column"] {{
            display: flex !important;
            flex-direction: column !important;
            height: 20% !important;
        }}

        [class*="st-key-metric_body_"] > div[data-testid="stHorizontalBlock"] {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}

        /* --- Lado do Valor --- */
        [class*="st-key-metric_body_value_"] {{
            width: 100% !important;
            height: 100% !important; 
            flex-grow: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important; /* Alinha o texto à esquerda */
            justify-content: center !important;
            padding-left: 20px !important; /* Respiro na esquerda */
            margin-left: -30% !important;

            # background:red;
        }}

        .mcard-sub-label {{
            color: rgba(255, 255, 255, 0.4) !important;
        }}

        /* --- Lado do Sparkline --- */
        [class*="st-key-metric_body_spark_"] {{
            height: 100% !important;
            transform: translateY(-20px) !important;
            padding-bottom: 10px !important;
            padding-right: 4px !important;
        }}

        /* Forçar o ECharts a ocupar a largura mas crescer na altura */
        [class*="st-key-metric_body_spark_"] > div {{
            width: 100% !important;
            height: 80px !important; /* Aumenta a altura do gráfico dentro do card */
        }}
    """