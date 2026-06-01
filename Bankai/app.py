import sys
import os
import streamlit as st

from system.control.managers import page_man
from system.control.managers import state_man
from system.control.managers import layout_man

from system.control.contexts import AppContext

def check_args() -> str:
    """
    Garante que o diretório raiz está no sys.path e resolve o app alvo.
    Prioriza parâmetros de URL (?app=nome), com fallback para linha de comando.
    """
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path not in sys.path:
        sys.path.append(root_path)

    # 1. Tenta capturar o app diretamente da URL no navegador
    # Ex: http://localhost:8501/?app=sandbox
    if "app" in st.query_params:
        return st.query_params["app"].lower()

    # 2. Fallback para linha de comando caso não tenha parâmetro na URL
    # Ex: streamlit run main.py -- --sandbox
    target_app = "bankai"
    args = [arg for arg in sys.argv if arg.startswith("--")]
    
    if args:
        target_app = args[0].replace("--", "").lower()

    return target_app

def get_context(target_app: str) -> AppContext:
    """
    Recupera o AppContext do session_state para o app solicitado.

    Se o contexto não existir ou não puder ser inicializado, exibe uma
    página de erro e interrompe a execução via st.stop().

    Retorna:
        Instância ativa do AppContext para o app alvo.
    """
    context = state_man.get_context(target_app)
    if context is None:
        page_man.run_error_page(f"{target_app} (Erro de Inicialização de Estado)")
        st.stop()
    else:
        return context

def main():
    """
    Ponto de entrada da aplicação.

    Fluxo:
        1. Resolve o app alvo via argumentos de linha de comando.
        2. Configura a página do Streamlit.
        3. Recupera o contexto global da sessão.
        4. Inicializa o tema visual a partir do contexto.
        5. Delega a renderização ao page_man.
    """
    target_app = check_args()

    st.set_page_config(
        page_title=f"{target_app.upper()}",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "About": "Teste"
        }
    )

    context = get_context(target_app)
    
    layout_man.init_theme(context.theme)
    page_man.run(target_app, context)

if __name__ == "__main__":
    main()