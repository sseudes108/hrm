from dataclasses import dataclass, field
from typing import Literal, Optional, get_args

from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig 


ChartModel = Literal["pie", "bar", "line", "scatter", "radar"]
VALID_MODELS = set(get_args(ChartModel))


@dataclass
class BaseChartConfig:
    app_name: str
    model:    ChartModel
    title:    str
    theme:    dict
    series:   object

    subtitle:        Optional[str] = None
    width:           str           = "100%"
    height:          str           = "400px"
    in_card:         bool          = True

    tooltip: TooltipConfig = field(default_factory=TooltipConfig) 
    legend:  LegendConfig  = field(default_factory=LegendConfig)
    toolbox: ToolboxConfig = field(default_factory=ToolboxConfig)

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            raise ValueError(
                f"Chart — model inválido: '{self.model}'. "
                f"Escolha entre: {VALID_MODELS}"
            )