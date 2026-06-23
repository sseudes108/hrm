import streamlit as st
from system.core.contexts import AppContext
import system.core.managers.config.hash as hash_man

def render(page_to_render=None, context:AppContext=None):
    if page_to_render is None:
        st.error("Page Renderer - Render page is None")
        return
    if context is None:
        st.error("Page Renderer - Context is None")
        return
    
    page_hash = hash_man.get_hash(str(page_to_render))
    with st.container(key=f"co_page_content_{context.app_name}_{page_hash}"):
        page_to_render.main(context)