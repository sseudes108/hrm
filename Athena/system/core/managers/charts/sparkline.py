import pandas as pd
from typing import Literal

from system.core.contexts import AppContext
from system.core.managers.chart_data import ChartDataError, group_series, prepare_axis_data
from system.core.managers.charts.presets import axis_tooltip
from system.core.managers.charts.interactions import ChartClickType, apply_click_filter
from system.core.managers.charts.payload import attach_filter_values
from system.core.log.view import warnings

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config import (
    BaseChartConfig, TooltipConfig, GridConfig
)
from system.view.components.charts.echarts.config.series.line import LineSeriesConfig

def draw(
    df: pd.DataFrame,
    title: str,
    column_x: str, 
    column_y: str,
    context: AppContext, 
    sparkline_color="success",
    subtitle: str = None,
    agg_func: Literal["sum", "mean", "min", "max", "count"] = "sum",
    click_type: ChartClickType | None = None,
    height: str = "150px",
    update_context: bool = False,
    filter_column: str | None = None,
    date_frequency: str | None = None,
    period_column: str | None = None,
):
    
    resolved_click_type: ChartClickType = click_type or "date_click"

    # Agrupamento Dinâmico
    try:
        chart_df, axis_column = prepare_axis_data(
            df,
            column_x=column_x,
            date_frequency=date_frequency,
            period_column=period_column,
        )
        df_agrupado = group_series(
            chart_df,
            column_x=axis_column,
            columns_y=[column_y],
            aggregation=agg_func,
        )
        if resolved_click_type == "categoric_click":
            df_agrupado = attach_filter_values(
                df_agrupado, chart_df,
                filter_column=filter_column or column_x,
                match_columns=[axis_column],
            )
    except ChartDataError as exc:
        warnings.draw(str(exc), alert="error", context=context)
        return

    # Reutilizamos o LineSeriesConfig, o sparkline_builder saberá lidar com ele
    series = LineSeriesConfig(
        column_x=axis_column, 
        columns_y=[column_y],
        smooth=True,
    )

    tooltip = axis_tooltip(resolved_click_type)

    grid = GridConfig(
        left=5, right=3, bottom=75, top=3
    )

    # O Model "sparkline" aciona o nosso novo builder!
    config = BaseChartConfig(
        app_name        = context.app_name,
        context         = context,
        model           = "sparkline", 
        title           = title,
        subtitle        = subtitle,
        show_card       = False,
        has_card_title  = False,
        card_hover      = False,
        theme           = context.theme,
        height          = height,
        series          = series,
        tooltip         = tooltip,
        grid            = grid,
        sparkline_color = sparkline_color
    )
    
    # Chama o Renderizador Padrão
    clicked = chart.draw(config, df_agrupado, context)
    if update_context:
        apply_click_filter(
            df=chart_df,
            context=context,
            column=filter_column or column_x,
            event_column=axis_column,
            event_data=clicked if isinstance(clicked, dict) else None,
            click_type=resolved_click_type,
        )
