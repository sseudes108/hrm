from dataclasses import dataclass


@dataclass
class SunburstSeriesConfig:
    path_columns: list[str]
    value_column: str
