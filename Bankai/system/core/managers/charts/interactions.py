"""Converte cliques ECharts em filtros do estado da aplicação."""

from typing import Any, Literal
import re

import pandas as pd

from system.core.contexts import ChartFilterState
from system.core.managers.charts.payload import FILTER_VALUE_KEY


ChartClickType = Literal["categoric_click", "date_click", "categoric", "date"]


def apply_click_filter(
    *,
    df: pd.DataFrame,
    context: Any,
    column: str | None,
    event_data: dict | None,
    click_type: ChartClickType = "categoric_click",
    event_column: str | None = None,
) -> bool:
    """Aplica ou remove um filtro a partir de um evento do gráfico.

    ``column`` é a coluna real a ser salva no estado. ``event_column`` é a
    coluna que produziu o rótulo clicado no gráfico. Quando forem diferentes,
    o valor de ``event_column`` é resolvido primeiro e então convertido para
    o valor correspondente em ``column`` na mesma linha do DataFrame.

    A interação é deliberadamente segura: sem coluna, evento válido ou estado
    compatível, ela apenas não faz nada. Isso permite habilitá-la em gráficos
    reutilizáveis sem acoplar o componente a um DataFrame específico.
    """
    source_column = event_column or column
    if (
        not column
        or not source_column
        or column not in df.columns
        or source_column not in df.columns
        or not event_data
    ):
        return False
    state = getattr(context, "state", None)
    if not isinstance(state, ChartFilterState):
        return False

    event = event_data.get("chart_event", event_data)
    if not isinstance(event, dict) or not _is_data_event(event):
        return False
    timestamp = event.get("ts")
    if timestamp is not None and state.get_last_event_ts(column) == timestamp:
        return False

    normalized_type = _normalize_type(click_type)
    explicit_value = _explicit_filter_value(event) if normalized_type == "categoric_click" else None
    if explicit_value is not None:
        return _toggle_filter(state, column, explicit_value, timestamp)

    source_value = (
        _resolve_date_value(df, source_column, event)
        if normalized_type == "date_click"
        else _resolve_category_value(df, source_column, event)
    )
    if source_value is None:
        return False

    value = _resolve_filter_value(
        df=df,
        source_column=source_column,
        target_column=column,
        source_value=source_value,
        click_type=normalized_type,
    )
    if value is None:
        return False

    return _toggle_filter(state, column, value, timestamp)


def _toggle_filter(state: ChartFilterState, column: str, value: Any, timestamp: int | None) -> bool:
    if timestamp is not None:
        state.set_last_event_ts(column, timestamp)
    if state.active_filters.get(column) == value:
        return state.remove_filter(column)
    return state.update_filter(column, value)


def _resolve_filter_value(
    *,
    df: pd.DataFrame,
    source_column: str,
    target_column: str,
    source_value: Any,
    click_type: Literal["categoric_click", "date_click"],
) -> Any | None:
    """Converte o rótulo do gráfico no valor da coluna de filtro.

    Intervalos de data já são valores de filtro completos. Para categorias
    agregadas, exige uma relação não ambígua entre o label exibido e o valor
    real que será aplicado à base original.
    """
    if source_column == target_column or click_type == "date_click":
        return source_value

    matches = df.loc[df[source_column].eq(source_value), target_column].dropna().unique()
    return matches[0] if len(matches) == 1 else None


def _is_data_event(event: dict) -> bool:
    component = event.get("componentType")
    return component in (None, "series")


def _normalize_type(click_type: ChartClickType) -> Literal["categoric_click", "date_click"]:
    return "date_click" if click_type in {"date", "date_click"} else "categoric_click"


def _resolve_category_value(df: pd.DataFrame, column: str, event: dict) -> Any | None:
    values = df[column].dropna()
    by_text = {str(value): value for value in values.unique()}
    for candidate in _event_candidates(event):
        if str(candidate) in by_text:
            return by_text[str(candidate)]
    return None


def _resolve_date_value(df: pd.DataFrame, column: str, event: dict) -> list | None:
    dates = pd.to_datetime(df[column], errors="coerce").dropna()
    if dates.empty:
        return None
    valid_dates = {item.date() for item in dates}
    for candidate in _event_candidates(event):
        if isinstance(candidate, str) and re.fullmatch(r"\d{4}-\d{2}", candidate):
            start = pd.Timestamp(candidate)
            end = start + pd.offsets.MonthEnd(1)
            if dates.between(start, end).any():
                return [start.date(), end.date()]
        parsed = pd.to_datetime(candidate, errors="coerce")
        if not pd.isna(parsed) and parsed.date() in valid_dates:
            return [parsed.date(), parsed.date()]
    return None


def _event_candidates(event: dict) -> list[Any]:
    candidates = [event.get("name"), event.get("seriesName")]
    value = event.get("value")
    if not isinstance(value, (list, tuple, dict)):
        candidates.append(value)
    return [candidate for candidate in candidates if candidate is not None]


def _explicit_filter_value(event: dict) -> Any | None:
    """Obtém o valor anexado pelo builder ao ponto clicado, quando houver."""
    point = event.get("data")
    if isinstance(point, dict):
        return point.get(FILTER_VALUE_KEY)
    return None
