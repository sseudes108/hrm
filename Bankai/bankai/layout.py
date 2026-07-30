"""Shell visual da aplicação Bankai."""

from typing import Any
import streamlit as st

from system.view.components.layout import header
from system.view.components.layout.navigator import NavigationItem

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
        _render_header(context)
        route.renderer(context)

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
