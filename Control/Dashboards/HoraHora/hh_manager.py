import pandas as pd
import streamlit as st
from datetime import date

from View import filtros as Filtros
from View import graficos as Graficos
from View import metricas as Metricas
from Control.Managers import json_manager as JsonMan
from Control.Managers import design_manager as DesignMan

PATH_FILTROS = "Control/Dashboards/HoraHora"

def show_dataframe(df_filtrado: pd.DataFrame):
    st.markdown(f"**Registros encontrados:** {len(df_filtrado)}")
    st.dataframe(df_filtrado, width='stretch')

    st.markdown("---")

def show_metricas(df_filtrado):
    with st.container():
        # Criando os cards de resumo
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            total = len(df_filtrado)
            Metricas.draw_metric_card("📊", "Total", total, "#2c3e50")

        with col2:
            aprovados = len(df_filtrado[df_filtrado["resultado"] == "Aprovado"])
            Metricas.draw_metric_card("✅", "Aprovados", aprovados, "#27ae60")

        with col3:
            pendentes = len(df_filtrado[df_filtrado["resultado"] == "Pendente"])
            Metricas.draw_metric_card("⏳", "Pendentes", pendentes, "#f39c12")

        with col4:
            reprovados = len(df_filtrado[df_filtrado["resultado"].str.contains("Reprovado Politica")])
            Metricas.draw_metric_card("❌", "Reprovado por Politica", reprovados, "#e74c3c")

        with col5:
            reprovados = len(df_filtrado[df_filtrado["resultado"].str.contains("Reprovado Fraude")])
            Metricas.draw_metric_card("💀", "Reprovado por Fraude", reprovados, "#200300")

def draw_graficos(df_filtrado:pd.DataFrame, cliente, periodo):
    with st.container():
        col1, col2 = st.columns([1.5, 2.5])

    with col1:
        DesignMan.draw_borda_topo(cliente)
        with st.container(border=False):
            Graficos.draw_donut_chart(df_filtrado, "resultado", "Status", cliente, key=f"{cliente}_{periodo}")

    with col2:
        DesignMan.draw_borda_topo(cliente)
        with st.container(border=False):
            Graficos.draw_bar_chart(df_filtrado, "hora", "Produção Hora a Hora", cliente, key=f"{cliente}_{periodo}")


def draw_filtros(cliente, periodo, df: pd.DataFrame):
    filtro_path = f"{PATH_FILTROS}/filtros_{periodo}.json"
    filtros_salvos = JsonMan.load_json(filtro_path, cliente)
    filtros_atuais = {}

    if periodo == "hoje":
        campos = ["cliente", "fila", "analista", "resultado"]
        labels = ["Cliente", "Fila", "Analista", "Resultado"]
    elif periodo == "historico":
        campos = ["inicio", "fim", "cliente", "fila", "analista", "resultado"]
        labels = ["Início", "Fim", "Cliente", "Fila", "Analista", "Resultado"]

    with st.container():
        cols = st.columns(len(campos))
        
        for i, campo in enumerate(campos):
            with cols[i]:
                # Se for Início ou Fim no Histórico, desenha Date Input
                if periodo == "historico" and campo in ["inicio", "fim"]:
                    # Recupera do JSON ou usa hoje se vazio
                    val_salvo = filtros_salvos.get(f"{periodo}_{campo}", str(date.today()))
                    
                    # Desenha o filtro de data (passando o valor salvo convertido em date)
                    selecionado = Filtros.draw_date_filter(
                        label=labels[i], 
                        key=f"{periodo}_{campo}",
                        value=pd.to_datetime(val_salvo).date()
                    )
                    # Guarda como string para o JSON
                    filtros_atuais[f"{periodo}_{campo}"] = str(selecionado)
                
                else:
                    # --- Lógica de Filtragem Cruzada Corrigida ---
                    df_temp = df.copy()

                    # A) Primeiro passo: Aplicar SEMPRE o filtro de data no df_temp
                    # para que as opções de categoria respeitem o tempo selecionado
                    if periodo == "historico":
                        df_temp["data"] = pd.to_datetime(df_temp["data"])
                        f_ini = filtros_salvos.get(f"{periodo}_inicio", str(date.today()))
                        f_fim = filtros_salvos.get(f"{periodo}_fim", str(date.today()))
                        
                        mask = (df_temp["data"] >= pd.to_datetime(f_ini)) & \
                               (df_temp["data"] <= pd.to_datetime(f_fim))
                        df_temp = df_temp.loc[mask]

                    # B) Segundo passo: Aplicar os outros filtros de categoria (exceto o atual)
                    for outro_campo in campos:
                        if outro_campo in ["inicio", "fim"]: 
                            continue # Datas já foram tratadas acima
                            
                        val = filtros_salvos.get(f"{periodo}_{outro_campo}", "Todos")
                        if outro_campo != campo and val != "Todos":
                            # Verifica se a coluna existe no DF (ex: evita erro com chaves de UI)
                            if outro_campo in df_temp.columns:
                                df_temp = df_temp[df_temp[outro_campo] == val]
                    
                    # Agora sim: as opções únicas virão do DF já cortado por data e outros filtros
                    opcoes = ["Todos"] + sorted(df_temp[campo].unique().tolist())
                    
                    val_previo = filtros_salvos.get(f"{periodo}_{campo}", "Todos")
                    idx = opcoes.index(val_previo) if val_previo in opcoes else 0

                    selecionado = Filtros.draw_select_filter(
                        label=labels[i], 
                        options=opcoes, 
                        index=idx,
                        key=f"widget_{periodo}_{campo}"
                    )
                    filtros_atuais[f"{periodo}_{campo}"] = selecionado

    # Persistência e Rerun
    if filtros_atuais != filtros_salvos:
        filtros_salvos.update(filtros_atuais)
        JsonMan.save_json(filtro_path, filtros_salvos, cliente)
        st.rerun()
        
    return {c: filtros_atuais.get(f"{periodo}_{c}") for c in campos}