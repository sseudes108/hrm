"""Estado e transições de navegação pertencentes à Athena."""

from dataclasses import dataclass, field
from typing import Any

import streamlit as st


@dataclass
class AthenaState:
    current_route: str
    active_filters: dict[str, object] = field(default_factory=dict)
    payload: Any | None = None

    def navigate(self, route: str) -> None:
        self.current_route = route

    def update_filter(self, column: str, value: object, rerun: bool = True) -> bool:
        if self.active_filters.get(column) == value:
            return False
        self.active_filters[column] = value
        if rerun:
            st.rerun()
        return True


def create_state(initial_route: str) -> AthenaState:
    return AthenaState(current_route=initial_route)
