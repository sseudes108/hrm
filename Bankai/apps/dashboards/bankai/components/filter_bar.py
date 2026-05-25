import pandas as pd
import streamlit as st
from system.control.contexts import AppContext
import system.view.components.filters.select as select_filter
from system.view.components.cards import draw_card

def get_options_config(df:pd.DataFrame, label:str, column:str):
    options = {
        "df": df,
        "label": label.upper(),
        "column": column
    }
    config = {
        "id": f"ft_sel_{label.lower()}_bankai",
        "has_card": True, 
        "allow_all": True,
        "update_app_context": True,
    }
    return options, config

def draw_filters(df:pd.DataFrame, context:AppContext):
    st.info("sidebar")
    # title, status, rating, popularity, year, genres, themes, demografic
    selects = {}

    ###########################################################
    options,config = get_options_config(df, "title", "title")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["title"] = title_selected

    ###########################################################
    options,config = get_options_config(df, "status", "status")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["status"] = title_selected

    ###########################################################
    options,config = get_options_config(df, "rating", "rating")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["rating"] = title_selected

    ###########################################################
    options,config = get_options_config(df, "popularity", "popularity")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["popularity"] = title_selected
    
    ###########################################################
    options,config = get_options_config(df, "year", "year")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["year"] = title_selected

    ###########################################################
    options,config = get_options_config(df, "genres", "genres")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["genres"] = title_selected

    ###########################################################
    options,config = get_options_config(df, "themes", "themes")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["themes"] = title_selected

    ###########################################################
    options,config = get_options_config(df, "demographics", "demographics")
    title_selected = select_filter.draw_filter(
        options=options, context=context,
        config=config
    )
    selects["demographics"] = title_selected


def draw_filters_bar(df:pd.DataFrame, context:AppContext):
    card_config = {
        "hover": False
    }
    ft_bar_args = {
        "df":df,
        "context": context
    }
    draw_card(
        "bankai", "filter_bar",
        card_config, render_content=draw_filters,
        **ft_bar_args
    )