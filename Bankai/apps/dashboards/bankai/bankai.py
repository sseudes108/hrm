"""
app.py — Bankai 
Ponto de entrada do projeto.
Para trocar o tema, altere apenas a string em get_theme().
"""
import streamlit as st

from system.control.contexts import AppContext

import system.control.managers.data     as data_man
import system.control.managers.filter   as filter_man

import system.view.components.tables.table as table
import system.view.components.tables.bodies as bodies
from system.view.components.cards import draw_card                      
from system.view.components.filters import select as select_filtter

from system.view.components.charts.echarts import pie
from system.view.components.charts.echarts import line


def main(context:AppContext):
    # st.write("")
    # st.write("")
    # st.write("")
    # st.write("")

    # main2(context)

    # return

    st.info("Header Space")

    df = data_man.get_data_csv("apps/dashboards/bankai/data/anime_dataset.csv")
    df_filtrado = filter_man.apply_filters(df, context.active_filters)

    tabs = st.tabs(["Echarts Filter Callbacks", "HTML Table"])

    with tabs[0]:
        cols = st.columns([2,5])

        with cols[0]:
            chart_config = {
                "app_name": "bankai",
                "in_card": True,
                "card_hover": True,
                "title": "ECHART CALLBACKS",
                "column": "source",
                "height": 330,
                "theme": context.theme,
                "radius": ["42%", "72%"],
                "legend_config":{
                    "orientation": "horizontal",
                    "top": "85%", "left": "2%", "bottom": "0%", "right": "0%"
                },
                    "toolbox": {
                    "magic": False,
                    "view": True,
                }
            }
            clicked_value_pie = pie.draw_pie(
                chart_config, df_filtrado
            )

            last_sel = context.active_filters.get("source", {})
            # st.warning(f"Last Selected - {key} - {last_sel}")
            # st.json(context.active_filters)

            if clicked_value_pie["chart_event"] is not None:
                selected = clicked_value_pie["chart_event"]["name"]
                if selected != last_sel:
                    context.update_filter("source", selected)
                else:
                    context.remove_filter("source")

            # st.json(clicked_value_pie)
            # st.json(clicked_value_pie["chart_event"])
            # st.write(clicked_value_pie["chart_event"]["name"])

        with cols[1]:
            pass
            # clicked_value_line = line.draw_line(
            #     chart_config={
            #         "app_name": "bankai",
            #         "title": "Vendas por mês",
            #         "x_axis": "year",
            #         "y_axis": ["popularity", "rank"],
            #         "height": 330,
            #         "smooth": True,
            #         "in_card": False,
            #         "legend_config": {
            #             "orientation": "horizontal",
            #             "top": "2%",
            #             "left": "center"
            #         },
            #         "toolbox": {
            #             "magic": ["bar", "line", "stack"],
            #             "view": True,
            #             "zoom": True
            #         }
            #     },
            #     df=df_filtrado, context=context
            # )

            # last_sel = context.active_filters.get("year", {})
            # st.warning(f"Last Selected - year - {last_sel}")
            # st.json(context.active_filters)

            # if clicked_value_line["chart_event"] is not None:
            #     selected = clicked_value_line["chart_event"]["name"]
            #     if selected != last_sel:
            #         context.update_filter("year", selected)
            #     else:
            #         context.remove_filter("year")
        
            # st.json(clicked_value_line)
            # st.json(clicked_value_line["chart_event"])
            # st.write(clicked_value_line["chart_event"]["name"])

    st.dataframe(df_filtrado)

    with tabs[1]:
        table_config = {
            "app_name": "bankai",
            "titulo": "Tabela Teste",
            "subtitulo": "Subititulo Teste",
            "height": 500,
            "ft_bar_config": {
                "update_app_context": False,
                "num_colunas": 5, 
                "labels": {
                    "title": "Title",
                    "status": "Status",
                    "rating": "Rating",
                    "year": "Year",
                    "genres": "Genres"
                },
                "columns_df": ["title", "status", "rating", "year", "genres"]
            }
        }
        table.draw(
            df_filtrado, context,
            table_config, bodies.delta.draw_body
        ) 

# def main2(context:AppContext):
#     df = data_man.get_data_csv("apps/dashboards/bankai/data/anime_dataset.csv")
#     df_filtrado = filter_man.apply_filters(df, context.active_filters)

#     cols = st.columns([2,5])
#     with cols[0]:
#         chart_config = {
#             "app_name": "bankai",
#             "in_card": True,
#             "card_hover": True,
#             "title": "echarts_pie_source",
#             "column": "source",
#             "height": 330,
#             "theme": context.theme,
#             "radius": ["42%", "72%"],
#             "legend_config":{
#                 "orientation": "horizontal",
#                 "top": "85%", "left": "2%", "bottom": "0%", "right": "0%"
#             },
#                 "toolbox": {
#                 "magic": False,
#                 "view": True,
#             }
#         }
#         clicked_value_pie_source = pie.draw_pie(
#             chart_config, df_filtrado
#         )
#         last_sel = context.active_filters.get("source", {})
#         if clicked_value_pie_source["chart_event"] is not None:
#             selected = clicked_value_pie_source["chart_event"]["name"]

#             if selected != last_sel:
#                 selected = clicked_value_pie_source["chart_event"]["name"]
#                 context.update_filter("source", selected)
#             else:
#                 context.remove_filter("source")

#         chart_config = {
#             "app_name": "bankai",
#             "in_card": True,
#             "card_hover": True,
#             "title": "echarts_pie_season",
#             "column": "season",
#             "height": 330,
#             "theme": context.theme,
#             "radius": ["42%", "72%"],
#             "legend_config":{
#                 "orientation": "horizontal",
#                 "top": "85%", "left": "2%", "bottom": "0%", "right": "0%"
#             },
#                 "toolbox": {
#                 "magic": False,
#                 "view": True,
#             }
#         }
#         clicked_value_pie_season = pie.draw_pie(
#             chart_config, df_filtrado
#         )
#         last_sel = context.active_filters.get("season", {})
#         if clicked_value_pie_season["chart_event"] is not None:
#             selected = clicked_value_pie_season["chart_event"]["name"]

#             if selected != last_sel:
#                 selected = clicked_value_pie_season["chart_event"]["name"]
#                 context.update_filter("season", selected)
#             else:
#                 context.remove_filter("season")





#         chart_config = {
#             "app_name": "bankai",
#             "in_card": True,
#             "card_hover": True,
#             "title": "echarts_pie_year",
#             "column": "year",
#             "height": 330,
#             "theme": context.theme,
#             "radius": ["42%", "72%"],
#             "legend_config":{
#                 "orientation": "horizontal",
#                 "top": "85%", "left": "2%", "bottom": "0%", "right": "0%"
#             },
#                 "toolbox": {
#                 "magic": False,
#                 "view": True,
#             }
#         }
#         clicked_value_pie_year = pie.draw_pie(
#             chart_config, df_filtrado
#         )
#         last_sel = context.active_filters.get("year", {})
#         if clicked_value_pie_year["chart_event"] is not None:
#             selected = clicked_value_pie_year["chart_event"]["name"]

#             if selected != last_sel:
#                 selected = clicked_value_pie_year["chart_event"]["name"]
#                 context.update_filter("year", selected)
#             else:
#                 context.remove_filter("year")

#     df_filtrado = filter_man.apply_filters(df, context.active_filters)
        
#     with cols[1]:
#         st.json(context.active_filters)
#         st.dataframe(df_filtrado)
