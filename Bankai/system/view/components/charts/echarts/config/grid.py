from dataclasses import dataclass

@dataclass
class GridConfig:
    show: bool = False
    left: str = "3%"
    right: str = "4%"
    bottom: str = "5%"
    top: str = "10%"
    contain_label: bool = True