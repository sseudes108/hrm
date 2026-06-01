import streamlit as st
import pandas as pd

import system.view.components.filters as select_filter
from system.control.contexts.app import AppContext
from system.control.managers import hash as hash_man

# Exemplo de como a configuração deve chegar
config = {
    "num_colunas": 4, 
    "labels": {
        "pais": "País",
        "estado": "Estado",
        "cidade": "Cidade",
        "status": "Status"
    },
    "columns_df": ["pais", "estado", "cidade", "status"]
}
##############################################

def renderizar_filtros_dinamicos(
        df:pd.DataFrame, context:AppContext, config:dict, title_key:str
    ):
    num_cols = config.get("num_colunas", 4)
    colunas_para_filtrar = config.get("columns_df", [])
    labels = config.get("labels", {})
    
    selects = {}

    # Quebra a lista de colunas em blocos do tamanho de 'num_cols'
    for i in range(0, len(colunas_para_filtrar), num_cols):
        bloco = colunas_para_filtrar[i : i + num_cols]
        
        # Cria a linha do Streamlit com o número fixo de colunas
        st_cols = st.columns(num_cols, gap='xxsmall')
        
        # Preenche cada coluna da linha atual
        for idx, nome_coluna in enumerate(bloco):
            with st_cols[idx]:
                label = labels.get(nome_coluna, nome_coluna)
                label_key = hash_man.get_hash(label)

                options = {
                    "df": df,
                    "label": label,
                    "column": nome_coluna
                }
                config = {
                    "id": f"{title_key}_{label_key}",
                    "has_card": False,
                    "allow_all": True,
                    "update_app_context": config["update_app_context"],
                }
                selected = select_filter.draw(
                    options, context, config
                )

                selects[nome_coluna] = selected
    
    return selects