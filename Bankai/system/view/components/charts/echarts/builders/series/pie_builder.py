import pandas as pd
import streamlit as st
from typing import Optional

from system.view.components.charts.echarts.config import BaseChartConfig
from system.view.components.charts.echarts.config.series import PieSeriesConfig

def build(df: pd.DataFrame, config: BaseChartConfig) -> list:
    series      = config.series         # PieSeriesConfig
    theme       = config.theme
    colors      = theme["colors"]
    typography  = theme["typography"]
    echarts_cfg = theme["chart"]["echarts"]
    borders     = theme["borders"]

    data = _process_data(df, series.column)
    if data is None:
        return []

    border_radius = int(borders["radius_md"].replace("px", ""))

    return [
        {
            "name": series.column,
            "type": "pie",
            "radius": series.radius,
            "avoidLabelOverlap": series.avoid_overlap,
            "itemStyle": {
                "borderRadius": border_radius,
                "borderColor":  colors["background"],
                "borderWidth":  borders["radius_sm"]
            },
            "label": _build_label(series, typography, colors),
            "emphasis": _build_emphasis(series, typography, colors, echarts_cfg),
            "labelLine": {"show": series.show_label_line},
            "data": data
        }
    ]


# ── Dados ──────────────────────────────────────────────────────────────────────

def _process_data(df: pd.DataFrame, column: str) -> Optional[list]:
    if column not in df.columns:
        st.error(f"PieSeriesConfig — coluna '{column}' não encontrada no DataFrame.")
        return None

    counts = df[column].value_counts().reset_index()
    # pandas moderno: colunas são [column, "count"], não ["name", "value"]
    counts.columns = ["name", "value"]

    return counts.to_dict(orient="records")


# ── Label ──────────────────────────────────────────────────────────────────────

def _build_label(config: PieSeriesConfig, typography: dict, colors: dict) -> dict:
    if config.label_formatter:
        return {
            "show":      True,
            "formatter": config.label_formatter
        }

    return {
        "show":     config.show_label,
        "position": config.label_position,
        "color":    colors["text"],
        "fontSize": typography["size_base"],
    }


# ── Emphasis ───────────────────────────────────────────────────────────────────

def _build_emphasis(
    config:     PieSeriesConfig,
    typography: dict,
    colors:     dict,
    echarts_cfg: dict
) -> dict:
    return {
        "label": {
            "show":       True,
            "fontSize":   typography["size_title"],
            "fontWeight": "bold",
            "color":      colors["text"]
        },
        "itemStyle": {
            "shadowBlur":    echarts_cfg["glow_blur"],
            "shadowOffsetX": 0,
            "shadowColor":   echarts_cfg["tooltip_border"]
        }
    }