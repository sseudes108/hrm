import streamlit as st
import pandas as pd
import numpy as np
from system.view.components.cards import card
from system.view.components.inputs.number import number_input
from system.view.components.inputs.text import text_input
from system.view.components.inputs.file_uploader import file_uploader
from apps.engines.athena.config.payload import AthenaPayload, TurnoTemplate
from system.view.components.layout import fixes
from system.view.components.inputs.select import multiselect

APP_NAME = "athena"
CATALOGO_TURNOS = {
    1: TurnoTemplate(id=1, nome="8:48", minutos_trabalho=588, minutos_almoco=60),
    2: TurnoTemplate(id=2, nome="8:00", minutos_trabalho=540, minutos_almoco=60),
}

def quebrar_demanda_por_sla(df_original: pd.DataFrame, sla_minutos: int) -> pd.DataFrame:
    fator_quebra = 60 / sla_minutos
    
    if fator_quebra == 1.0:
        return df_original.copy()
        
    df_expandido = df_original.loc[df_original.index.repeat(int(fator_quebra))].reset_index(drop=True)
    
    # CORREÇÃO AQUI: Arredonda para cima e converte para INTEIRO
    df_expandido['quantidade'] = np.ceil(df_expandido['quantidade'] / fator_quebra).astype(int)
    
    df_expandido['horario'] = list(range(len(df_expandido)))
    
    return df_expandido

def draw(context):
    return card.draw(
        card.CardConfig(
            card_id="espada_ortools_input_bar_wrapper", context=context, hover=False, model="wrapper"
        ), card.CardRenderConfig(
            content=lambda:card.draw(
                card.CardConfig(
                    card_id="espada_ortools_input_bar", context=context, hover=False
                ), card.CardRenderConfig(
                    content=lambda:_draw_component(context)
                )
            )
        )
    )

def _draw_component(context):
    spc_1, input_col, files_col, spc_2 = st.columns([0.05, 6, 2, 0.05], gap="xxsmall")
    with input_col:
        up_cols = st.columns(4, gap="xxsmall")
        with up_cols[0]:
            tma = number_input.draw(
                context=context, label="TMA - SEGUNDOS", 
                input_id="ortools_tma_inp", default=215
            )
        with up_cols[1]:
            sla = number_input.draw(
                context=context, label="SLA - MINUTOS", 
                input_id="ortools_sla_inp", default=60
            )
        with up_cols[2]:
            inicio = text_input.draw(
                context=context, label="INICIO", input_id="ortools_ope_ini"
            )
        with up_cols[3]:
            fim = text_input.draw(
                context=context, label="FIM", input_id="ortools_ope_fim"
            )
            
        fixes.horizontal_spacer("0.01rem")
        cols = st.columns([5, 3, 2], gap="xxsmall")
        with cols[0]:
            opcoes_nomes = [turno.nome for turno in CATALOGO_TURNOS.values()]
            turnos_selecionados_nomes = multiselect.draw(
                context=context, input_id="ortools_turnos_mtslct_inp",
                label="TURNOS", options=opcoes_nomes
            )
        with cols[1]:
            opcoes_nomes = [turno.nome for turno in CATALOGO_TURNOS.values()]
            turnos_selecionados_nomes = multiselect.draw(
                context=context, input_id="ortools_holder_mtslct_inp",
                label="HOLDER", options=opcoes_nomes
            )
        with cols[2]:
            # =========================================================
            # BOTÃO DE DISPARO DA OTIMIZAÇÃO
            # =========================================================
            btn_col = st.columns([0.1, 1.5, 0.1], gap="xxsmall")[1] 
            with btn_col:
                # O st.button nativo retorna True apenas no exato frame em que é clicado
                disparar_otimizacao = st.button(
                    label="Calcular",
                    icon=":material/functions:",
                    key="btn_athena_otimizar",
                    use_container_width=True
                )

    with files_col:
        fl_cols = st.columns(2)
        with fl_cols[0]:
            csv_uploaded = file_uploader.draw(
                app_name=APP_NAME, label="PERFIL CSV", input_id="ortools_up_csv"
            )
        with fl_cols[1]:
            zip_uploaded = file_uploader.draw(
                app_name=APP_NAME, label="LOG ZIP", input_id="ortools_up_zip"
            )

    df_demand = None
    if csv_uploaded:
        df_bruto = pd.read_csv(csv_uploaded)
        sla_valido = sla if sla > 0 else 30 
        df_demand = quebrar_demanda_por_sla(df_bruto, sla_valido)
    
    turnos_objetos = []
    if turnos_selecionados_nomes:
        for nome in turnos_selecionados_nomes:
            turno_encontrado = next(t for t in CATALOGO_TURNOS.values() if t.nome == nome)
            turnos_objetos.append(turno_encontrado)
        
    payload = AthenaPayload(
        df_demand=df_demand,
        sla=sla,
        tma=tma,
        turnos=turnos_objetos
    )
    
    # Injetamos dinamicamente a ação do botão no payload para transporte seguro
    payload.disparar_otimizacao = disparar_otimizacao

    return payload