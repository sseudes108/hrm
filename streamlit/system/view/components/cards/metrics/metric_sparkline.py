import streamlit as st
import uuid
import re
from system.control.config import hex_to_rgba
from system.view.components.cards.helper import get_lucide_svg
from system.view.components.charts.echarts.sparkline import draw_sparkline_chart

def sparkline_metric(
    theme: dict,
    titulo: str,
    valor: str,
    show_spark = False,
    sparkline_data = None,
    icone: str = "activity",
    secundario_valor: str = "",
    secundario_label: str = "",
    tooltip: str = "",
    cor: str = "#00f0ff",
    glow: bool = True,
    key: str = None,
    border_radius = None
) -> None:
    
    if border_radius == None:
        border_radius = theme["spacing"]["md"]

    colors = theme["colors"]
    cor_html = colors[cor]
    
    if key is None:
        key = f"spark_{hash(titulo) if titulo else uuid.uuid4().hex[:6]}"

    # CSS de Escopo Dinâmico
    unique_style = f"""
        <style>
            [class*="st-key-metric_card_{key}"] {{
                border-radius: {border_radius} !important;
            }}
        
            .mcard-valor-{key} {{
                margin-top: 0.2em;
                color: {theme['colors']['text']};
                {f"text-shadow: 0 0 15px {cor_html}66;" if glow else ""}
                font-size: 2rem !important;
                font-weight: 800 !important;
                line-height: 1 !important;
                margin-bottom: 4px !important;
            }}

            [class*="st-key-metric_card_{key}"] .mcard-info {{
                width: 1.5em;
                height: 1.5em;
                margin-right: 4%;
                border-radius: 50%;
                background: {hex_to_rgba(colors['text_muted'], 0.05)};
                border: 1px solid {hex_to_rgba(colors['text_muted'], 0.7)};
                color: {hex_to_rgba(colors['text'], 0.5)};
                font-size: 0.7em;
                font-family: sans-serif;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: help;
                pointer-events: auto !important;
                transition: all 0.2s ease-in-out;
                position: relative !important;
                z-index: 101;
                overflow: visible !important;
            }}

            /* Hover do BOTÃO (só o círculo ?) */
            [class*="st-key-metric_card_{key}"] .mcard-info:hover {{
                background: rgba(255, 255, 255, 0.15);
                border-color: {cor_html};
                color: white;
                box-shadow: 0 0 10px {cor_html}44;
                transform: scale(1.1);
            }}

            /* Hover do TOOLTIP (aparece quando passa no botão) */
            [class*="st-key-metric_card_{key}"] .mcard-info:hover .mcard-tooltip {{
                visibility: visible !important;
                opacity: 1 !important;
                transform: translateY(0) !important;
            }}
        </style>
    """

    icon_svg = get_lucide_svg(icone, cor_html)
    
    # 1. HTML do Header
    # info_html = f'<div class="mcard-info">?<div class="mcard-tooltip">{tooltip}</div></div>' if tooltip else ""

    # Teste temporário - substitua o info_html
    info_html = f'''
    <style>
        .mcard-info-{key}:hover .tip {{
            visibility: visible !important;
            opacity: 1 !important;
        }}
    </style>
    <div class="mcard-info-{key}" style="
        width: 1.5em; height: 1.5em; border-radius: 50%;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.5);
        color: rgba(255,255,255,0.5);
        font-size: 0.7em; font-weight: bold;
        display: flex; align-items: center; justify-content: center;
        cursor: help; position: relative; z-index: 101;
        margin-right: 8px; overflow: visible !important;
        
        /* Expande a área de hover sem mudar o visual */
        padding: 12px !important;
        box-sizing: content-box !important;
        margin: -12px !important;        /* compensa o padding para não deslocar o layout */
        margin-right: 4px !important;    /* mantém margem direita mínima */
    ">
        ?
        <div class="tip" style="
            visibility: hidden; opacity: 0;
            position: absolute; z-index: 999999;
            bottom: 130%; right: -10px;
            background: #1a1a1a;
            border: 1px solid rgba(255,255,255,0.15);
            padding: 8px 12px; border-radius: 6px;
            white-space: nowrap; font-size: 1.4em;
            color: rgba(255,255,255,0.8);
            pointer-events: none;
            transition: opacity 0.2s ease, visibility 0.2s ease;
        ">
            {tooltip}
        </div>
    </div>
    ''' if tooltip else ""

    header_html = f'''
        <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
            <div style="display:flex; align-items:center; gap:8px;">
                {icon_svg}
                <span class="mcard-titulo">{titulo}</span>
            </div>
            {info_html} 
        </div>
    '''

    # 2. HTML do Valor (Lado Esquerdo)
    value_html = f'''
    <div style="display:flex; flex-direction:column; justify-content:center; height:100%; padding-left:12px; line-height:1; z-index:2;">
        
        <div class="mcard-valor-{key}" style="white-space:nowrap;">
            {valor}
        </div>

        <div style="margin-top:0.5em; display:flex; align-items:center; gap:0.3em; flex-wrap:nowrap;">
            <span style="font-size:0.6rem; color:rgba(255,255,255,0.4); text-transform:uppercase; white-space:nowrap;">
                {secundario_label}
            </span>
            <span style="font-size:0.8rem; color:{cor_html}; font-family:monospace; white-space:nowrap;">
                {secundario_valor}
            </span>
        </div>

    </div>
    '''

    with st.container(key=f"metric_card_{key}"):
        st.markdown(unique_style, unsafe_allow_html=True)
        
        with st.container(key=f"metric_header_{key}"):
            st.markdown(header_html.replace('\n', ' '), unsafe_allow_html=True)
        
        with st.container(key=f"metric_body_{key}"):
            value_col, sparkline_col = st.columns([2,5], gap='xxsmall')

            with value_col:
                with st.container(key=f"metric_body_value_{key}"):
                    clean_value = re.sub(r'>\s+<', '><', value_html).strip()
                    st.markdown(clean_value, unsafe_allow_html=True)

            with sparkline_col:
                with st.container(key=f"metric_body_spark_{key}"):
                    if show_spark:
                        draw_sparkline_chart(theme, sparkline_data, cor, key=f"echart_{key}")
                    else:
                        pass