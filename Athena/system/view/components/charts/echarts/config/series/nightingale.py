from dataclasses import dataclass


@dataclass
class NightingaleSeriesConfig:
    category_column: str
    value_column: str
    radius: list[str]
    center: list[str]
