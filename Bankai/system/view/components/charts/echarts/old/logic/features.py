DEFAULT_TOOLBOX = {
    "save": True,
    "restore": True,
    "view": False,
    "zoom": False,
    "magic": ["line", "bar"]
}

def _assemble_features(custom_toolbox: dict):
    # 2.5 MESCLAR E MONTAR O TOOLBOX
    if custom_toolbox is None:
        custom_toolbox = {}
        
    # Cria uma cópia do padrão para não alterar a constante global
    tb_config = DEFAULT_TOOLBOX.copy()
    # Atualiza a cópia com os valores customizados
    tb_config.update(custom_toolbox)

    # Traduz para o padrão de leitura do ECharts
    echarts_features = {}
    if tb_config.get("save"): 
        echarts_features["saveAsImage"] = {"show": True}
    if tb_config.get("view"): 
        echarts_features["dataView"] = {"show": True, "readOnly": False}
    if tb_config.get("zoom"): 
        echarts_features["dataZoom"] = {"show": True, "type": tb_config["zoom"]}
    if tb_config.get("magic"): 
        echarts_features["magicType"] = {"show": True, "type": tb_config["magic"]}
    if tb_config.get("restore"): 
        echarts_features["restore"] = {"show": True}
        
    return echarts_features

def build_base_echarts_options(theme: dict, chart_config: dict, custom_toolbox: dict):
    ty = theme["typography"]
    chart_cfg = theme["chart"]
    echarts_cfg = chart_cfg["echarts"]

    return {
        "backgroundColor": "transparent",
        "color": chart_cfg["colorscale_extended"],
        "toolbox": {
            "show": True,
            "feature": _assemble_features(custom_toolbox),
            "iconStyle": {
                "borderColor": chart_cfg["font_color"]
            }
        },
        "tooltip": {
            "trigger": chart_config.get("tooltip_trigger", "item"),
            "backgroundColor": echarts_cfg["tooltip_bg"],
            "borderColor": echarts_cfg["tooltip_border"],
            "borderWidth": 1,
            "textStyle": {
                "color": echarts_cfg["tooltip_text"],
                "fontFamily": ty["font_family"],
                "fontSize": ty["size_base"]
            }
        },
        "legend": {
            "orient": chart_config.get("legend_config", {}).get("orientation", "vertical"),
            "top": chart_config.get("legend_config", {}).get("top", "85%"),
            "left": chart_config.get("legend_config", {}).get("left", "2%"),
            "bottom": chart_config.get("legend_config", {}).get("bottom", "10%"),
            "right": chart_config.get("legend_config", {}).get("right", "0%"),
            "textStyle": {
                "color": chart_cfg["font_color"],
                "fontFamily": ty["font_family"]
            }
        }
    }