"""Mensagens visuais padronizadas para a aplicação ativa."""

from html import escape
from typing import Any, Literal

import streamlit as st

from system.core.managers.config import hash as hash_man
from system.view.components.cards import card


AlertKind = Literal["info", "warning", "error"]


def draw(
    message: str,
    alert: AlertKind = "warning",
    *,
    context: Any | None = None,
) -> None:
    """Renderiza um alerta no card do sistema quando há contexto visual."""
    if alert not in {"info", "warning", "error"}:
        raise ValueError(f"Tipo de alerta inválido: '{alert}'")
    if context is None:
        _draw_native_alert(alert, message)
        return

    identifier = hash_man.get_hash(f"{alert}:{message}")
    card.draw(
        card.CardConfig(
            card_id=f"alert_{alert}_{identifier}",
            context=context,
            model="base",
            variant="outline",
            padding="normal",
            hover=False,
        ),
        card.CardRenderConfig(content=lambda: _draw_content(alert, message)),
    )


def _draw_native_alert(alert: AlertKind, message: str) -> None:
    if alert == "info":
        st.info(message)
    elif alert == "error":
        st.error(message)
    else:
        st.warning(message)


def _draw_content(alert: AlertKind, message: str) -> None:
    icon = {"info": "info", "warning": "warning", "error": "error"}[alert]
    css_class = f"ui-alert ui-alert--{alert}"
    st.html(
        f'<div class="{css_class}">'
        f'<span class="material-symbols-rounded">{icon}</span>'
        f"<div>{escape(message)}</div>"
        "</div>"
    )
