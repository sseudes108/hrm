import streamlit as st
from system.view.components.layout.header import HeaderConfig

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

def draw_tools(header_config: HeaderConfig):
    initial = header_config.title[0].upper()

    html = f"""
        <div class="header-tools">
            <p class="header-status">SISTEMA ONLINE</p>
            <div class="header-avatar">{initial}</div>
        </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def get_component(header_config: HeaderConfig):
    set_unique_style(header_config)

    header_cols = st.columns([2, 5, 1], gap='xxsmall')

    with header_cols[0]:
        draw_title(header_config)
    with header_cols[2]:
        draw_tools(header_config)