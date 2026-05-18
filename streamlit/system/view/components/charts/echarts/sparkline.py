import streamlit as st
from system.control.config import hex_to_rgba
from streamlit_echarts import st_echarts

# Remova o cache daqui. O custo de processar um loop de 3-5 itens é quase zero.
def get_series_list(series_dict, cor, colors, charts):
    color = colors[cor]
    echart = charts["echarts"]
    series_list = []
    
    for i, (name, data) in enumerate(series_dict.items()):
        
        series_item = {
            "name": name,
            "data": data,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 3,
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
                "width": 2,
                "color": color,
                "shadowColor": hex_to_rgba(color, 0.6),
                "shadowBlur": echart.get('glow_blur', 10)
            },
            "areaStyle": {
                "color": {
                    "type": "linear",
                    "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": hex_to_rgba(color, 0.9)},
                        {"offset": 1, "color": hex_to_rgba(color, 0.01)}
                    ]
                }
            }
        }
        series_list.append(series_item)
    return series_list

def _get_sparkline_fig(theme: dict, cor:str, x_data: list, series_dict: dict):
    colors = theme["colors"]
    charts = theme["chart"]
    
    # Chama a construção das séries
    series_list = get_series_list(series_dict, cor, colors, charts)
                
    fig = {
        "backgroundColor": "transparent",
        "grid": {
            "left": 40, "right": 5, "bottom": 10, "top": 10, # Corta as margens internas do gráfico
            "containLabel": False
        },
        "tooltip": {
            "trigger": "axis",
            "backgroundColor": hex_to_rgba(colors['surface'], 0.9),
            "borderColor": hex_to_rgba(colors['primary'], 0.3),
            "textStyle": {"color": colors['text']},
            "formatter": None
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "show": False,
            "data": x_data,
        },
        "yAxis": {
            "type": "value",
            "show": False,
        },
        "series": series_list
    }
    
    return fig

def draw_sparkline_chart(theme, data=None, cor="success", key=None):
    if key == None:
        st.error("Grafico sem titulo. Defina a key.")
        return

    if data == None:
        st.error("Grafico sem dados.")
        return

    # 2. Gera a configuração do ECharts (lógica pura)
    fig = _get_sparkline_fig(
        theme=theme, 
        cor=cor,
        x_data=data.get("x"), 
        series_dict=data.get("y"),
    )

    st_echarts(options=fig, height="100px", key=f"echart_{key}")