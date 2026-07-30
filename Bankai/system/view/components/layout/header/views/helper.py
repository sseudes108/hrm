import streamlit as st

from system.core.auth.guard import logout
from system.view.components import button

def draw_tools(context):
    if context.mode == "dark":
        # Usando os ícones oficiais do Material Design com a sintaxe correta
        btn_icon = ":material/light_mode:" 
        next_mode = "light"
    else:
        btn_icon = ":material/dark_mode:"
        next_mode = "dark"

    with st.container(key="co_header_tools"):
        auth_config = getattr(context, "auth_config", None)
        principal_key = f"auth_{context.app_name}_principal"
        if auth_config and auth_config.enabled and principal_key in st.session_state:
            button.draw(
                context=context,
                label=" ",
                button_id="header_logout",
                variant="ghost",
                icon=":material/logout:",
                on_click=logout,
                args=(context, auth_config),
                help="Sair",
            )
        button.draw(
            context=context,
            label=" ",
            button_id="header_theme_toggle",
            variant="ghost",
            icon=btn_icon,
            help=f"Ativar tema {next_mode}",
            on_click=lambda: context.update_mode(new_mode=next_mode),
        )
