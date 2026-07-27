"""Rotas declarativas da aplicação Athena."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from system.view.components.layout import PageLayout

from .pages.espada.ortools import page as capacity
from .pages.components.layout import sidebar

RouteRenderer = Callable[[Any], None]

@dataclass(frozen=True)
class RouteDefinition:
    renderer: RouteRenderer
    layout: PageLayout
    sidebar_renderer: RouteRenderer | None = None


ROUTES: dict[str, RouteDefinition] = {
    "capacity": RouteDefinition(
        renderer=capacity.render,
        layout=PageLayout(header="sticky", sidebar="sticky", sidebar_width=0.2),
        sidebar_renderer=sidebar.draw,
    ),
}


def get_current_route(context: Any) -> RouteDefinition:
    route = ROUTES.get(context.state.current_route)
    if route is None:
        raise ValueError(f"Rota Athena não registrada: {context.state.current_route}")
    return route
