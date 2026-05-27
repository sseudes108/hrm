from dataclasses import dataclass, field
from typing import Optional

VALID_MODELS = {"slim", "nav", "ticker"}

@dataclass
class HeaderConfig:
    app_name: str
    model: str
    title: str
    subtitle: Optional[str] = None
    has_card: bool = True
    hover: bool = False
    nav_pages: Optional[list] = field(default=None)
    key: Optional[str] = None

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            raise ValueError(f"model inválido: '{self.model}'. Escolha entre: {VALID_MODELS}")
        
        if self.model == "nav" and not self.nav_pages:
            raise ValueError("nav_pages é obrigatório quando model='nav'")