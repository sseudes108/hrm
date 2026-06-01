from dataclasses import dataclass
from typing import Optional

@dataclass
class SecondaryLineConfig:
    """Configura uma segunda coluna do DataFrame para ser desenhada como linha."""
    column: str
    name: Optional[str] = None # Nome que vai aparecer na legenda/tooltip
    color: str = "#f59e0b" # Amarelo/Laranja padrão para destacar
    smooth: bool = True