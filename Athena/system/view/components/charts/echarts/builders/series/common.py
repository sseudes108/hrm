"""Blocos reutilizáveis dos builders de séries cartesianas."""

from collections.abc import Iterable
from typing import Any

import pandas as pd

from system.core.log.view import warnings
from system.core.managers.charts.payload import FILTER_VALUE_KEY, point_filter_metadata


def validate_columns(
    df: pd.DataFrame,
    *,
    column_x: str,
    columns_y: Iterable[str],
    config_name: str,
    context: Any,
) -> bool:
    """Valida as colunas antes de o builder acessar o DataFrame."""
    missing = [column for column in (column_x, *columns_y) if column not in df.columns]
    if not missing:
        return True

    warnings.draw(
        f"{config_name} — colunas não encontradas: {missing}",
        alert="error",
        context=context,
    )
    return False


def axis_style(echarts_config: dict) -> dict:
    return {
        "axisLine": {"lineStyle": {"color": echarts_config["axis_line_color"]}},
        "axisLabel": {"color": echarts_config["axis_label_color"]},
        "splitLine": {"lineStyle": {"color": echarts_config["split_line_color"]}},
    }


def apply_grid(options: dict, grid: Any) -> None:
    if grid is None:
        return
    options["grid"] = {
        "show": grid.show,
        "left": grid.left,
        "right": grid.right,
        "bottom": grid.bottom,
        "top": grid.top,
        "containLabel": grid.contain_label,
    }


def theme_color(config: Any, theme: dict) -> str:
    """Prioriza uma cor explícita e usa o token de severidade como fallback."""
    return config.color or theme["chart"]["severity"][config.color_token]


def point_value(value: Any, row: pd.Series) -> Any:
    """Mantém o formato simples, exceto quando o ponto possui filtro real."""
    metadata = point_filter_metadata(row)
    if not metadata:
        return _native(value)
    return {"value": _native(value), **metadata}


def _native(value: Any) -> Any:
    if isinstance(value, list):
        return [_native(item) for item in value]
    return value.item() if hasattr(value, "item") else value
