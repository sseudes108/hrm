import pandas as pd
import numpy as np

def formatar_eixo_temporal(df: pd.DataFrame, sla_minutos: int) -> pd.DataFrame:
    """Transforma o índice numérico de blocos em strings de horário (HH:MM)."""
    df_formatado = df.copy()
    horarios = []
    for indice in range(len(df_formatado)):
        minutos_totais = indice * sla_minutos
        horas = (minutos_totais // 60) % 24
        minutos = minutos_totais % 60
        horarios.append(f"{horas:02d}:{minutos:02d}")
        
    df_formatado['horario'] = horarios
    return df_formatado