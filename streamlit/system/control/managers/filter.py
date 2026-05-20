import pandas as pd

def apply_filters(df: pd.DataFrame, active_filters: dict) -> pd.DataFrame:
    """
    Recebe um DataFrame e o dicionário active_filters do contexto.
    Retorna o DataFrame filtrado dinamicamente com base nos filtros ativos.
    """
    # Se o DataFrame estiver vazio ou não houver filtros, retorna ele mesmo
    if df.empty or not active_filters:
        return df
    
    df_filtered = df.copy()
    
    # Valores que o sistema deve ignorar e NÃO aplicar como filtro no Pandas
    # Adicionamos "Todos", None, strings vazias ou listas vazias
    ignored_values = ["Todos", "", None, [], {}]
    
    # Varre o dicionário de filtros injetado pelo contexto
    for column, value in active_filters.items():
        
        # 1. Se o valor estiver na lista de ignorados, pulamos para o próximo filtro
        if value in ignored_values:
            continue
            
        # 2. Se a coluna existir no DF, aplica o corte de forma segura
        if column in df_filtered.columns:
            df_filtered = df_filtered[df_filtered[column] == value]
            
    return df_filtered