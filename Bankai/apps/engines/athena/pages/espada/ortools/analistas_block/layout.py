import streamlit as st
import pandas as pd
from system.view.components.cards import card
from apps.engines.athena.pages.espada.ortools.analistas_block import table
from apps.engines.athena.pages.espada.ortools.analistas_block import controls
from apps.engines.athena.pages.espada.ortools.analistas_block import info

APP_NAME = "athena"

def _agrupar_escala(df_escala: pd.DataFrame) -> pd.DataFrame:
    if df_escala is None or df_escala.empty: return pd.DataFrame()
        
    # Agrupamos pelas STRINGS exatas (08:00 é diferente de 08:10)
    colunas_agrupamento = ['turno_aplicado', 'str_entrada', 'str_almoco_inicio', 'str_almoco_fim', 'str_saida', 'min_entrada']
    
    df_agrupado = df_escala.groupby(colunas_agrupamento).size().reset_index(name='quantidade')
    df_agrupado = df_agrupado.sort_values(by='min_entrada').reset_index(drop=True)
    return df_agrupado

def draw(context, df_escala, payload):
    card.draw(
        card.CardConfig(
            card_id="espada_ortools_analista_table_wrapper", context=context, hover=False, model="wrapper"
        ), card.CardRenderConfig(
            content=lambda:_draw_component(context, df_escala, payload)
        )
    )
    
def _draw_component(context, df_escala, payload):
    cols = st.columns([1.4, 2.5],  gap="xsmall")
    df_escala_agrupado = _agrupar_escala(df_escala)

    with cols[0]:
        card.draw(
            card.CardConfig(
                card_id="_analistas_table_controls", context=context,
                has_title=True, title="CONTROLS", subtitle="modificar quadro", 
                icon=":material/contextual_token_add:"
            ), card.CardRenderConfig(
                content=lambda: controls.draw(context, payload)
            )
        )
        card.draw(
            card.CardConfig(
                card_id="_analistas_table_capacity_info", context=context,
                has_title=True, title="CAPACITY", subtitle="informações principais",
                icon=":material/factory:"
            ), card.CardRenderConfig(
                content=lambda: info.draw(df_escala, payload)
            )
        )

    with cols[1]:
        card.draw(
            card.CardConfig(
                card_id="_analistas_table_table_analistas", context=context,
                has_title=True, title="ANALISTAS", subtitle="quadro operacional", hover=False,
                icon=":material/account_circle:"
            ), card.CardRenderConfig(
                content=lambda: table.draw(df_escala_agrupado, payload.sla)
            )
        )