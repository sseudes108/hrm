from dataclasses import dataclass

@dataclass
class LegendConfig:
    orientation: str = "vertical"
    top:         str = "85%"
    left:        str = "2%"
    bottom:      str = "10%"
    right:       str = "0%"