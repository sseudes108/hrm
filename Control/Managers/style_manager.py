import streamlit as st
from Control.Managers import design_manager as DesignMan

def carregar_css(cliente):
    cor_cliente = DesignMan.get_cor_destaque(cliente)
    
    # Cálculo do RGB para o fundo da aba
    r = int(cor_cliente[1:3], 16)
    g = int(cor_cliente[3:5], 16)
    b = int(cor_cliente[5:7], 16)

    st.markdown(f"""
        <style>
        /* 1. Reset de Espaçamento Principal - Mantemos, mas com cuidado */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }}

        /* 2. REMOVIDO o margin-top negativo global que quebrou tudo */
        /* Em vez disso, apenas reduzimos o gap padrão entre blocos */
        [data-testid="stVerticalBlock"] {{
            gap: 0.5rem !important;
        }}

        /* 3. Estilização das Abas (Tabs) - Ajustado para não colar */
        button[data-baseweb="tab"] {{
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #5f6368 !important;
            padding: 8px 16px !important;
        }}

        button[aria-selected="true"] {{
            color: {cor_cliente} !important;
            border-bottom: 3px solid {cor_cliente} !important;
            background-color: rgba({r}, {g}, {b}, 0.08) !important;
        }}

        /* 4. Selectboxes mais compactos */
        div[data-baseweb="select"] > div {{
            background-color: #f8f9fa !important;
            border-radius: 6px !important;
            min-height: 35px !important;
        }}

        /* 5. FIX: Aproximar apenas os filtros e métricas, sem quebrar o resto */
        /* Isso remove o espaço excessivo acima das abas */
        .stTabs {{
            margin-top: -1.5rem !important;
        }}

        /* 6. Esconder lixo visual */
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* 7. Ajuste para os Gráficos não ficarem colados no topo do container */
        [data-testid="stMetric"] {{
            background-color: white !important;
            padding: 10px !important;
            border-radius: 8px !important;
        }}

        /* 1. Espaço entre os Filtros e os Cards de Métricas */
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]),
        div[data-testid="stHorizontalBlock"]:has(div[style*="border-left"]) {{
            margin-top: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }}

        /* 2. Garante que o container do gráfico tenha um respiro interno no topo */
        /* Isso evita que o rótulo da barra (ex: 123) encoste na borda colorida */
        [data-testid="stVerticalBlock"] > div:has(div[style*="background-color"]) + div {{
            padding-top: 10px !important;
        }}

        /* 3. Espaço extra acima do rodapé "Registros encontrados" */
        .stMarkdown:has(code), .stText {{
            margin-top: 2rem !important;
        }}
        </style>
    """, unsafe_allow_html=True)