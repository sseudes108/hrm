import streamlit as st
from system.view.layout.css.base import get_css_base
from system.view.layout.css.streamlit import get_css_settings
from system.view.layout.css.containers.index import get_css_containers
from system.view.layout.css.header.index import get_css_header
from system.view.layout.css.filters.index import get_css_filters
from system.view.layout.css.metrics.index import get_css_metrics

def init_layout(title, theme, sidebar_state="collapsed"):
    st.set_page_config(
        page_title=title,
        initial_sidebar_state=sidebar_state,
    )

    _init_css(theme)

def _init_css(theme):
    st.markdown(f"""
        <style>
            {get_css_settings()}
            {get_css_header(theme)}
            {get_css_base(theme)}
            {get_css_metrics(theme)}
            {get_css_containers(theme)}
            {get_css_filters(theme)}
        </style>
    """, unsafe_allow_html=True)
