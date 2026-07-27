import pandas as pd
from system.core.contexts import AppContext
from system.core.managers.charts.interactions import ChartClickType, apply_click_filter
from system.core.managers.charts.payload import attach_filter_values
from system.core.managers.chart_data import ChartDataError, group_pie

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig
from system.view.components.charts.echarts.config.series.pie import PieSeriesConfig

from system.core.log.view import warnings
from streamlit_echarts import JsCode

def draw(
        title:str, 
        subtitle:str,
        df:pd.DataFrame, 
        column_pie:str,
        context:AppContext,
        column_value:str = None,  
        agg_func:str = "sum",     
        update_context:bool = True,
        click_type: ChartClickType = "categoric_click",
        filter_column: str | None = None,
        show_card:bool = True,
        card_hover:bool = True,
        has_card_title:bool = True,
        card_variant: str = "surface",
        card_padding: str = "normal",
        card_title_case: str = "upper",
        card_title_align: str = "left",
        chart_id: str | None = None,
        height:str = "270px",
        center:list = None,
        radius:list = None,
        toolbox:ToolboxConfig = None,
        tooltip:TooltipConfig = None,
        legend:LegendConfig = None,
        column_emoji:str = ""
    ):

    try:
        df_agrupado = group_pie(
            df,
            category_column=column_pie,
            value_column=column_value,
            aggregation=agg_func,
        )
        if click_type == "categoric_click":
            df_agrupado = attach_filter_values(
                df_agrupado, df,
                filter_column=filter_column or column_pie,
                match_columns=[column_pie],
            )
    except ChartDataError as exc:
        warnings.draw(str(exc), alert="error", context=context)
        return

    if df_agrupado.empty:
        warnings.draw(
            f"O gráfico de pizza '{title}' não possui dados para exibir.",
            alert="info",
            context=context,
        )
        return
    
    if "value" in df_agrupado.columns and (df_agrupado["value"] < 0).any():
        warnings.draw(
            alert="warning",
            message=f"""O gráfico de pizza '{title}' contém valores negativos e não pode ser renderizado corretamente. Considere usar um Gráfico de Barras para essa métrica.""",
            context=context,
        )
        return

    if center is None:
        center = ["50%", "40%"]
    if radius is None:
        radius = ["42%", "72%"]
        
    series  = PieSeriesConfig(
        center=center,
        radius=radius,
        column=column_pie # Ele continua sabendo qual é a coluna das fatias (nomes)
    )

    if toolbox is None:
        toolbox = ToolboxConfig(
            restore=False, view=True, left="85%"
        )
    
    if legend is None:
        legend=LegendConfig(
            orientation="horizontal", top="77%"
        )

    if tooltip is None:
        # 🚀 Injeta o símbolo de moeda no JavaScript apenas se houver coluna de valor
        prefixo_moeda = "$ " if column_value else ""

        tooltip = TooltipConfig(
            trigger="item",
            formatter=JsCode(f"""
                function(params) {{
                    return '{column_emoji}' + params.seriesName + '<br/>' + 
                        params.marker + ' ' + params.name + 
                        '&nbsp;&nbsp;&nbsp;<b>{prefixo_moeda}' + params.value.toLocaleString() + '</b> ' + 
                        '<span style="color:{context.theme["colors"]["text_muted"]}; font-size:0.9em;">(' + params.percent + '%)</span>';
                }}"""
            )
        )

    config = BaseChartConfig(
        app_name       = context.app_name,
        context        = context,
        model          = "pie",
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
        series         = series,
        toolbox        = toolbox,
        legend         = legend,
        tooltip        = tooltip,
    )

    column_pie_selected = chart.draw(config, df_agrupado, context)
    if update_context:
        apply_click_filter(
            df=df,
            context=context,
            column=filter_column or column_pie,
            event_column=column_pie,
            event_data=column_pie_selected,
            click_type=click_type,
        )
