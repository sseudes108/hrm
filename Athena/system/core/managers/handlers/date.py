"""Adaptador legado para interações temporais de gráficos."""

import pandas as pd

from system.core.contexts import AppContext
from system.core.managers.charts.interactions import apply_click_filter


def date_chart(
    column: str,
    event_data: dict,
    context: AppContext,
    df: pd.DataFrame | None = None,
) -> bool:
    if df is None:
        return False
    return apply_click_filter(
        df=df,
        context=context,
        column=column,
        event_data=event_data,
        click_type="date_click",
    )
