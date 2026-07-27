"""Contratos e registro para aplicações carregadas pelo sistema."""

from .contracts import ApplicationDefinition, ApplicationStateFactory, ThemeLoader
from .registry import ApplicationRegistry, registry

__all__ = [
    "ApplicationDefinition",
    "ApplicationRegistry",
    "ApplicationStateFactory",
    "ThemeLoader",
    "registry",
]
