from dataclasses import dataclass
from typing import Optional


@dataclass
class ScatterSeriesConfig:
    column_x: str
    column_y: str
    size_column: Optional[str] = None
    category_column: Optional[str] = None
    symbol_size: int = 12
