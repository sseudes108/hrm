import pandas as pd
import streamlit as st
from typing import Optional

from system.view.components.charts.echarts.config import BaseChartConfig
from system.view.components.charts.echarts.config.series import PieSeriesConfig

def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
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

    options["series"] = [
        {
            "name": series.column,
            "type": "pie",
            "center": series.center,
            "radius": series.radius,
            "avoidLabelOverlap": series.avoid_overlap,
            "itemStyle": {
                "borderRadius": border_radius,
                "borderColor":  colors["background"],
                "borderWidth":  borders["radius_md"]
            },
            "label": _build_label(series, typography, colors),
            "emphasis": _build_emphasis(series, typography, colors, echarts_cfg),
            "labelLine": {"show": series.show_label_line},
            "data": data
        }
    ]
    return options


# ── Dados ──────────────────────────────────────────────────────────────────────

def _process_data(df: pd.DataFrame, column: str) -> Optional[list]:
    # Agora validamos se as duas colunas esperadas vieram do pie_man
    if column not in df.columns or "value" not in df.columns:
        st.error(f"PieSeriesConfig — colunas '{column}' ou 'value' não encontradas. O Gerenciador agrupou corretamente?")
        return None

    # O pie_man já fez o agrupamento pesado. 
    # Só precisamos renomear a coluna de categoria para "name" para agradar o ECharts
    df_echarts = df[[column, "value"]].copy()
    df_echarts.rename(columns={column: "name"}, inplace=True)

    return df_echarts.to_dict(orient="records")

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