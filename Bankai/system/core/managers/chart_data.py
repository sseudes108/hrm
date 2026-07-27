"""Preparação e validação compartilhadas dos dados usados pelos gráficos."""

from collections.abc import Iterable

import pandas as pd


class ChartDataError(ValueError):
    """Indica que os dados recebidos não atendem ao contrato do gráfico."""


_PERIOD_SUFFIXES = {
    "D": "day",
    "W": "week",
    "M": "month",
    "Q": "quarter",
    "Y": "year",
}


def period_column_name(source_column: str, frequency: str) -> str:
    """Gera um nome estável para a coluna visual de período.

    ``open_date`` com frequência mensal, por exemplo, torna-se
    ``open_month``. O valor é apenas uma dimensão de exibição; a coluna de
    origem continua sendo a referência para os filtros de dados.
    """
    normalized = frequency.upper()
    suffix = _PERIOD_SUFFIXES.get(normalized, normalized.lower())
    stem = source_column.removesuffix("_date")
    return f"{stem}_{suffix}"


def add_period_column(
    df: pd.DataFrame,
    *,
    source_column: str,
    frequency: str,
    target_column: str | None = None,
) -> pd.DataFrame:
    """Retorna uma cópia enriquecida com uma dimensão temporal para gráficos."""
    _require_columns(df, [source_column])
    target = target_column or period_column_name(source_column, frequency)
    if target == source_column:
        raise ChartDataError("A coluna de período deve ser diferente da coluna de origem.")

    dates = pd.to_datetime(df[source_column], errors="coerce")
    if dates.notna().sum() == 0:
        raise ChartDataError(f"A coluna '{source_column}' não possui datas válidas.")
    try:
        periods = dates.dt.to_period(frequency)
    except ValueError as exc:
        raise ChartDataError(f"Frequência de período inválida: '{frequency}'.") from exc

    enriched = df.copy()
    enriched[target] = periods.astype("string")
    return enriched


def prepare_axis_data(
    df: pd.DataFrame,
    *,
    column_x: str,
    date_frequency: str | None = None,
    period_column: str | None = None,
) -> tuple[pd.DataFrame, str]:
    """Prepara o eixo X, derivando períodos quando uma frequência é informada."""
    if not date_frequency:
        return df, column_x
    axis_column = period_column or period_column_name(column_x, date_frequency)
    return (
        add_period_column(
            df,
            source_column=column_x,
            frequency=date_frequency,
            target_column=axis_column,
        ),
        axis_column,
    )


def group_series(
    df: pd.DataFrame,
    *,
    column_x: str,
    columns_y: Iterable[str],
    aggregation: str,
    secondary_columns: Iterable[str] = (),
) -> pd.DataFrame:
    """Valida as colunas e agrega séries sem conhecer a camada visual."""
    required = _unique((column_x, *columns_y, *secondary_columns))
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ChartDataError(f"Colunas não encontradas: {missing}")
    return df[required].groupby(column_x, as_index=False).agg(aggregation)


def group_pie(
    df: pd.DataFrame,
    *,
    category_column: str,
    value_column: str | None = None,
    aggregation: str = "sum",
) -> pd.DataFrame:
    """Agrupa dados de pizza no contrato ``categoria``/``value`` do ECharts."""
    required = [category_column] + ([value_column] if value_column else [])
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ChartDataError(f"Colunas não encontradas para o gráfico: {missing}")

    data = df[required].dropna(subset=[category_column])
    if value_column is None:
        return (
            data.groupby(category_column, as_index=False)
            .size()
            .rename(columns={"size": "value"})
        )

    return data.groupby(category_column, as_index=False)[value_column].agg(aggregation).rename(
        columns={value_column: "value"}
    )


def prepare_scatter(
    df: pd.DataFrame,
    *,
    column_x: str,
    column_y: str,
    size_column: str | None = None,
    category_column: str | None = None,
    extra_columns: Iterable[str] = (),
) -> pd.DataFrame:
    """Valida e remove linhas inválidas de uma série de dispersão."""
    required = _unique((
        column_x, column_y,
        *(value for value in (size_column, category_column) if value),
        *extra_columns,
    ))
    _require_columns(df, required)
    return df[required].dropna(subset=[column_x, column_y]).copy()


def prepare_radar(
    df: pd.DataFrame, *, label_column: str, indicator_columns: Iterable[str]
) -> pd.DataFrame:
    """Agrega indicadores numéricos por entidade para um gráfico radar."""
    indicators = list(indicator_columns)
    if not indicators:
        raise ChartDataError("O gráfico radar requer ao menos um indicador.")
    _require_columns(df, _unique((label_column, *indicators)))
    data = df[[label_column, *indicators]].dropna(subset=[label_column]).copy()
    for column in indicators:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data.groupby(label_column, as_index=False)[indicators].mean().fillna(0)


def prepare_boxplot(
    df: pd.DataFrame, *, category_column: str, value_column: str
) -> pd.DataFrame:
    """Calcula min, quartis, mediana e máximo por categoria."""
    _require_columns(df, [category_column, value_column])
    data = df[[category_column, value_column]].dropna(subset=[category_column]).copy()
    data[value_column] = pd.to_numeric(data[value_column], errors="coerce")
    data = data.dropna(subset=[value_column])
    if data.empty:
        return pd.DataFrame(columns=[category_column, "min", "q1", "median", "q3", "max"])
    return data.groupby(category_column)[value_column].agg(
        min="min",
        q1=lambda values: values.quantile(0.25),
        median="median",
        q3=lambda values: values.quantile(0.75),
        max="max",
    ).reset_index()


def prepare_heatmap(
    df: pd.DataFrame,
    *,
    column_x: str,
    column_y: str,
    value_column: str,
    aggregation: str = "sum",
) -> pd.DataFrame:
    """Agrega uma matriz categórica X/Y para o heatmap."""
    _require_columns(df, [column_x, column_y, value_column])
    data = df[[column_x, column_y, value_column]].dropna(subset=[column_x, column_y]).copy()
    data[value_column] = pd.to_numeric(data[value_column], errors="coerce")
    return data.dropna(subset=[value_column]).groupby(
        [column_x, column_y], as_index=False
    )[value_column].agg(aggregation)


def prepare_sunburst(
    df: pd.DataFrame, *, path_columns: Iterable[str], value_column: str,
    filter_column: str | None = None,
) -> list[dict]:
    """Converte um DataFrame plano em nós hierárquicos aceitos pelo ECharts."""
    path = list(path_columns)
    if not path:
        raise ChartDataError("O gráfico sunburst requer ao menos uma coluna de hierarquia.")
    _require_columns(df, _unique((*path, value_column)))
    columns = [*path, value_column]
    if filter_column and filter_column in df.columns and filter_column not in columns:
        columns.append(filter_column)
    data = df[columns].dropna(subset=path).copy()
    data[value_column] = pd.to_numeric(data[value_column], errors="coerce")
    data = data.dropna(subset=[value_column])

    def build_level(current: pd.DataFrame, level: int) -> list[dict]:
        column = path[level]
        nodes: list[dict] = []
        for name, group in current.groupby(column, sort=True):
            node: dict = {"name": str(name), "value": float(group[value_column].sum())}
            if filter_column and filter_column in group.columns:
                node["__zanpakutou_filter_value"] = _collapse_node_values(group[filter_column])
            if level + 1 < len(path):
                node["children"] = build_level(group, level + 1)
            nodes.append(node)
        return nodes

    return build_level(data, 0) if not data.empty else []


def _collapse_node_values(values: pd.Series):
    unique = list(dict.fromkeys(value.item() if hasattr(value, "item") else value for value in values.dropna()))
    return unique[0] if len(unique) == 1 else unique


def _unique(columns: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(columns))


def _require_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ChartDataError(f"Colunas não encontradas para o gráfico: {missing}")
