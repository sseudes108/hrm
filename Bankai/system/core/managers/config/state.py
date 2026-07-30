from functools import partial

import streamlit as st

from system.core.applications import ApplicationDefinition
from system.core.contexts import AppContext
from system.core.managers.config import theme_preferences

def get_context(application: ApplicationDefinition) -> AppContext:
    """Garante o contexto de sessão pertencente à aplicação carregada."""
    session_key = f"app_context_{application.app_id}"
    state_key = application.app_id
    if state_key not in st.session_state:
        st.session_state[state_key] = application.state_factory(application.initial_route)

    application_state = st.session_state[state_key]
    if session_key not in st.session_state:
        mode = theme_preferences.load_theme_mode(
            application.app_id,
            application.default_mode,
        )
        try:
            loaded_theme = application.load_theme(mode)
        except ValueError:
            if mode == application.default_mode:
                raise
            mode = application.default_mode
            loaded_theme = application.load_theme(mode)
            theme_preferences.save_theme_mode(application.app_id, mode)
        st.session_state[session_key] = AppContext(
            app_name=application.app_id,
            theme=loaded_theme,
            mode=mode,
            theme_loader=application.load_theme,
            theme_mode_persister=partial(
                theme_preferences.save_theme_mode,
                application.app_id,
            ),
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
            theme_mode_persister=partial(
                theme_preferences.save_theme_mode,
                application.app_id,
            ),
            state=application_state,
        )
        st.session_state[session_key] = context

    context.set_theme_loader(application.load_theme)
    context.set_theme_mode_persister(
        partial(theme_preferences.save_theme_mode, application.app_id)
    )
    context.set_state(application_state)
    return context
