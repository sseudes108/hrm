import os, sys
from pathlib import Path
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from system.core.applications import ApplicationDefinition, registry
from system.core.auth import require_authentication
from system.core.infrastructure import load_environment
from system.core.managers.view import layout as layout_man
from system.core.managers.config import state as state_man
from system.core.managers.config import page as page_man
from system.view.pages import error

DEFAULT_APP = "bankai"


def _check_args() -> str:
    """
    Garante que o diretório raiz está no sys.path e resolve o app alvo.
    Prioriza parâmetros de URL (?app=nome), com fallback para linha de comando.
    """
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path not in sys.path:
        sys.path.append(root_path)

    # 1. Tenta capturar o app diretamente da URL no navegador
    # Ex: http://localhost:8501/?app=bankai
    url_target = st.query_params.get("app")
    if url_target:
        return str(url_target).strip().lower()

    # 2. Fallback para linha de comando caso não tenha parâmetro na URL
    # Ex: streamlit run app.py -- --bankai
    target_app = DEFAULT_APP
    args = [arg for arg in sys.argv if arg.startswith("--")]
    
    if args:
        target_app = args[0].replace("--", "").lower()

    return target_app

def _load_application(target_app: str) -> ApplicationDefinition:
    """Carrega uma aplicação pela convenção ``<nome>.app``."""
    if not target_app.isidentifier():
        error.main(target_app)
        st.stop()

    module_path = f"{target_app}.app"
    try:
        return registry.load_module(module_path)
    except ModuleNotFoundError as exc:
        if exc.name not in {target_app, module_path}:
            raise
        error.main(target_app)
        st.stop()

def main():
    """
    Ponto de entrada da aplicação.

    Fluxo:
        1. Resolve e carrega o app alvo pela convenção de diretórios.
        2. Configura a página do Streamlit com os metadados do app.
        3. Recupera o contexto global da sessão.
        4. Inicializa o tema visual a partir do contexto.
        5. Delega a renderização ao page_man.
    """
    load_environment(Path(__file__).with_name(".env"))

    target_app = _check_args()
    application = _load_application(target_app)

    st.set_page_config(
        page_title=application.title,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # ── Detecta largura da tela uma única vez por sessão ──
    width = streamlit_js_eval(js_expressions="window.innerWidth", key="screen_w_global")
    if width is not None and width != st.session_state.get("screen_width"):
        st.session_state["screen_width"] = width
        st.rerun()

    context = state_man.get_context(application)
    context.screen_width = st.session_state.get("screen_width") or 1920
    context.auth_config = application.auth

    layout_man.init_theme(context.theme)
    # O placeholder impede que o formulário de login e a página coexistam no
    # mesmo ciclo de renderização após uma autenticação bem-sucedida.
    auth_slot = st.empty()
    with auth_slot.container():
        authenticated = require_authentication(context, application.auth)
    if not authenticated:
        st.stop()
    auth_slot.empty()
    page_man.run(application, context)

if __name__ == "__main__":
    main()
