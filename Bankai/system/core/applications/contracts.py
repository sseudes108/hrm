"""Contratos agnósticos para aplicações hospedadas pelo sistema."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from system.core.auth.config import AuthConfig


ThemeLoader = Callable[[str], Mapping[str, Any]]
ApplicationRenderer = Callable[[Any], None]
ApplicationStateFactory = Callable[[str], Any]


@dataclass(frozen=True, slots=True)
class ApplicationDefinition:
    """Descrição mínima de uma aplicação que pode ser hospedada.

    A aplicação dona desta definição fornece as funções de tema e de
    renderização. Este contrato não conhece diretórios, páginas ou regras
    de negócio de qualquer aplicação concreta.
    """

    app_id: str
    title: str
    render: ApplicationRenderer
    load_theme: ThemeLoader
    state_factory: ApplicationStateFactory
    initial_route: str = "home"
    default_mode: str = "dark"
    auth: AuthConfig = field(default_factory=AuthConfig)

    def __post_init__(self) -> None:
        normalized_id = self.app_id.strip().lower()
        if not normalized_id:
            raise ValueError("app_id não pode ser vazio.")
        if normalized_id != self.app_id:
            object.__setattr__(self, "app_id", normalized_id)

        if not self.title.strip():
            raise ValueError("title não pode ser vazio.")
        if not self.initial_route.strip():
            raise ValueError("initial_route não pode ser vazia.")
        if not callable(self.render):
            raise TypeError("render deve ser uma função chamável.")
        if not callable(self.load_theme):
            raise TypeError("load_theme deve ser uma função chamável.")
        if not callable(self.state_factory):
            raise TypeError("state_factory deve ser uma função chamável.")
