import pandas as pd
import numpy as np
import datetime

def apply_filters(df: pd.DataFrame, active_filters: dict) -> pd.DataFrame:
    """
    Fatia um DataFrame com base em um dicionário de filtros ativos.
    As chaves devem corresponder aos nomes das colunas.
    """
    filtered_df = df.copy()

    for column, values in active_filters.items():
        if column not in filtered_df.columns:
            continue
            
        if not values:
            continue

        if not isinstance(values, (list, tuple, set)):
            values = [values]

        if "Todos" in values:
            continue

        # (Seus códigos anteriores do apply_filters: ignora se não existir, checa se é "Todos", etc...)

        # 🚀 NOVO: Se for uma tupla com 2 datas, cortamos o dataframe usando a regra de range (>= e <=)
        if isinstance(values, (list, tuple)) and len(values) == 2 and isinstance(values[0], datetime.date):
            mask = (
                (pd.to_datetime(filtered_df[column]).dt.date >= values[0]) & 
                (pd.to_datetime(filtered_df[column]).dt.date <= values[1])
            )
            filtered_df = filtered_df[mask]
            continue
            
        # (Aqui continua o seu código antigo para os Selects...)
        if not isinstance(values, (list, tuple, set)):
            values = [values]
            
        mask = np.isin(filtered_df[column].values, values)
        filtered_df = filtered_df[mask]

    return filtered_df