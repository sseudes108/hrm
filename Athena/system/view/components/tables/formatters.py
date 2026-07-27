"""Formatadores puros para as células das tabelas HTML."""

from datetime import date, datetime
from html import escape
from numbers import Number
from typing import Any, Callable


CellFormatter = Callable[[Any], str]


def text(value: Any) -> str:
    return "—" if value is None else escape(str(value))


def integer(value: Any) -> str:
    return "—" if value is None else f"{int(value):,}".replace(",", ".")


def decimal(value: Any, places: int = 2) -> str:
    if value is None:
        return "—"
    return f"{float(value):,.{places}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def currency(value: Any) -> str:
    return "—" if value is None else f"R$ {decimal(value)}"


def percent(value: Any) -> str:
    return "—" if value is None else f"{float(value):.1f}%".replace(".", ",")


def date_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, datetime):
        value = value.date()
    return value.strftime("%d/%m/%Y") if isinstance(value, date) else text(value)


def badge(value: Any) -> str:
    label = text(value)
    normalized = str(value).strip().lower() if value is not None else "unknown"
    tone = {
        "active": "success", "ativo": "success", "success": "success",
        "closed": "muted", "inactive": "muted", "inativo": "muted",
        "dormant": "warning", "warning": "warning",
        "error": "danger", "danger": "danger", "failed": "danger",
    }.get(normalized, "info")
    return f'<span class="ui-table-badge ui-table-badge--{tone}">{label}</span>'


def trend(value: Any) -> str:
    if value is None:
        return "—"
    numeric = float(value)
    tone = "positive" if numeric > 0 else "negative" if numeric < 0 else "neutral"
    icon = "↑" if numeric > 0 else "↓" if numeric < 0 else "→"
    return f'<span class="ui-table-trend ui-table-trend--{tone}">{icon} {percent(abs(numeric))}</span>'


FORMATTERS: dict[str, CellFormatter] = {
    "text": text,
    "integer": integer,
    "decimal": decimal,
    "currency": currency,
    "percent": percent,
    "date": date_value,
    "badge": badge,
    "trend": trend,
}


def format_cell(value: Any, formatter: str | CellFormatter = "text") -> str:
    if callable(formatter):
        return formatter(value)
    try:
        return FORMATTERS[formatter](value)
    except KeyError as exc:
        raise ValueError(f"Formatador de tabela não suportado: '{formatter}'.") from exc
