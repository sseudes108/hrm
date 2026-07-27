"""Metadados de interação transportados nos pontos renderizados pelo ECharts."""

from collections.abc import Iterable
from typing import Any

import pandas as pd


FILTER_VALUE_KEY = "__zanpakutou_filter_value"


def attach_filter_values(
    display_df: pd.DataFrame,
    source_df: pd.DataFrame,
    *,
    filter_column: str | None,
    match_columns: Iterable[str],
) -> pd.DataFrame:
    """Acrescenta ao dado visual o valor real que deve ser filtrado.

    Um ponto pode representar uma ou várias linhas da base. Nesse segundo
    caso, o metadado é uma lista de valores únicos; ``apply_filters`` já a
    interpreta com ``isin``. Se alguma coluna não existir, a função devolve
    os dados originais sem falhar, mantendo o gráfico reutilizável.
    """
    keys = list(dict.fromkeys(match_columns))
    if (
        not filter_column
        or filter_column not in source_df.columns
        or not keys
        or any(column not in source_df.columns or column not in display_df.columns for column in keys)
    ):
        return display_df

    if filter_column in keys:
        enriched = display_df.copy()
        enriched[FILTER_VALUE_KEY] = enriched[filter_column].map(_native)
        return enriched

    source = source_df[[*keys, filter_column]].dropna(subset=[filter_column])
    if source.empty:
        return display_df
    values = (
        source.groupby(keys, dropna=False)[filter_column]
        .agg(_collapse_values)
        .reset_index(name=FILTER_VALUE_KEY)
    )
    return display_df.merge(values, on=keys, how="left")


def _collapse_values(values: pd.Series) -> Any:
    unique = list(dict.fromkeys(_native(value) for value in values.tolist()))
    return unique[0] if len(unique) == 1 else unique


def _native(value: Any) -> Any:
    if isinstance(value, (list, tuple)):
        return [_native(item) for item in value]
    return value.item() if hasattr(value, "item") else value


def point_filter_metadata(row: Any) -> dict[str, Any]:
    """Retorna somente metadados serializáveis e presentes para um ponto."""
    value = row.get(FILTER_VALUE_KEY) if hasattr(row, "get") else None
    if value is None or (not isinstance(value, (list, tuple, set)) and pd.isna(value)):
        return {}
    return {FILTER_VALUE_KEY: _native(value)}
