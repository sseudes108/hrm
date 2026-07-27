import streamlit as st
import pandas as pd
from dataclasses import dataclass, field

from system.core.managers.config import hash as hash_man
from system.core.contexts import AppContext, require_filter_state
from system.core.log.view import warnings
from system.view.components.cards import CardConfig, card
from system.view.components.filters.state import sync_widget_value
from system.view.components.layout import fixes

@dataclass
class DateFilterConfig:
    app_name: str
    df: pd.DataFrame
    column: str
    label: str
    filter_id: str = "default"
    has_card: bool = False
    update_app_context: bool = True
    
    # Gerado dinamicamente para garantir unicidade no Streamlit
    key: str = field(init=False)

    def __post_init__(self):
        # 1. Trava de segurança
        if self.column not in self.df.columns:
            raise ValueError(f"Erro no filtro '{self.label}': A coluna '{self.column}' não existe no DataFrame.")
            
        # 2. Gera a chave hash 
        raw_string = f"{self.app_name}_ft_date_{self.filter_id}"
        self.key = hash_man.get_hash(raw_string)

def _draw_component(config: DateFilterConfig, context: AppContext):
    """
    Componente de filtro de data customizado com Sincronização Bidirecional.
    """
    fixes.horizontal_spacer("1px")
    dates = pd.to_datetime(config.df[config.column], errors="coerce").dropna()
    if dates.empty:
        warnings.draw(
            f"O filtro de data '{config.label}' não possui datas válidas.",
            alert="warning",
            context=context,
        )
        return None
    min_date = dates.min().date()
    max_date = dates.max().date()

    context_key = config.column
    state = require_filter_state(context)
    previous_value = state.active_filters.get(context_key)

    # 1. Definindo os valores iniciais do contexto
    if isinstance(previous_value, (list, tuple)) and len(previous_value) == 2:
        default_start = previous_value[0]
        default_end = previous_value[1]
    else:
        default_start = min_date
        default_end = max_date

    # 🚀 O SEGREDO DO ESTADO BIDIRECIONAL
    start_key = f"{config.key}_start"
    end_key   = f"{config.key}_end"

    # A) Sincronização Forçada: Se o contexto mudou por fora (ex: Gráfico),
    # nós esmagamos a memória interna do Widget para ele obedecer o Contexto.
    sync_widget_value(start_key, default_start)
    sync_widget_value(end_key, default_end)

    # B) O Callback: Só atualiza o contexto se o usuário mexer no Input manualmente!
    def _on_date_change():
        if config.update_app_context:
            new_start = st.session_state[start_key]
            new_end   = st.session_state[end_key]
            
            # Trava de UX: Se o start for maior, puxa o end junto
            if new_start > new_end:
                new_end = new_start
                st.session_state[end_key] = new_end
                
            state.update_filter(config.column, [new_start, new_end], rerun=False)

    # 2. Renderiza DOIS inputs lado a lado
    surface = "card" if config.has_card else "plain"
    with st.container(key=f"co_filter_date_{surface}_{context.app_name}_{config.key}"):
        col1, col2 = st.columns(2, gap='xxsmall')
        
        with col1:
            # Prepara os argumentos, MAS omite o "value" por enquanto
            start_kwargs = {
                "label": "START",
                "key": start_key,
                "format": "DD/MM/YYYY",
                "on_change": _on_date_change
            }
            # O pulo do gato: Só passa o valor se não tiver memória!
            if start_key not in st.session_state:
                start_kwargs["value"] = default_start
                
            start_date = st.date_input(**start_kwargs)
            
        with col2:
            end_kwargs = {
                "label": "END",
                "key": end_key,
                "min_value": start_date,
                "format": "DD/MM/YYYY",
                "on_change": _on_date_change
            }
            # Mesma regra para o Fim
            if end_key not in st.session_state:
                end_kwargs["value"] = default_end
                
            end_date = st.date_input(**end_kwargs)
    
    return [start_date, end_date]

def draw_start_end(df: pd.DataFrame, column: str, id: str, context: AppContext, has_card: bool = False):
    app_name = context.app_name
    card.draw(
        CardConfig(
            context=context,
            card_id=f"ft_date_{column}_{id}_card",
            model="filter",
            hover=False,
            show_card=has_card,
            padding="normal",
        ),
        card.CardRenderConfig(
            content=lambda: _draw_component(
                DateFilterConfig(
                    app_name=app_name,
                    df=df,
                    column=column,
                    label=column.upper(),
                    filter_id=f"{app_name}_ft_date_{column}_{id}",
                    has_card=has_card,
                ),
                context=context,
            )
        ),
    )
