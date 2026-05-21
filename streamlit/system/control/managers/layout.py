import streamlit as st
from system.view.layout.css.base import get_css_base
from system.view.layout.css.streamlit import get_css_settings
from system.view.layout.css.containers.index import get_css_containers
from system.view.layout.css.header.index import get_css_header
from system.view.layout.css.filters.index import get_css_filters
from system.view.layout.css.metrics.index import get_css_metrics

def init_theme(theme):
    """
    Injeta o mapa de variáveis no :root e carrega os blocos de CSS estruturais
    que agora consomem essas variáveis nativamente.
    """
    st.markdown(f"""
        <style>
            {get_css_settings()}
            
            /* 1. O base cria o :root dinâmico com o JSON */
            {get_css_base(theme)} 
            
            /* 2. Os demais agora são ESTÁTICOS e limpos, usam apenas var(--bk-*) */
            {get_css_header(theme)}

            {get_css_metrics()}
            {get_css_containers()}
            {get_css_filters()}
        </style>
    """, unsafe_allow_html=True)