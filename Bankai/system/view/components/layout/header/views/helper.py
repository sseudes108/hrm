import streamlit as st

def draw_tools(context):
    if context.mode == "dark":
        # Usando os ícones oficiais do Material Design com a sintaxe correta
        btn_icon = ":material/light_mode:" 
        next_mode = "light"
    else:
        btn_icon = ":material/dark_mode:"
        next_mode = "dark"

    with st.container(key="co_header_tools"):
        st.button(
            label=" ", # Label vazio/espaço para criar um botão só de ícone
            icon=btn_icon, # Parâmetro dedicado para o ícone
            on_click=lambda: context.update_mode(new_mode=next_mode),
        )