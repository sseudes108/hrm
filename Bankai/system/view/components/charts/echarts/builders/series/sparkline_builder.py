import pandas as pd

from system.view.components.charts.echarts.config.base import BaseChartConfig

def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Converte a cor HEX do seu tema para RGBA para o ECharts fazer o Fade."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"
    return hex_color

def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series = config.series
    
    # Busca a cor de aviso (warning) do seu tema, ou usa um dourado padrão
    print(config.sparkline_color)
    base_color = config.theme["colors"].get(config.sparkline_color, "#e6be88")

    # Força a cor principal do gráfico
    options["color"] = [base_color]

    # 1. Eixos Invisíveis (A Mágica do Sparkline)
    options["xAxis"] = {
        "type": "category",
        "show": False, # Esconde tudo
        "data": df[series.column_x].astype(str).tolist(),
        "boundaryGap": False
    }
    
    options["yAxis"] = {
        "type": "value",
        "show": False, # Esconde tudo
        "scale": True, # Impede que a linha cole no teto ou no chão (ajusta a escala dinamicamente)
    }

    # 2. Constrói a Série (A Linha Neon e o Fade)
    col_y = series.columns_y[0] # Sparklines geralmente têm só 1 linha
    
    options["series"] = [{
        "name": col_y,
        "type": "line",
        "smooth": True, # Curvas suaves
        "symbol": "circle", # Esconde os pontinhos da linha para ficar limpo
        
        "lineStyle": {
            "width": 3,
            "shadowBlur": 5, # Glow mais forte!
            "shadowColor": base_color,
            "shadowOffsetY": 0
        },
        
        "areaStyle": {
            "color": {
                "type": "linear",
                "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [
                    {"offset": 0, "color": hex_to_rgba(base_color, 0.5)}, # Começa com 50% de opacidade
                    {"offset": 1, "color": hex_to_rgba(base_color, 0.0)}  # Termina 100% invisível (fade out)
                ]
            }
        },
        "data": df[col_y].fillna(0).tolist()
    }]

    # 3. Grid Colado nas Bordas (Sem margens desperdiçadas)
    options["grid"] = {
        "show": False,
        "left": config.grid.left,
        "right": config.grid.right,
        "top": config.grid.top,
        "bottom": config.grid.bottom
    }

    # Limpa coisas desnecessárias que possam ter vindo do Base
    options.pop("legend", None)
    options.pop("toolbox", None)

    return options