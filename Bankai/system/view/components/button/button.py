"""Botão Streamlit integrado ao contrato visual do System."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

import streamlit as st

from system.view.components._keys import scoped_key


ButtonVariant = Literal["primary", "secondary", "ghost"]
ButtonWidth = Literal["content", "stretch"] | int
VALID_BUTTON_VARIANTS = {"primary", "secondary", "ghost"}


@dataclass(slots=True)
class ButtonConfig:
    """Configuração declarativa de um botão Streamlit temático."""

    context: Any
    button_id: str
    label: str
    variant: ButtonVariant = "primary"
    icon: str | None = None
    help: str | None = None
    disabled: bool = False
    width: ButtonWidth = "content"
    on_click: Callable[..., Any] | None = None
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.context is None or not getattr(self.context, "app_name", None):
            raise ValueError("context com app_name é obrigatório para criar um botão")
        if not isinstance(self.button_id, str) or not self.button_id.strip():
            raise ValueError("button_id não pode ser vazio")
        if not isinstance(self.label, str) or not self.label:
            raise ValueError("label não pode ser vazio")
        if self.variant not in VALID_BUTTON_VARIANTS:
            raise ValueError(
                f"variant inválida para botão: '{self.variant}'. "
                f"Escolha entre: {VALID_BUTTON_VARIANTS}"
            )
        if self.width not in {"content", "stretch"} and (
            not isinstance(self.width, int) or isinstance(self.width, bool) or self.width <= 0
        ):
            raise ValueError("width deve ser 'content', 'stretch' ou um inteiro positivo")

        available_variants = (
            getattr(self.context, "theme", {})
            .get("components", {})
            .get("button", {})
            .get("variants", {})
        )
        if available_variants and self.variant not in available_variants:
            raise ValueError(f"variant de botão não existe no tema ativo: '{self.variant}'")

    @property
    def widget_key(self) -> str:
        """Chave estável do widget, independente da variante visual."""
        return scoped_key(self.context, "button", self.button_id)

    @property
    def container_key(self) -> str:
        """Chave semântica usada pelos seletores CSS da variante."""
        return scoped_key(self.context, f"co_button_{self.variant}", self.button_id)


def draw(
    context: Any,
    label: str,
    button_id: str,
    *,
    variant: ButtonVariant = "secondary",
    icon: str | None = None,
    help: str | None = None,
    disabled: bool = False,
    width: ButtonWidth = "content",
    on_click: Callable[..., Any] | None = None,
    args: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
) -> bool:
    """Renderiza um botão e devolve True no rerun em que ele foi clicado.

    A variante controla somente a aparência. Identidade, callback e estado do
    widget permanecem estáveis quando a variante muda.
    """
    config = ButtonConfig(
        context=context,
        button_id=button_id,
        label=label,
        variant=variant,
        icon=icon,
        help=help,
        disabled=disabled,
        width=width,
        on_click=on_click,
        args=args,
        kwargs=dict(kwargs or {}),
    )

    with st.container(key=config.container_key):
        return st.button(
            label=config.label,
            key=config.widget_key,
            help=config.help,
            on_click=config.on_click,
            args=config.args,
            kwargs=config.kwargs,
            type="secondary",
            icon=config.icon,
            disabled=config.disabled,
            width=config.width,
        )
