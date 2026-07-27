"""Aplicação determinística de filtros de estado sobre DataFrames."""

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

import pandas as pd


def apply_filters(df: pd.DataFrame, filters: Mapping[str, Any]) -> pd.DataFrame:
    """Retorna uma cópia filtrada, ignorando chaves que não existam no DataFrame.

    Valores escalares usam igualdade; coleções usam ``isin``; pares de datas
    são interpretados como intervalo inclusivo. Essa função não conhece estado
    nem Streamlit, portanto pode ser reutilizada e testada isoladamente.
    """
    filtered = df
    for column, value in filters.items():
        if column not in filtered.columns or _is_no_filter(value):
            continue
        if _is_date_range(value):
            filtered = _filter_date_range(filtered, column, value)
        elif isinstance(value, (list, tuple, set, frozenset)):
            filtered = filtered.loc[filtered[column].isin(value)]
        else:
            filtered = filtered.loc[filtered[column] == value]
    return filtered.copy()


def _is_date_range(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and len(value) == 2
        and all(isinstance(item, (date, datetime, pd.Timestamp)) for item in value)
    )


def _is_no_filter(value: Any) -> bool:
    return value is None or value == "" or value == "Todos"


def _filter_date_range(df: pd.DataFrame, column: str, values: list | tuple) -> pd.DataFrame:
    start, end = (pd.Timestamp(item) for item in values)
    dates = pd.to_datetime(df[column], errors="coerce")
    return df.loc[dates.between(start, end)]
