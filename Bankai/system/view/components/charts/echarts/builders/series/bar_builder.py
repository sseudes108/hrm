import pandas as pd
import streamlit as st

from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.series.bar import BarSeriesConfig


def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series      = config.series
    echarts_cfg = config.theme["chart"]["echarts"]

    if not _validate(df, series):
        return options

    options["xAxis"], options["yAxis"] = _build_axes(df, series, echarts_cfg)
    options["series"] = [
        _build_serie(df, col, series, echarts_cfg)
        for col in series.columns_y
    ]

    return options


# ── Validação ──────────────────────────────────────────────────────────────────

def _validate(df: pd.DataFrame, series: BarSeriesConfig) -> bool:
    missing = [
        col for col in [series.column_x, *series.columns_y]
        if col not in df.columns
    ]
    if missing:
        st.error(f"BarSeriesConfig — colunas não encontradas: {missing}")
        return False
    return True


# ── Eixos ──────────────────────────────────────────────────────────────────────

def _build_axes(
    df:         pd.DataFrame,
    series:     BarSeriesConfig,
    echarts_cfg: dict
) -> tuple[dict, dict]:
    axis_style = {
        "axisLine":  {"lineStyle": {"color": echarts_cfg["axis_line_color"]}},
        "axisLabel": {"color":     echarts_cfg["axis_label_color"]},
        "splitLine": {"lineStyle": {"color": echarts_cfg["split_line_color"]}}
    }

    category_axis = {"type": "category", "data": df[series.column_x].tolist(), **axis_style}
    value_axis    = {"type": "value", **axis_style}

    if series.orient == "horizontal":
        return value_axis, category_axis
    else:
        return category_axis, value_axis


# ── Série ──────────────────────────────────────────────────────────────────────

def _build_serie(
    df:         pd.DataFrame,
    col_y:      str,
    series:     BarSeriesConfig,
    echarts_cfg: dict
) -> dict:
    return {
        "name":     col_y,
        "type":     "bar",
        "barWidth": series.bar_width,
        "itemStyle": {
            "borderRadius": series.border_radius
        },
        "emphasis": {
            "itemStyle": {
                "shadowBlur":    echarts_cfg["glow_blur"],
                "shadowOffsetX": 0,
                "shadowColor":   echarts_cfg["tooltip_border"]
            }
        },
        "data": df[col_y].tolist()
    }