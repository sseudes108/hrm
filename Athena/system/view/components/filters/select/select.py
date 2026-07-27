import streamlit as st
import pandas as pd
from dataclasses import dataclass, field

from system.core.managers.config import hash as hash_man
from system.core.contexts import AppContext, require_filter_state
from system.view.components.cards import CardConfig, card
from system.view.components.filters.state import sync_widget_value
from system.view.components.layout import fixes

@dataclass
class SelectFilterConfig:
    app_name: str
    df: pd.DataFrame
    column: str
    label: str
    filter_id: str = "default"
    has_card: bool = False
    allow_all: bool = True
    all_label: str = "Todos"
    all_value: object = "Todos"
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
    if config.allow_all and config.all_label not in modified_options:
        modified_options.insert(0, config.all_label)

    context_key = config.column
    state = require_filter_state(context)
    previous_value = state.active_filters.get(context_key, config.all_value)

    # Garante que o valor vindo do contexto exista na lista (fallback para "Todos")
    if previous_value not in modified_options:
        previous_value = config.all_label

    # 🚀 A) Sincronização Forçada: Se o gráfico mudou o Contexto, 
    # esmagamos a memória do Widget para ele obedecer!
    sync_widget_value(config.key, previous_value)

    # 🚀 B) O Callback: Só envia pro Contexto se o usuário clicar no Select!
    def _on_select_change():
        if config.update_app_context:
            selected_value = st.session_state[config.key]
            new_value = (
                config.all_value
                if config.allow_all and selected_value == config.all_label
                else selected_value
            )
            # O contexto trata o filtro e não recarrega a página de novo (rerun=False)
            state.update_filter(config.column, new_value, rerun=False)

    surface = "card" if config.has_card else "plain"
    with st.container(key=f"co_filter_select_{surface}_{config.key}"):
        fixes.horizontal_spacer("1px")
        selected = st.selectbox(
            label=config.label,
            options=modified_options,
            key=config.key,
            on_change=_on_select_change # 🚀 Injeta o Callback
            # Nota: Removemos o "index=default_index" porque o st.session_state
            # que forçamos lá em cima já obriga o select a ficar no valor correto.
        )
        
    # A atualização é tratada pelo estado fornecido pela aplicação.
    return selected

def draw(
    df: pd.DataFrame,
    column: str,
    id: str,
    context: AppContext,
    has_card: bool = False,
    *,
    allow_all: bool = True,
    all_label: str = "Todos",
    all_value: object = "Todos",
):
    """Desenha um filtro de seleção.

    ``all_label`` é o texto apresentado ao usuário; ``all_value`` é o valor
    salvo no estado. Aplicações podem separá-los quando a base possuir um
    valor real chamado ``Todos``.
    """
    app_name = context.app_name
    
    card.draw(
        CardConfig(
            context=context,
            card_id=f"ft_sel_{column}_{id}_card",
            model="filter",
            hover=False,
            show_card=has_card,
            padding="normal",
        ),
        card.CardRenderConfig(
            content=lambda: _draw_component(
                SelectFilterConfig(
                    app_name=app_name,
                    df=df,
                    column=column,
                    label=column.upper(),
                    filter_id=f"{app_name}_ft_sel_{column}_{id}",
                    has_card=has_card,
                    allow_all=allow_all,
                    all_label=all_label,
                    all_value=all_value,
                ),
                context=context,
            )
        ),
    )
