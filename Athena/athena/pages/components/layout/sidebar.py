"""Barra lateral fixa com os parâmetros do Capacity Planner."""

from typing import Any

from athena.pages.espada.ortools import inputs


def draw(context: Any) -> None:
    context.state.payload = inputs.draw_sidebar(context)
