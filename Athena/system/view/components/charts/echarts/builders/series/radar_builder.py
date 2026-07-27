import pandas as pd

from system.view.components.charts.echarts.config import BaseChartConfig, RadarSeriesConfig
from system.core.managers.charts.payload import point_filter_metadata


def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series: RadarSeriesConfig = config.series
    colors = config.theme["colors"]
    indicators = [
        {"name": column, "max": series.max_values[column]}
        for column in series.indicator_columns
    ]
    options["radar"] = {
        "indicator": indicators,
        "axisName": {"color": config.theme["chart"]["font_color"]},
        "splitLine": {"lineStyle": {"color": config.theme["chart"]["echarts"]["split_line_color"]}},
        "splitArea": {"areaStyle": {"color": ["transparent"]}},
    }
    options["series"] = [{
        "type": "radar",
        "data": [
            {
                "name": str(row[series.label_column]),
                "value": [float(row[column]) for column in series.indicator_columns],
                **point_filter_metadata(row),
            }
            for _, row in df.iterrows()
        ],
        "areaStyle": {"opacity": 0.15},
        "lineStyle": {"width": 2},
        "itemStyle": {"borderColor": colors["primary"]},
    }]
    return options
