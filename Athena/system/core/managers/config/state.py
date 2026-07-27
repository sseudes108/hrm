import streamlit as st

from system.core.applications import ApplicationDefinition
from system.core.contexts import AppContext

def get_context(application: ApplicationDefinition) -> AppContext:
    """Garante o contexto de sessão pertencente à aplicação carregada."""
    session_key = f"app_context_{application.app_id}"
    state_key = application.app_id
    if state_key not in st.session_state:
        st.session_state[state_key] = application.state_factory(application.initial_route)

    application_state = st.session_state[state_key]
    if session_key not in st.session_state:
        mode = application.default_mode
        st.session_state[session_key] = AppContext(
            app_name=application.app_id,
            theme=application.load_theme(mode),
            mode=mode,
            theme_loader=application.load_theme,
            state=application_state,
        )

    context = st.session_state[session_key]
    if not isinstance(context, AppContext):
        mode = getattr(context, "mode", application.default_mode)
        context = AppContext(
            app_name=application.app_id,
            theme=application.load_theme(mode),
            mode=mode,
            theme_loader=application.load_theme,
            state=application_state,
        )
        st.session_state[session_key] = context

    context.set_theme_loader(application.load_theme)
    context.set_state(application_state)
    return context
