import streamlit as st
from system.view.components.cards import card

def draw(
    context,
    title: str, 
    value: str | int | float,
    icon:str = ":material/dataset:",
    subtitle:str = None,
    title_html: str = None, 
    value_html: str = None, 
    info_html: str = None, 
    footer_html: str = None
):
    with st.container(key="co_metric_"):
        card.draw(
            card.CardConfig(
                card_id=f"metric_{context.app_name}_{title}_{value}", icon=icon,
                context=context, model="metric", title=title, subtitle=subtitle,
                has_title=True
            ), 
            card.CardRenderConfig(
                content=lambda: _draw_component(title, value, title_html, info_html, value_html, footer_html),
                right_side_html=info_html
            )
        )

def _draw_component(title, value, title_html, info_html, value_html, footer_html):
    pass
    # # 1. FALLBACKS: Se não vier HTML customizado, usa o padrão com as classes CSS da Lakshmi
    # html_title_final = title_html if title_html else f'<div class="metric-title">{title}</div>'
    html_value_final = value_html if value_html else f'<div class="metric-value-main">{value}</div>'

    # 3. VALOR (Body)
    with st.container(key="co_metric_value_"):
        st.html(html_value_final)

    # 4. FOOTER (Condicional)
    # Só cria o container do rodapé se realmente houver conteúdo para ele
    if footer_html:
        with st.container(key="co_metric_footer_"):
            st.html(footer_html)