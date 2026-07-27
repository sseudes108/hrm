import pandas as pd
from typing import Literal, Optional, List

from system.core.contexts import AppContext
from system.core.managers.charts.interactions import ChartClickType, apply_click_filter
from system.core.managers.charts.payload import attach_filter_values
from system.core.managers.chart_data import ChartDataError, group_series, prepare_axis_data
from system.core.managers.charts.presets import axis_tooltip
from system.core.log.view import warnings

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config import (
    BaseChartConfig, ToolboxConfig, LegendConfig, GridConfig,
    MarkLineConfig, SecondaryLineConfig
)
# 🚀 Importa o novo LineSeriesConfig
from system.view.components.charts.echarts.config.series.line import LineSeriesConfig

def draw(
    df: pd.DataFrame, 
    title: str,
    column_x: str, 
    columns_y: list, 
    context: AppContext, 
    subtitle: str = None,
    agg_func: Literal["sum", "mean", "min", "max", "count"] = "sum",
    click_type: ChartClickType | None = None,
    filter_column: str | None = None,
    date_frequency: str | None = None,
    period_column: str | None = None,
    smooth: bool = True,            # Opção de curvar as linhas
    step: str = "start",
    fill_area: bool = False,        # Opção de pintar embaixo da linha
    update_context: bool = True,
    show_card: bool = True,
    card_hover: bool = True,
    has_card_title: bool = True,
    card_variant: str = "surface",
    card_padding: str = "normal",
    card_title_case: str = "upper",
    card_title_align: str = "left",
    chart_id: str | None = None,
    height: str = "270px",
    grid: GridConfig = None,
    toolbox: ToolboxConfig = None,
    mark_lines: Optional[List[MarkLineConfig]] = None,
    secondary_lines: Optional[List[SecondaryLineConfig]] = None
):
    
    resolved_click_type: ChartClickType = click_type or (
        "date_click" if date_frequency else "categoric_click"
    )

    # 1. Agrupamento Dinâmico (Mesma lógica das barras)
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
            columns_y=columns_y,
            secondary_columns=(line.column for line in secondary_lines or ()),
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

    # 2. Configuração da Série usando LineSeriesConfig
    series = LineSeriesConfig(
        column_x=axis_column, 
        columns_y=columns_y,
        smooth=smooth,
        step=step,
        fill_area=fill_area,
        mark_lines=mark_lines,
        secondary_lines=secondary_lines
    )

    if toolbox is None:
        toolbox = ToolboxConfig(magic=["bar","line","stack"], top="-5%")

    legend  = LegendConfig()

    tooltip = axis_tooltip(resolved_click_type)

    if grid is None:
        grid = GridConfig(show=False, top="10%", bottom="18%")

    # 🚀 O Model aqui é "line" para que o dispatcher saiba quem chamar!
    config = BaseChartConfig(
        app_name       = context.app_name,
        context        = context,
        model          = "line", 
        title          = title,
        subtitle       = subtitle,
        show_card      = show_card,
        has_card_title = has_card_title,
        card_hover     = card_hover,
        card_variant   = card_variant,
        card_padding   = card_padding,
        card_title_case = card_title_case,
        card_title_align = card_title_align,
        chart_id         = chart_id,
        theme          = context.theme,
        height         = height,
        grid           = grid,
        series         = series,
        toolbox        = toolbox,
        legend         = legend,
        tooltip        = tooltip,
    )
    
    # 3. Chama o Renderizador Padrão
    column_x_selected = chart.draw(config, df_agrupado, context)

    if update_context:
        apply_click_filter(
            df=chart_df,
            context=context,
            column=filter_column or column_x,
            event_column=axis_column,
            event_data=column_x_selected,
            click_type=resolved_click_type,
        )
