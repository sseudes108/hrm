"""Shell visual da aplicação Bankai."""

from typing import Any
import streamlit as st

from system.view.components.layout import header
from system.view.components.layout.navigator import NavigationItem
from system.view.components.layout import page_layout

from .routes import get_current_route

NAVIGATION = (
    NavigationItem(route="home", label="Início"),
    NavigationItem(route="analysis", label="Análise"),
    NavigationItem(route="reports", label="Relatórios"),
    NavigationItem(route="catalog", label="Catálogo"),
)

def render(context: Any) -> None:
    route = get_current_route(context)

    with st.container(key=f"co_layout_shell_{context.app_name}"):
        page_layout.render(
            context,
            layout=route.layout,
            header=lambda: (route.header_renderer or _render_header)(context),
            sidebar=(
                lambda: route.sidebar_renderer(context)
                if route.sidebar_renderer
                else None
            ),
            filters=(
                lambda: route.filters_renderer(context)
                if route.filters_renderer
                else None
            ),
            content=lambda: route.renderer(context),
        )

def _render_header(context: Any) -> None:
    header.draw(
        context=context,
        title="Bankai",
        subtitle="Zanpakutou System",
        model="nav",
        nav_items=list(NAVIGATION),
        active_route=context.state.current_route,
        on_navigate=context.state.navigate,
    )
