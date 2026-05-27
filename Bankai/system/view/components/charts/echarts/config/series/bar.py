from dataclasses import dataclass, field
from typing import Literal, Optional

BarOrient = Literal["vertical", "horizontal"]

@dataclass
class BarSeriesConfig:
    column_x:  str
    columns_y: list                              # uma ou mais colunas

    orient:       BarOrient = "vertical"
    bar_width:    str       = "40%"
    border_radius: int      = 4                 # canto arredondado das barras