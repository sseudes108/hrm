import streamlit as st
from system.view.components.cards import card
from system.view.components.layout.header.views import helper

def set_unique_style(header_config):
    # Injeta reset APENAS quando não tem card wrapper
    unique_style = ""
    
    key = header_config.key

    if not header_config.has_card:
        unique_style += f"""
            <style>
                [class*="st-key-co_card_header_{key}"] {{
                    background:              transparent !important;
                    backdrop-filter:         none !important;
                    -webkit-backdrop-filter: none !important;
                    border-radius:           0 !important;
                    box-shadow:              none !important;
                    border:                  none !important;
                }}
            </style>
        """

    if header_config.hover == False:
        unique_style += f"""
            <style>
                [class*="st-key-co_card_header_{key}"]:hover {{
                    box-shadow: none !important;
                    transform:  none !important;
                }}
            </style>
        """
        st.html(unique_style.replace('\n', ' '))

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
                card_id="header_logo", context=context, show_card=False ,hover=False, model="wrapper"
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
        html = f"""
        <div class="header-brand">
            <div class="header-brand-text">
                <p class="header-brand-title">{title}</p>
                <p class="header-brand-subtitle">{subtitle}</p>
            </div>
        </div>
        """
        card.draw(
            card.CardConfig(
                card_id="header_title_text", context=context, show_card=False, hover=False, model="wrapper"
            ),card.CardRenderConfig(
                content=lambda: st.html(html)
            )
        )

def get_component(header_config, context):
    # As colunas são criadas diretamente, pois já estamos "dentro" do container do Card.draw()
    header_cols = st.columns([2, 4, 0.5], gap='xxsmall', vertical_alignment="bottom")

    with header_cols[0]:
        draw_title(header_config, context)

    with header_cols[2]:
        helper.draw_tools(context)