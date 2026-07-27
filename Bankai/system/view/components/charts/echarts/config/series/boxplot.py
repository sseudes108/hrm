from dataclasses import dataclass


@dataclass
class BoxplotSeriesConfig:
    category_column: str
    value_column: str
