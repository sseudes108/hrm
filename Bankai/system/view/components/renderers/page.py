import streamlit as st
from system.core.contexts import AppContext
import system.core.managers.config.hash as hash_man
from system.core.log.view import warnings

def render(page_to_render=None, context: AppContext | None = None) -> None:
    if page_to_render is None:
        warnings.draw("Page Renderer - Render page is None", alert="error", context=context)
        return
    if context is None:
        warnings.draw("Page Renderer - Context is None", alert="error")
        return
    
    page_hash = hash_man.get_hash(str(page_to_render))
    with st.container(key=f"co_page_content_{context.app_name}_{page_hash}"):
        page_to_render.main(context)
