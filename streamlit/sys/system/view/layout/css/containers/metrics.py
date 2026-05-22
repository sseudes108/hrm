"""
control/styles/css_metrics.py — Bankai 
Containers de métricas com efeito glassmorphism adaptado ao tema.
"""

from system.control.config import hex_to_rgba

def get_css_metrics(theme: dict) -> str:
    c    = theme["colors"]
    b    = theme["borders"]
    ty   = theme["typography"]
    sp   = theme["spacing"]
    ef   = theme["effects"]
    dark = theme["meta"]["base"] == "dark"

    if dark:
        bg_normal    = "rgba(255, 255, 255, 0.05)"
        bg_hover     = "rgba(255, 255, 255, 0.08)"
        border       = "1px solid rgba(255, 255, 255, 0.08)"
        border_hover = f"1px solid {hex_to_rgba(c['primary'], 0.4)}"
        shadow       = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
        shadow_hover = "0 12px 40px 0 rgba(0, 0, 0, 0.5)"
        backdrop     = "backdrop-filter: blur(10px) !important; -webkit-backdrop-filter: blur(10px) !important;"
        text_primary = "rgba(255, 255, 255, 0.95)"
        text_muted   = "rgba(255, 255, 255, 0.35)"
    else:
        bg_normal    = c["surface"]
        bg_hover     = c["surface_2"]
        border       = f"1px solid {c['border']}"
        border_hover = f"1px solid {c['border_focus']}"
        shadow       = b["shadow_sm"]
        shadow_hover = b["shadow_md"]
        backdrop     = ""
        text_primary = c["text"]
        text_muted   = c["text_muted"]

    return f"""
        /* ─── 1. CONTAINER PAI ─────────────────────────────────────────── */
        [class*="st-key-metric_card_"] {{
            background: {bg_normal} !important;
            {backdrop}
            border: {border} !important;
            border-radius: {b['radius_md']} !important;
            min-height: 120px !important;
            max-height: 120px !important; /* Altura travada para evitar pulos */
            box-shadow: {shadow} !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: visible !important; /* Permite o tooltip flutuar fora */
        }}

        [class*="st-key-metric_card_"]:hover {{
            background:    {bg_hover} !important;
            border:        {border_hover} !important;
            transform:     translateY({ef["hover_y"]});
            box-shadow:    {shadow_hover} !important;
        }}

        .mcard {{
            height: 100%;
            padding: {sp['md']};
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }}

        /* ─── 2. ÍCONE LUCIDE ─────────────────────────────────────────── */
        .mcard-icon-wrapper {{
            position: absolute;
            top: 5%;
            right: 5%;
            opacity: 0.8;
        }}
        
        .mcard-icon {{
            width: 1.2em;
            height: 1.2em;
            color: {text_muted};
        }}

        /* ─── 3. TEXTOS ───────────────────────────────────────────────── */
        .mcard-titulo {{
            font-size: 0.65rem;
            color: {text_muted};
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.9em;
        }}

        .mcard-valor {{
            font-family: {ty['font_family_mono']};
            font-size: 2.2rem;
            font-weight: 300;
            color: {text_primary};
            line-height: 1;
        }}

        /* ─── 4. INFO & TOOLTIP (CORREÇÃO DE LAYOUT) ───────────────────── */
        /* 1. Forçar o container do Streamlit a permitir que o tooltip "vaze" */
        [data-testid="stVerticalBlock"]:has(> [class*="st-key-metric_card_"]) {{
            overflow: visible !important;
        }}

        /* 2. O Tooltip propriamente dito */
        .mcard-tooltip {{
            visibility: hidden;
            position: absolute;
            z-index: 100000 !important; /* Valor astronômico para passar o ECharts */
            background: {hex_to_rgba(c['background'], 0.95)};
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: {hex_to_rgba(c['text'], 0.95)};
            padding: 0.8em 1em;
            border-radius: 0.3em;
            width: max-content;
            max-width: 200px;
            
            /* Posicionamento Inteligente */
            bottom: 120%; /* Aparece acima do '?' */
            right: 0;    /* Alinha a borda direita com o '?' */
            
            opacity: 0;
            transition: opacity 0.3s, transform 0.3s;
            transform: translateY(10px);
            pointer-events: none;
            line-height: 1.4;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
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

        .mcard-info:hover .mcard-tooltip {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0);
        }}
    """