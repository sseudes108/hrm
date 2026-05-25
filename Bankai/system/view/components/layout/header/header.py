import streamlit as st
from system.view.components.cards import draw_card
import system.control.managers.hash as hash_man
from system.view.components.layout.header import nav_header

## EXEMPLO
# header_config = {
#     "model": "nav", # nav, ticker, slim
#     "nav_pages": ["tab1", "tab2"], #only with model nav
#     "has_card": True,
#     "hover": False,
#     "app_name": "bankai",
#     "title": "title",
#     "subtitle": "subtitle",
#     "logo_left": "png"
# }

def draw(header_config: dict):
    header_config["key"] = hash_man.get_hash_key(
        header_config["app_name"], header_config["title"]
    )
    
    card_config = {
        "model": "header",
        "has_title": False,
        "header": {"title": "title", "subtitle": "subtitle"},
        "hover": False,
        "key": header_config["key"]
    }

    draw_card(card_config, render_content=lambda: get_component(header_config))

def get_component(header_config:dict):
    if header_config["model"] == "nav":
        nav_header.get_component(header_config)

# import streamlit as st
# import base64
# from system.control.managers.error import check_title_key
# # from system.control.config import set_theme
# from system.view.components.helper import get_lucide_svg
# from system.control.contexts.app import AppContext
# from system.view.layout.fixes import draw_empty_element

# def get_b64(theme):
#     is_dark = theme["meta"]["base"] == "dark"

#     if is_dark:
#         svg_code = get_lucide_svg("lightbulb", theme["colors"]["text"])
#     else:
#         svg_code = get_lucide_svg("lightbulb-off", theme["colors"]["text"])

#     b64 = base64.b64encode(svg_code.encode()).decode()
#     return b64

# def draw(icon, context:AppContext , title=None, background=False, toggle_btn=True, ticker=True, ticker_list=None, key=None):
#     if check_title_key(title, key) == 0:
#         st.error("Header sem titulo. Defina a key.")
#         return

#     with st.container(key="container_header_"):
#         unique_style = ""
#         if background:
#             unique_style = f"""
#                 <style>
#                     /* Wrapper */
#                     [class*="st-key-container_header_"] {{
#                         background-color: var(--bk-secondary) !important;
#                         position: absolute !important; 
#                         left: 0 !important;
#                         top: 0 !important;

#                         height: var(--bk-header-h) !important; /* <--- DINÂMICO! */
#                         z-index: 1000;

#                         padding-left: var(--bk-sp-lg) !important;
#                         padding-right: var(--bk-sp-lg) !important;
#                         display: flex !important;
#                         align-items: center !important;
#                     }}
#                     /* Color Title */
#                     [class*="st-key-container_header_"] .header-title {{
#                         color: var(--bk-bg) !important;
#                     }}
#                     /* Color Ticker */
#                     [class*="st-key-container_header_"] .ticker-move {{
#                         color: var(--bk-bg) !important;
#                     }}
#                 </style>
#             """
#         st.markdown(unique_style.replace('\n', ' '), unsafe_allow_html=True)
#         cols = st.columns([1.5, 7, 0.5], gap='xxsmall')
#         with cols[0]:
#             if title:
#                 st.markdown(f"""
#                     <div class="custom-header">
#                         <div class="header-title">
#                             <span>{icon}</span> 
#                             <span>{title}</span>
#                         </div>
#                     </div>
#                 """.replace("\n", "").strip(), unsafe_allow_html=True)
#             else:
#                 pass
        
#         with cols[1]:
#             if ticker:
#                 ticker_list = [
#                     "🚨 Alerta de Fraude detectado em São Paulo às 11:20",
#                     "⚔️ Batalha de Kurukshetra: Novos manuscritos traduzidos",
#                     "🚀 Sistema atualizado para Versão 1.1",
#                     "💎 Valor do Dharma subiu 5% no último capítulo",
#                     "📈 Dashboard conectado à base JSON com sucesso"
#                 ]
#                 news_string = " &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; ".join(ticker_list)
#                 st.markdown(f"""
#                     <div class="ticker-wrap">
#                         <div class="ticker-move">
#                             {news_string}
#                         </div>
#                     </div>
#                 """.replace("\n", "").strip(), unsafe_allow_html=True)
#             else:
#                 pass

#         with cols[2]:
#             if toggle_btn:
#                 with st.container(key=f"toggle_theme_btn_container_{key}"):                    
#                     if st.button(f"", key=f"toggle_{key}"):

#                         next_mode = "light" if context.mode == "dark" else "dark"

#                         context.update_mode(next_mode)
#             else:
#                 pass

#     draw_empty_element(42)