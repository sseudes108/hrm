import streamlit as st
from system.view.components.cards import card
from system.view.components.layout.navigator import navigator
from system.view.components.layout.header.views import helper

def set_unique_style(header_config):
    # Injeta reset APENAS quando não tem card wrapper
    if not header_config.has_card:
        key = header_config["key"]
        unique_style = f"""
            <style>
                [class*="st-key-co_card_header_{key}"] {{
                    background:              transparent !important;
                    backdrop-filter:         none !important;
                    -webkit-backdrop-filter: none !important;
                    border-radius:           0 !important;
                    box-shadow:              none !important;
                    border:                  none !important;
                }}
                [class*="st-key-co_card_header_{key}"]:hover {{
                    box-shadow: none !important;
                    transform:  none !important;
                }}
            </style>
        """
        st.html(unique_style)

def draw_title(header_config: dict, context):
    title    = header_config.title.upper()
    subtitle = header_config.subtitle.upper()

    logo_size = int(context.theme["layout"]["logo_size"])

    if logo_size < 80:
        header_cols = st.columns([0.2, 0.8], gap='small', vertical_alignment="bottom")
    else:
        header_cols = st.columns([0.3, 0.6], gap='small', vertical_alignment="bottom")

    with header_cols[0]:
        card.draw(
            card.CardConfig(
                card_id="header_logo", context=context, 
                show_card=header_config.logo_card, 
                hover=False, model="wrapper"
            ),card.CardRenderConfig(
                content=lambda: st.image(
                    context.theme["layout"]["logo_png"], 
                    width=logo_size
                )
            )
        )
        
    with header_cols[1]:
        # Aqui o seu HTML será renderizado dentro de uma coluna que agora está 
        # forçada a alinhar o conteúdo no fundo (flex-end)
        html_content = f"""
        <div class="header-brand">
            <div class="header-brand-text">
                <p class="header-brand-title">{title}</p>
                <p class="header-brand-subtitle">{subtitle}</p>
            </div>
        </div>
        """
        card.draw(
            card.CardConfig(
                card_id="header_title_text", context=context, 
                show_card=False, hover=False, model="wrapper"
            ),card.CardRenderConfig(
                content=lambda: st.html(html_content)
            )
        )

def get_component(header_config, context):
    set_unique_style(header_config)

    # Adicionamos vertical_alignment="bottom" para garantir que o Streamlit 
    # jogue tudo das 3 colunas para a linha de base
    header_cols = st.columns([2, 5, 0.5], gap='xxsmall', vertical_alignment="bottom")

    with header_cols[0]:
        draw_title(header_config, context)

    with header_cols[1]:
        navigator.draw(
            context=context, 
            model="header_nav", is_sub=False, 
            nav_pages=header_config.nav_pages
        )

    with header_cols[2]:
        helper.draw_tools(context)