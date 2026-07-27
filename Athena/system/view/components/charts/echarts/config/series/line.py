from dataclasses import dataclass, field
from typing import List, Optional, Literal
from system.view.components.charts.echarts.config import MarkLineConfig, SecondaryLineConfig

@dataclass
class LineSeriesConfig:
    column_x: str
    columns_y: List[str]
    orient: str = "horizontal"
    
    # 🚀 Propriedades exclusivas de gráficos de linha
    smooth: bool = True           # Deixa a linha curvada em vez de reta
    fill_area: bool = False       # Preenche a área abaixo da linha
    line_width: int = 3           # Espessura da linha principal
    symbol: str = "circle"        # Formato dos pontos ('circle', 'rect', 'none', etc)
    symbol_size: int = 6          # Tamanho dos pontos
    step: Optional[Literal["start", "middle", "end"]] = None
    
    mark_lines: Optional[List[MarkLineConfig]] = None
    secondary_lines: Optional[List[SecondaryLineConfig]] = None