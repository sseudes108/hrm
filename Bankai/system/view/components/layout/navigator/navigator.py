import streamlit as st
from dataclasses import dataclass
from system.view.components.cards import card

VALID_MODELS = ["tabs", "arrows", "header_nav"]

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
    html_content = f"""
        <style>
        [class*="st-key-{active_key}"] button {{
            border-bottom: 2px solid var(--bk-primary) !important;
            color: var(--bk-text) !important;
            font-weight: var(--bk-w-medium) !important;
        }}
        </style>
    """
    st.html(html_content)


def _inject_active_css(app_name: str, active_key: str):
    """Destaca o botão ativo pelo seu st-key único."""
    html_content = f"""
        <style>
        [class*="st-key-{active_key}"] button {{
            border-bottom: 2px solid var(--bk-primary) !important;
            color:         var(--bk-text) !important;
            font-weight:   var(--bk-w-medium) !important;
        }}
        </style>
    """
    st.html(html_content)

def _split_pyramid(labels: list) -> list[list]:
    """Divide labels em linhas de pirâmide invertida. Ex: 8 -> [5, 3] | 6 -> [4, 2] | 3 -> [2, 1]"""
    total = len(labels)
    if total <= 4:
        return [labels]  # linha única
    
    first = (total + 1) // 2 + (1 if total % 2 == 0 else 0)
    return [labels[:first], labels[first:]]

def _draw_button(label, callback, btn_prefix, start, i):
    st.button(label, key=f"{btn_prefix}--{start + i}",
        on_click=callback, args=[start + i],
        use_container_width=True)
    
def _draw_button_sl(label, callback, btn_prefix, page_index, in_card=False):
    st.button(label, key=f"{btn_prefix}--{page_index}",
        on_click=callback, args=[page_index],
        use_container_width=True)

def draw(context, model: str = "tabs", is_sub: bool = False, nav_pages=[]):
    if nav_pages is []:
        st.error("Nav Pages esta vazia")
        return

    config = NavigatorConfig(context.app_name, model, nav_pages)

    if is_sub:
        current    = context.current_subpage or 1
        callback   = context.set_subpage
        btn_prefix = f"subnav-{config.app_name}"
    else:
        current    = context.current_page
        callback   = context.set_page
        btn_prefix = f"nav-{config.app_name}"

    active_key = f"{btn_prefix}--{current}"
    _inject_active_css(config.app_name, active_key)

    is_mobile = (context.screen_width < 640)

    with st.container(key=f"co_navigator_{model}_{config.app_name}_{nav_pages[0]}"):
        if is_mobile and len(config.labels) > 3:
            rows = _split_pyramid(config.labels)
            
            # A largura máxima é a quantidade de botões da primeira linha (Ex: 5)
            base_width = len(rows[0]) 
            start = 1
            
            for row in rows:
                n = len(row)
                
                if n == base_width:
                    # Linha 1 (Cheia): Não tem mola, apenas divide o espaço por igual
                    cols = st.columns(n)
                    for i, label in enumerate(row):
                        with cols[i]:
                            _draw_button(
                                label=label, callback=callback,
                                btn_prefix=btn_prefix, start=start, i=i
                            )
                else:
                    # Linha 2 (Menor): Calcula a mola usando a diferença da base
                    pad = (base_width - n) / 2
                    ratios = [pad] + [1] * n + [pad]
                    cols = st.columns(ratios)
                    for i, label in enumerate(row):
                        with cols[1 + i]: # Pula a coluna [0] que é a mola
                            _draw_button(
                                label=label, callback=callback,
                                btn_prefix=btn_prefix, start=start, i=i
                            )
                start += n
        else:
            # Desktop: linha única original
            cols = st.columns(len(config.labels))
            for i, (col, label) in enumerate(zip(cols, config.labels)):
                page_index = i + 1
                with col:
                    _draw_button_sl(
                        label=label, callback=callback,
                        btn_prefix=btn_prefix, page_index=page_index
                    )