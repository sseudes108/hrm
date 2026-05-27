from dataclasses import dataclass
from typing import Optional, Literal
from streamlit_echarts import JsCode

TooltipTrigger = Literal["item", "axis", "none"]

@dataclass
class TooltipConfig:
    trigger:   TooltipTrigger  = "item"
    formatter: Optional[JsCode] = None  # None = ECharts usa o padrão