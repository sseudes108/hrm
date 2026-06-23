import pandas as pd
from streamlit_echarts import JsCode
from typing import Literal, Optional, List

from system.core.contexts import AppContext
from system.core.managers.handlers import categoric, date

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config import (
    BaseChartConfig, ToolboxConfig, LegendConfig, TooltipConfig, GridConfig, 
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
    click_type: Literal["categoric", "date"] = "categoric",
    smooth: bool = True,            # Opção de curvar as linhas
    step:str = "start",
    fill_area: bool = False,        # Opção de pintar embaixo da linha
    update_context: bool = True,
    show_card: bool = True,
    card_hover: bool = True,
    has_card_title: bool = True,
    height: str = "270px",
    grid: GridConfig = None,
    toolbox: ToolboxConfig = None,
    mark_lines: Optional[List[MarkLineConfig]] = None,
    secondary_lines: Optional[List[SecondaryLineConfig]] = None
):
    
    # 1. Agrupamento Dinâmico (Mesma lógica das barras)
    colunas_necessarias = [column_x] + columns_y
    if secondary_lines:
        for sl in secondary_lines:
            if sl.column not in colunas_necessarias:
                colunas_necessarias.append(sl.column)

    df_agrupado = df[colunas_necessarias].groupby(column_x, as_index=False).agg(agg_func)

    # 2. Configuração da Série usando LineSeriesConfig
    series = LineSeriesConfig(
        column_x=column_x, 
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

    if grid is None:
        grid = GridConfig(show=False, top="10%", bottom="18%")

    # 🚀 O Model aqui é "line" para que o dispatcher saiba quem chamar!
    config = BaseChartConfig(
        app_name       = context.app_name,
        model          = "line", 
        title          = title,
        subtitle       = subtitle,
        show_card      = show_card,
        has_card_title = has_card_title,
        card_hover     = card_hover,
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

    if update_context == True:
        if click_type == "categoric":
            categoric.categoric_chart(column_x, column_x_selected, context)
        elif click_type == "date":
            date.date_chart(column_x, column_x_selected, context)