from system.core.contexts import AppContext

def categoric_chart(column: str, event_data: dict, context: AppContext):
    """
    Controlador: Processa o evento do ECharts e decide se adiciona ou remove o filtro.
    Usa o AppContext apenas para ler e salvar o estado.
    """
    if not event_data:
        return

    # 1. Extrai os dados brutos do evento
    event = event_data.get("chart_event", event_data)
    
    if not event:
        return
    
    name = event.get("name")
    ts = event.get("ts")

    if not name or not ts:
        return

    # 2. VALIDAÇÃO DO TIMESTAMP (Lendo do Contexto)
    last_ts = context.get_last_event_ts(column)
    
    # Se o timestamp for o mesmo, o Streamlit apenas recarregou a tela. Abortamos.
    if last_ts == ts:
        return

    # Se passou, é um clique novo! Salvamos o novo timestamp no Contexto.
    context.set_last_event_ts(column, ts)

    # 3. A LÓGICA DE TOGGLE
    current_value = context.active_filters.get(column)

    if current_value == name:
        # Já estava filtrado: Remove
        context.remove_filter(column)
    else:
        # É uma fatia nova: Atualiza
        context.update_filter(column, name)