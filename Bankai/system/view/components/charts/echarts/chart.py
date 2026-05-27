import streamlit as st
from streamlit_echarts import st_echarts
import system.control.managers.hash as hash_man
from system.view.components.cards import card, CardConfig

from system.view.components.charts.echarts.config   import BaseChartConfig
from system.view.components.charts.echarts.builders import base_builder
from system.view.components.charts.echarts.builders.series import (
    pie_builder,
    # bar_builder,
    # line_builder,
)
from typing import Optional

_SERIES_BUILDERS = {
    "pie":  pie_builder.build,
    # "bar":  bar_builder.build,
    # "line": line_builder.build,
}

def draw(chart_config: Optional[BaseChartConfig], df) -> None:
    if chart_config is None:
        return

    key = hash_man.get_hash_key(chart_config.app_name, chart_config.title)

    with st.container(key=f"{chart_config.model}_container_{key}"):
        if chart_config.in_card:
            card_config = CardConfig(
                model="chart", key=key
            )
            return card.draw_card(
                card_config,
                render_content=lambda: _render(chart_config, df, key)
            )
        else:
            return _render(chart_config, df, key)


def _render(chart_config: BaseChartConfig, df, key: str) -> None:
    builder_fn = _SERIES_BUILDERS.get(chart_config.model)
    if builder_fn is None:
        st.error(f"Builder não implementado para model='{chart_config.model}'")
        return

    # Monta base (tooltip, legend, toolbox, backgroundColor…)
    options = base_builder.build(chart_config)

    # Delega a série para o builder específico
    options["series"] = builder_fn(df, chart_config)

    echarts_events = {
        "click": "function(params) { return { name: params.name, ts: Date.now() }; }"
    }
    clicked_value = st_echarts(
        options=options,
        events=echarts_events,
        renderer="canvas",
        theme=None,
        width=chart_config.width,
        height=chart_config.height,
        key=f"{chart_config.model}_{key}",
    )
    return clicked_value