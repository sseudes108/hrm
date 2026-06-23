import streamlit as st
from system.view.components.cards import card
from apps.engines.athena.pages.espada.ortools.charts import step_line
from apps.engines.athena.pages.espada.ortools.charts import acumulo

def draw(
    context,
    df_demanda_grafico, df_capacidade_grafico, 
    capacidade_por_bloco, df_fifo
):
    # grf_cols = st.columns(2, gap="xxsmall")

    # with grf_cols[0]:
        card.draw(
            card.CardConfig(
                card_id="grf_dem_cap_wrp", context=context,
                model="wrapper", hover=False
            ), card.CardRenderConfig(
                content=lambda: step_line.draw(
                    context=context,
                    title="Demanda vs Capacidade", 
                    subtitle="Linhas em Propostas. Etiquetas indicam analistas (FTE).",
                    df_demand=df_demanda_grafico,
                    df_capacity=df_capacidade_grafico,
                    capacidade_por_bloco=capacidade_por_bloco,
                    height="233px"
                )
            )
        )

    # with grf_cols[1]:
        card.draw(
            card.CardConfig(
                card_id="grf_acum_wrp", context=context,
                model="wrapper", hover=False
            ), card.CardRenderConfig(
                content=lambda: acumulo.draw(
                    context=context,
                    title="Acumulo", 
                    subtitle="Linhas em Propostas. Etiquetas indicam analistas (FTE).",
                    df_fluxo=df_fifo,
                    height="229px"
                )
            )
        )