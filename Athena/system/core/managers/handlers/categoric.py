import pandas as pd

from system.core.contexts import AppContext
from system.core.managers.charts.interactions import apply_click_filter

def categoric_chart(column: str, event_data: dict, context: AppContext, df: pd.DataFrame | None = None):
    """
    Controlador: Processa o evento do ECharts e decide se adiciona ou remove o filtro.
    Usa o AppContext apenas para ler e salvar o estado.
    """
    # Mantido como adaptador de compatibilidade para chamadas legadas.
    if df is None:
        return False
    return apply_click_filter(
        df=df, context=context,
        column=column, event_data=event_data, click_type="categoric_click",
    )
