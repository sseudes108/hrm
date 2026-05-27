import pandas as pd
import streamlit as st

import system.control.managers.hash as hash_man
from system.control.contexts import AppContext
from system.view.components.cards import card

from system.view.components.charts.echarts.line import render_echarts_line

def render(df:pd.DataFrame, chart_config:dict):
    if chart_config["chart"] == "line":
        return render_echarts_line(df, chart_config)

def draw(chart_config:dict, df:pd.DataFrame, context:AppContext):
    key = hash_man.get_hash_key(chart_config["app_name"], chart_config["title"])
    chart_config["key"] = key
    with st.container(key=f"co_echart_{chart_config["chart"]}_{key}"):
        if chart_config.get("in_card", True):
            card_config = {
                "model": "echart",
                "has_title": False,
                "header":{
                    "title": "title",
                    "subtitle": "subtitle",
                },
                "hover": True,
                "key": key
            }
            clicked_value = card.draw_card(
                card_config, render_content=lambda: render(df, chart_config)
            )
        else:
            clicked_value = render(df, chart_config)