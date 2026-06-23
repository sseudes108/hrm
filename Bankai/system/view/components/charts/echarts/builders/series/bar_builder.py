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
    
    # 1. Constrói as Barras Principais
    options["series"] = [
        _build_serie(df, col, series, echarts_cfg)
        for col in series.columns_y
    ]
    
    # 🚀 NOVIDADE 1: Constrói as Séries Secundárias (Gráfico Misto de Linha)
    if getattr(series, "secondary_lines", None):
        for sec_line in series.secondary_lines:
            if sec_line.column in df.columns:
                options["series"].append({
                    "name": getattr(sec_line, "name", sec_line.column) or sec_line.column,
                    "type": "line",
                    "smooth": getattr(sec_line, "smooth", True),
                    "data": df[sec_line.column].fillna(0).tolist(),
                    "itemStyle": {"color": sec_line.color},
                    "lineStyle": {"width": 3},
                    "symbol": "circle",
                    "symbolSize": 6
                })
    
    # 2. Constrói o Grid
    if config.grid:
        options["grid"] = {
            "show": config.grid.show,
            "left": config.grid.left,
            "right": config.grid.right,
            "bottom": config.grid.bottom,
            "top": config.grid.top,
            "containLabel": config.grid.contain_label
        }

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

def _build_axes(df: pd.DataFrame, series: BarSeriesConfig, echarts_cfg: dict) -> tuple[dict, dict]:
    axis_style = {
        "axisLine":  {"lineStyle": {"color": echarts_cfg["axis_line_color"]}},
        "axisLabel": {"color":     echarts_cfg["axis_label_color"]},
        "splitLine": {"lineStyle": {"color": echarts_cfg["split_line_color"]}}
    }

    # 🚀 PROTEÇÃO AQUI: .astype(str) antes de .tolist()
    category_axis = {
        "type": "category", 
        "data": df[series.column_x].astype(str).tolist(), 
        **axis_style
    }
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
    
    # 1. Cria a base da série apenas com o que é obrigatório e seguro
    serie_dict = {
        "name":     col_y,
        "type":     "bar",
        "emphasis": {
            "itemStyle": {
                "shadowBlur":    echarts_cfg["glow_blur"],
                "shadowOffsetX": 0,
                "shadowColor":   echarts_cfg["tooltip_border"]
            }
        },
        # .fillna(0) garante que não vai um NaN pro JavaScript
        "data": df[col_y].fillna(0).tolist() 
    }
    
    # 2. Injeta propriedades opcionais APENAS se elas tiverem valor
    if getattr(series, "bar_width", None) is not None:
        serie_dict["barWidth"] = series.bar_width
        
    if getattr(series, "border_radius", None) is not None:
        if "itemStyle" not in serie_dict:
            serie_dict["itemStyle"] = {}
        serie_dict["itemStyle"]["borderRadius"] = series.border_radius

    # 🚀 NOVIDADE 2: Injeta MarkLines (Metas Fixas ou Médias da barra)
    if getattr(series, "mark_lines", None):
        mark_data = []
        for ml in series.mark_lines:
            if getattr(ml, "value", None) is not None:
                # Se o gráfico for horizontal, a linha corta o eixo X, senão, o Y!
                axis_key = "xAxis" if series.orient == "horizontal" else "yAxis"
                mark_data.append({axis_key: ml.value, "name": ml.name, "itemStyle": {"color": ml.color}})
                
            elif getattr(ml, "calc_type", None) is not None:
                mark_data.append({"type": ml.calc_type, "name": ml.name, "itemStyle": {"color": ml.color}})

    if mark_data:
        serie_dict["markLine"] = {
            "data": mark_data,
            "lineStyle": {"type": getattr(ml, "line_style", "dashed"), "width": 2},
            "label": {
                "position": "insideEndTop",
                "formatter": "{b}: {c}",
                "distance": 5,
                
                # 🚀 REMOVE A BORDA BRANCA E PEGA A COR DO TEMA
                "color": echarts_cfg["axis_label_color"], # Usa a mesma cor dos textos do eixo
                "textBorderWidth": 0,                     # Zera o contorno (stroke)
                "textShadowBlur": 0                       # Garante que não tem sombra perdida
            }
        }

    return serie_dict