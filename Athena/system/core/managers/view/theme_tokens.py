"""Compilação genérica de temas JSON em variáveis CSS."""

import re
from collections.abc import Mapping
from typing import Any


def compile_css_variables(theme: Mapping[str, Any], *, prefix: str = "--ui") -> str:
    """Converte todos os tokens primitivos em variáveis CSS previsíveis.

    Exemplo: ``components.card.radius`` torna-se
    ``--ui-components-card-radius``. Não é necessário alterar este módulo para
    publicar novos tokens de uma aplicação.
    """
    declarations = [
        f"{_variable_name(prefix, path)}: {_css_value(value, path)};"
        for path, value in _flatten(theme)
    ]
    return "\n".join(f"    {declaration}" for declaration in declarations)


def _flatten(value: Any, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    if isinstance(value, Mapping):
        tokens: list[tuple[tuple[str, ...], Any]] = []
        for key in sorted(value):
            tokens.extend(_flatten(value[key], (*path, str(key))))
        return tokens

    if isinstance(value, list):
        if all(isinstance(item, (str, int, float)) and not isinstance(item, bool) for item in value):
            return [(path, ", ".join(str(item) for item in value))]
        return []

    if isinstance(value, (str, int, float, bool)) and not isinstance(value, type(None)):
        return [(path, value)]
    return []


def _variable_name(prefix: str, path: tuple[str, ...]) -> str:
    normalized_path = "-".join(_normalize_part(part) for part in path)
    return f"{prefix}-{normalized_path}"


def _normalize_part(part: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", part.lower()).strip("-")
    return normalized or "token"


def _css_value(value: Any, path: tuple[str, ...]) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if (
        isinstance(value, (int, float))
        and len(path) == 2
        and path[0] == "typography"
        and path[1].startswith("size_")
    ):
        return f"{value}px"
    return str(value)
