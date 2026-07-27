"""Registro de rotas pertencente exclusivamente à aplicação Bankai."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from system.view.components.layout import PageLayout
from .pages.components.layout import filter_bar
from .pages.components.layout import analysis_filters

from .pages import analysis, catalog, home, reports


RouteRenderer = Callable[[Any], None]


@dataclass(frozen=True)
class RouteDefinition:
    renderer: RouteRenderer
    layout: PageLayout
    header_renderer: RouteRenderer | None = None
    sidebar_renderer: RouteRenderer | None = None
    filters_renderer: RouteRenderer | None = None


ROUTES: dict[str, RouteDefinition] = {
    "home": RouteDefinition(
        renderer=home.render,
        layout=PageLayout(header="sticky", sidebar="sticky"),
        sidebar_renderer=filter_bar.draw,
    ),
    "reports": RouteDefinition(
        renderer=reports.render, 
        layout=PageLayout(header="sticky", filters="sticky"),
        filters_renderer=filter_bar.draw
    ),
    "analysis": RouteDefinition(
        renderer=analysis.render,
        layout=PageLayout(header="sticky", filters="sticky"),
        filters_renderer=analysis_filters.draw,
    ),
    "catalog": RouteDefinition(
        renderer=catalog.render,
        layout=PageLayout(header="sticky"),
    ),
}


def get_current_route(context: Any) -> RouteDefinition:
    """Resolve a definição da rota guardada no estado da aplicação."""
    route = ROUTES.get(context.state.current_route)
    if route is None:
        raise ValueError(f"Rota Bankai não registrada: {context.state.current_route}")
    return route
