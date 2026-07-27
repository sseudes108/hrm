from typing import Any

import pandas as pd

from .base import ColumnConfig, HtmlTableConfig, draw as draw_table


def draw(df: pd.DataFrame, *, context: Any, table_id: str, columns: list[ColumnConfig], title: str = "Resumo") -> None:
    draw_table(df, HtmlTableConfig(table_id, columns, title=title, variant="surface"), context)
