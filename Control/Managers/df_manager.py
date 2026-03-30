from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

@st.cache_data
def filtrar_df(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    # 1. Criamos uma cópia para preservar o original
    df_filtrado = df.copy()

    # 2. Garantimos que a coluna de data seja do tipo datetime (caso existam filtros de data)
    if "inicio" in filtros or "fim" in filtros:
        if "data" in df_filtrado.columns:
            df_filtrado["data"] = pd.to_datetime(df_filtrado["data"])

    # 3. Loop dinâmico por todos os filtros recebidos
    for campo, valor in filtros.items():
        # Pulamos se o valor for "Todos" ou se for nulo
        if valor == "Todos" or valor is None:
            continue
        
        # Lógica especial para o intervalo de Datas
        if campo == "inicio":
            df_filtrado = df_filtrado[df_filtrado["data"] >= pd.to_datetime(valor)]
        elif campo == "fim":
            df_filtrado = df_filtrado[df_filtrado["data"] <= pd.to_datetime(valor)]
        
        # Lógica para colunas normais (cliente, fila, analista, etc)
        else:
            # Só filtra se a coluna realmente existir no DataFrame
            if campo in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado[campo] == valor]

    return df_filtrado

def calcular_deltas(df_historico):
    # Pega a hora atual e a hora anterior
    agora = datetime.now()
    hora_atual = agora.strftime("%H:00")
    hora_anterior = (agora - timedelta(hours=1)).strftime("%H:00")
    
    # Filtra os totais
    total_atual = len(df_historico[df_historico['hora'] == hora_atual])
    total_anterior = len(df_historico[df_historico['hora'] == hora_anterior])
    
    delta = total_atual - total_anterior
    return delta