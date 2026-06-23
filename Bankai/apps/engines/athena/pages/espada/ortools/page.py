import streamlit as st

from system.core.log.view import infos
from system.view.components.layout import fixes

from apps.engines.athena.core import athena, helper
from apps.engines.athena.core.calculadora import page as calculadora
from apps.engines.athena.pages.espada.ortools import inputs
from apps.engines.athena.pages.espada.ortools.charts import graficos_block
from apps.engines.athena.pages.espada.ortools.analistas_block import layout as analistas_block

def calcular_capacity(payload, capacidade_por_bloco):
    with st.spinner("Atena está calculando a escala ideal no OR-Tools..."):
        engine = athena.AthenaEngine(
            df_demand=payload.df_demand,
            tma_per_block=capacidade_por_bloco,
            sla=payload.sla,
            turnos=payload.turnos
        )
        engine.build_model()
        resultados = engine.solve()
        
    # Retorna o dicionário de resultados cru da engine
    return resultados

def main(context):
    payload = inputs.draw(context)

    # Trava de segurança inicial
    if not payload or payload.df_demand is None:
        infos.draw(
            message="Aguardando configuração de parâmetros e upload do arquivo."
        )
        return
    
    # =========================================================================
    # DEFINIÇÃO DOS PARÂMETROS BASE
    # =========================================================================
    tamanho_bloco_segundos = payload.sla * 60
    capacidade_por_bloco = int(tamanho_bloco_segundos / payload.tma) if payload.tma > 0 else 0
    total_blocos_do_dia = len(payload.df_demand)
    
    # Inicialização do Cache de Estado
    if "athena_escala_base" not in st.session_state:
        st.session_state.athena_escala_base = None

    # =========================================================================
    # MOTOR DE OTIMIZAÇÃO (Dispara apenas quando necessário)
    # =========================================================================
    if payload.disparar_otimizacao or st.session_state.athena_escala_base is None:
        
        resultados = calcular_capacity(payload, capacidade_por_bloco)
        
        # SALVAMOS APENAS A TABELA CRUA NO STATE. Ela é a fonte da verdade.
        df_enriquecido = calculadora.enriquecer_escala(resultados["df_escala"], payload.sla)
        st.session_state.athena_escala_base = df_enriquecido
        
    # =========================================================================
    # COMPILAÇÃO DOS DATAFRAMES PRINCIPAIS
    # =========================================================================
    # ANALISTAS e CAPACIDADE TOTAL (Gerados em tempo real)
    # Sempre que a tela der rerun, ele recalcula a soma total em milissegundos
    df_analistas, df_capacidade = calculadora.processar_dados_da_escala(
        df_escala_crua=st.session_state.athena_escala_base,
        total_blocks=total_blocos_do_dia,
        cap_por_bloco=capacidade_por_bloco,
        sla_minutos=payload.sla
    )

    # =========================================================================
    # Como a sua demanda já foi "quebrada" pelo input de SLA, 1 bloco = 1 janela de SLA
    df_fifo = calculadora.gerar_fluxo_fifo(
        df_demanda=payload.df_demand, 
        df_capacidade=df_capacidade, 
        sla_blocks=1 
    )

    # Normalização temporal do eixo X para visualização gráfica (HH:MM)
    df_demanda_grafico = helper.formatar_eixo_temporal(payload.df_demand, payload.sla)
    df_capacidade_grafico = helper.formatar_eixo_temporal(df_capacidade, payload.sla)
    df_fifo = helper.formatar_eixo_temporal(df_fifo, payload.sla)

    lcols = st.columns([2, 1.4], gap="xxsmall")
    with lcols[0]:
        analistas_block.draw(
            context=context, df_escala=df_analistas, payload=payload
        )
    with lcols[1]:
        graficos_block.draw(
            context=context, df_demanda_grafico=df_demanda_grafico,
            df_capacidade_grafico=df_capacidade_grafico,
            capacidade_por_bloco=capacidade_por_bloco,
            df_fifo=df_fifo
        )
        
    fixes.horizontal_spacer("0.1em")