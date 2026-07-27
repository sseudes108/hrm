"""Raiz de composição da aplicação Athena."""

from pathlib import Path
from typing import Any

from system.core.applications import ApplicationDefinition
from system.core.managers.view import theme as theme_man

from .layout import render as render_layout
from .state import create_state


APP_ROOT = Path(__file__).resolve().parent
THEME_DIRECTORY = APP_ROOT / "theme"


def load_theme(mode: str) -> dict[str, Any]:
    normalized_mode = mode.strip().lower()
    mode_path = THEME_DIRECTORY / f"{normalized_mode}.json"
    if not mode_path.is_file():
        raise ValueError(f"Modo de tema não suportado pela aplicação Athena: {mode}")
    return theme_man.load(THEME_DIRECTORY / "base.json", mode_path)


def render(context: Any) -> None:
    render_layout(context)


def get_application() -> ApplicationDefinition:
    return ApplicationDefinition(
        app_id="athena",
        title="Athena — Capacity Planner",
        initial_route="capacity",
        default_mode="dark",
        render=render,
        load_theme=load_theme,
        state_factory=create_state,
    )
