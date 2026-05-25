import pandas as pd

def apply_filters(df: pd.DataFrame, active_filters: dict) -> pd.DataFrame:
    if df.empty or not active_filters:
        return df

    df_filtered = df.copy()

    for column, value in active_filters.items():
        if column not in df_filtered.columns:
            raise KeyError(f"[apply_filters] Coluna '{column}' não existe no DataFrame. Colunas disponíveis: {list(df_filtered.columns)}")

        if value is None or value == "" or value == "Todos":
            continue

        if isinstance(value, (list, dict)) and not value:
            continue

        col_dtype = df_filtered[column].dtype

        # Cast do valor para o tipo da coluna — explode se não conseguir
        if isinstance(value, list):
            try:
                value = [col_dtype.type(v) for v in value]
            except (ValueError, TypeError) as e:
                raise TypeError(f"[apply_filters] Não foi possível converter lista de valores para '{col_dtype}' na coluna '{column}': {e}")
            df_filtered = df_filtered[df_filtered[column].isin(value)]

        else:
            try:
                value = col_dtype.type(value)
            except (ValueError, TypeError) as e:
                raise TypeError(f"[apply_filters] Não foi possível converter '{value}' ({type(value).__name__}) para '{col_dtype}' na coluna '{column}': {e}")
            df_filtered = df_filtered[df_filtered[column] == value]

    return df_filtered