from system.control.contexts import AppContext
from system.control.managers import layout as layout_man

from system.view.components.layout.header    import HeaderConfig, header
# from system.view.components.layout.navigator import NavigatorConfig

import streamlit as st
import pandas as pd
from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig
from system.view.components.charts.echarts.config.series.pie import PieSeriesConfig
from system.view.components.layout.navigator.old import navigator

APP_NAME = "lakshmi"

def draw_header():
    header.draw(
        HeaderConfig(
            app_name=APP_NAME, model="slim", 
            title="lakshmi", subtitle="goddess of prosperity"
        )
    )

# def draw_navigator():
#     return navigator.draw(
#         NavigatorConfig(
#             app_name=APP_NAME, model="in_header",
#             nav_pages = [
#                 "Adi",
#                 "Dhana",
#                 "Vidya",
#                 "Veera",
#                 "Gaja",
#                 "Santana",
#                 "Dhanya",
#                 "Vijaya"
#             ]
#         )
#     )

def draw_pie(df:pd.DataFrame, column_pie:str, context:AppContext):
    # 1. Monta as subconfigs desejadas (todos têm padrões, só sobrescreve o que precisa)
    series  = PieSeriesConfig(column=column_pie)
    toolbox = ToolboxConfig()
    legend  = LegendConfig(orientation="vertical", top="20%", left="85%")
    tooltip = TooltipConfig(trigger="item")

    # 2. Monta a config principal
    config = BaseChartConfig(
        app_name = "lakshmi",
        model    = "pie",
        title    = "default",
        theme    = context.theme,
        series   = series,
        toolbox  = toolbox,
        legend   = legend,
        tooltip  = tooltip,
    )

    # 3. Renderiza
    return chart.draw(config, df)

def main(context:AppContext):
    layout_man.set_bg("apps/engines/lakshmi/layout/bg-palacio.png")
    draw_header()

    df = pd.DataFrame({
        "categoria": ["A", "B", "C", "A", "B", "A"],
        "valor":     [10, 20, 30, 15, 25, 5]
    })
    clicked = draw_pie(df, "categoria", context)

    st.success(clicked)

if __name__ == "__main__":
    main()