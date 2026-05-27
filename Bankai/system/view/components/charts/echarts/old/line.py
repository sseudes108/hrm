import pandas as pd
import streamlit as st

import system.control.managers.hash as hash_man
from system.control.contexts import AppContext

from system.view.components.cards import card
from system.view.components.charts.echarts.logic import chart
from system.view.components.charts.echarts.logic import features

def normalize_y_axis(y_axis) -> list[str]:
    if isinstance(y_axis, list):
        return y_axis

    return [y_axis]

def process_line_data(
    df: pd.DataFrame,
    x_axis: str,
    y_axis
) -> tuple[list, dict]:
    """
    Prepara os dados para um gráfico de linha com uma ou múltiplas séries.

    Retorna:
        x_data: valores do eixo X
        series_data: dict no formato {"coluna_y": [valores]}
    """
    y_columns = normalize_y_axis(y_axis)

    line_df = df[[x_axis, *y_columns]].dropna().copy()

    x_data = line_df[x_axis].tolist()

    series_data = {
        y_col: line_df[y_col].tolist()
        for y_col in y_columns
    }

    return x_data, series_data

def build_line_series(
    series_data: dict,
    chart_config: dict,
    theme: dict
) -> list[dict]:
    chart_cfg = theme["chart"]
    echarts_cfg = chart_cfg["echarts"]
    colorscale = chart_cfg["colorscale_extended"]

    series = []

    for index, (series_name, values) in enumerate(series_data.items()):
        color = colorscale[index % len(colorscale)]

        series.append(
            {
                "name": chart_config.get("series_names", {}).get(series_name, series_name),
                "type": "line",
                "data": values,
                "smooth": chart_config.get("smooth", True),
                "symbol": chart_config.get("symbol", "circle"),
                "symbolSize": chart_config.get("symbol_size", 7),
                "showSymbol": chart_config.get("show_symbol", True),
                "lineStyle": {
                    "width": chart_config.get("line_width", 3)
                },
                "itemStyle": {
                    "color": color
                },
                "areaStyle": chart_config.get("area_style", None),
                "emphasis": {
                    "focus": "series",
                    "itemStyle": {
                        "shadowBlur": echarts_cfg["glow_blur"],
                        "shadowColor": echarts_cfg["tooltip_border"]
                    }
                }
            }
        )

    return series

def render_echarts_line(
    df: pd.DataFrame,
    chart_config: dict
):
    """
    Monta e renderiza um gráfico de linha usando ECharts.

    Responsabilidades desta função:
    - preparar os dados específicos da linha;
    - reaproveitar as opções base comuns aos gráficos ECharts;
    - adicionar eixos X/Y;
    - adicionar uma ou múltiplas séries line;
    - delegar a renderização final para chart.render().
    """
    theme = chart_config["theme"]
    custom_toolbox = chart_config["custom_toolbox"]

    options = features.build_base_echarts_options(
        theme,
        chart_config,
        custom_toolbox
    )

    x_axis = chart_config["x_axis"]
    y_axis = chart_config["y_axis"]

    x_data, series_data = process_line_data(df, x_axis, y_axis)

    chart_cfg = theme["chart"]
    typography = theme["typography"]
    colors = theme["colors"]
    echarts_cfg = chart_cfg["echarts"]

    options["grid"] = {
        "top": chart_config.get("grid_top", "12%"),
        "left": chart_config.get("grid_left", "3%"),
        "right": chart_config.get("grid_right", "4%"),
        "bottom": chart_config.get("grid_bottom", "12%"),
        "containLabel": True
    }

    options["xAxis"] = {
        "type": chart_config.get("x_type", "category"),
        "data": x_data,
        "axisLine": {
            "lineStyle": {
                "color": chart_cfg["font_color"]
            }
        },
        "axisLabel": {
            "color": chart_cfg["font_color"],
            "fontFamily": typography["font_family"]
        },
        "splitLine": {
            "show": False
        }
    }

    options["yAxis"] = {
        "type": chart_config.get("y_type", "value"),
        "axisLine": {
            "lineStyle": {
                "color": chart_cfg["font_color"]
            }
        },
        "axisLabel": {
            "color": chart_cfg["font_color"],
            "fontFamily": typography["font_family"]
        },
        "splitLine": {
            "show": True,
            "lineStyle": {
                "color": echarts_cfg.get("grid_line", colors.get("border", "#333333")),
                "type": "dashed"
            }
        }
    }

    options["series"] = build_line_series(
        series_data,
        chart_config,
        theme
    )
    chart_config["type"] = "line"
    chart.render(options, chart_config)

# Exemplo de configuração aceita por draw_line/render_echarts_line.
#
# chart_config = {
#     "app_name": "bankai",
#     "title": "Evolução de vendas",
#     "x_axis": "data",
#     "y_axis": "vendas",
#     "in_card": True,
#     "card_hover": True,
#     "height": 330,
#     "smooth": True,
#     "show_symbol": True,
#     "line_width": 3,
#     "legend_config": {
#         "orientation": "horizontal",
#         "top": "2%",
#         "left": "center",
#         "bottom": "auto",
#         "right": "auto"
#     },
#     "toolbox": {
#         "magic": ["bar", "line", "stack"],
#         "view": True,
#         "zoom": True
#     }
# }

def draw_line(chart_config: dict, df: pd.DataFrame, context:AppContext):
    """
    Desenha o gráfico de linha na página Streamlit.

    Esta função cuida da camada de apresentação:
    - gera uma chave estável para o componente;
    - injeta a chave no chart_config;
    - extrai configurações opcionais da toolbox;
    - decide se o gráfico será renderizado dentro de um card ou diretamente.
    """
    key = hash_man.get_hash_key(chart_config["app_name"], chart_config["title"])

    chart_config["key"] = key
    custom_toolbox = chart_config.get("toolbox", {})

    with st.container(key=f"line_container_{key}"):
        if chart_config.get("in_card", True):
            card.draw_card(
                chart_config["app_name"],
                chart_config["title"],
                {"hover": chart_config.get("card_hover", True)},
                render_content=lambda: render_echarts_line(
                    df,
                    chart_config,
                    custom_toolbox
                )
            )
        else:
            render_echarts_line(
                df,
                chart_config,
                custom_toolbox
            )