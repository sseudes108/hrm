"""
app.py — Bankai Template
Ponto de entrada do projeto.
Para trocar o tema, altere apenas a string em get_theme().
"""

import streamlit as st
from system.control.managers.layout import init_layout
from system.control.managers.data import get_data_json
from system.view.components.layout.header import draw_header
from system.control.contexts.dash import DashboardContext
from system.view.components.filters.select import draw_select_filter
import system.control.managers.filter as filter_man

def main(context:DashboardContext):
    theme = context.theme
    init_layout("She Battle", theme)
    draw_header(theme=theme, title="She Battle", icon="🏳️‍⚧️", context=context)

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.table(context.active_filters)
    st.write(f"**Modo Ativo:** `{context.mode}`")

    df = get_data_json("apps/engines/shebattle/data/she_base.json")
    df_filtrado = filter_man.apply_filters(df, context.active_filters)

    list_names = df_filtrado["nome"].unique().tolist()
    list_pais = df_filtrado["pais"].unique().tolist()
    nome_selecionado = draw_select_filter("Nome", list_names, theme)
    pais_selecionado = draw_select_filter("Pais", list_pais, theme)
    context.update_filter("nome",nome_selecionado)
    context.update_filter("pais",pais_selecionado)

    st.dataframe(df_filtrado)

if __name__ == "__main__":
    main()