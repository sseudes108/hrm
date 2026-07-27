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
    BaseChartConfig, ToolboxConfig, LegendConfig, BarSeriesConfig,
    GridConfig, MarkLineConfig, SecondaryLineConfig
)

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
    # 🚀 Alteramos a tipagem aqui para esperar uma Lista de Configs!
    mark_lines: Optional[List[MarkLineConfig]] = None,
    secondary_lines: Optional[List[SecondaryLineConfig]] = None
):
    
    resolved_click_type: ChartClickType = click_type or (
        "date_click" if date_frequency else "categoric_click"
    )

    # 1. Agrupamento de Dados Dinâmico
    # (Dica: Se a coluna secundária existir, ela também precisa ir para o groupby!)
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

    # 2. Configurações da Série de Barras
    series = BarSeriesConfig(
        column_x=axis_column, 
        columns_y=columns_y,
        # 🚀 Repassa as variáveis recebidas direto para o Config da série!
        mark_lines=mark_lines,
        secondary_lines=secondary_lines
    )

    if toolbox is None:
        toolbox = ToolboxConfig(
            magic=["line","bar","stack"],
            top="-5%"
        )

    legend  = LegendConfig()

    tooltip = axis_tooltip(resolved_click_type)

    if grid is None:
        grid = GridConfig(
            show=False, top="10%", bottom="18%"
        )

    config = BaseChartConfig(
        app_name       = context.app_name,
        context        = context,
        model          = "bar",
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
    
    # 3. Entrega o dado limpo e agrupado para o ECharts renderizar
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

def meta(valor: float, nome: str = "Meta", cor: str | None = None) -> MarkLineConfig:
    return MarkLineConfig(name=nome, value=valor, color=cor)

def media(nome: str = "Média", cor: str | None = None) -> MarkLineConfig:
    return MarkLineConfig(name=nome, calc_type="average", color=cor, color_token="warning")

def linha(coluna: str, nome: str = None, cor: str | None = None, suave: bool = True) -> SecondaryLineConfig:
    """
    Factory para criar uma linha secundária (Gráfico Misto) sobrepondo as barras.
    """
    return SecondaryLineConfig(column=coluna, name=nome, color=cor, smooth=suave)
