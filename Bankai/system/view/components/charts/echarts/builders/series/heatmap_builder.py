import pandas as pd

from system.view.components.charts.echarts.config import BaseChartConfig, HeatmapSeriesConfig
from .common import axis_style
from system.core.managers.charts.payload import point_filter_metadata


def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series: HeatmapSeriesConfig = config.series
    x_values = df[series.column_x].astype(str).drop_duplicates().tolist()
    y_values = df[series.column_y].astype(str).drop_duplicates().tolist()
    x_index = {value: index for index, value in enumerate(x_values)}
    y_index = {value: index for index, value in enumerate(y_values)}
    data = []
    for _, row in df.iterrows():
        value = [x_index[str(row[series.column_x])], y_index[str(row[series.column_y])], float(row[series.value_column])]
        metadata = point_filter_metadata(row)
        data.append({"value": value, **metadata} if metadata else value)
    family = config.theme["chart"]["families"]
    style = axis_style(config.theme["chart"]["echarts"])
    options["xAxis"] = {"type": "category", "data": x_values, **style}
    options["yAxis"] = {"type": "category", "data": y_values, **style}
    options["visualMap"] = {
        "min": float(df[series.value_column].min()),
        "max": float(df[series.value_column].max()),
        "calculable": True,
        "orient": "horizontal",
        "left": "center",
        "bottom": "0%",
        "inRange": {"color": [family["heatmap_low"], family["heatmap_mid"], family["heatmap_high"]]},
        "textStyle": {"color": config.theme["chart"]["font_color"]},
    }
    options["series"] = [{"name": series.value_column, "type": "heatmap", "data": data}]
    return options
