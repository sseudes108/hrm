from dataclasses import dataclass, field
from typing import Literal, Optional, List
from system.view.components.charts.echarts.config import MarkLineConfig, SecondaryLineConfig

BarOrient = Literal["vertical", "horizontal"]

@dataclass
class BarSeriesConfig:
    column_x:  str
    columns_y: list                              # uma ou mais colunas

    orient:       BarOrient = "vertical"
    bar_width:    str       = "40%"
    border_radius: int      = 4                 # canto arredondado das barras

    mark_lines: Optional[List[MarkLineConfig]] = None
    secondary_lines: Optional[List[SecondaryLineConfig]] = None