import pandas as pd

from system.view.components.charts.echarts.config import BaseChartConfig, SunburstSeriesConfig


def build(data: list[dict], config: BaseChartConfig, options: dict) -> dict:
    series: SunburstSeriesConfig = config.series
    options.pop("legend", None)
    options["series"] = [{
        "name": series.value_column,
        "type": "sunburst",
        "data": data,
        "radius": ["12%", "88%"],
        "sort": None,
        "label": {"color": config.theme["chart"]["families"]["hierarchy_label"]},
        "levels": [
            {},
            {},
            {},
            {"label": {"show": False}},
        ],
        "itemStyle": {"borderColor": config.theme["chart"]["families"]["hierarchy_border"], "borderWidth": 1},
    }]
    return options
