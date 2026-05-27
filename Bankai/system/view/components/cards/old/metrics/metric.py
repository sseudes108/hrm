import streamlit as st
import uuid
import re

from system.view.components.cards.old.helper import get_lucide_svg

def metric_card(
    titulo: str,
    valor: str,
    icone: str = "activity",
    secundario_valor: str = "",
    secundario_label: str = "",
    tooltip: str = "",
    cor: str = "#00f0ff",
    glow: bool = True,
    key: str = None,
    border_radius: str = "18px",
) -> None:
    if key is None:
        key = f"card_{hash(titulo) if titulo else uuid.uuid4().hex[:6]}"

    # CSS embutido com escopo único para este card
    unique_style = f"""
    <style>
        .metric-card-{key} {{
            border-radius: {border_radius} !important;
            transition: all 0.3s ease !important;
        }}
        .metric-card-{key} .mcard-valor {{
            {f"text-shadow: 0 0 15px {cor}55;" if glow else ""}
        }}
    </style>
    """

    # Tratamento de Tooltip e Secundário
    tooltip_clean = tooltip.replace('\n', '<br>')
    info_html = f'<div class="mcard-info">?<div class="mcard-tooltip">{tooltip_clean}</div></div>' if tooltip else ""
    
    secondary_html = ""
    if secundario_valor:
        label_html = f'<span class="mcard-secondary-label">{secundario_label}</span>' if secundario_label else ""
        secondary_html = f'<div class="mcard-bottom"><div class="mcard-secondary">{label_html}<span class="mcard-secondary-valor">{secundario_valor}</span></div></div>'

    # Ícone SVG direto
    icon_html = f'<div class="mcard-icon-wrapper">{get_lucide_svg(icone, cor)}</div>'

    # Montagem final
    html_content = (
        f'<div class="mcard metric-card-{key}">'
        f'{info_html}{icon_html}'
        f'<div class="mcard-top"><div class="mcard-titulo">{titulo}</div><div class="mcard-valor">{valor}</div></div>'
        f'{secondary_html}</div>'
    )

    # Limpeza de strings para evitar o bug de renderização do Streamlit
    final_html = f"{unique_style}{html_content}"
    final_html = re.sub(r'>\s+<', '><', final_html).replace('\n', ' ')

    with st.container(key=f"metric_card_{key}"):
        st.markdown(final_html, unsafe_allow_html=True)