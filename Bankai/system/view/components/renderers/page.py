import streamlit as st
from system.control.contexts import AppContext

def render(page_to_render=None, context:AppContext=None):
    if page_to_render is None:
        st.error("Page Renderer - Render page is None")
        return
    if context is None:
        st.error("Page Renderer - Context is None")
        return
    
    with st.container(key=f"co_page_content_{context.app_name}"):
        page_to_render.main(context)