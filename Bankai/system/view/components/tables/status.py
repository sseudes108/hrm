from typing import Any

import pandas as pd

from .base import ColumnConfig, HtmlTableConfig, draw as draw_table


def draw(
    df: pd.DataFrame, *, context: Any, table_id: str, label_column: str,
    status_column: str, value_column: str | None = None, title: str = "Status",
) -> None:
    columns = [ColumnConfig(label_column, "Item"), ColumnConfig(status_column, "Status", "badge")]
    if value_column:
        columns.append(ColumnConfig(value_column, "Valor", "currency", "right"))
    draw_table(df, HtmlTableConfig(table_id, columns, title=title, variant="surface"), context)
