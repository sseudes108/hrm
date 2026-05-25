import pandas as pd
import streamlit as st
from system.control.contexts.app import AppContext
from system.view.components.filters.select import draw_filter

from apps.engines.shebattle.logic import filters
from system.view.components.cards import draw_card

def draw_pais_filter(options:dict, context:AppContext, config:dict):
    return draw_filter(options, context, config)

def draw_tam_pau_filter(options:dict, context:AppContext, config:dict):
    return draw_filter(options, context, config)

def draw_tam_bunda_filter(options:dict, context:AppContext, config:dict):
    return draw_filter(options, context, config)

def draw_filter_bar(df_filtrado:pd.DataFrame, context:AppContext, config:dict):
    gap = 'xsmall' if config["has_card"] == False else 'xxsmall'
    cols = st.columns(3, gap=gap)
    selects = {}
    options = {
        "df": df_filtrado
    }

    with st.container():
        with cols[0]:
            options["label"] = "PAU"
            options["column"] = "tamanho_pau"
            pau_selected = filters.draw_tam_pau_filter(
                options,context, config
            )
        with cols[1]:
            options["label"] = "BUNDA"
            options["column"] = "tamanho_bunda"
            bunda_selected = filters.draw_tam_bunda_filter(
                options,context, config
            )
        with cols[2]:
            options["label"] = "PAÍS"
            options["column"] = "pais"
            pais_selected = filters.draw_pais_filter(
                options,context, config
            )
    
    selects["pau"] = pau_selected
    selects["bunda"] = bunda_selected
    selects["pais"] = pais_selected

    return selects

def draw_filter_bar_card(df_filtrado:pd.DataFrame, context:AppContext, config:dict):
    filter_bar_args = {
        "df_filtrado":df_filtrado,
        "context":context,
        'config':config,
    }
    selects = draw_card(
        "shebattle", "filters_bar_card",
        filters.draw_filter_bar,
        **filter_bar_args
    )

    return selects