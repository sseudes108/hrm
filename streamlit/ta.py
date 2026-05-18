from streamlit_echarts import st_echarts

def draw_matrix_table():
    # Para o Heatmap, o ECharts prefere [x, y, valor]
    # Vamos passar os dados extras como dimensões extras
    # [coluna, linha, total, sla, delta]
    data = [
        [0, 0, 150, 98, 5],   # CRM - Segunda
        [1, 0, 180, 95, -2],  # CRM - Terça
        [0, 1, 89, 92, 10],   # ERP - Segunda
    ]

    options = {
        "backgroundColor": "transparent",
        "tooltip": {"position": "top"},
        "grid": {"top": "10%", "bottom": "15%"},
        "xAxis": {"type": "category", "data": ["Segunda", "Terça", "Quarta"]},
        "yAxis": {"type": "category", "data": ["CRM", "ERP", "Chatbot"]},
        "series": [{
            "type": "heatmap",
            "data": data,
            "label": {
                "show": True,
                # Usamos a sintaxe de string do Python com quebra de linha real
                "formatter": (
                    "{title|Σ {@[2]}}\n"      # @[2] é o 3º item da lista (total)
                    "{hr|}\n"                 # Linha separadora
                    "{sub|SLA: {@[3]}%  }{delta|{@[4]}%}" # @[3]=sla, @[4]=delta
                ),
                "rich": {
                    "title": {
                        "color": "#fff",
                        "fontWeight": "bold",
                        "fontSize": 14,
                        "padding": [5, 0]
                    },
                    "hr": {
                        "borderColor": "rgba(255,255,255,0.2)",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                        "lineHeight": 10
                    },
                    "sub": {
                        "color": "rgba(255,255,255,0.5)",
                        "fontSize": 11
                    },
                    "delta": {
                        "color": "#00ff00",
                        "fontSize": 11,
                        "fontWeight": "bold"
                    }
                }
            },
            "itemStyle": {
                "color": "rgba(255, 255, 255, 0.05)",
                "borderColor": "rgba(255, 255, 255, 0.1)",
                "borderWidth": 1
            }
        }]
    }

    st_echarts(options=options, height="400px")