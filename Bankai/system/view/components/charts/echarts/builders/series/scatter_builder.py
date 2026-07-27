import pandas as pd

from system.view.components.charts.echarts.config import BaseChartConfig, ScatterSeriesConfig
from .common import axis_style
from system.core.managers.charts.payload import point_filter_metadata


def build(df: pd.DataFrame, config: BaseChartConfig, options: dict) -> dict:
    series: ScatterSeriesConfig = config.series
    style = axis_style(config.theme["chart"]["echarts"])
    bubble_sizes = _bubble_sizes(df, series.size_column)
    categories = [None]
    if series.category_column:
        categories = sorted(df[series.category_column].dropna().unique().tolist())

    rendered = []
    for category in categories:
        data = df if category is None else df.loc[df[series.category_column] == category]
        points = []
        for index, row in data.iterrows():
            size = bubble_sizes.get(index, series.symbol_size)
            value = [_native(row[series.column_x]), _native(row[series.column_y]), _native(size)]
            metadata = point_filter_metadata(row)
            if metadata:
                points.append({"value": value, **metadata})
            else:
                points.append(value)
        item = {
            "name": str(category) if category is not None else series.column_y,
            "type": "scatter",
            "data": points,
        }
        if series.size_column is None:
            item["symbolSize"] = series.symbol_size
        rendered.append(item)

    options["xAxis"] = {"type": "value", "name": series.column_x, **style}
    options["yAxis"] = {"type": "value", "name": series.column_y, **style}
    options["series"] = rendered
    return options


def _native(value):
    return value.item() if hasattr(value, "item") else value


def _bubble_sizes(df: pd.DataFrame, size_column: str | None) -> dict:
    if size_column is None:
        return {}
    values = pd.to_numeric(df[size_column], errors="coerce").fillna(0)
    minimum, maximum = values.min(), values.max()
    if minimum == maximum:
        return {index: 16 for index in values.index}
    return {
        index: round(8 + ((value - minimum) / (maximum - minimum)) * 24, 2)
        for index, value in values.items()
    }
