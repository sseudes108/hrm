import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import uuid

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Bankai Dashboard - Interativo", layout="wide")

# --- 2. ESTADO DA SESSÃO (O "Cérebro" do Filtro) ---
if "filtro_faccao" not in st.session_state:
    st.session_state.filtro_faccao = None

# --- 3. MOCK DATA (Dados Fictícios) ---
def get_mock_data():
    data = {
        "Pandavas": {
            "cor": "#c084fc",
            "poder": [850, 950, 1100, 1050, 1300, 1400, 1450],
            "metricas": {"Dharma": "98%", "Soldados": "1.2M", "Líder": "Yudhisthira"}
        },
        "Kauravas": {
            "cor": "#ef4444",
            "poder": [1200, 1150, 1300, 1250, 1200, 1100, 1050],
            "metricas": {"Dharma": "42%", "Soldados": "1.5M", "Líder": "Duryodhana"}
        }
    }
    return data

mock_db = get_mock_data()

# --- 4. CSS CUSTOMIZADO (Glassmorphism sutil) ---
st.markdown("""
    <style>
    [data-testid="stMetricBlock"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #c084fc;
    }
    .main { background-color: #1a1a2e; }
    </style>
""", unsafe_allow_html=True)

# --- 5. FUNÇÕES DE RENDERIZAÇÃO ---

def render_pie_filter():
    options = {
        "backgroundColor": "transparent",
        "title": {"text": "Distribuição de Exércitos", "left": "center", "textStyle": {"color": "#eee"}},
        "tooltip": {"trigger": "item"},
        "legend": {"bottom": "0", "textStyle": {"color": "#aaa"}},
        "series": [{
            "name": "Facção",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 10, "borderColor": "#1a1a2e", "borderWidth": 2},
            "label": {"show": False},
            "data": [
                {"value": 7, "name": "Pandavas", "itemStyle": {"color": "#c084fc"}},
                {"value": 11, "name": "Kauravas", "itemStyle": {"color": "#ef4444"}},
            ]
        }]
    }
    
    # Captura o clique no nome da fatia
    events = {"click": "function(params) { return params.name; }"}
    
    return st_echarts(options=options, events=events, height="400px", key="pie_main")

def render_line_chart(faccao=None):
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    if faccao and faccao in mock_db:
        # Mostra apenas a facção selecionada
        series_data = [{
            "name": faccao,
            "type": "line",
            "smooth": True,
            "data": mock_db[faccao]["poder"],
            "lineStyle": {"width": 4, "color": mock_db[faccao]["cor"]},
            "areaStyle": {"opacity": 0.1, "color": mock_db[faccao]["cor"]}
        }]
    else:
        # Mostra ambas para comparação
        series_data = [
            {"name": "Pandavas", "type": "line", "smooth": True, "data": mock_db["Pandavas"]["poder"], "lineStyle": {"color": "#c084fc"}},
            {"name": "Kauravas", "type": "line", "smooth": True, "data": mock_db["Kauravas"]["poder"], "lineStyle": {"color": "#ef4444"}}
        ]

    options = {
        "backgroundColor": "transparent",
        "title": {"text": "Evolução do Poder de Batalha", "textStyle": {"color": "#eee"}},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": dias, "axisLabel": {"color": "#888"}},
        "yAxis": {"type": "value", "splitLine": {"lineStyle": {"color": "#333"}}},
        "series": series_data
    }
    st_echarts(options=options, height="400px", key=f"line_{faccao}")

# --- 6. LAYOUT DA PÁGINA ---

st.title("🏹 Kurukshetra Strategy Room")
st.markdown("---")

col_left, col_right = st.columns([1, 2])

with col_left:
    res = render_pie_filter()

    # Verifica se res não é nulo e se é um dicionário (o novo padrão do st_echarts)
    if res and isinstance(res, dict):
        # O valor clicado geralmente fica dentro de 'chart_event'
        # Se for nulo dentro do dicionário, ignoramos
        evento = res.get("chart_event")
        if evento:
            st.session_state.filtro_faccao = str(evento)
            st.rerun()
    elif res and isinstance(res, str):
        # Caso sua versão ainda retorne string pura
        st.session_state.filtro_faccao = res
        st.rerun()

with col_right:
    # Métricas dinâmicas
    f = st.session_state.filtro_faccao
    m_col1, m_col2, m_col3 = st.columns(3)
    
    if f:
        m_col1.metric("Dharma", mock_db[f]["metricas"]["Dharma"])
        m_col2.metric("Efetivo", mock_db[f]["metricas"]["Soldados"])
        m_col3.metric("Líder Atual", mock_db[f]["metricas"]["Líder"])
    else:
        m_col1.metric("Total de Facções", "2")
        m_col2.metric("Total de Divisões", "18 Akshauhinis")
        m_col3.metric("Status", "Em Conflito")

    # Gráfico de Linha dependente do filtro
    render_line_chart(f)

st.info("💡 **Dica:** Clique em uma fatia do gráfico de pizza para filtrar o dashboard inteiro.")