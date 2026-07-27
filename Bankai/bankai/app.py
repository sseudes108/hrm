"""Raiz de composição da aplicação Bankai."""

from pathlib import Path
from typing import Any

from system.core.applications import ApplicationDefinition
from system.core.auth import AuthConfig
from system.core.managers.view import theme as theme_man

from .layout import render as render_layout
from .state import create_state


APP_ROOT = Path(__file__).resolve().parent
THEME_DIRECTORY = APP_ROOT / "theme"
DEVELOPMENT_USERS = {
    "admin": "pbkdf2$sha256$310000$YmFua2FpLWRldi1zYWx0IQ$fVjoRzQb9F_0KITnANhoHXTVM0kwkhYJTJyCwch-Zec",
}


def load_theme(mode: str) -> dict[str, Any]:
    """Carrega um tema pertencente exclusivamente à aplicação Bankai."""
    normalized_mode = mode.strip().lower()
    base_path = THEME_DIRECTORY / "base.json"
    mode_path = THEME_DIRECTORY / f"{normalized_mode}.json"

    if not mode_path.is_file():
        raise ValueError(f"Modo de tema não suportado pela aplicação Bankai: {mode}")

    return theme_man.load(base_path, mode_path)


def render(context: Any) -> None:
    """Delega a composição visual ao shell pertencente à aplicação."""
    render_layout(context)


def get_application() -> ApplicationDefinition:
    """Expõe a definição consumida pelo carregador genérico do sistema."""
    return ApplicationDefinition(
        app_id="bankai",
        title="Bankai",
        initial_route="home",
        default_mode="light",
        render=render,
        load_theme=load_theme,
        state_factory=create_state,
        auth=AuthConfig(enabled=False, allow_local_auth=True, local_users=DEVELOPMENT_USERS),
    )
