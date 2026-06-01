from dataclasses import dataclass, field
from typing import Optional

from system.control.managers import hash_man

VALID_MODELS = {"slim", "nav", "ticker"}

@dataclass
class HeaderConfig:
    app_name: str
    model: str
    title: str
    subtitle: Optional[str] = None
    has_card: bool = True
    hover: bool = False
    nav_pages: Optional[list] = None
    
    # Declaramos o tipo e avisamos para não exigir isso na criação do objeto
    key: str = field(init=False) 

    def __post_init__(self):
        # 1. Monta a chave dinamicamente usando a própria instância (self)
        self.key = f"{self.app_name}_{hash_man.get_hash(self.app_name)}"

        # 2. Mantém as suas validações originais
        if self.model not in VALID_MODELS:
            raise ValueError(f"model inválido: '{self.model}'. Escolha entre: {VALID_MODELS}")
        
        if self.model == "nav" and not self.nav_pages:
            raise ValueError("nav_pages é obrigatório quando model='nav'")