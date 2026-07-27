"""Shell visual da aplicação Athena."""

from typing import Any

import streamlit as st

from system.view.components.layout import header, page_layout
from system.view.components.layout.navigator import NavigationItem

from .routes import get_current_route


NAVIGATION = (NavigationItem(route="capacity", label="Capacity Planner"),)


def render(context: Any) -> None:
    route = get_current_route(context)
    with st.container(key=f"co_layout_shell_{context.app_name}"):
        page_layout.render(
            context,
            layout=route.layout,
            header=lambda: _render_header(context),
            sidebar=(
                lambda: route.sidebar_renderer(context)
                if route.sidebar_renderer
                else None
            ),
            content=lambda: route.renderer(context),
        )


def _render_header(context: Any) -> None:
    header.draw(
        context=context,
        title="Athena",
        subtitle="Capacity Planner",
        model="nav",
        nav_items=list(NAVIGATION),
        active_route=context.state.current_route,
        on_navigate=context.state.navigate,
        padding="compact",
    )
