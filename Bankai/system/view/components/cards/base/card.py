import streamlit as st
from dataclasses import dataclass, field
from typing import Optional, Callable

from system.core.managers.config import hash as hash_man
from system.core.contexts import AppContext

from system.core.log.view import warnings

# Defina os modelos válidos de card (ajuste conforme os tipos que você tem no sistema)
VALID_CARD_MODELS = {"base", "header", "wrapper", "metric", "chart"}

@dataclass
class CardConfig:
    card_id: str        # Identificador único DESTE card (ex: "sales_summary", "main_header")
    context: AppContext = None,
    model: str = "base"
    show_card:bool = True
    has_title: bool = False
    title: Optional[str] = None
    subtitle: Optional[str] = None
    icon: Optional[str] = None
    hover: bool = True

    # A chave será gerada pelo sistema, não deve ser passada na criação
    key: str = field(init=False) 

    def __post_init__(self):
        # 1. Valida o modelo do card
        if self.model not in VALID_CARD_MODELS:
            raise ValueError(f"model inválido para card: '{self.model}'. Escolha entre: {VALID_CARD_MODELS}")

        # 2. Cria a chave combinando as strings base para garantir unicidade total
        raw_string = f"{self.context.app_name}_{self.card_id}_{self.model}"
        
        # Gera o hash e anexa um prefixo claro para facilitar o debug no CSS do navegador
        self.key = f"{hash_man.get_hash(raw_string)}"

@dataclass
class CardRenderConfig:
    content: Callable[[], None]
    custom_title_html: Optional[str] = None
    right_side_html: Optional[str] = None

def draw(config: CardConfig, render: CardRenderConfig):
    if render.content is None:
        warnings.draw(
            alert="error", message="Render Content is None"
        )
        return
    
    comportamento = "hover" if config.hover else "static"
    bg = "bg" if config.show_card else "nobg"
    chave_container = f"co_card_{config.model}_{bg}_{comportamento}_{config.key}"

    with st.container(key=chave_container):

        if config.has_title:
            if render.right_side_html:
                title_col, r_html_col = st.columns([0.8, 0.2], gap="small")
            else:
                title_col, r_html_col = st.columns([1, 0.01])
            
            with title_col:
                if render.custom_title_html:
                    st.html(render.custom_title_html)

                elif config.title:
                    # 🚀 LÓGICA DO ÍCONE
                    icon_html = ""
                    if config.icon:
                        if config.icon.startswith(":material/"):
                            icon_name = config.icon.replace(":material/", "").replace(":", "")
                            # Usamos a cor do texto padrão ou primary, você pode ajustar no style
                            icon_html = f'<span class="material-symbols-rounded" style="font-size: 1.15em; color: var(--bk-text-muted);">{icon_name}</span>'
                        else:
                            icon_html = f'<span>{config.icon}</span>'

                    sub_html = f'<div class="bk-card-subtitle">{config.subtitle}</div>' if config.subtitle else ''
                    
                    custom_header = f"""            
                        <div class="bk-card-header">
                            <div class="bk-card-title">{icon_html}{config.title}</div>
                            {sub_html}
                        </div>
                    """
                    st.html(custom_header)
                
            with r_html_col:
                if render.right_side_html:
                    with st.container(key="co_cd_right_html_"):
                        st.html(render.right_side_html)

        return render.content()



























# def draw(config: CardConfig, render: CardRenderConfig):
#     # A verificação de None no content ainda é uma boa prática de segurança
#     if render.content is None:
#         st.error("Render Content is None")
#         return

#     comportamento = "hover" if config.hover else "static"
#     bg = "bg" if config.show_card else "nobg"
#     chave_container = f"co_card_{bg}_{comportamento}_{config.model}_{config.key}"

#     with st.container(key=chave_container):
        
#         # Só renderiza a área de cabeçalho se has_title for True
#         if config.has_title:
            
#             if config.has_action and render.right_side:
#                 title_col, col_action = st.columns([0.6, 0.4], gap="small")
#             else:
#                 title_col, col_action = st.columns([1, 0.01])
            
#             with title_col:
#                 if render.custom_title:
#                     render.custom_title()
#                 elif config.title:
                    
#                     # 🚀 LÓGICA DO ÍCONE
#                     icon_html = ""
#                     if config.icon:
#                         if config.icon.startswith(":material/"):
#                             # Limpa a string para pegar apenas o nome do ícone (ex: 'add', 'settings')
#                             icon_name = config.icon.replace(":material/", "").replace(":", "")
#                             # Usamos a cor do texto padrão ou primary, você pode ajustar no style
#                             icon_html = f'<span class="material-symbols-rounded" style="font-size: 1.15em; color: var(--bk-text-muted);">{icon_name}</span>'
#                         else:
#                             # Cai aqui se for um emoji
#                             icon_html = f'<span>{config.icon}</span>'

#                     sub_html = f'<div class="bk-card-subtitle">{config.subtitle}</div>' if config.subtitle else ''
                    
#                     custom_header = f"""            
#                         <div class="bk-card-header">
#                             <div class="bk-card-title">{icon_html}{config.title}</div>
#                             {sub_html}
#                         </div>
#                     """
#                     st.html(custom_header)
                
#             with col_action:
#                 if config.has_action and render.right_side:
#                     render.right_side()
                                
#         # Desenha o conteúdo principal (obrigatório)
#         return render.content()