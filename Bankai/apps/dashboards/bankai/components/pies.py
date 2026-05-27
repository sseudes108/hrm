import pandas as pd
import streamlit as st
from system.control.contexts import AppContext
from system.view.components.charts.echarts import pie
from system.view.components.cards import card

def draw_pie(df:pd.DataFrame, context:AppContext):
    cols = st.columns([1,2])

    with cols[0]:
        card_config = {
            "hover": False
        }
        chart_config = {
            "title": "RATING",
            "column": "rating",
            "height": 400,
            "legend_config":{
                "orientation": "horizontal",
                "top": "80%", "left": "2%", "bottom": "0%", "right": "0%"
            },
            "toolbox": {
                "magic": False,
                "view": True,
            }
        }
        card.draw_card(
            "bankai", "pie_rating_chart",
            card_config,
            render_content=lambda: pie.draw_pie(chart_config, df, context)
        )

        card_config = {
            "hover": True
        }
        chart_config = {
            "title": "STATUS",
            "column": "status",
            "height": 270,
            "radius": ["55%", "72%"],
            "legend_config":{
                "orientation": "vertical",
                "top": "0%", "left": "2%", "bottom": "0%", "right": "0%"
            },
            "toolbox": {
                "magic": False, 
                "view": False
            }
        }
        card.draw_card(
            "bankai", "pie_status_chart",
            card_config,
            render_content=lambda: pie.draw_pie(chart_config, df, context)
        )
    with cols[1]:
        pass