"""
app.py — Bankai 
Ponto de entrada do projeto.
Para trocar o tema, altere apenas a string em get_theme().
"""

import streamlit as st
import pandas as pd

from system.control.contexts import AppContext

import system.control.managers.data     as data_man
import system.control.managers.filter   as filter_man

import system.view.components.filters       as select_filter
import system.view.components.tables.table.table  as table
import system.view.components.tables.bodies as bodies

def draw_filters(df:pd.DataFrame, context:AppContext):
    ft_cols = st.columns(2, gap='xxsmall')

    selects = {}
    with ft_cols[0]:
        options = {
            "df": df,
            "label": "Nome",
            "column": "nome"
        }
        config = {
            "id": "ft_nome_main_teste",
            "has_card": False, 
            "allow_all": True,
            "update_app_context": True,
        }
        nome_selecionado = select_filter.draw_filter(
            options=options, context=context,
            config=config
        )

        selects["nome"] = nome_selecionado

     #########################################################
        options = {
            "df": df,
            "label": "Pau",
            "column": "tamanho_pau"
        }
        config = {
            "id": "ft_pau_main_teste",
            "has_card": False, 
            "allow_all": True,
            "update_app_context": True,
        }
        pau_selecionado = select_filter.draw_filter(
            options=options, context=context,
            config=config
        )

        selects["tamanho_pau"] = pau_selecionado

    #########################################################
    with ft_cols[1]:
        options = {
            "df": df,
            "label": "País",
            "column": "pais"
        }
        config = {
            "id": "ft_pais_main_teste",
            "has_card": False, 
            "allow_all": True,
            "update_app_context": True,
        }
        pais_selecionado = select_filter.draw_filter(
            options=options, context=context,
            config=config
        )

        selects["pais"] = pais_selecionado

    #########################################################
        options = {
            "df": df,
            "label": "Bunda",
            "column": "tamanho_bunda"
        }
        config = {
            "id": "ft_bunda_main_teste",
            "has_card": False, 
            "allow_all": True,
            "update_app_context": True,
        }
        pais_selecionado = select_filter.draw_filter(
            options=options, context=context,
            config=config
        )

        selects["tamanho_bunda"] = pais_selecionado

    return selects

def draw_debug(df_filtrado:pd.DataFrame, context:AppContext):
    debug_cols = st.columns(2, gap='xxsmall')

    with debug_cols[0]:
        selects = draw_filters(df_filtrado, context)

    with debug_cols[1]:
        st.json(context.active_filters)

        wr_cols = st.columns(2, gap='small')
        with wr_cols[0]:
            st.info(f"Nome Selecionado: {selects["nome"]}")
            st.info(f"Pau Selecionado: {selects["tamanho_pau"]}")

        with wr_cols[1]:
            st.info(f"País Selecionado: {selects["pais"]}")
            st.info(f"Bunda Selecionad: {selects["tamanho_bunda"]}")

def main(context:AppContext):
    df = data_man.get_data_json("apps/engines/shebattle/data/she_base.json")
    df_filtrado = filter_man.apply_filters(df, context.active_filters)

    draw_debug(df_filtrado, context)

    table_config = {
        "app_name": "bankai",
        "titulo": "test_debug_table",
        "height": 700,
        "ft_bar_config": {
            "update_app_context": False,
            "num_colunas": 4, 
            "labels": {
                "pais": "País",
                "tamanho_pau": "Pau",
                "tamanho_bunda": "Bunda",
                "preferencia_anal": "Anal"
            },
            "columns_df": ["pais", "tamanho_pau", "tamanho_bunda", "preferencia_anal"]
        }
    }
    table.draw(
        df_filtrado, context,
        table_config, bodies.common.draw_body
    )

    df_filtrado = filter_man.apply_filters(df, context.active_filters)

if __name__ == "__main__":
    main()