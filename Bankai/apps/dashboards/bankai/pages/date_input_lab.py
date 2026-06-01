import streamlit as st
import pandas as pd

from system.control.contexts import AppContext
from system.control.managers import psql_man
from system.control.managers import data_man
from system.control.managers import filter_man

from system.view.components.filters.select import select
from system.view.components.filters.date import date
from system.view.layout import fixes

from system.control.managers.charts import pie_man, bar_man
from system.view.components.cards import card, CardConfig
from system.view.components.tables import table

@st.cache_data
def get_base():
    return data_man.get_data_csv("apps/dashboards/bankai/data/anime_dataset.csv")
    # query = """
    #     select 
    #         ship_date as "Data",
    #         ship_mode as "Shipping Method",
    #         state as "State",
    #         region as "Region",
    #         category as "Category",
    #         discount as "Discount",
    #         sales as "Price",
    #         profit as "Profit",
    #         quantity as "Quantity"
    #     from superstore_sales
    #     where ship_date::date > '2017-12-15'
    # """
    # return psql_man.consultar_banco(query)

def draw_filters(df_superstore:pd.DataFrame, context:AppContext):
    df_filtrado = filter_man.apply_filters(df_superstore, context.active_filters)

    date.draw_start_end(
        df=df_filtrado, column="aired_from", 
        id="begin_date_input_bkn_pg1", context=context, has_card=False
    )

    select.draw(
        df=df_filtrado, 
        column="demographics",
        id="dt_lb_rg_sl",
        context=context, 
        has_card=False
    )

    select.draw(
        df=df_filtrado, 
        column="year",
        id="dt_lb_st_sl",
        context=context, 
        has_card=False
    )

    select.draw(
        df=df_filtrado, 
        column="type",
        id="dt_lb_spm_sl",
        context=context, 
        has_card=False
    )

    fixes.draw_empty_element(510)

    return filter_man.apply_filters(df_filtrado, context.active_filters)

def draw_first_line(df_filtrado:pd.DataFrame, context:AppContext):
    cols = st.columns([1, 1, 1.5], gap="xxsmall")

    with cols[0]:
        pie_man.draw(
            title="type", subtitle="type",
            df=df_filtrado, column_pie="type", agg_func="sum",
            context=context, column_emoji="🚢"
        )

    with cols[1]:
        pie_man.draw(
            title="source", subtitle="source",
            df=df_filtrado, column_pie="source", 
            context=context, column_emoji="📦"
        )
    
    with cols[2]:
        bar_man.draw(
            title="status", subtitle="status",
            df=df_filtrado,
            column_x="aired_from", columns_y=["favorites"], 
            context=context, agg_func="sum", click_type="date",
            mark_lines=[
                bar_man.meta(3, "M1", "#ef4444"),
                bar_man.meta(4, "M2", "#75ef44"),
                bar_man.meta(9, "M3", "#ff20fb"),
                bar_man.media(),
            ],
            secondary_lines=[
                bar_man.linha(coluna="episodes", nome="episodes")
            ]
        )

    table.draw(
        df_filtrado, "Teste Tabela HTML", subtitle="T", context=context, height=366, sort_by="year"
    )

def main(context:AppContext):
    df_superstore = get_base()
    
    layout_cols = st.columns([0.5,2], gap="xsmall")

    with layout_cols[0]:
        df_filtrado = card.draw(
            CardConfig(
                app_name="bankai", card_id="sidebar_filters", model="base"
            ), render_content=lambda: draw_filters(df_superstore, context)
        )
    
    with layout_cols[1]:
        draw_first_line(df_filtrado, context)