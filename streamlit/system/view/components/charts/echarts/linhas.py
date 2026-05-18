import streamlit as st
from system.control.config import hex_to_rgba
from system.view.components.cards.chart import chart_card

DEFAULT_TOOLBOX = {
    "save": True,
    "restore": True,
    "view": True,
    "zoom": True,
    "magic": ["line", "bar"]
}

# Remova o cache daqui. O custo de processar um loop de 3-5 itens é quase zero.
def get_series_list(series_dict, colors, charts):
    colorscale = charts["colorscale"]
    echart = charts["echarts"]
    series_list = []
    
    for i, (name, data) in enumerate(series_dict.items()):
        color = colorscale[i % len(colorscale)]        
        if isinstance(color, dict):
            color = list(color.values())[0]
        
        series_item = {
            "name": name,
            "data": data,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 10,
            "itemStyle": {
                "color": color,
                "borderColor": color,
                "borderWidth": 3,
                "shadowBlur": echart.get('glow_blur', 10),
                "shadowColor": color
            },
            "emphasis": {
                "itemStyle": {
                    "color": color,
                    "borderWidth": 2,
                    "borderColor": colors['text']
                }
            },
            "lineStyle": {
                "width": 4,
                "color": color,
                "shadowColor": hex_to_rgba(color, 0.6),
                "shadowBlur": echart.get('glow_blur', 10)
            },
            "areaStyle": {
                "color": {
                    "type": "linear",
                    "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": hex_to_rgba(color, 0.4)},
                        {"offset": 1, "color": "rgba(0, 0, 0, 0)"}
                    ]
                }
            }
        }
        series_list.append(series_item)
    return series_list

def _get_fig(theme: dict, x_data: list, series_dict: dict, toolbox_config: dict = None):
    colors = theme["colors"]
    charts = theme["chart"]
    
    grid_color = charts["grid_color"]
    label_color = charts["font_color"]

    # Chama a construção das séries
    series_list = get_series_list(series_dict, colors, charts)
    
    config = DEFAULT_TOOLBOX.copy()
    if toolbox_config:
        config.update(toolbox_config)

    feature = {}
    
    if config.get("save"):
        feature["saveAsImage"] = {
            "show": True, "title": "PNG", "type": "png", "pixelRatio": 2,
            "backgroundColor": colors["background"]
        }
    
    if config.get("view"):
        feature["dataView"] = {"show": True, "title": "Dados", "lang": ["Dados", "Fechar", "Atualizar"]}
        
    if config.get("restore"):
        feature["restore"] = {"show": True, "title": "Resetar"}

    if config.get("zoom"):
        feature["dataZoom"] = {"show": True, "title": "Zoom"}
        
    # O Pulo do Gato: MagicType dinâmico
    magic_types = config.get("magic", [])
    if magic_types:
        feature["magicType"] = {
            "show": True,
            "title": {"line": "Linha", "bar": "Barra", "stack": "Empilhar", "tiled": "Lado a Lado"},
            "type": magic_types
        }

    fig = {
        "backgroundColor": "transparent",
        "toolbox": {
            "show": True,
            "orient": "vertical",
            "right": "0%",
            "top": "-3%",
            "feature": feature,
            "iconStyle": {"borderColor": colors['text']}
        },
        "tooltip": {
            "trigger": "axis",
            "backgroundColor": hex_to_rgba(colors['surface_2'], 0.9),
            "borderColor": hex_to_rgba(colors['primary'], 0.3),
            "textStyle": {"color": colors['text']},
            "formatter": None
        },
        "legend": {
            "textStyle": {"color": label_color},
            "bottom": "0%"
        },
        "grid": {
            "left": "3%", "right": "8%", "bottom": "12%", "top": "5%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False, # Faz a linha encostar nos cantos (estética Bankai)
            "data": x_data,
            "axisLine": {"lineStyle": {"color": grid_color}},
            "axisLabel": {"color": label_color}
        },
        "yAxis": {
            "type": "value",
            "splitLine": {"lineStyle": {"color": grid_color}},
            "axisLabel": {"color": label_color}
        },
        "series": series_list
    }
    
    return fig

def draw_linhas_chart(theme, data: dict, title=None, subtitle=None, value=None, value_sub=None, key=None):
    if title == None and key == None:
        st.error("Grafico sem titulo. Defina a key.")
        return

    toolbox_config = data.get("toolbox")

    # 2. Gera a configuração do ECharts (lógica pura)
    fig = _get_fig(
        theme=theme, 
        x_data=data.get("x"), 
        series_dict=data.get("y"),
        toolbox_config=toolbox_config
    )

    # 3. Manda para o layout master
    chart_card(
        theme=theme,
        fig=fig, 
        title=title, 
        subtitle=subtitle, 
        value=value,
        value_sub=value_sub,
        key=key,
    )