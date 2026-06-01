from dataclasses import dataclass, field
from typing import Literal, Optional, get_args

from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig 
from system.view.components.charts.echarts.config.grid import GridConfig

ChartModel = Literal["pie", "bar", "line", "scatter", "radar"]
VALID_MODELS = set(get_args(ChartModel))


@dataclass
class BaseChartConfig:
    app_name: str
    model:    ChartModel
    title:    str
    theme:    dict
    series:   object

    subtitle:       Optional[str] = None
    width:          str           = "100%"
    height:         str           = "400px"
    show_card:      bool          = True
    has_card_title: bool          = False
    card_hover:     bool          = True

    tooltip: TooltipConfig = field(default_factory=TooltipConfig) 
    legend:  LegendConfig  = field(default_factory=LegendConfig)
    toolbox: ToolboxConfig = field(default_factory=ToolboxConfig)
    grid:    GridConfig    = field(default_factory=GridConfig)

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            raise ValueError(
                f"Chart — model inválido: '{self.model}'. "
                f"Escolha entre: {VALID_MODELS}"
            )