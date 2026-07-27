import pandas as pd
from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.series.line import LineSeriesConfig
from .common import apply_grid, axis_style, point_value, theme_color, validate_columns

def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series      = config.series
    echarts_cfg = config.theme["chart"]["echarts"]

    if not validate_columns(
        df,
        column_x=series.column_x,
        columns_y=series.columns_y,
        config_name="LineSeriesConfig",
        context=config.context,
    ):
        return options

    options["xAxis"], options["yAxis"] = _build_axes(df, series, echarts_cfg)
    
    # 1. Constrói as Linhas Principais
    options["series"] = [
        _build_serie(df, col, series, echarts_cfg, config.theme)
        for col in series.columns_y
    ]
    
    # 2. Constrói as Séries Secundárias (Linhas adicionais no Gráfico Misto)
    if getattr(series, "secondary_lines", None):
        for sec_line in series.secondary_lines:
            if sec_line.column in df.columns:
                options["series"].append({
                    "name": getattr(sec_line, "name", sec_line.column) or sec_line.column,
                    "type": "line",
                    "smooth": getattr(sec_line, "smooth", True),
                    "data": [
                        point_value(row[sec_line.column] if pd.notna(row[sec_line.column]) else 0, row)
                        for _, row in df.iterrows()
                    ],
                    "itemStyle": {"color": _secondary_line_color(sec_line, config.theme)},
                    "lineStyle": {"width": 2, "type": "dashed"}, # Geralmente secundárias são tracejadas
                    "symbol": "circle",
                    "symbolSize": 5
                })
    
    # 3. Constrói o Grid
    apply_grid(options, config.grid)

    return options


# ── Eixos ──────────────────────────────────────────────────────────────────────

def _build_axes(df: pd.DataFrame, series: LineSeriesConfig, echarts_cfg: dict) -> tuple[dict, dict]:
    style = axis_style(echarts_cfg)

    # Proteção: converte o eixo X para string
    category_axis = {
        "type": "category", 
        "data": df[series.column_x].astype(str).tolist(), 
        "boundaryGap": True, # 🚀 Diferença da barra: as linhas começam coladas na borda
        "axisTick": {"alignWithLabel": True},
        **style
    }
    value_axis = {"type": "value", **style}

    if getattr(series, "orient", "horizontal") == "horizontal":
        return category_axis, value_axis
    else:
        return value_axis, category_axis


# ── Série Principal ────────────────────────────────────────────────────────────

def _build_serie(
    df:         pd.DataFrame,
    col_y:      str,
    series:     LineSeriesConfig,
    echarts_cfg: dict,
    theme: dict,
) -> dict:
    
    # Base da série de Linha
    serie_dict = {
        "name":     col_y,
        "type":     "line",
        "smooth":   series.smooth,
        "symbol":   series.symbol,
        "symbolSize": series.symbol_size,
        "lineStyle": {
            "width": series.line_width,
            "shadowBlur": echarts_cfg.get("glow_blur", 0),
            "shadowColor": echarts_cfg.get("tooltip_border", "transparent"),
            "shadowOffsetY": 2
        },
        "data": [point_value(row[col_y] if pd.notna(row[col_y]) else 0, row) for _, row in df.iterrows()]
    }

    if series.step:
        serie_dict["step"] = series.step
    
    # Efeito de preenchimento (Gráfico de Área)
    if series.fill_area:
        serie_dict["areaStyle"] = {
            "opacity": 0.2 # Preenchimento translúcido elegante
        }

    # Injeta MarkLines (Metas Fixas ou Médias) igual nas Barras
    if getattr(series, "mark_lines", None):
        mark_data = []
        for ml in series.mark_lines:
            if getattr(ml, "value", None) is not None:
                axis_key = "xAxis" if getattr(series, "orient", "horizontal") == "vertical" else "yAxis"
                mark_data.append({"value": ml.value, axis_key: ml.value, "name": ml.name, "itemStyle": {"color": _mark_line_color(ml, theme)}})
            elif getattr(ml, "calc_type", None) is not None:
                mark_data.append({"type": ml.calc_type, "name": ml.name, "itemStyle": {"color": _mark_line_color(ml, theme)}})

        if mark_data:
            ml_style = series.mark_lines[0]
            serie_dict["markLine"] = {
                "data": mark_data,
                "lineStyle": {"type": getattr(ml_style, "line_style", "dashed"), "width": 2},
                "label": {
                    "position": "insideEndTop",
                    "formatter": "{b}: {c}",
                    "distance": 5,
                    "color": echarts_cfg["axis_label_color"]
                }
            }

    return serie_dict


def _secondary_line_color(config, theme: dict) -> str:
    return theme_color(config, theme)


def _mark_line_color(config, theme: dict) -> str:
    return theme_color(config, theme)
