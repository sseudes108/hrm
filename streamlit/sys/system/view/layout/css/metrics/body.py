"""
styles/metrics/body.py — Bankai 
CSS do corpo interno das métricas (valores, colunas e alinhamento do Sparkline).
Totalmente estático e acoplado às variáveis de texto do design system.
"""

def get_css_body() -> str:
    return """
        /* Container que envolve as colunas */
        [class*="st-key-metric_body_"] {
            flex-grow: 1 !important; /* Ocupa todo o resto do card */
            display: flex !important;
            flex-direction: column !important;
            width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
            margin-top: 0 !important;
        }

        /* A estrutura de colunas do Streamlit */
        [class*="st-key-metric_body_"] > div[data-testid="stHorizontalBlock"] {
            height: 100% !important;
            flex-grow: 1 !important;
            gap: 0 !important; /* Cola uma coluna na outra */
        }

        /* Cada coluna individual */
        [class*="st-key-metric_body_"] div[data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
            height: 20% !important;
        }

        [class*="st-key-metric_body_"] > div[data-testid="stHorizontalBlock"] {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* --- Lado do Valor --- */
        [class*="st-key-metric_body_value_"] {
            width: 100% !important;
            height: 100% !important; 
            flex-grow: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important; /* Alinha o texto à esquerda */
            justify-content: center !important;
            padding-left: 20px !important; /* Respiro na esquerda */
            margin-left: -30% !important;
        }

        /* Sub-label adaptável baseada no tema ativo */
        .mcard-sub-label {
            color: var(--bk-text-muted) !important;
            font-family: var(--bk-font) !important;
            font-size: var(--bk-sm) !important;
        }

        /* --- Lado do Sparkline --- */
        [class*="st-key-metric_body_spark_"] {
            height: 100% !important;
            transform: translateY(-20px) !important;
            padding-bottom: 10px !important;
            padding-right: 4px !important;
        }

        /* Forçar o ECharts a ocupar a largura mas crescer na altura */
        [class*="st-key-metric_body_spark_"] > div {
            width: 100% !important;
            height: 80px !important; /* Aumenta a altura do gráfico dentro do card */
        }
    """