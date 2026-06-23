from typing import Optional
from dataclasses import dataclass, field

from system.core.log import warnings
from system.core.managers.config import hash as hash_man
from system.view.components.cards import card

from system.view.components.layout.header.views import slim, nav

VALID_MODELS = {"slim", "nav", "ticker", "full"}

@dataclass
class HeaderConfig:
    app_name: str
    model: str
    title: str
    subtitle: Optional[str] = None
    has_card: bool = True
    hover: bool = False
    logo_card: bool = True,
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

def _get_component(header_config: HeaderConfig, context):
    if header_config.model == "slim":
        slim.get_component(header_config, context)

    elif header_config.model == "nav":
        nav.get_component(header_config, context)

    else:
        warnings.draw(
            app_name=context.app_name, title="erro_header",
            message=f"Componente não implementado para model='{header_config.model}'"
        )

def draw(
        title:str, subtitle:str, context,
        show_card:bool = True, hover:bool = False, 
        model:str = "slim", nav_pages=[], logo_card=False
    ):

    card.draw(
        card.CardConfig(
            card_id=f"{context.app_name}_main_header", context=context,
            hover=hover, show_card=show_card, model="header",
        ), card.CardRenderConfig(
            content=lambda:
            _get_component(
                HeaderConfig(
                    app_name=context.app_name, model=model, logo_card=logo_card,
                    title=title, subtitle=subtitle, hover=hover, nav_pages=nav_pages
                ), context=context
            )
        )
    )