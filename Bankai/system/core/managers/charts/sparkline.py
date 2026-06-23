import pandas as pd
from typing import Literal

from system.core.contexts import AppContext
from streamlit_echarts import JsCode

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
    click_type: Literal["categoric", "date"] = "date",
    height: str = "150px"
):
    
    # Agrupamento Dinâmico
    df_agrupado = df[[column_x, column_y]].groupby(column_x, as_index=False).agg(agg_func)

    # Reutilizamos o LineSeriesConfig, o sparkline_builder saberá lidar com ele
    series = LineSeriesConfig(
        column_x=column_x, 
        columns_y=[column_y],
        smooth=True,
    )

    # Tooltip customizado
    if click_type == "date":
        tooltip = TooltipConfig(
            trigger="axis",
            formatter=JsCode("""
                function(params) {
                    let rawDate = params[0].name;
                    let formattedDate = rawDate;
                    if (rawDate && rawDate.indexOf('-') !== -1) {
                        let datePart = rawDate.split('T')[0];
                        let parts = datePart.split('-');
                        if (parts.length === 3) {
                            formattedDate = parts[2] + '/' + parts[1] + '/' + parts[0];
                        }
                    }
                    let html = '<div style="margin-bottom: 6px; font-size: 1.05em; font-weight: bold;">' + '📅' + formattedDate + '</div>';
                    params.forEach(function(item) {
                        let val = item.value;
                        let formattedVal = (typeof val === 'number') 
                            ? val.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 2}) 
                            : val;
                        html += '<div style="display: flex; justify-content: space-between; align-items: center; gap: 32px; line-height: 1.6;">' +
                                '   <div>' + item.marker + ' ' + item.seriesName + '</div>' +
                                '   <div style="font-weight: bold;">' + formattedVal + '</div>' +
                                '</div>';
                    });
                    return html;
                }
            """)
        )
    else:
        tooltip = TooltipConfig(trigger="axis") # Tooltip padrão para categórico

    grid = GridConfig(
        left=5, right=3, bottom=75, top=3
    )

    # O Model "sparkline" aciona o nosso novo builder!
    config = BaseChartConfig(
        app_name        = context.app_name,
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
    chart.draw(config, df_agrupado, context)