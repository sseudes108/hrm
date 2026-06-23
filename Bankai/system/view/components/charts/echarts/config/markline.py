from dataclasses import dataclass
from typing import Optional

@dataclass
class MarkLineConfig:
    """Configura linhas estáticas ou calculadas sobre uma série (Ex: Meta, Média)."""
    name: str
    value: Optional[float] = None  # Use para valores fixos (ex: 5000)
    calc_type: Optional[str] = None # Use "average", "min", ou "max" para cálculos automáticos do ECharts
    color: str = "#ef4444" # Vermelho padrão para metas
    line_style: str = "dashed" # dashed, solid, dotted