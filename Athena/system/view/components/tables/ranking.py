from typing import Any

import pandas as pd

from .base import ColumnConfig, HtmlTableConfig, draw as draw_table


def draw(
    df: pd.DataFrame, *, context: Any, table_id: str, label_column: str,
    value_column: str, title: str = "Ranking", trend_column: str | None = None,
) -> None:
    data = df.copy().sort_values(value_column, ascending=False).reset_index(drop=True)
    data.insert(0, "position", range(1, len(data) + 1))
    columns = [
        ColumnConfig("position", "#", "integer", "center"),
        ColumnConfig(label_column, "Item"),
        ColumnConfig(value_column, "Valor", "currency", "right"),
    ]
    if trend_column:
        columns.append(ColumnConfig(trend_column, "Variação", "trend", "right"))
    draw_table(data, HtmlTableConfig(table_id, columns, title=title, variant="chart"), context)
