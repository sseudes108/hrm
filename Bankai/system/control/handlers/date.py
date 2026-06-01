import pandas as pd
from system.control.contexts import AppContext

def date_chart(column: str, event_data: dict, context: AppContext):
    """
    Controlador de Tempo: Processa o clique em gráficos temporais.
    Ignora cliques em linhas de meta e converte strings válidas para datetime.date.
    """
    if not event_data:
        return

    # 1. Extrai os dados brutos do evento
    event = event_data.get("chart_event", event_data)
    if not event:
        return
    
    # 🚀 PROTEÇÃO 1: Ignora cliques em componentes auxiliares (ex: markLine, markPoint, title)
    # O ECharts envia "series" quando o clique é na barra/linha real de dados.
    component_type = event.get("componentType")
    if component_type and component_type != "series":
        return

    name = event.get("name") # Ex: "2018-01-05"
    ts = event.get("ts")

    if not name or not ts:
        return

    # 2. VALIDAÇÃO DO TIMESTAMP
    last_ts = context.get_last_event_ts(column)
    if last_ts == ts:
        return

    context.set_last_event_ts(column, ts)

    # 3. TRADUÇÃO DE TIPOS (De String para Date)
    try:
        clicked_date = pd.to_datetime(name).date()
    except Exception:
        # 🚀 PROTEÇÃO 2: Se mesmo passando pelo componentType, o dado não for 
        # uma data válida, nós ABORTAMOS a função silenciosamente.
        # Jamais enviamos uma string bizarra para o AppContext.
        return 

    # 4. A LÓGICA DE TOGGLE COM RANGE
    current_value = context.active_filters.get(column)
    
    # Monta o padrão Bankai para um dia específico
    clicked_range = [clicked_date, clicked_date]

    if current_value == clicked_range:
        context.remove_filter(column)
    else:
        context.update_filter(column, clicked_range)