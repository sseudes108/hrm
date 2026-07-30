"""Persistência técnica das preferências visuais entre sessões Streamlit."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import RLock
from typing import Any


PREFERENCES_VERSION = 1
DEFAULT_PREFERENCES_PATH = (
    Path(__file__).resolve().parents[4] / ".streamlit" / "runtime_preferences.json"
)
_PREFERENCES_LOCK = RLock()


def load_theme_mode(
    app_id: str,
    default_mode: str,
    *,
    path: Path | None = None,
) -> str:
    """Recupera o último modo salvo para uma aplicação.

    Arquivos ausentes ou JSON inválido não impedem a inicialização: nesses
    casos, o modo padrão declarado pela aplicação é usado.
    """
    normalized_app_id = _normalize_identifier(app_id, field_name="app_id")
    normalized_default = _normalize_identifier(default_mode, field_name="default_mode")
    preferences_path = path or DEFAULT_PREFERENCES_PATH

    with _PREFERENCES_LOCK:
        preferences = _read_preferences(preferences_path)

    theme_modes = preferences.get("theme_modes", {})
    if not isinstance(theme_modes, dict):
        return normalized_default
    stored_mode = theme_modes.get(normalized_app_id)
    if not isinstance(stored_mode, str):
        return normalized_default
    try:
        return _normalize_identifier(stored_mode, field_name="theme_mode")
    except ValueError:
        return normalized_default


def save_theme_mode(app_id: str, mode: str, *, path: Path | None = None) -> None:
    """Salva atomicamente o modo visual de uma aplicação."""
    normalized_app_id = _normalize_identifier(app_id, field_name="app_id")
    normalized_mode = _normalize_identifier(mode, field_name="theme_mode")
    preferences_path = path or DEFAULT_PREFERENCES_PATH

    with _PREFERENCES_LOCK:
        preferences = _read_preferences(preferences_path)
        theme_modes = preferences.setdefault("theme_modes", {})
        if not isinstance(theme_modes, dict):
            theme_modes = {}
            preferences["theme_modes"] = theme_modes
        theme_modes[normalized_app_id] = normalized_mode
        preferences["version"] = PREFERENCES_VERSION
        _write_preferences(preferences_path, preferences)


def _read_preferences(path: Path) -> dict[str, Any]:
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return _empty_preferences()
    if not isinstance(content, dict):
        return _empty_preferences()
    return content


def _write_preferences(path: Path, preferences: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            json.dump(preferences, temporary_file, ensure_ascii=False, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _empty_preferences() -> dict[str, Any]:
    return {"version": PREFERENCES_VERSION, "theme_modes": {}}


def _normalize_identifier(value: str, *, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} deve ser uma string")
    normalized = value.strip().lower()
    if not normalized or not normalized.replace("-", "_").isidentifier():
        raise ValueError(f"{field_name} deve ser um identificador simples e não vazio")
    return normalized
