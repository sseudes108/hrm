import pandas as pd
import streamlit as st

import system.control.managers.hash as hash_man
from system.view.components.cards import card
from system.view.components.charts.echarts.logic import chart
from system.view.components.charts.echarts.logic import features

def process_data(df: pd.DataFrame, col_name: str) -> list[dict]:
    """
    Conta a frequência dos valores de uma coluna categórica e converte
    o resultado para o formato esperado por séries do tipo pie no ECharts.

    Retorno esperado:
        [
            {"name": "Categoria A", "value": 10},
            {"name": "Categoria B", "value": 5}
        ]
    """
    data_counts = df[col_name].value_counts().reset_index()
    data_counts.columns = ["name", "value"]

    return data_counts.to_dict("records")


def render_echarts_pie(
    df: pd.DataFrame,
    chart_config: dict,
    custom_toolbox: dict
):
    """
    Monta e renderiza um gráfico de rosca/pizza usando ECharts.

    Responsabilidades desta função:
    - preparar os dados específicos do pie;
    - reaproveitar as opções base comuns aos gráficos ECharts;
    - adicionar a configuração específica da série pie;
    - delegar a renderização final para chart.render().
    """
    theme = chart_config["theme"]

    # Dados específicos do gráfico de pizza/rosca.
    pie_data = process_data(df, chart_config["column"])

    # Opções comuns entre diferentes gráficos ECharts:
    # background, paleta, tooltip, legenda e toolbox.
    options = features.build_base_echarts_options(
        theme,
        chart_config,
        custom_toolbox
    )

    # Atalhos para partes do tema usadas pela configuração específica do pie.
    colors = theme["colors"]
    typography = theme["typography"]
    echarts_cfg = theme["chart"]["echarts"]

    # Série específica do gráfico pie.
    # Tudo aqui descreve comportamento visual das fatias, labels e destaque.
    options["series"] = [
        {
            "name": chart_config["column"],
            "type": "pie",
            "radius": chart_config.get("radius", ["42%", "72%"]),
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": int(theme["borders"]["radius_md"].replace("px", "")),
                "borderColor": colors["background"],
                "borderWidth": 3
            },
            "label": {
                "show": False,
                "position": "center"
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": typography["size_title"],
                    "fontWeight": "bold",
                    "color": colors["text"]
                },
                "itemStyle": {
                    "shadowBlur": echarts_cfg["glow_blur"],
                    "shadowOffsetX": 0,
                    "shadowColor": echarts_cfg["tooltip_border"]
                }
            },
            "labelLine": {
                "show": False
            },
            "data": pie_data
        }
    ]
    chart_config["type"] = "pie"
    return chart.render(options, chart_config)


# Exemplo de configuração aceita por draw_pie/render_echarts_pie.
#
# chart_config = {
#     "app_name": "bankai",
#     "title": "Título",
#     "column": "coluna",
#     "in_card": True,
#     "card_hover": True,
#     "height": 330,
#     "radius": ["42%", "72%"],
#     "legend_config": {
#         "orientation": "horizontal",
#         "top": "85%",
#         "left": "2%",
#         "bottom": "0%",
#         "right": "0%"
#     },
#     "toolbox": {
#         "magic": False,
#         "view": True
#     }
# }


def draw_pie(chart_config: dict, df: pd.DataFrame):
    """
    Desenha o gráfico pie na página Streamlit.

    Esta função cuida da camada de apresentação:
    - gera uma chave estável para o componente;
    - injeta a chave no chart_config;
    - extrai configurações opcionais da toolbox;
    - decide se o gráfico será renderizado dentro de um card ou diretamente.
    """
    key = hash_man.get_hash_key(chart_config["app_name"], chart_config["title"])

    # A chave é usada depois por chart.render para identificar o componente.
    chart_config["key"] = key

    # Configuração opcional da toolbox.
    # Se não vier nada no chart_config, usa um dict vazio.
    custom_toolbox = chart_config.get("toolbox", {})

    with st.container(key=f"pie_container_{key}"):
        if chart_config.get("in_card", True):

            # card_config = {
            #     "model": "echart_pie",
            #     "has_title": False,
            #     "header":{
            #         "title": "title",
            #         "subtitle": "subtitle",
            #     },
            #     "hover": False,
            #     "key": key
            # }
            card_config = card.get_config(
                "echart_pie", key
            )
            return card.card.draw_card(
                card_config,
                render_content=lambda: render_echarts_pie(
                    df,
                    chart_config,
                    custom_toolbox
                )
            )
        else:
            return render_echarts_pie(
                df,
                chart_config,
                custom_toolbox
            )