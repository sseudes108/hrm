import streamlit as st
from dataclasses import dataclass
from system.control.contexts import AppContext

VALID_MODELS = ["tabs", "arrows"]

@dataclass
class NavigatorConfig:
    """
    Configuração do componente Navigator.

    Atributos:
        app_name: Identificador único do app — usado para nomear keys e seletores CSS.
        model:    Estilo visual do navegador. Valores aceitos: 'tabs', 'arrows'.
        labels:   Lista de rótulos exibidos nos botões, um por página.
    """
    app_name: str
    model: str
    labels: list[str]

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            st.error(f"Navigator — model inválido: '{self.model}'. Escolha entre: {VALID_MODELS}")
            st.stop()

        if not self.labels:
            st.error("Navigator — 'labels' não pode ser vazio.")
            st.stop()

def _inject_active_css(app_name: str, active_index: int):
    active_key = f"pag_{app_name}_p{active_index + 1}"
    st.markdown(f"""
        <style>
        [class*="st-key-{active_key}"] button {{
            border-bottom: 2px solid var(--bk-primary) !important;
            color: var(--bk-text) !important;
            font-weight: var(--bk-w-medium) !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def _inject_active_css(app_name: str, active_key: str):
    """Destaca o botão ativo pelo seu st-key único."""
    st.markdown(f"""
        <style>
        [class*="st-key-{active_key}"] button {{
            border-bottom: 2px solid var(--bk-primary) !important;
            color:         var(--bk-text) !important;
            font-weight:   var(--bk-w-medium) !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def draw(context: AppContext, model:str = "tabs", is_sub: bool = False, nav_pages=[]):
    """
    Renderiza o navegador de páginas.

    Parâmetros:
        config: Configuração do navigator (app_name, model, labels).
        context: Contexto global da aplicação.
        is_sub: Se True, controla current_subpage. Se False, controla current_page.

    Comportamento:
        - Navigator principal (is_sub=False): ao clicar, chama context.set_page()
          que troca a página e reseta current_subpage para None.
        - Subnavegador (is_sub=True): ao clicar, chama context.set_subpage()
          que troca apenas a subpágina sem tocar em current_page.
    """
    
    if nav_pages is []:
        st.error("Nav Pages esta vazia")
        return
    
    config = NavigatorConfig(
        context.app_name, model, nav_pages
    )
    
    if is_sub:
        current  = context.current_subpage or 1
        callback = context.set_subpage
        btn_prefix = f"subnav-{config.app_name}"
    else:
        current  = context.current_page
        callback = context.set_page
        btn_prefix = f"nav-{config.app_name}"

    active_key = f"{btn_prefix}--{current}"
    _inject_active_css(config.app_name, active_key)

    with st.container(key=f"co_navigator_{config.app_name}"):
        cols = st.columns(len(config.labels))
        for i, (col, label) in enumerate(zip(cols, config.labels)):
            page_index = i + 1
            btn_key    = f"{btn_prefix}--{page_index}"
            with col:
                st.button(
                    label,
                    key=btn_key,
                    on_click=callback,
                    args=[page_index],
                    use_container_width=True,
                )