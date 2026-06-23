import pandas as pd
from streamlit_echarts import JsCode
from typing import Literal, Optional, List

from system.core.contexts import AppContext
from system.core.managers.handlers import categoric, date

from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config import (
    BaseChartConfig, ToolboxConfig, LegendConfig, BarSeriesConfig,
    TooltipConfig, GridConfig, MarkLineConfig, SecondaryLineConfig
)

def draw(
    df: pd.DataFrame, 
    title: str,
    column_x: str, 
    columns_y: list, 
    context: AppContext, 
    subtitle: str = None,
    agg_func: Literal["sum", "mean", "min", "max", "count"] = "sum",
    click_type: Literal["categoric", "date"] = "categoric",
    update_context: bool = True,
    show_card: bool = True,
    card_hover: bool = True,
    has_card_title: bool = True,
    height: str = "270px",
    grid: GridConfig = None,
    toolbox: ToolboxConfig = None,
    # 🚀 Alteramos a tipagem aqui para esperar uma Lista de Configs!
    mark_lines: Optional[List[MarkLineConfig]] = None,
    secondary_lines: Optional[List[SecondaryLineConfig]] = None
):
    
    # 1. Agrupamento de Dados Dinâmico
    # (Dica: Se a coluna secundária existir, ela também precisa ir para o groupby!)
    colunas_necessarias = [column_x] + columns_y
    
    # Adiciona as colunas secundárias na lista do groupby para não dar erro
    if secondary_lines:
        for sl in secondary_lines:
            if sl.column not in colunas_necessarias:
                colunas_necessarias.append(sl.column)

    # Faz o groupby dinâmico e aplica a função
    df_agrupado = df[colunas_necessarias].groupby(column_x, as_index=False).agg(agg_func)

    # 2. Configurações da Série de Barras
    series = BarSeriesConfig(
        column_x=column_x, 
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

    if click_type == "date":
        tooltip = TooltipConfig(
            trigger="axis",
            formatter=JsCode("""
                function(params) {
                    // 1. Extrai a data do Eixo X (basta olhar o 1º item do array)
                    let rawDate = params[0].name;
                    let formattedDate = rawDate;
                    
                    // Converte de YYYY-MM-DD para DD/MM/YYYY com segurança
                    if (rawDate && rawDate.indexOf('-') !== -1) {
                        // Pega só a parte da data caso tenha horas (T00:00:00)
                        let datePart = rawDate.split('T')[0];
                        let parts = datePart.split('-');
                        if (parts.length === 3) {
                            formattedDate = parts[2] + '/' + parts[1] + '/' + parts[0];
                        }
                    }

                    // 2. Inicia o HTML do Tooltip com a Data no cabeçalho
                    let html = '<div style="margin-bottom: 6px; font-size: 1.05em; font-weight: bold;">' + '📅' + formattedDate + '</div>';

                    // 3. Itera sobre cada métrica (Profit, Price, Quantity, etc)
                    params.forEach(function(item) {
                        let val = item.value;
                        
                        // Formata o número padrão BR (ponto milhar, vírgula decimal com 2 casas)
                        let formattedVal = (typeof val === 'number') 
                            ? val.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 2}) 
                            : val;

                        // Monta a linha com display:flex para empurrar o número para a direita
                        html += '<div style="display: flex; justify-content: space-between; align-items: center; gap: 32px; line-height: 1.6;">' +
                                '   <div>' + item.marker + ' ' + item.seriesName + '</div>' +
                                '   <div style="font-weight: bold;">' + formattedVal + '</div>' +
                                '</div>';
                    });

                    return html;
                }
            """)
        )

    if grid is None:
        grid = GridConfig(
            show=False, top="10%", bottom="18%"
        )

    config = BaseChartConfig(
        app_name       = context.app_name,
        model          = "bar",
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
    
    # 3. Entrega o dado limpo e agrupado para o ECharts renderizar
    column_x_selected = chart.draw(config, df_agrupado)

    if update_context == True:
        if click_type == "categoric":
            categoric.categoric_chart(column_x, column_x_selected, context)

        elif click_type == "date":
            date.date_chart(column_x, column_x_selected, context)

def meta(valor: float, nome: str = "Meta", cor: str = "#ef4444") -> MarkLineConfig:
    return MarkLineConfig(name=nome, value=valor, color=cor)

def media(nome: str = "Média", cor: str = "#eab308") -> MarkLineConfig:
    return MarkLineConfig(name=nome, calc_type="average", color=cor)

def linha(coluna: str, nome: str = None, cor: str = "#f59e0b", suave: bool = True) -> SecondaryLineConfig:
    """
    Factory para criar uma linha secundária (Gráfico Misto) sobrepondo as barras.
    """
    return SecondaryLineConfig(column=coluna, name=nome, color=cor, smooth=suave)