import streamlit as st
import uuid

def draw_select_filter(title, options, theme, label_width="5"):
    key = f"f_select_{hash(title) if title else uuid.uuid4().hex[:6]}"

    unique_style = f"""
        <style>
            [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {{
                width:{label_width}rem !important;
                min-width: 5rem !important;
            }}

            /* Hover no campo */
            [class*="st-key-container_filter_bar_{key}"]:hover [data-baseweb="select"] > div {{
                border-color: {theme['colors']['primary']} !important;
            }}
        </style>
    """
    
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    with st.container(key=f"container_filter_bar_{key}"):
        selected = st.selectbox(
            label=title,
            options=options,
            key=key
        )

    return selected