import json
from pathlib import Path
from collections.abc import Mapping
from typing import Any

from .theme_schema import ThemeValidationError, normalize_and_validate
from .mapping import deep_merge

def merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Combina mapas de tema sem conhecer sua origem ou aplicação dona."""
    return deep_merge(base, override)

def load(base_path: Path, override_path: Path) -> dict[str, Any]:
    """Lê, combina, normaliza e valida os arquivos explícitos de um tema."""
    base = _load_json(base_path)
    override = _load_json(override_path)
    source = f"{base_path.name} + {override_path.name}"
    return normalize_and_validate(merge(base, override), source=source)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as theme_file:
            content = json.load(theme_file)
    except json.JSONDecodeError as exc:
        raise ThemeValidationError(
            f"Tema '{path}': JSON inválido na linha {exc.lineno}, coluna {exc.colno}."
        ) from exc

    if not isinstance(content, dict):
        raise ThemeValidationError(f"Tema '{path}': a raiz deve ser um objeto JSON.")
    return content
