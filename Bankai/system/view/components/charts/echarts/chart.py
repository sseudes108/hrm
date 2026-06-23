import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import system.core.managers.config.hash as hash_man
from system.view.components.cards import card

from system.view.components.charts.echarts.config import BaseChartConfig
from system.view.components.charts.echarts.builders import base_builder
from system.view.components.charts.echarts.builders.series import (
    pie_builder,
    bar_builder,
    line_builder,
    sparkline_builder
)
from typing import Optional

_SERIES_BUILDERS = {
    "pie":  pie_builder.build,
    "bar":  bar_builder.build,
    "line": line_builder.build,
    "sparkline": sparkline_builder.build,
}

def draw(chart_config: Optional[BaseChartConfig], df:pd.DataFrame, context) -> None:
    if chart_config is None:
        return

    key = hash_man.get_hash(chart_config.title)

    return  card.draw(
        card.CardConfig(
            card_id=f"{chart_config.app_name}_{chart_config.model}_{chart_config.title}",
            model="chart", has_title=chart_config.has_card_title, context=context,
            title=chart_config.title.upper(), subtitle=chart_config.subtitle.upper(), 
            hover=chart_config.card_hover, show_card=chart_config.show_card
        ), card.CardRenderConfig(
            content=lambda: _render(
                chart_config, df, key
            )
        )
    )

def _render(chart_config: BaseChartConfig, df:pd.DataFrame, key: str) -> None:
    builder_fn = _SERIES_BUILDERS.get(chart_config.model)
    if builder_fn is None:
        st.error(f"Builder não implementado para model='{chart_config.model}'")
        return

    # Monta base (tooltip, legend, toolbox, backgroundColor…)
    options = base_builder.build(chart_config)
    options = builder_fn(df, chart_config, options)    # ← recebe e devolve options

    echarts_events = {
        "click": "function(params) { return { name: params.name, ts: Date.now() }; }"
    }
   
    clicked_value = st_echarts(
        options=options,
        events=echarts_events,
        renderer="svg",
        theme=None,
        width=chart_config.width,
        height=chart_config.height,
        key=f"{chart_config.model}_{key}",
    )
    return clicked_value