"""Registro de rotas pertencente exclusivamente à aplicação Bankai."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .pages import analysis, catalog, home, reports


RouteRenderer = Callable[[Any], None]


@dataclass(frozen=True)
class RouteDefinition:
    renderer: RouteRenderer


ROUTES: dict[str, RouteDefinition] = {
    "home": RouteDefinition(renderer=home.render),
    "reports": RouteDefinition(renderer=reports.render),
    "analysis": RouteDefinition(renderer=analysis.render),
    "catalog": RouteDefinition(renderer=catalog.render),
}


def get_current_route(context: Any) -> RouteDefinition:
    """Resolve a definição da rota guardada no estado da aplicação."""
    route = ROUTES.get(context.state.current_route)
    if route is None:
        raise ValueError(f"Rota Bankai não registrada: {context.state.current_route}")
    return route
