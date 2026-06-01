import streamlit as st
import pandas as pd
from dataclasses import dataclass, field

import system.control.managers.hash as hash_man
from system.control.contexts        import AppContext
from system.view.components.cards   import CardConfig, card

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
    min_date = pd.to_datetime(config.df[config.column]).min().date()
    max_date = pd.to_datetime(config.df[config.column]).max().date()

    context_key = config.column
    previous_value = context.active_filters.get(context_key)

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
    if start_key in st.session_state and st.session_state[start_key] != default_start:
        st.session_state[start_key] = default_start
        
    if end_key in st.session_state and st.session_state[end_key] != default_end:
        st.session_state[end_key] = default_end

    # B) O Callback: Só atualiza o contexto se o usuário mexer no Input manualmente!
    def _on_date_change():
        if config.update_app_context:
            new_start = st.session_state[start_key]
            new_end   = st.session_state[end_key]
            
            # Trava de UX: Se o start for maior, puxa o end junto
            if new_start > new_end:
                new_end = new_start
                st.session_state[end_key] = new_end
                
            context.update_filter(config.column, [new_start, new_end], rerun=False)

    # Estilização CSS customizada... (MANTIDO)
    if not config.has_card:
        label_bg = "--bk-bg"
        hover_label_bg = "--bk-bg"
        padding = "0"
    else:
        label_bg = "--bk-surface"
        hover_label_bg = "--bk-surface-2"
        padding = "0.4"

    unique_style = f"""
        <style>
            [class*="st-key-co_filter_date_{config.key}"] {{
                padding-left: {padding}em !important;
                padding-bottom: {padding}em !important;
                padding-right: {padding}em !important;
            }}
            [class*="st-key-co_filter_date_{config.key}"] [data-testid="stWidgetLabel"]{{
                background-color: var({label_bg}) !important; 
            }}
            [class*="st-key-co_filter_date_{config.key}"] div:hover > [data-testid="stWidgetLabel"]{{
                background-color: var({hover_label_bg}) !important;
            }}
            [class*="st-key-co_filter_date_{config.key}"] [data-baseweb="input"]:hover > div {{
                border-color: var(--bk-primary) !important;
            }}
        </style>
    """
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    # 2. Renderiza DOIS inputs lado a lado
    with st.container(key=f"co_filter_date_{context.app_name}_{config.key}"):
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
    
    if has_card:
        card.draw(
            CardConfig(
                app_name=app_name, card_id=f"ft_date_{column}_{id}_card",
                hover=False, model="base"
            ),
            render_content=lambda:
                _draw_component(
                DateFilterConfig(
                    app_name=app_name, df=df,
                    column=column, label=column.upper(), 
                    filter_id=f"{app_name}_ft_date_{column}_{id}"
                ), context=context
            )
        )
    else:
        _draw_component(
            DateFilterConfig(
                app_name=app_name, df=df,
                column=column, label=column.upper(), 
                filter_id=f"{app_name}_ft_date_{column}_{id}"
            ), context=context
        )