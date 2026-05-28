from system.control.contexts import AppContext
from system.control.managers import layout as layout_man

from system.view.components.layout.header    import HeaderConfig, header
from system.view.components.layout.navigator import NavigatorConfig

import streamlit as st
import pandas as pd
from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig
from system.view.components.charts.echarts.config.series import (
    PieSeriesConfig, BarSeriesConfig
)

APP_NAME = "bankai"

def draw_header():
    st.write("")
    st.write("")
    header.draw(
        HeaderConfig(
            app_name=APP_NAME, model="slim", 
            title="bankai", subtitle="Zanpakuto Framework"
        )
    )

def draw_bar(df:pd.DataFrame, column_x:str, columns_y:list, context:AppContext):
    series  = BarSeriesConfig(column_x=column_x, columns_y=columns_y)
    toolbox = ToolboxConfig(magic=["line","bar","stack"])
    legend  = LegendConfig()
    tooltip = TooltipConfig(trigger="axis")

    config = BaseChartConfig(
        app_name = "bankai",
        model    = "bar",
        title    = "bar",
        theme    = context.theme,
        series   = series,
        toolbox  = toolbox,
        legend   = legend,
        tooltip  = tooltip,
    )

    return chart.draw(config, df)


def draw_pie(df:pd.DataFrame, column_pie:str, context:AppContext):
    series  = PieSeriesConfig(column=column_pie)
    toolbox = ToolboxConfig()
    legend  = LegendConfig(orientation="vertical", top="20%", left="85%")
    tooltip = TooltipConfig(trigger="item")

    config = BaseChartConfig(
        app_name = "bankai",
        model    = "pie",
        title    = "pie",
        theme    = context.theme,
        series   = series,
        toolbox  = toolbox,
        legend   = legend,
        tooltip  = tooltip,
    )

    return chart.draw(config, df)

from system.view.components.layout.navigator import navigator, NavigatorConfig
from system.view.components.renderers import page
from apps.dashboards.bankai import p1,p2,p3

PAGES = {1: p1, 2: p2, 3: p3}

def get_page(context: AppContext):
    return PAGES.get(context.current_page)

def main(context:AppContext):
    st.success(context.current_page)
    draw_header()
    navigator.draw(
        NavigatorConfig(
            "bankai", "tabs", ["Pagina1", "Pagina2", "Pagina3"]
        ), context
    )

    page_to_render = get_page(context)
    page.render("bankai", page_to_render, context)