# import io
# import pandas as pd
# import streamlit as st

# from system.control.managers import hash as hash_man
# import system.control.managers.filter   as filter_man
# from system.view.components.tables.logic import filter_columns

# ## EXEMPLO
# # table_config = {
# #     "app_name": "bankai",
# #     "titulo": "test_debug_table",
# #     "subtitulo": "subtitulo"
# #     "height": 500,
# #     "ft_bar_config": {
# #         "update_app_context": False,
# #         "num_colunas": 5, 
# #         "labels": {
# #             "title": "Title",
# #             "status": "Status",
# #             "rating": "Rating",
# #             "year": "Year",
# #             "genres": "Genres"
# #         },
# #         "columns_df": ["title", "status", "rating", "year", "genres"]
# #     }
# # }
# ######################################################################

# def get_table_config(
#     app_name:str, titulo:str, subtitulo:str, height:int = 500, 
#     filter_labels:dict = {}, filter_df_coluns:list = []
# ):
#     if filter_labels == {}:
#         st.error("Defina o dicionario de labels.")
#         return
    
#     if filter_df_coluns == []:
#         st.error("Defina o a lista de colunas correspondentes dicionario de labels.")
#         return
    
#     if len(filter_labels) != len(filter_df_coluns):
#         st.error("Número de labels diferente do numero de colunas")
#         return
    
#     return {
#         "app_name": app_name,
#         "titulo": titulo,
#         "subtitulo": subtitulo,
#         "height": height,
#         "ft_bar_config": {
#             "update_app_context": False,
#             "num_colunas": len(filter_df_coluns), 
#             "labels": filter_labels,
#             "columns_df": filter_df_coluns
#         }
#     }


# def reset_table_filters(context, config, title_key):
#     """Callback para limpar o session_state dos filtros e ordenação"""
    
#     # 1. Força os filtros de volta para "Todos"
#     for col in config.get("columns_df", []):
#         label = config["labels"].get(col, col)
#         label_key = hash_man.get_hash(label)
#         widget_key = hash_man.get_hash_key(f"{context.app_name}_{title_key}_{label_key}", label)
        
#         if widget_key in st.session_state:
#             st.session_state[widget_key] = "Todos" # Em vez de del, forçamos o valor

#     # 2. Reseta a ordenação para o padrão (1ª coluna, Decrescente)
#     sort_col_key = f"sort_col_{title_key}"
#     sort_asc_key = f"sort_asc_{title_key}"
    
#     if sort_col_key in st.session_state:
#         st.session_state[sort_col_key] = config["columns_df"][0]
#     if sort_asc_key in st.session_state:
#         st.session_state[sort_asc_key] = False

# def draw(df: pd.DataFrame, context, table_config: dict, table_body):
#     key = hash_man.get_hash(table_config["titulo"])
    
#     # ---------------------------------------------------------
#     # 1. INICIALIZAÇÃO DE ESTADO DE ORDENAÇÃO
#     # ---------------------------------------------------------
#     sort_col_key = f"sort_col_{key}"
#     sort_asc_key = f"sort_asc_{key}"
    
#     if sort_col_key not in st.session_state:
#         st.session_state[sort_col_key] = table_config["ft_bar_config"]["columns_df"][0] # Padrão: 1ª coluna
#     if sort_asc_key not in st.session_state:
#         st.session_state[sort_asc_key] = False # Padrão: Maior pro Menor

#     # ---------------------------------------------------------
#     # 2. RENDERIZAÇÃO DOS FILTROS (Guarda os selects ativos)
#     # Aqui os selectboxes são desenhados invisivelmente ou na UI
#     # e retornam o dicionário de filtros aplicados.
#     # ---------------------------------------------------------
#     with st.container(key=f"co_table_{key}", height=table_config["height"]):
#         head_cols = st.columns([2.2, 8, 3], gap='small', vertical_alignment="center")

#         # --- O NOVO TÍTULO HTML ---
#         with head_cols[0]:
#             titulo_txt = table_config.get("titulo", "Tabela")
#             subtitulo_txt = table_config.get("subtitulo", "Dados de Performance") # Subtítulo padrão
            
#             html_header = f"""
#             <div class="table-header-group">
#                 <div class="title-accent"></div>
#                 <div class="header-text-stack">
#                     <span class="table-header-main-title">{titulo_txt}</span>
#                     <span class="table-header-sub-title">{subtitulo_txt}</span>
#                 </div>
#             </div>
#             """
#             st.markdown(html_header, unsafe_allow_html=True)

#         with head_cols[1]:
#             # Desenha os filtros no meio
#             selects = filter_columns.renderizar_filtros_dinamicos(
#                 df, context, config=table_config["ft_bar_config"], title_key=key
#             )

#         # ---------------------------------------------------------
#         # 3. PIPELINE DE DADOS (Processa TUDO antes do body)
#         # ---------------------------------------------------------
#         # A. Aplica filtros
#         df_final = filter_man.apply_filters(df.copy(), selects)
        
#         # B. Aplica Ordenação
#         coluna_ordenacao = st.session_state[sort_col_key]
#         ordem_ascendente = st.session_state[sort_asc_key]
        
#         # Só ordena se a coluna existir no DF
#         if coluna_ordenacao in df_final.columns:
#             df_final = df_final.sort_values(by=coluna_ordenacao, ascending=ordem_ascendente)

#         # ---------------------------------------------------------
#         # 4. TOOLBAR (Botões de Ação + Ordenação)
#         # ---------------------------------------------------------
#         with head_cols[2]:
#             with st.container(key=f"co_table_tools_{key}"):
#                 # Proporção: Selectbox recebe peso 3, cada botão peso 1
#                 tool_cols = st.columns([6, 1, 1, 1, 1], gap='xxsmall', vertical_alignment="center")
                
#                 # O Selectbox de Ordenação (Agora espremido à esquerda dos botões)
#                 with tool_cols[0]:
#                     st.selectbox(
#                         "Ordenar por", 
#                         options=table_config["ft_bar_config"]["columns_df"], 
#                         key=sort_col_key+"0",
#                         label_visibility="collapsed"
#                     )
                
#                 # Os 4 botões na sequência
#                 with tool_cols[1]:
#                     st.button("🔄", key=f"btn_reset_{key}", help="Resetar",
#                               on_click=reset_table_filters,
#                               args=(context, table_config["ft_bar_config"], key))
                    
#                 with tool_cols[2]:
#                     if st.button("🔼", key=f"btn_asc_{key}", help="Menor para Maior"):
#                         st.session_state[sort_asc_key] = True
#                         st.rerun()

#                 with tool_cols[3]:
#                     if st.button("🔽", key=f"btn_desc_{key}", help="Maior para Menor"):
#                         st.session_state[sort_asc_key] = False
#                         st.rerun()

#                 with tool_cols[4]:
#                     # Download Excel
#                     buffer = io.BytesIO()
#                     df_final.to_excel(buffer, index=False, engine='openpyxl')
#                     st.download_button(
#                         label="⬇️", data=buffer.getvalue(), 
#                         file_name=f"{table_config['titulo']}.xlsx",
#                         key=f"btn_down_{key}", help="Baixar Excel"
#                     )
        
#         # ---------------------------------------------------------
#         # 5. RENDER DO BODY
#         # ---------------------------------------------------------
#         with st.container(key=f"table_body_{key}"):
#             # Passa o dado já mastigado, filtrado e ordenado para o renderizador customizado
#             table_body(df=df_final, key=key)