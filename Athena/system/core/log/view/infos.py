"""Compatibilidade para mensagens informativas do sistema."""

from typing import Any

from .warnings import draw as draw_alert


def draw(message: str, alert: str = "info", *, context: Any | None = None) -> None:
    """Delega ao único componente de alertas do framework."""
    draw_alert(message, alert=alert, context=context)
