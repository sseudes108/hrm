import pandas as pd

from system.view.components.charts.echarts.config import BaseChartConfig, NightingaleSeriesConfig
from system.core.managers.charts.payload import point_filter_metadata


def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series: NightingaleSeriesConfig = config.series
    options["series"] = [{
        "name": series.category_column,
        "type": "pie",
        "roseType": "area",
        "radius": series.radius,
        "center": series.center,
        "itemStyle": {
            "borderRadius": 4,
            "borderColor": config.theme["chart"]["families"]["hierarchy_border"],
            "borderWidth": 1,
        },
        "data": [
            {
                "name": str(row[series.category_column]),
                "value": float(row[series.value_column]),
                **point_filter_metadata(row),
            }
            for _, row in df.iterrows()
        ],
    }]
    return options
