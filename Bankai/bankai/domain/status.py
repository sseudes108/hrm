"""Modelo de domínio da disponibilidade da aplicação."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationStatus:
    """Representa o estado observável de uma aplicação, sem detalhes de UI."""

    name: str
    is_ready: bool
