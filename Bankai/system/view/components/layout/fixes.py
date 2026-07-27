import streamlit as st

def horizontal_spacer(height: str = "16px") -> None:
    st.html(f'<div style="height: {height};"></div>')