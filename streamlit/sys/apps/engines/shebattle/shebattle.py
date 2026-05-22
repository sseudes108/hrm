"""
app.py — Bankai 
Ponto de entrada do projeto.
Para trocar o tema, altere apenas a string em get_theme().
"""

import streamlit as st
from system.control.managers.data import get_data_json
from system.view.components.layout.header import draw_header
from system.control.contexts.dash import DashboardContext
from system.view.components.filters.select import draw_select_filter
import system.control.managers.filter as filter_man

def main(context:DashboardContext):
    theme = context.theme
    with st.container():
        draw_header(theme=theme, title="She Battle", icon="🏳️‍⚧️", context=context)

    df = get_data_json("apps/engines/shebattle/data/she_base.json")
    df_filtrado = filter_man.apply_filters(df, context.active_filters)

    list_names = df_filtrado["nome"].unique().tolist()
    list_pais = df_filtrado["pais"].unique().tolist()
    nome_selecionado = draw_select_filter("Nome", list_names, context)
    pais_selecionado = draw_select_filter("Pais", list_pais, context)
    context.update_filter("nome",nome_selecionado)
    context.update_filter("pais",pais_selecionado)

    st.dataframe(df_filtrado)

if __name__ == "__main__":
    main()


"""
app.py — Bankai 
Ponto de entrada do projeto.
Para trocar o tema, altere apenas a string em get_theme().
"""
from system.view.components.cards.index import (
    sparkline_metric
)
import streamlit as st
from system.control.managers.data import get_data_json
from system.view.components.layout.header import draw_header
from system.control.contexts.dash import DashboardContext
from system.view.components.filters.select import draw_select_filter
import system.control.managers.filter as filter_man

def main(context:DashboardContext):
    theme = context.theme
    with st.container():
        draw_header(
            background=True,
            title="Shebattle", ticker=True,
            icon="🏳️‍⚧️", 
            context=context
        )

    # df = get_data_json("apps/engines/shebattle/data/she_base.json")
    # df_filtrado = filter_man.apply_filters(df, context.active_filters)

    # list_names = df_filtrado["nome"].unique().tolist()
    # list_pais = df_filtrado["pais"].unique().tolist()
    # nome_selecionado = draw_select_filter("Nome", list_names, context)
    # pais_selecionado = draw_select_filter("Pais", list_pais, context)
    # context.update_filter("nome",nome_selecionado)
    # context.update_filter("pais",pais_selecionado)

    # st.dataframe(df_filtrado)

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

if __name__ == "__main__":
    main()