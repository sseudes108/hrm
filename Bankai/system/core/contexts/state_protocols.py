"""Contratos opcionais de estado consumidos por componentes compartilhados."""

from collections.abc import MutableMapping
from typing import Protocol, runtime_checkable


@runtime_checkable
class FilterState(Protocol):
    """Estado mínimo para filtros visuais bidirecionais."""

    active_filters: MutableMapping[str, object]

    def update_filter(self, column: str, value: object, rerun: bool = True) -> bool: ...

    def remove_filter(self, column: str, rerun: bool = True) -> bool: ...


@runtime_checkable
class ChartFilterState(FilterState, Protocol):
    """Extensão usada por interações de gráficos."""

    def get_last_event_ts(self, column: str) -> int | None: ...

    def set_last_event_ts(self, column: str, timestamp: int) -> None: ...


def require_filter_state(context) -> FilterState:
    """Obtém o contrato de filtros ou informa claramente o requisito ausente."""
    state = getattr(context, "state", None)
    if not isinstance(state, FilterState):
        raise TypeError(
            "O componente requer um estado com active_filters, update_filter() e remove_filter()."
        )
    return state


def require_chart_filter_state(context) -> ChartFilterState:
    """Obtém o contrato de interação de gráficos."""
    state = getattr(context, "state", None)
    if not isinstance(state, ChartFilterState):
        raise TypeError(
            "O handler de gráfico requer o contrato FilterState e os métodos de eventos do gráfico."
        )
    return state
