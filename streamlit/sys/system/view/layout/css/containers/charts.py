"""
styles/containers/charts.py — Bankai 
Containers de gráficos com efeito tridimensional agnóstico e polido.
"""

def get_css_charts() -> str:
    return """
        /* 1. O CONTAINER PAI (Herança Direta da Placa Polida) */
        [class*="st-key-chart_container_"] {
            position: relative !important;
            
            /* Fundo e Efeitos de Vidro baseados no Tema Ativo */
            background: var(--bk-grad-surface) !important;
            backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            -webkit-backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            
            border: var(--bk-border-w) solid var(--bk-border) !important;
            border-radius: var(--bk-radius-md) !important;
            
            /* Sombras de peso + Chanfro de luz interno (Polimento) */
            box-shadow: var(--bk-shadow-sm), var(--bk-card-inner-shadow) !important;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out, border-color 0.3s ease-in-out, background 0.3s ease-in-out !important;

            margin-top: -1%;
            padding-top: 2%;
            padding-bottom: 1%;

            display:        flex !important;
            flex-direction: column !important;
            align-items:    center !important;
            overflow: hidden;
            z-index: 1;
        }

        /* Pseudo-elemento para aplicar o Rim Light (Contraluz nas bordas de cristal) */
        [class*="st-key-chart_container_"]::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: var(--bk-radius-md);
            padding: var(--bk-border-w);
            background: var(--bk-card-border-edge);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            z-index: -1;
        }

        /* HOVER DA PLACA DE GRÁFICOS */
        [class*="st-key-chart_container_"]:hover {
            border-color: var(--bk-border-focus) !important;
            transform: translateY(var(--bk-hover-y)) !important;
            box-shadow: var(--bk-shadow-md), var(--bk-glow-primary) !important;
        }

        /* 2. APENAS O CABEÇALHO (Markdown) */
        [class*="st-key-chart_container_"] .stMarkdown {
            width: 92% !important; /* Alinha com o início do desenho do gráfico */
            margin-left: auto !important;
            margin-right: auto !important;
            margin-bottom: -3% !important; /* Mantém o gráfico próximo ao texto */
            display: block !important;
        }

        /* 3. TIPOGRAFIA CONTROLADA PELO DESIGN SYSTEM */
        [class*="st-key-chart_container_"] h3 {
            color:       var(--bk-text) !important;
            font-family: var(--bk-font) !important;
            font-size:   var(--bk-sub) !important; /* var(--bk-sub) já traz px do base */
            font-weight: var(--bk-w-bold) !important;
            margin:      0 !important;
        }

        [class*="st-key-chart_container_"] p {
            color:       var(--bk-text-muted) !important;
            font-family: var(--bk-font) !important;
            font-size:   var(--bk-sm) !important;
            margin:      0 !important;
        }

        /* Destaque numérico interno */
        [class*="st-key-chart_container_"] .metric-value {
            color:       var(--bk-primary) !important;
            font-family: var(--bk-font-mono) !important;
            font-size:   var(--bk-sub) !important;
            font-weight: var(--bk-w-medium) !important;
        }
    """