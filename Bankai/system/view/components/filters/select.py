import streamlit as st
import system.control.managers.hash as hash_man
from system.control.contexts import AppContext

# Exemplo de como a configuração deve chegar #
# options = {
#     "df": "pd.DataFrame",
#     "label": "label",
#     "column": "nome_coluna"
# }
# config = {
#     "id": "default",
#     "has_card": False, 
#     "allow_all": True,
#     "update_app_context": True,
# }
##############################################

def draw_filter(options:dict, context:AppContext, config:dict):
    """
    Componente de filtro customizado com suporte a 'Selecionar Todos' e persistência de estado.
    """
    key = hash_man.get_hash_key(f"{context.app_name}_ft_sel_{config["id"]}", options["label"])
    options_list = options["df"][options["column"]].dropna().unique().tolist()

    # 2. Injeta a opção "Todos" no início da lista, se permitido
    modified_options = list(options_list)
    if config["allow_all"] and "Todos" not in modified_options:
        modified_options.insert(0, "Todos")

    # 3. Mapeia o título para a chave exata que você usa no context (ex: "Nome" -> "nome")
    context_key = options["column"].lower()

    # 4. CAPTURA DO ESTADO ANTERIOR: Verifica se já existia um valor salvo no contexto
    previous_value = context.active_filters.get(context_key, "Todos")

    # 5. Descobre qual o índice do valor anterior na nova lista de opções
    # Se o valor anterior sumiu da lista devido a outro filtro cruzado, foca no "Todos" (índice 0)
    try:
        default_index = modified_options.index(previous_value)
    except ValueError:
        default_index = 0

    # Estilização CSS customizada
    if config["has_card"] == False:
        label_bg = "--bk-bg"
        hover_label_bg = "--bk-bg"
        padding = "0"

    else:
        label_bg = "--bk-surface"
        hover_label_bg = "--bk-surface-2"
        padding = "0.4"

    unique_style = f"""
        <style>
            /* Padding */
            [class*="st-key-co_filter_bar_{key}"] {{
                padding-left: {padding}em !important;
                padding-bottom: {padding}em !important;
                padding-right: {padding}em !important;
            }}

            /* Background Label */
            [class*="st-key-co_filter_bar_{key}"] [data-testid="stWidgetLabel"]{{
                background-color: var({label_bg}) !important; 
            }}
            [class*="st-key-co_filter_bar_{key}"]:hover [data-testid="stWidgetLabel"]{{
                background-color: var({hover_label_bg}) !important;
            }}

            /* Hover Border */
            [class*="st-key-co_filter_bar_{key}"]:hover [data-baseweb="select"] > div {{
                border-color: var(--bk-primary) !important;
            }}

        </style>
    """
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    # 6. Renderização do Selectbox já indexado no valor correto
    with st.container(key=f"co_filter_bar_{key}"):
        selected = st.selectbox(
            label=options["label"],
            options=modified_options,
            index=default_index,
            key=key
        )

    if config["update_app_context"] == True:
        context.update_filter(options["column"], selected)
        return selected
    else:
        return selected