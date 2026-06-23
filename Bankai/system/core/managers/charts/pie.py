import pandas as pd
import streamlit as st
from streamlit_echarts import JsCode

from system.core.contexts import AppContext
from system.core.managers.handlers import categoric

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config.base import BaseChartConfig
from system.view.components.charts.echarts.config.toolbox import ToolboxConfig
from system.view.components.charts.echarts.config.legend import LegendConfig
from system.view.components.charts.echarts.config.tooltip import TooltipConfig
from system.view.components.charts.echarts.config.series.pie import PieSeriesConfig

from system.core.log.view import warnings

def draw(
        title:str, 
        subtitle:str, 
        df:pd.DataFrame, 
        column_pie:str,
        context:AppContext,
        column_value:str = None,  
        agg_func:str = "sum",     
        update_context:bool = True,
        show_card:bool = True,
        card_hover:bool = True,
        has_card_title:bool = True,
        height:str = "270px",
        center:list = None,
        radius:list = None,
        toolbox:ToolboxConfig = None,
        tooltip:TooltipConfig = None,
        legend:LegendConfig = None,
        column_emoji:str = ""
    ):

    # 🚀 A MÁGICA DO AGRUPAMENTO (O "Cérebro" do Pie Man)
    if column_value is None:
        # Cenário 1: Conta as ocorrências (Ex: Quantidade de pedidos por Categoria)
        df_agrupado = df[column_pie].value_counts().reset_index()
        # O value_counts() cria uma coluna 'count'. Vamos renomear para 'value' para padronizar.
        df_agrupado.columns = [column_pie, "value"] 
    else:
        # Cenário 2: Faz o cálculo matemático (Ex: Soma do 'Sales' por Categoria)
        df_agrupado = df.groupby(column_pie, as_index=False)[column_value].agg(agg_func)
        # Renomeia a coluna matemática para 'value' também!
        df_agrupado.rename(columns={column_value: "value"}, inplace=True)
    
    if "value" in df_agrupado.columns and (df_agrupado["value"] < 0).any():
        warnings.draw(
            alert="warning",
            message=f"""O gráfico de pizza '{title}' contém valores negativos e não pode ser renderizado corretamente. Considere usar um Gráfico de Barras para essa métrica."""
        )
        return

    if center == None:
        center = ["50%", "40%"]
    if radius == None:
        radius = ["42%", "72%"]
        
    series  = PieSeriesConfig(
        center=center,
        radius=radius,
        column=column_pie # Ele continua sabendo qual é a coluna das fatias (nomes)
    )

    if toolbox == None:
        toolbox = ToolboxConfig(
            restore=False, view=True, left="85%"
        )
    
    if legend == None:
        legend=LegendConfig(
            orientation="horizontal", top="77%"
        )

    if tooltip == None:
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
        model          = "pie",
        title          = title,
        subtitle       = subtitle,
        show_card      = show_card,
        has_card_title = has_card_title,
        card_hover     = card_hover,
        theme          = context.theme,
        height         = height,
        series         = series,
        toolbox        = toolbox,
        legend         = legend,
        tooltip        = tooltip,
    )

    column_pie_selected = chart.draw(config, df_agrupado)
    if update_context == True:
        categoric.categoric_chart(column_pie, column_pie_selected, context)
