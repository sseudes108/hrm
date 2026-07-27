import pandas as pd

from system.view.components.charts.echarts.config import BaseChartConfig, BoxplotSeriesConfig
from .common import axis_style
from .common import point_value


def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series: BoxplotSeriesConfig = config.series
    style = axis_style(config.theme["chart"]["echarts"])
    options["xAxis"] = {
        "type": "category",
        "data": df[series.category_column].astype(str).tolist(),
        **style,
    }
    options["yAxis"] = {"type": "value", **style}
    options["series"] = [{
        "name": series.value_column,
        "type": "boxplot",
        "data": [
            point_value(
                [round(float(row[column]), 4) for column in ("min", "q1", "median", "q3", "max")],
                row,
            )
            for _, row in df.iterrows()
        ],
    }]
    return options
