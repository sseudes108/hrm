import streamlit as st
import plotly.express as px
import pandas as pd
from Control.Managers import json_manager as JsonMan

def draw_donut_chart(df: pd.DataFrame, coluna: str, titulo: str, cliente, key=None):
    """
    Desenha um gráfico de rosca baseado em uma coluna do DataFrame.
    Recebe um dicionário opcional de cores (ex: {'Aprovado': '#27AE60'}).
    """
    if df.empty:
        st.info("Sem dados para gerar o gráfico.")
        return
    
    config_cliente = JsonMan.load_json("Control/Config/clientes.json", cliente)
    paleta = config_cliente.get("paleta_grafico", px.colors.qualitative.Prism)

    # 1. Agrupa os dados para contar as ocorrências
    df_counts = df[coluna].value_counts().reset_index()
    df_counts.columns = [coluna, 'quantidade']

    # 2. Cria o gráfico de rosca (hole=0.5 define o buraco no meio)
    fig = px.pie(
        df_counts, 
        values='quantidade', 
        names=coluna, 
        hole=0.5,
        title=f"<b>{titulo}</b>",
        color_discrete_sequence=paleta # Aplica a paleta do cliente aqui
    )

    # 3. Ajustes de Layout para o estilo Corporativo
    fig.update_traces(
        textposition='inside', 
        textinfo='percent',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1,
    )

    fig.update_layout(
        showlegend=True,
        # Ajuste da Legenda para o canto superior direito
        legend=dict(
            orientation="v",      # "v" para vertical (um embaixo do outro)
            yanchor="top",        # Alinha o topo da legenda
            y=1,                  # Posiciona no topo (1)
            xanchor="left",       # Ancoragem à esquerda do ponto X
            x=1.05,               # Um pouco para fora do gráfico (à direita)
        ),
        margin=dict(t=50, b=20, l=20, r=100), # Aumentamos a margem direita (r) para caber a legenda
        height=400
    )
    # 4. Renderiza no Streamlit
    st.plotly_chart(fig, width='stretch', key=f"{key}_donut_chart")

def draw_bar_chart(df: pd.DataFrame, eixo_x: str, titulo: str, cliente, key=None):
    if df.empty:
        st.info("Sem dados para gerar o gráfico.")
        return

    config_cliente = JsonMan.load_json("Control/Config/clientes.json", cliente)
    paleta = config_cliente.get("paleta_grafico", ["#D3D3D3", "#4A90E2"])
    
    # Invertemos a paleta para o maior valor ter a cor mais forte
    paleta_corrigida = paleta[::-1] 

    # 1. Agrupamento
    df_counts = df[eixo_x].value_counts().reset_index()
    df_counts.columns = [eixo_x, 'quantidade']
    
    # --- ORDENAÇÃO DO DATAFRAME ---
    # Ordenamos o DF pela coluna do eixo X (ex: as horas) de forma crescente
    # antes de passar para o Plotly
    df_counts = df_counts.sort_values(by=eixo_x, ascending=True)
    
    # Garantimos que seja string para o layout categórico
    df_counts[eixo_x] = df_counts[eixo_x].astype(str)

    # 2. Criação do Gráfico
    fig = px.bar(
        df_counts,
        x=eixo_x,
        y='quantidade',
        title=f"<b>{titulo}</b>",
        text='quantidade',
        color='quantidade',
        color_continuous_scale=paleta_corrigida 
    )

    # 3. Ajustes de Layout e Ordenação do Eixo
    fig.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # margin=dict(t=50, b=20, l=20, r=20),
        yaxis=dict(range=[0, df_counts['quantidade'].max() * 1.15]), # Dá 15% de folga no topo
        margin=dict(t=30, b=0, l=0, r=0), # Garante margem superior interna
        height=400,
        # 'category ascending' força o Plotly a seguir a ordem alfabética/numérica das labels
        xaxis={
            'type': 'category', 
            'categoryorder': 'category ascending' 
        }
    )
    
    fig.update_traces(
        textposition='outside',
        opacity=0.9,
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )

    st.plotly_chart(fig, width='stretch', key=f"{key}_bar_chart")