import pandas as pd
import streamlit as st
from datetime import datetime

import pages.erro as Erro

from Control.Managers import df_manager as DFMan
from Control.Managers import url_manager as UrlMan
from Control.Managers import streamlit_manager as STMan
from Control.Managers import design_manager as DesignMan
from Control.Managers import layout_manager as LayoutMan

from Control.Dashboards.HoraHora import hh_manager as HHMan

CLIENTES_VALIDOS = ["Santander", "Pan", "Itau", "Nubank"]

def create_tabs(cliente):
    cor_destaque = DesignMan.get_cor_destaque(cliente)
    hoje_tab, historico_tab = STMan.create_tabs(
        ["Hoje", "Histórico"], cor_destaque
    )
    return hoje_tab, historico_tab

def draw_hh(df, cliente, periodo):
    filtros = HHMan.draw_filtros(cliente, periodo, df)
    df_filtrado = DFMan.filtrar_df(df, filtros)

    st.write("")
    HHMan.show_metricas(df_filtrado)
    st.write("")
    HHMan.draw_graficos(df_filtrado, cliente, periodo)
    HHMan.show_dataframe(df_filtrado)

@st.cache_data
def load_base():
    df = pd.read_csv("df.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    df['inicio'] = pd.to_datetime(df['inicio'])
    df['hora'] = df['inicio'].dt.strftime('%H:00')
    hoje_str = datetime.now().strftime("%Y-%m-%d")

    df_hoje = df[df['data'] == hoje_str]
    df_historico = df

    return df_hoje, df_historico

def draw_page(cliente):
    DesignMan.draw_header(cliente, "Hora Hora")

    df_hoje, df_historico = load_base()
    hoje_tab, historico_tab = create_tabs(cliente)

    with hoje_tab:
        draw_hh(df_hoje, cliente, "hoje")
    
    with historico_tab:
        draw_hh(df_historico, cliente, "historico")

def main():
    cliente_param = st.query_params.get("cliente")
    acesso = UrlMan.validar_acesso(cliente_param, CLIENTES_VALIDOS)

    # Chamada do método de validação
    if acesso == True:
        # Normaliza o nome para exibição/lógica (ex: "santander" -> "Santander")
        cliente_final = cliente_param.strip().capitalize()
        
        LayoutMan.init_layout(cliente_final)
        draw_page(cliente_final)
    else:
        # Se validar_acesso for False, cai aqui
        LayoutMan.init_layout("Sistema")
        Erro.draw_page()

if __name__ == "__main__":
    main()