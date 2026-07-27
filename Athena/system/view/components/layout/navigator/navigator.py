"""Navegação visual agnóstica ao estado de cada aplicação."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import streamlit as st


VALID_MODELS = {"tabs", "header_nav"}


@dataclass(frozen=True)
class NavigationItem:
    """Item de navegação pertencente à aplicação que consome o componente."""

    route: str
    label: str

    def __post_init__(self) -> None:
        if not self.route or not self.route.isidentifier():
            raise ValueError("route deve ser um identificador simples e não vazio")
        if not self.label.strip():
            raise ValueError("label não pode ser vazio")


@dataclass
class NavigatorConfig:
    app_name: str
    model: str
    items: Sequence[NavigationItem]
    active_route: str
    on_navigate: Callable[[str], None]

    def __post_init__(self) -> None:
        if self.model not in VALID_MODELS:
            raise ValueError(f"model inválido para Navigator: '{self.model}'. Escolha entre: {VALID_MODELS}")
        if not self.items:
            raise ValueError("items não pode ser vazio")
        if self.active_route not in {item.route for item in self.items}:
            raise ValueError("active_route deve corresponder a um item de navegação")
        if not callable(self.on_navigate):
            raise TypeError("on_navigate deve ser uma função chamável")


def draw(
    context,
    *,
    items: Sequence[NavigationItem],
    active_route: str,
    on_navigate: Callable[[str], None],
    model: str = "tabs",
) -> None:
    """Renderiza rotas sem conhecer o formato do estado da aplicação."""
    config = NavigatorConfig(
        app_name=context.app_name,
        model=model,
        items=items,
        active_route=active_route,
        on_navigate=on_navigate,
    )

    with st.container(key=f"co_navigator_{config.model}_{config.app_name}"):
        _draw_items(config, is_mobile=context.is_mobile)


def _draw_items(config: NavigatorConfig, *, is_mobile: bool) -> None:
    items = list(config.items)
    if is_mobile and len(items) > 3:
        for row in _split_rows(items):
            _draw_row(config, row)
        return
    _draw_row(config, items)


def _draw_row(config: NavigatorConfig, items: Sequence[NavigationItem]) -> None:
    columns = st.columns(len(items))
    for column, item in zip(columns, items):
        with column:
            state = "is_active" if item.route == config.active_route else "is_inactive"
            st.button(
                item.label,
                key=f"nav_{config.app_name}_{item.route}_{state}",
                on_click=config.on_navigate,
                args=(item.route,),
                width='stretch',
            )


def _split_rows(items: Sequence[NavigationItem]) -> list[Sequence[NavigationItem]]:
    """Evita uma única linha comprimida em telas móveis."""
    midpoint = (len(items) + 1) // 2
    return [items[:midpoint], items[midpoint:]]
