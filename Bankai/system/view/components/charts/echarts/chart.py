import streamlit as st
from typing import Any
import system.core.managers.config.hash as hash_man
from system.view.components.cards import card
from system.core.log.view import warnings
from streamlit_echarts import st_echarts

from system.view.components.charts.echarts.config import BaseChartConfig
from system.view.components.charts.echarts.builders import base_builder
from system.view.components.charts.echarts.builders.series import (
    pie_builder,
    bar_builder,
    line_builder,
    sparkline_builder,
    scatter_builder,
    radar_builder,
    boxplot_builder,
    heatmap_builder,
    sunburst_builder,
    nightingale_builder,
)
from typing import Optional

_SERIES_BUILDERS = {
    "pie":  pie_builder.build,
    "bar":  bar_builder.build,
    "line": line_builder.build,
    "sparkline": sparkline_builder.build,
    "scatter": scatter_builder.build,
    "radar": radar_builder.build,
    "boxplot": boxplot_builder.build,
    "heatmap": heatmap_builder.build,
    "sunburst": sunburst_builder.build,
    "nightingale": nightingale_builder.build,
}

def draw(chart_config: Optional[BaseChartConfig], df: Any, context) -> Any:
    if chart_config is None:
        return

    identity = chart_config.chart_id or (
        f"{chart_config.model}:{chart_config.title}:"
        f"{getattr(chart_config.series, 'column_x', '')}:"
        f"{getattr(chart_config.series, 'column', '')}:"
        f"{','.join(getattr(chart_config.series, 'columns_y', ()))}"
    )
    key = hash_man.get_hash(f"{chart_config.app_name}:{identity}")

    return  card.draw(
        card.CardConfig(
            card_id=(
                f"{chart_config.app_name}_{chart_config.model}_"
                f"{chart_config.chart_id or chart_config.title}"
            ),
            model="chart", has_title=chart_config.has_card_title, context=context,
            title=chart_config.title, subtitle=chart_config.subtitle,
            hover=chart_config.card_hover, show_card=chart_config.show_card,
            variant=chart_config.card_variant,
            padding=chart_config.card_padding,
            title_case=chart_config.card_title_case,
            title_align=chart_config.card_title_align,
        ), card.CardRenderConfig(
            content=lambda: _render(
                chart_config, df, key
            )
        )
    )

def _render(chart_config: BaseChartConfig, df: Any, key: str) -> Any:
    builder_fn = _SERIES_BUILDERS.get(chart_config.model)
    if builder_fn is None:
        warnings.draw(
            f"Builder não implementado para model='{chart_config.model}'",
            alert="error",
            context=chart_config.context,
        )
        return

    # Monta base (tooltip, legend, toolbox, backgroundColor…)
    options = base_builder.build(chart_config)
    options = builder_fn(df, chart_config, options)    # ← recebe e devolve options

    echarts_events = {
        "click": "function(params) { return { name: params.name, value: params.value, data: params.data, seriesName: params.seriesName, componentType: params.componentType, ts: Date.now() }; }"
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
