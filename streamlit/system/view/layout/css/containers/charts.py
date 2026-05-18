"""
control/styles/css_charts.py — Bankai Template
Containers de gráficos com efeito glassmorphism adaptado ao tema.
"""

from system.control.config import hex_to_rgba

def get_css_charts(theme: dict) -> str:
    c    = theme["colors"]
    b    = theme["borders"]
    ty   = theme["typography"]
    sp   = theme["spacing"]
    ef   = theme["effects"]
    dark = theme["meta"]["base"] == "dark"

    # Configuração Dinâmica de Glassmorphism vs Surface
    if dark:
        bg_normal    = "rgba(255, 255, 255, 0.05)"
        bg_hover     = "rgba(255, 255, 255, 0.08)"
        border       = "1px solid rgba(255, 255, 255, 0.10)"
        border_hover = f"1px solid {hex_to_rgba(c['primary'], 0.4)}"
        shadow       = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
        shadow_hover = "0 12px 40px 0 rgba(0, 0, 0, 0.5)"
        backdrop     = "backdrop-filter: blur(10px) !important; -webkit-backdrop-filter: blur(10px) !important;"
        text_color   = "rgba(255, 255, 255, 0.9)"
        text_muted   = c["text_muted"]
    else:
        bg_normal    = c["surface"]
        bg_hover     = c["surface_2"]
        border       = f"1px solid {c['border']}"
        border_hover = f"1px solid {c['border_focus']}"
        shadow       = b["shadow_sm"]
        shadow_hover = b["shadow_md"]
        backdrop     = ""
        text_color   = c["text"]
        text_muted   = c["text_muted"]

    return f"""
        /* 1. O CONTAINER PAI */
        [class*="st-key-chart_container_"] {{
            background:    {bg_normal} !important;
            {backdrop}
            border:        {border} !important;
            border-radius: {b['radius_md']} !important;
                        
            box-shadow:    {shadow} !important;
            transition:    all 0.3s ease-in-out !important;

            margin-top: -1%;
            padding-top: 2%;
            padding-bottom: 1%;

            display:        flex !important;
            flex-direction: column !important;
            align-items:    center !important;
        }}

        /* 2. APENAS O CABEÇALHO (Markdown) */
        [class*="st-key-chart_container_"] .stMarkdown {{
            width: 92% !important; /* Ajuste para alinhar com o início do desenho do gráfico */
            margin-left: auto !important;
            margin-right: auto !important;
            margin-bottom: -3% !important; /* Mantém o gráfico próximo ao texto */
            display: block !important;
        }}

        [class*="st-key-chart_container_"]:hover {{
            background:    {bg_hover} !important;
            border:        {border_hover} !important;
            transform:     translateY({ef['hover_y']});
            box-shadow:    {shadow_hover} !important;
        }}

        /* 3. TIPOGRAFIA */
        [class*="st-key-chart_container_"] h3 {{
            color:       {text_color} !important;
            font-family: {ty['font_family']} !important;
            font-size:   {ty['size_subtitle']}px !important;
            font-weight: {ty['weight_bold']} !important;
            margin:      0 !important;
        }}

        [class*="st-key-chart_container_"] p {{
            color:       {text_muted} !important;
            font-family: {ty['font_family']} !important;
            font-size:   {ty['size_sm']}px !important;
            margin:      0 !important;
        }}

        [class*="st-key-chart_container_"] .metric-value {{
            color:       {c['primary']} !important;
            font-family: {ty['font_family_mono']} !important;
            font-size:   {ty['size_subtitle']}px !important;
            font-weight: {ty['weight_medium']} !important;
        }}
    """