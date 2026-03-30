import streamlit as st

def draw_select_filter(label, options, key, index=0):
    """Componente puro de desenho do selectbox"""
    return st.selectbox(
        label=label,
        options=options,
        index=index,
        key=key
    )

def draw_date_filter(label, key, value='today'):
    return st.date_input(
        label, 
        value=value, 
        key=f"date_filter_{key}_{label}"
    )