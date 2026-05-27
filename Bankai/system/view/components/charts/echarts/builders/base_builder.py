from system.view.components.charts.echarts.config import BaseChartConfig, ToolboxConfig


DEFAULT_TOOLBOX = {
    "save":    True,
    "restore": True,
    "view":    False,
    "zoom":    False,
    "magic":   ["line", "bar"]
}


def build(config: BaseChartConfig) -> dict:
    ty          = config.theme["typography"]
    chart_cfg   = config.theme["chart"]
    echarts_cfg = chart_cfg["echarts"]

    return {
        "backgroundColor": "transparent",
        "color":           chart_cfg["colorscale_extended"],
        "toolbox":         _build_toolbox(config.toolbox, chart_cfg),
        "tooltip":         _build_tooltip(config, echarts_cfg, ty),
        "legend":          _build_legend(config, chart_cfg, ty),
    }


# ── Toolbox ────────────────────────────────────────────────────────────────────

def _build_toolbox(toolbox: ToolboxConfig, chart_cfg: dict) -> dict:
    layout = {"orient": toolbox.orient}

    if toolbox.top    is not None: layout["top"]    = toolbox.top
    if toolbox.right  is not None: layout["right"]  = toolbox.right
    if toolbox.bottom is not None: layout["bottom"] = toolbox.bottom
    if toolbox.left   is not None: layout["left"]   = toolbox.left

    return {
        "show": True,
        "feature": _assemble_features(toolbox),
        "iconStyle": {"borderColor": chart_cfg["font_color"]},
        **layout
    }

def _assemble_features(toolbox: ToolboxConfig) -> dict:
    features = {}

    if toolbox.save:
        features["saveAsImage"] = {"show": True}
    if toolbox.view:
        features["dataView"] = {"show": True, "readOnly": False}
    if toolbox.zoom:
        features["dataZoom"] = {"show": True, "type": toolbox.zoom}
    if toolbox.magic:
        features["magicType"] = {"show": True, "type": toolbox.magic}
    if toolbox.restore:
        features["restore"] = {"show": True}

    return features


# ── Tooltip ────────────────────────────────────────────────────────────────────

def _build_tooltip(config: BaseChartConfig, echarts_cfg: dict, ty: dict) -> dict:
    tooltip = {
        "trigger":         config.tooltip.trigger,
        "backgroundColor": echarts_cfg["tooltip_bg"],
        "borderColor":     echarts_cfg["tooltip_border"],
        "borderWidth":     1,
        "textStyle": {
            "color":      echarts_cfg["tooltip_text"],
            "fontFamily": ty["font_family"],
            "fontSize":   ty["size_base"]
        }
    }

    if config.tooltip.formatter is not None:
        tooltip["formatter"] = config.tooltip.formatter

    return tooltip


# ── Legend ─────────────────────────────────────────────────────────────────────

LEGEND_DEFAULTS = {
    "orientation": "vertical",
    "top":         "85%",
    "left":        "2%",
    "bottom":      "10%",
    "right":       "0%",
}

def _build_legend(config: BaseChartConfig, chart_cfg: dict, ty: dict) -> dict:
    lg = config.legend

    legend_dict = {
        "orient": lg.orientation,
        "top":    lg.top,
        "left":   lg.left,
        "bottom": lg.bottom,
        "right":  lg.right,
        "textStyle": {
            "color":      chart_cfg["font_color"],
            "fontFamily": ty["font_family"]
        }
    }
    return legend_dict