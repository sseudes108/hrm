

def teste_line_echarts(theme):
    col1, col2 = st.columns([1,1], gap='xsmall')
    with col1:
        data_simples = {
            "x": ["Seg", "Ter", "Qua"],
            "y": {"Arjuna": [10, 20, 15]},
            "toolbox": {"magic": ["line", "bar"]}
        }
        draw_linhas_chart(
            theme=theme, 
            data=data_simples,
            title="Evolução de Dharma",
            subtitle="Análise semanal de alinhamento cósmico",
            value="98.2%",
            value_sub="Média por Dia"
        )

    with col2:
        data_simples = {
            "x": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"],
            "y": {
                "Arjuna (Precisão)": [820, 932, 901, 934, 1290, 1330, 1320],
                "Karna (Poder)": [850, 1132, 701, 634, 1090, 1930, 920],
                "Bishma (Poder)": [880, 1032, 801, 734, 1590, 2930, 1020]
            },
            "toolbox": {"magic": ["line", "bar", "stack"]}
        }
        draw_linhas_chart(
            theme=theme,
            data=data_simples,
            key="l2"
        )

from system.view.components.charts.echarts.linhas import draw_linhas_chart
from system.view.components.cards.index import (
    sparkline_metric
)
import streamlit as st
from system.control.contexts.dash import DashboardContext
from system.view.components.layout.header import draw_header
from system.view.components.filters.select import draw_select_filter

def main(context:DashboardContext):
    theme = context.theme
    draw_header(
        theme=theme, title="Bankai", icon="⚔️", 
        ticker=True, background=False,
        key="header_bankai",
        context=context
    )

    st.write("")
    st.write("")
    st.write("")

    cols = st.columns(3)
    with cols[0]:
        options = ["t1","t2","t3"]
        filter = draw_select_filter("Options", options=options, theme=theme)
        st.write(filter)
        
    with cols[1]:
        options = ["t1","t2","t3"]
        filter = draw_select_filter("Options - 1", options=options, label_width="5.5", theme=theme)
        st.write(filter)

    with cols[2]:
        options = ["t1","t2","t3"]
        filter = draw_select_filter("Options - 2", options=options, label_width="5.5", theme=theme)
        st.write(filter)

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        # 1. Defina as opções do Sparkline ECharts (Design "Invisível")
        data_simples = {
            "x": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"],
            "y": {
                "Arjuna (Precisão)": [820, 932, 901, 934, 1290, 1330, 1320]
            }
        }

        # 2. Faça a chamada do Card Híbrido
        sparkline_metric(
            theme=theme,
            titulo="Entradas",
            valor="98%",
            icone="zap", # Ícone Lucide agora ao lado do título
            secundario_valor="+4.2%",
            secundario_label="vs ontem",
            cor="success",
            tooltip="Acumulado\nno arco Pain",
            border_radius="8px"
        )

    with col2:
        data_simples = {
            "x": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"],
            "y": {
                "Karna (Poder)": [650, 2132, 1001, 634, 1090, 1530, 520],
            }
        }

        # 2. Faça a chamada do Card Híbrido
        sparkline_metric(
            theme=theme,
            titulo="Saidas",
            valor="98%",
            icone="zap", # Ícone Lucide agora ao lado do título
            show_spark=True,
            sparkline_data=data_simples, # O gráfico aninhado
            secundario_valor="+4.2%",
            secundario_label="vs ontem",
            cor="warning",
            tooltip="Acumulado\nno arco Pain"
        )
    with col3:
        # 1. Defina as opções do Sparkline ECharts (Design "Invisível")
        data_simples = {
            "x": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"],
            "y": {
                "Bishma (Poder)": [880, 1032, 801, 734, 1590, 2930, 1020]
            }
        }

        # 2. Faça a chamada do Card Híbrido
        sparkline_metric(
            theme=theme,
            titulo="Chakra Total",
            valor="98%",
            icone="zap", # Ícone Lucide agora ao lado do título
            show_spark=True,
            sparkline_data=data_simples, # O gráfico aninhado
            secundario_valor="+4.2%",
            secundario_label="vs ontem",
            cor="danger",
            tooltip="Acumulado\nno arco Pain"
        )

    st.divider()
    teste_line_echarts(theme)