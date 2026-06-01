from dataclasses import dataclass, field
from typing import Optional, Literal
from streamlit_echarts import JsCode

LabelPosition = Literal["center", "inside", "outside"]

@dataclass
class PieSeriesConfig:
    column: str

    # Forma
    radius:        list
    center:        list
    avoid_overlap: bool = False

    # Label
    show_label:      bool                = False
    label_position:  LabelPosition       = "center"
    label_formatter: Optional[JsCode]    = None

    # Label line (linha que conecta fatia ao label externo)
    show_label_line: bool = True