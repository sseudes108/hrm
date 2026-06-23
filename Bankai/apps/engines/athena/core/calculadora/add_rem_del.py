import uuid
import pandas as pd
import streamlit as st
from apps.engines.athena.pages.espada.ortools.inputs import CATALOGO_TURNOS
from apps.engines.athena.core.calculadora import helper

def adicionar_analista(grupo_info):
    """Clona um analista do grupo clicado e insere no final da tabela base."""
    df_base = st.session_state.athena_escala_base
    
    # A máscara agora usa as strings de hora (que são exatas e sempre existem!)
    mask = (
        (df_base['turno_aplicado'] == grupo_info['turno_aplicado']) &
        (df_base['str_entrada'] == grupo_info['str_entrada']) &
        (df_base['str_saida'] == grupo_info['str_saida'])
    )
    
    matches = df_base[mask]
    if not matches.empty:
        # O TRUQUE: Copiamos a linha inteira do primeiro analista que bater com a regra!
        # Assim levamos todos os min_entrada, str_almoco, bloco_entrada, etc., automaticamente.
        novo_analista = matches.iloc[0].copy()
        novo_analista['analista_id'] = f"Clone_{uuid.uuid4().hex[:4].upper()}"
        
        df_atualizado = pd.concat([df_base, pd.DataFrame([novo_analista])], ignore_index=True)
        st.session_state.athena_escala_base = df_atualizado

def remover_analista(grupo_info):
    """Encontra uma pessoa do grupo clicado e remove da tabela base."""
    df_base = st.session_state.athena_escala_base
    
    mask = (
        (df_base['turno_aplicado'] == grupo_info['turno_aplicado']) &
        (df_base['str_entrada'] == grupo_info['str_entrada']) &
        (df_base['str_saida'] == grupo_info['str_saida'])
    )
    
    matches = df_base[mask]
    if not matches.empty:
        idx_para_remover = matches.index[-1]
        df_atualizado = df_base.drop(idx_para_remover).reset_index(drop=True)
        st.session_state.athena_escala_base = df_atualizado

def deletar_grupo(grupo_info):
    """Remove TODOS os analistas que fazem esse horário."""
    df_base = st.session_state.athena_escala_base
    
    mask = (
        (df_base['turno_aplicado'] == grupo_info['turno_aplicado']) &
        (df_base['str_entrada'] == grupo_info['str_entrada']) &
        (df_base['str_saida'] == grupo_info['str_saida'])
    )
    
    df_atualizado = df_base[~mask].reset_index(drop=True)
    st.session_state.athena_escala_base = df_atualizado

def adicionar_analistas_customizados(turno_nome, entrada_str, almoco_ini_str, saida_str, qtd, sla_minutos):
    """Injeta pessoas manuais usando a hora cravada (ex: 16:50)."""
    turno_t = next((t for t in CATALOGO_TURNOS.values() if t.nome == turno_nome), None)
    min_almoco = turno_t.minutos_almoco if turno_t else 60
    
    m_ent = helper.hora_para_minuto(entrada_str)
    m_alm_ini = helper.hora_para_minuto(almoco_ini_str)
    m_sai = helper.hora_para_minuto(saida_str)
    m_alm_fim = (m_alm_ini + min_almoco) % 1440
    
    novos = []
    for _ in range(qtd):
        novos.append({
            'analista_id': f"Custom_{uuid.uuid4().hex[:4].upper()}",
            'turno_aplicado': turno_nome,
            # Mantemos os blocos pro OR-Tools não chorar, mas o sistema usará as variáveis min_
            'bloco_entrada': m_ent // sla_minutos,
            'bloco_almoco_inicio': m_alm_ini // sla_minutos,
            'bloco_almoco_fim': m_alm_fim // sla_minutos,
            'bloco_saida': m_sai // sla_minutos,
            
            # As variáveis de precisão matemática!
            'min_entrada': m_ent,
            'min_alm_inicio': m_alm_ini,
            'min_alm_fim': m_alm_fim,
            'min_saida': m_sai,
            'str_entrada': entrada_str,
            'str_almoco_inicio': almoco_ini_str,
            'str_almoco_fim': helper.minuto_para_hora(m_alm_fim),
            'str_saida': saida_str
        })
        
    df_base = st.session_state.athena_escala_base
    st.session_state.athena_escala_base = pd.concat([df_base, pd.DataFrame(novos)], ignore_index=True)