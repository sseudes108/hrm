import sys
import os
import streamlit as st

import system.control.managers.page    as page_man
import system.control.managers.state    as state_man
import system.control.managers.layout   as layout_man

from system.control.contexts import AppContext

def check_args():
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path not in sys.path:
        sys.path.append(root_path)

    target_app = "bankai" 

    args = [arg for arg in sys.argv if arg.startswith("--")]
    if args:
        target_app = args[0].replace("--", "").lower()
    
    return target_app

def get_context(target_app) -> AppContext:
    context = state_man.get_context(target_app)
    if context is None:
        page_man.run_error_page(f"{target_app} (Erro de Inicialização de Estado)")
        st.stop()
    else:
        return context

def main():
    target_app = check_args()
    
    st.set_page_config(
        page_title=f"{target_app.upper()}",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Busca o contexto com validação
    context = get_context(target_app)
        
    layout_man.init_theme(context.theme)
    page_man.run(target_app, context)

if __name__ == "__main__":
    main()