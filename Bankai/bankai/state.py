"""Estado e transições de navegação pertencentes à aplicação Bankai."""

from dataclasses import dataclass, field

import streamlit as st


@dataclass
class BankaiState:
    """Fonte de verdade da aplicação, persistida em ``st.session_state['bankai']``."""

    current_route: str
    active_filters: dict[str, object] = field(default_factory=dict)
    show_details: bool = False
    _processed_events: dict[str, int] = field(default_factory=dict)

    def navigate(self, route: str) -> None:
        """Seleciona uma rota da aplicação; a validação é feita pelo registro de rotas."""
        self.current_route = route

    def update_filter(self, column: str, value: object, rerun: bool = True) -> bool:
        if self.active_filters.get(column) == value:
            return False
        self.active_filters[column] = value
        if rerun:
            st.rerun()
        return True

    def remove_filter(self, column: str, rerun: bool = True) -> bool:
        if column not in self.active_filters:
            return False
        del self.active_filters[column]
        if rerun:
            st.rerun()
        return True

    def clear_all(self) -> None:
        self.active_filters.clear()
        self.show_details = False

    def get_last_event_ts(self, column: str) -> int | None:
        return self._processed_events.get(column)

    def set_last_event_ts(self, column: str, timestamp: int) -> None:
        self._processed_events[column] = timestamp


def create_state(initial_route: str) -> BankaiState:
    """Fábrica consumida pelo contrato de aplicação."""
    return BankaiState(current_route=initial_route)
