import streamlit as st
import pandas as pd

from system.control.contexts import AppContext
from system.control.managers import layout as layout_man

from system.view.components.renderers import page
from system.view.components.layout.header    import HeaderConfig, header

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig
from system.view.components.charts.echarts.config.series.pie import PieSeriesConfig

from apps.engines.lakshmi.pages import (
    adi
)

APP_NAME = "lakshmi"
PAGES = {
    1: adi, 
}

def get_page(context: AppContext):
    return PAGES.get(context.current_page)

def draw_header(context:AppContext):
    header.draw(
        title="lakshmi",  subtitle="goddess of prosperity",
        model="nav",
        nav_pages=[
            "Adi",
            "Dhana",
            "Vidya",
            "Veera",
            "Gaja",
            "Santana",
            "Dhanya",
            "Vijaya"
        ], context=context
    )

def main(context:AppContext):
    # layout_man.set_bg("apps/engines/lakshmi/layout/bg-palacio.png")
    if context.mode == "dark":
        layout_man.set_bg("apps/engines/lakshmi/layout/bg-dark.png")
    else:
        layout_man.set_bg("apps/engines/lakshmi/layout/bg-light.png")

    draw_header(context)

    page_to_render = get_page(context)
    page.render(page_to_render, context)

if __name__ == "__main__":
    main()