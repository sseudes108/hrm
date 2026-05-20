import sys
import os
import streamlit as st
import system.control.managers.pages as page_man
import system.control.managers.state as state_man
import system.control.config as config_man

def check_args():
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path not in sys.path:
        sys.path.append(root_path)

    target_app = "bankai" 

    args = [arg for arg in sys.argv if arg.startswith("--")]
    if args:
        target_app = args[0].replace("--", "").lower()
    
    return target_app

def get_context(target_app):
    try:
        filter_context = state_man.get_context(target_app)
        if filter_context:
            return filter_context
    except Exception as e:
        print(f"Falha crítica no state_man: {e}")
    
    # Garante explicitamente o retorno None caso falte o contexto ou estoure erro
    return None

def load_app(target_app, context):
    if target_app == "bankai":
        page_man.bankai(context)

    elif target_app == "shebattle":
        page_man.shebattle(context)
        
    else:
        page_man.show_error_page(target_app)

def main():
    target_app = check_args()
    
    st.set_page_config(
        page_title=f"Bankai - {target_app.upper()}",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Busca o contexto com validação
    filter_context = get_context(target_app)
    
    # Se o contexto não voltar, interrompe e mostra a variação do erro
    if filter_context is None:
        page_man.show_error_page(f"{target_app} (Erro de Inicialização de Estado)")
        st.stop() # Garante que o Python para a execução aqui e não renderiza mais nada
        
    load_app(target_app, filter_context)

if __name__ == "__main__":
    main()