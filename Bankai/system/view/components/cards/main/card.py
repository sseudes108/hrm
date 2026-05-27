from dataclasses import dataclass
from typing import Optional
import streamlit as st

@dataclass
class CardConfig:
    model: str
    key: str
    has_title: bool = False
    title: Optional[str] = None
    subtitle: Optional[str] = None
    hover: bool = False

def draw_card(config: CardConfig, render_content=None, *args, **kwargs):
    if render_content is None:
        st.error("Render Content is None")
        return

    # Se hover for True, adicionamos a tag '_hover_' na chave
    comportamento = "hover" if config.hover else "static"
    
    # A chave gerada será algo como: co_card_hover_vendas_kpi1
    chave_container = f"co_card_{config.model}_{comportamento}_{config.key}"

    # Container perfeitamente limpo, sem injetar <style> no meio do HTML
    with st.container(key=chave_container):
        
        # Você já pode renderizar o título aqui dentro se quiser!
        if config.has_title and config.title:
            st.markdown(f"### {config.title}")
            if config.subtitle:
                st.caption(config.subtitle)
                
        # Roda o conteúdo dinâmico
        response = render_content(*args, **kwargs)

    return response

# def get_config(
#     model:str, 
#     key:str,
#     has_title:bool = False,
#     title:str = None,
#     subtitle:str = None,
#     hover:bool = False,
# ):
#     return {
#         "model": model,
#         "has_title": has_title,
#         "header":{
#             "title": title,
#             "subtitle": subtitle,
#         },
#         "hover": hover,
#         "key": key
#     }

# def draw_card(card_config: dict, render_content=None, *args, **kwargs):
#     if render_content is None:
#         st.error("Render Content is None")
#         return

#     key   = card_config["key"]
#     model = card_config["model"]
#     hover_y = "--bk-hover-y" if card_config["hover"] else "0"

#     # Injeta o estilo FORA do container (escopo global da página)
#     unique_style = f"""
#         <style>
#             [class*="st-key-co_card_{model}_{key}"]:hover {{
#                 transform: translateY(var({hover_y})) !important;
#             }}
#         </style>
#     """
#     st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)

#     # Container só com o conteúdo
#     with st.container(key=f"co_card_{model}_{key}"):
#         response = render_content(*args, **kwargs)

#     return response