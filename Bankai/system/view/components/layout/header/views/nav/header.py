import streamlit as st
from system.control.contexts import AppContext
from system.view.components.layout.header import HeaderConfig
from system.view.components.layout.navigator import navigator, NavigatorConfig

def set_unique_style(header_config: HeaderConfig):
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
        st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

def draw_title(header_config: dict):
    title    = header_config.title.upper()
    subtitle = header_config.subtitle.upper()

    html = (
        f'<div class="header-brand">'
        f'<div class="header-logo-container">'
        f'<svg class="header-logo-icon" viewBox="0 0 24 24" fill="currentColor">'
        f'<path d="M12 2L14.8 9.2L22 12L14.8 14.8L12 22L9.2 14.8L2 12L9.2 9.2L12 2Z'
        f'M12 5.8L10.3 9.7L6.4 11.4L10.3 13.1L12 17.2L13.7 13.1L17.6 11.4L13.7 9.7L12 5.8Z"/>'
        f'</svg>'
        f'</div>'
        f'<div class="header-brand-text">'
        f'<p class="header-brand-title">{title}</p>'
        f'<p class="header-brand-subtitle">{subtitle}</p>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def draw_tools(header_config: HeaderConfig, context: AppContext):
    pass
    if context.mode == "dark":
        icon = "☀️"
        next_mode = "light"
    else:
        icon = "🌙"
        next_mode = "dark"

    with st.container(
        key="co_header_tools", 
        horizontal_alignment="right", 
        vertical_alignment="center"
    ):
        st.button(
            label=icon, 
            on_click=lambda: context.update_mode(new_mode=next_mode)
        )

def get_component(header_config: HeaderConfig, context:AppContext):
    set_unique_style(header_config)

    header_cols = st.columns([1.8, 6, 1], gap='xxsmall')

    with header_cols[0]:
        draw_title(header_config)

    with header_cols[1]:
        navigator.draw(
            context=context, model="tabs", is_sub=False, nav_pages=header_config.nav_pages
        )

    with header_cols[2]:
        draw_tools(header_config, context)