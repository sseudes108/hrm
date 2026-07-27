import streamlit as st
from html import escape
from system.view.components.cards import card
from system.view.components._keys import scoped_key

def draw(
    context,
    title: str, 
    value: str | int | float,
    icon:str = ":material/dataset:",
    subtitle:str = None,
    title_html: str = None, 
    value_html: str = None, 
    info_html: str = None, 
    footer_html: str = None,
    metric_id: str | None = None,
    variant: str = "surface",
    padding: str = "normal",
    title_case: str = "none",
    title_align: str = "left",
    value_color: str | None = None,
):
    identifier = metric_id or f"{title}_{value}"
    metric_key = scoped_key(context, "co_metric", identifier)
    with st.container(key=metric_key):
        card.draw(
            card.CardConfig(
                card_id=f"metric_{identifier}", icon=icon,
                context=context, model="metric", title=title, subtitle=subtitle,
                has_title=True, variant=variant, padding=padding,
                title_case=title_case, title_align=title_align,
            ), 
            card.CardRenderConfig(
                content=lambda: _draw_component(
                    context, identifier, value, info_html, value_html, footer_html,
                    value_color,
                ),
                custom_title_html=title_html,
                right_side_html=info_html,
            )
        )

def _draw_component(context, identifier, value, info_html, value_html, footer_html, value_color=None):
    html_value_final = value_html if value_html else f'<div class="metric-value-main">{escape(str(value))}</div>'
    color_style = f' style="--metric-value-color: {escape(value_color, quote=True)}"' if value_color else ""

    # 3. VALOR (Body)
    with st.container(key=scoped_key(context, "co_metric_value", identifier)):
        st.html(f'<div class="metric-value-color"{color_style}>{html_value_final}</div>')

    # 4. FOOTER (Condicional)
    # Só cria o container do rodapé se realmente houver conteúdo para ele
    if footer_html:
        with st.container(key=scoped_key(context, "co_metric_footer", identifier)):
            st.html(footer_html)
