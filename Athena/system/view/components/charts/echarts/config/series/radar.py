from dataclasses import dataclass


@dataclass
class RadarSeriesConfig:
    label_column: str
    indicator_columns: list[str]
    max_values: dict[str, float]
