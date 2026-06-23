import numpy as np
import pandas as pd
from apps.engines.athena.core.calculadora import fifo, add_rem_del, helper

def enriquecer_escala(df_crua: pd.DataFrame, sla_minutos: int) -> pd.DataFrame:
    """Lê os blocos brutos do OR-Tools e injeta as strings de hora exata."""
    df = df_crua.copy()
    if df.empty or 'min_entrada' in df.columns: return df
    
    # Converte os índices de bloco em Minutos Reais
    df['min_entrada'] = df['bloco_entrada'] * sla_minutos
    df['min_alm_inicio'] = df['bloco_almoco_inicio'] * sla_minutos
    df['min_alm_fim'] = df['bloco_almoco_fim'] * sla_minutos
    df['min_saida'] = df['bloco_saida'] * sla_minutos
    
    # Cria as strings bonitas para a UI ler diretamente
    df['str_entrada'] = df['min_entrada'].apply(helper.minuto_para_hora)
    df['str_almoco_inicio'] = df['min_alm_inicio'].apply(helper.minuto_para_hora)
    df['str_almoco_fim'] = df['min_alm_fim'].apply(helper.minuto_para_hora)
    df['str_saida'] = df['min_saida'].apply(helper.minuto_para_hora)
    
    return df

def _gerar_capacidade_proporcional(row, total_blocks: int, sla_minutos: int, cap_por_bloco: float) -> list:
    """Simula 1440 minutos e calcula a fração exata de produção."""
    dia_minutos = np.zeros(1440, dtype=int)
    
    m_ent = int(row['min_entrada'])
    m_sai = int(row['min_saida'])
    m_alm_ini = int(row['min_alm_inicio'])
    m_alm_fim = int(row['min_alm_fim'])
    
    # Preenche a agenda do cara minuto a minuto
    t = m_ent
    if m_ent != m_sai: # Trava de segurança
        while t != m_sai:
            is_almoco = False
            if m_alm_ini <= m_alm_fim:
                if m_alm_ini <= t < m_alm_fim: is_almoco = True
            else:
                if t >= m_alm_ini or t < m_alm_fim: is_almoco = True
                
            if not is_almoco:
                dia_minutos[t] = 1
                
            t = (t + 1) % 1440
            
    # Agrupa os minutos fatiando a matriz pelos blocos do SLA
    cap_array = []
    cap_por_minuto = cap_por_bloco / float(sla_minutos)
    
    for b in range(total_blocks):
        inicio = b * sla_minutos
        fim = inicio + sla_minutos
        
        # Conta quantos minutos ele de fato trabalhou nesse intervalo
        minutos_trab = np.sum(dia_minutos[inicio:fim])
        
        # A MÁGICA: (20 min trab / 60) * 16 propostas = 5.33 -> Arredonda para 5
        cap_array.append(round(minutos_trab * cap_por_minuto))
        
    return cap_array


def processar_dados_da_escala(df_escala_crua: pd.DataFrame, total_blocks: int, cap_por_bloco: int, sla_minutos: int):
    df_analistas = df_escala_crua.copy()
    if df_analistas.empty:
        return df_analistas, pd.DataFrame({'horario': range(total_blocks), 'quantidade': [0] * total_blocks})
        
    df_analistas['capacidade'] = df_analistas.apply(
        lambda row: _gerar_capacidade_proporcional(row, total_blocks, sla_minutos, cap_por_bloco), 
        axis=1
    )
    
    matriz_capacidades = np.vstack(df_analistas['capacidade'].values)
    capacidade_total = matriz_capacidades.sum(axis=0).tolist()
    
    df_capacidade = pd.DataFrame({'horario': range(total_blocks), 'quantidade': capacidade_total})
    return df_analistas, df_capacidade

def gerar_fluxo_fifo(df_demanda, df_capacidade, sla_blocks):
    return fifo.gerar_fluxo_fifo(df_demanda, df_capacidade, sla_blocks)

def adicionar_analista(grupo_info):
    add_rem_del.adicionar_analista(grupo_info)

def remover_analista(grupo_info):
    add_rem_del.remover_analista(grupo_info)

def deletar_grupo(grupo_info):
    add_rem_del.deletar_grupo(grupo_info)

def adicionar_analistas_customizados(
    turno_nome, entrada_str, almoco_ini_str,
    saida_str, qtd, sla_minutos
):
    add_rem_del.adicionar_analistas_customizados(
        turno_nome, entrada_str, almoco_ini_str,
        saida_str, qtd, sla_minutos
    )