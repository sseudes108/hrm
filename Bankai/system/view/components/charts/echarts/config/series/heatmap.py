from dataclasses import dataclass


@dataclass
class HeatmapSeriesConfig:
    column_x: str
    column_y: str
    value_column: str
