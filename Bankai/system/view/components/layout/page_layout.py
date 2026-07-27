"""Primitiva genérica para compor slots de layout de uma página."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

import streamlit as st


SlotPosition = Literal["hidden", "static", "sticky"]
_VALID_POSITIONS = {"hidden", "static", "sticky"}


@dataclass(frozen=True)
class PageLayout:
    """Define a posição dos slots compartilhados de uma rota.

    Um slot visível deve receber seu renderer pela composição da aplicação.
    """

    header: SlotPosition = "hidden"
    sidebar: SlotPosition = "hidden"
    filters: SlotPosition = "hidden"
    sidebar_width: float = 0.25

    def __post_init__(self) -> None:
        for slot_name, position in (
            ("header", self.header),
            ("sidebar", self.sidebar),
            ("filters", self.filters),
        ):
            if position not in _VALID_POSITIONS:
                raise ValueError(f"{slot_name} deve ser um de {_VALID_POSITIONS}; recebido '{position}'.")
        if not 0 < self.sidebar_width < 1:
            raise ValueError("sidebar_width deve estar entre 0 e 1.")


def render(
    context,
    *,
    layout: PageLayout,
    content: Callable[[], None],
    header: Callable[[], None] | None = None,
    sidebar: Callable[[], None] | None = None,
    filters: Callable[[], None] | None = None,
) -> None:
    """Renderiza slots declarados pela rota, sem conhecer a aplicação dona."""
    _render_slot(context, "header", layout.header, header)
    if layout.sidebar == "hidden":
        _render_content_column(context, layout, content, filters)
        return

    sidebar_column, content_column = st.columns(
        [layout.sidebar_width, 1 - layout.sidebar_width],
        gap=None,
    )
    with sidebar_column:
        _render_slot(context, "sidebar", layout.sidebar, sidebar)
    with content_column:
        _render_content_column(context, layout, content, filters)


def _render_content_column(
    context,
    layout: PageLayout,
    content: Callable[[], None],
    filters: Callable[[], None] | None,
) -> None:
    _render_slot(context, "filters", layout.filters, filters)
    with st.container(key=f"co_layout_content_{context.app_name}"):
        content()


def _render_slot(
    context,
    slot_name: str,
    position: SlotPosition,
    renderer: Callable[[], None] | None,
) -> None:
    if position == "hidden":
        return
    if renderer is None:
        raise ValueError(f"O slot '{slot_name}' está visível, mas não recebeu renderer.")
    with st.container(key=f"co_layout_{slot_name}_{position}_{context.app_name}"):
        renderer()
