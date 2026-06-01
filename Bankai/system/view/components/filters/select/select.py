import streamlit as st
import pandas as pd
from dataclasses import dataclass, field

import system.control.managers.hash as hash_man
from system.control.contexts        import AppContext
from system.view.components.cards   import CardConfig, card

@dataclass
class SelectFilterConfig:
    app_name: str
    df: pd.DataFrame
    column: str
    label: str
    filter_id: str = "default"
    has_card: bool = False
    allow_all: bool = True
    update_app_context: bool = True
    
    # Gerado dinamicamente para garantir unicidade no Streamlit
    key: str = field(init=False)

    def __post_init__(self):
        # 1. Trava de segurança: avisa o dev na hora se ele digitar a coluna errado
        if self.column not in self.df.columns:
            raise ValueError(f"Erro no filtro '{self.label}': A coluna '{self.column}' não existe no DataFrame.")
            
        # 2. Gera a chave hash idêntica ao padrão adotado no Header/Card
        raw_string = f"{self.app_name}_ft_sel_{self.filter_id}"
        self.key = hash_man.get_hash(raw_string)

def _draw_component(config: SelectFilterConfig, context: AppContext):
    """
    Componente de filtro customizado com Sincronização Bidirecional (Contexto <-> Widget).
    """
    options_list = config.df[config.column].dropna().unique().tolist()

    modified_options = list(options_list)
    if config.allow_all and "Todos" not in modified_options:
        modified_options.insert(0, "Todos")

    context_key = config.column
    previous_value = context.active_filters.get(context_key, "Todos")

    # Garante que o valor vindo do contexto exista na lista (fallback para "Todos")
    if previous_value not in modified_options:
        previous_value = "Todos"

    # 🚀 A) Sincronização Forçada: Se o gráfico mudou o Contexto, 
    # esmagamos a memória do Widget para ele obedecer!
    if config.key in st.session_state and st.session_state[config.key] != previous_value:
        st.session_state[config.key] = previous_value

    # 🚀 B) O Callback: Só envia pro Contexto se o usuário clicar no Select!
    def _on_select_change():
        if config.update_app_context:
            new_value = st.session_state[config.key]
            # O Contexto do Bankai trata o filtro e não recarrega a página de novo (rerun=False)
            context.update_filter(config.column, new_value, rerun=False)

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
            [class*="st-key-co_filter_{config.key}"] {{
                padding-left: {padding}em !important;
                padding-bottom: {padding}em !important;
                padding-right: {padding}em !important;
            }}
            [class*="st-key-co_filter_{config.key}"] [data-testid="stWidgetLabel"]{{
                background-color: var({label_bg}) !important; 
            }}
            [class*="st-key-co_filter_{config.key}"]:hover [data-testid="stWidgetLabel"]{{
                background-color: var({hover_label_bg}) !important;
            }}
            [class*="st-key-co_filter_{config.key}"]:hover [data-baseweb="select"] > div {{
                border-color: var(--bk-primary) !important;
            }}
        </style>
    """
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    with st.container(key=f"co_filter_select_{config.key}"):
        selected = st.selectbox(
            label=config.label,
            options=modified_options,
            key=config.key,
            on_change=_on_select_change # 🚀 Injeta o Callback
            # Nota: Removemos o "index=default_index" porque o st.session_state
            # que forçamos lá em cima já obriga o select a ficar no valor correto.
        )
        
    # Removemos o antigo context.update_filter daqui!
    return selected

def draw(df:pd.DataFrame, column:str, id:str, context:AppContext, has_card:bool = False):
    app_name = context.app_name
    
    if has_card:
        card.draw(
            CardConfig(
                app_name=app_name, card_id=f"ft_sel_{column}_{id}_card",
                hover=False, model="base"
            ),
            render_content=lambda:
                _draw_component(
                SelectFilterConfig(
                    app_name=app_name, df=df,
                    column=column, label=column.upper(), 
                    filter_id=f"{app_name}_ft_sel_{column}_{id}"
                ), context=context
            )
        )
    else:
        _draw_component(
            SelectFilterConfig(
                app_name=app_name, df=df,
                column=column, label=column.upper(), 
                filter_id=f"{app_name}_ft_sel_{column}_{id}"
            ), context=context
        )