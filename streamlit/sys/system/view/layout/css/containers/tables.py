"""
styles/containers/tables.py — Bankai 
Containers de tabelas de dados e linhas de filtros internos.
Totalmente estático, adaptando-se dinamicamente a temas Dark e Light.
"""

def get_css_tables() -> str:
    return """
        /* 1. CONTAINER PAI (O ENVELOPE DE VIDRO POLIDO) */
        [class*="st-key-chart_container_table_"] {
            position: relative !important;
            
            /* Fundo, desfoque e bordas herdam direto do tema ativo */
            background: var(--bk-grad-surface) !important;
            backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            -webkit-backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            
            border: var(--bk-border-w) solid var(--bk-border) !important;
            border-radius: var(--bk-radius-md) !important;
            margin-top: var(--bk-sp-xs) !important;
            padding: 0.1em !important;
            
            /* Sombras tridimensionais e quinas lapidadas */
            box-shadow: var(--bk-shadow-sm), var(--bk-card-inner-shadow) !important;
            transition: all 0.3s ease-in-out !important;
            margin-bottom: 20px !important;
            z-index: 1;
            overflow: hidden;
        }

        /* Pseudo-elemento para aplicar o Rim Light (Contraluz nas bordas de cristal) */
        [class*="st-key-chart_container_table_"]::before {
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

        [class*="st-key-chart_container_table_"]:hover {
            background: var(--bk-surface) !important;
            border-color: var(--bk-border-focus) !important;
            box-shadow: var(--bk-shadow-md), var(--bk-glow-primary) !important;
        }

        /* 2. CONTAINER DE FILTROS (A LINHA DE INPUTS) */
        [class*="st-key-table_filters_row_"] {
            background: transparent !important;
            border-radius: var(--bk-radius-md) !important;
            margin-top: 2em !important;
            margin-bottom: 0.2em !important;
            margin-left: 3em !important;
        }

        /* Estilo dos Labels dos Filtros */
        [class*="st-key-table_filters_row_"] label p {
            color: var(--bk-text-muted) !important;
            font-family: var(--bk-font) !important;
            font-size: 0.7rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-weight: var(--bk-w-bold) !important;
        }

        /* Inputs de Texto e Selectbox dentro da linha de filtros */
        [class*="st-key-table_filters_row_"] input, 
        [class*="st-key-table_filters_row_"] div[data-baseweb="select"] {
            /* color-mix gera um fundo escurecido sutil baseado na cor do texto do tema atual */
            background-color: color-mix(in srgb, var(--bk-text) 8%, transparent) !important;
            border: var(--bk-border-w) solid var(--bk-border) !important;
            color: var(--bk-text) !important;
            border-radius: var(--bk-radius-sm) !important;
            transition: border-color 0.2s ease, background-color 0.2s ease !important;
        }

        [class*="st-key-table_filters_row_"] input:focus {
            border-color: var(--bk-border-focus) !important;
        }

        /* 3. BOTÃO DE DOWNLOAD (EXPORTAR) */
        [class*="st-key-table_filters_row_"] button {
            background-color: transparent !important;
            border: var(--bk-border-w) solid var(--bk-primary) !important;
            color: var(--bk-primary) !important;
            font-family: var(--bk-font) !important;
            font-weight: var(--bk-w-medium) !important;
            border-radius: var(--bk-radius-sm) !important;
            transition: all 0.2s !important;
            width: 100% !important;
        }
        
        [class*="st-key-table_filters_row_"] button:hover {
            background-color: var(--bk-primary) !important;
            color: var(--bk-bg) !important; /* Texto inverte para a cor de fundo no hover */
            box-shadow: var(--bk-glow-primary) !important;
        }

        /* 4. AJUSTES DA TABELA HTML */
        [class*="st-key-chart_container_table_"] table {
            margin-top: 0px !important;
            margin-left: 0px !important;
            font-family: var(--bk-font) !important;
        }

        /* Efeito de zebra nas linhas adaptável */
        [class*="st-key-chart_container_table_"] tr:nth-child(even) {
            background: color-mix(in srgb, var(--bk-text) 2%, transparent) !important;
        }

        [class*="st-key-chart_container_table_"] tr:hover {
            background: color-mix(in srgb, var(--bk-text) 5%, transparent) !important;
        }
    """