from collections.abc import Callable
from typing import Optional
from dataclasses import dataclass

from system.core.log import warnings
from system.view.components.cards import card
from system.view.components.layout.navigator.navigator import NavigationItem

from system.view.components.layout.header.views import slim, nav
from system.view.components.layout import fixes

VALID_MODELS = {"slim", "nav"}

@dataclass
class HeaderConfig:
    app_name: str
    model: str
    title: str
    subtitle: Optional[str] = None
    show_card: bool = True
    hover: bool = False
    logo_card: bool = False
    nav_items: Optional[list[NavigationItem]] = None
    active_route: Optional[str] = None
    on_navigate: Optional[Callable[[str], None]] = None

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            raise ValueError(f"model inválido: '{self.model}'. Escolha entre: {VALID_MODELS}")
        if not self.title.strip():
            raise ValueError("title é obrigatório para o Header")
        if self.model == "nav":
            if not self.nav_items:
                raise ValueError("nav_items é obrigatório quando model='nav'")
            if self.active_route is None or self.on_navigate is None:
                raise ValueError("active_route e on_navigate são obrigatórios quando model='nav'")

def _get_component(header_config: HeaderConfig, context):
    if header_config.model == "slim":
        slim.get_component(header_config, context)

    elif header_config.model == "nav":
        nav.get_component(header_config, context)

    else:
        warnings.draw(
            message=f"Componente não implementado para model='{header_config.model}'",
            alert="error",
            context=context,
        )

def draw(
        title: str, subtitle: Optional[str] = None, context=None,
        show_card:bool = True, hover:bool = False, 
        model: str = "slim", nav_items: Optional[list[NavigationItem]] = None,
        active_route: Optional[str] = None, on_navigate: Optional[Callable[[str], None]] = None,
        logo_card: bool = False, padding: str = "compact", bottom_margin = 16
    ):
    """Renderiza um cabeçalho; o logo é obtido opcionalmente do tema ativo."""
    if context is None:
        raise ValueError("context é obrigatório para renderizar o Header")

    card.draw(
        card.CardConfig(
            card_id=f"{context.app_name}_main_header", context=context,
            hover=hover, show_card=show_card, model="header", padding=padding,
        ), card.CardRenderConfig(
            content=lambda:
            _get_component(
                HeaderConfig(
                    app_name=context.app_name, model=model, logo_card=logo_card,
                    title=title, subtitle=subtitle, show_card=show_card,
                    hover=hover, nav_items=nav_items, active_route=active_route,
                    on_navigate=on_navigate,
                ), context=context
            )
        )
    )
    fixes.horizontal_spacer(f"{bottom_margin}px")
