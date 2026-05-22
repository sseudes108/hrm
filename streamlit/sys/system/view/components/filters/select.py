import hashlib
import streamlit as st

def draw_select_filter(title, options, context, label_width="5", allow_all=True):
    """
    Componente de filtro customizado com suporte a 'Selecionar Todos' e persistência de estado.
    """
    # 1. Geração do Hash estável para a Key
    title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()[:6] if title else "default"
    key = f"f_select_{title_hash}"

    # 2. Injeta a opção "Todos" no início da lista, se permitido
    modified_options = list(options)
    if allow_all and "Todos" not in modified_options:
        modified_options.insert(0, "Todos")

    # 3. Mapeia o título para a chave exata que você usa no context (ex: "Nome" -> "nome")
    context_key = title.lower()

    # 4. CAPTURA DO ESTADO ANTERIOR: Verifica se já existia um valor salvo no contexto
    previous_value = context.active_filters.get(context_key, "Todos")

    # 5. Descobre qual o índice do valor anterior na nova lista de opções
    # Se o valor anterior sumiu da lista devido a outro filtro cruzado, foca no "Todos" (índice 0)
    try:
        default_index = modified_options.index(previous_value)
    except ValueError:
        default_index = 0

    # Estilização CSS customizada
    unique_style = f"""
        <style>
            [class*="st-key-container_filter_bar_"] [data-testid="stWidgetLabel"] {{
                width:{label_width}rem !important;
                min-width: 5rem !important;
            }}

            /* Hover no campo usando o seu theme dinâmico */
            [class*="st-key-container_filter_bar_{key}"]:hover [data-baseweb="select"] > div {{
                border-color: {context.theme['colors']['primary']} !important;
            }}
        </style>
    """
    st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

    # 6. Renderização do Selectbox já indexado no valor correto
    with st.container(key=f"container_filter_bar_{key}"):
        selected = st.selectbox(
            label=title,
            options=modified_options,
            index=default_index, # <--- ESSA É A CORREÇÃO CRUCIAL
            key=key
        )

    return selected