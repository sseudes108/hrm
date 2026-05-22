"""
styles/metrics/index.py — Bankai 
CSS dos cards de KPIs (Métricas).
Totalmente estático, utilizando variáveis globais e herança tridimensional.
"""

def get_css_header() -> str:
    return """
        /* O PAI (Container Externo - A Placa Polida) */
        [class*="st-key-metric_card_"] {            
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: stretch !important;
            justify-content: flex-start !important;
            
            min-height: 120px;
            max-height: 120px;
            
            /* Herança estrutural dinâmica do tema ativo */
            background: var(--bk-grad-surface) !important;
            backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            -webkit-backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            
            border: var(--bk-border-w) solid var(--bk-border) !important;
            border-radius: var(--bk-radius-md) !important;
            box-shadow: var(--bk-shadow-sm), var(--bk-card-inner-shadow) !important;
            
            /* Overflow visible para o tooltip vazar para cima */
            overflow: visible !important; 
            position: relative !important;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
        }

        /* Efeito de Hover no Card de Métrica */
        [class*="st-key-metric_card_"]:hover {
            transform: translateY(var(--bk-hover-y)) !important;
            border-color: var(--bk-border-focus) !important;
            box-shadow: var(--bk-shadow-md), var(--bk-glow-primary) !important;
        }

        /* Reduz o gap entre os elementos filhos do card */
        [class*="st-key-metric_card_"] > div {
            gap: 0 !important;
            row-gap: 0 !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* O FILHO (Cabeçalho do Card) */
        [class*="st-key-metric_header_"] {
            width: 100% !important;
            padding: var(--bk-sp-sm) var(--bk-sp-md) !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            min-height: 35px !important;
            overflow: visible !important;
            transform: translateY(-15px) !important;
        }
                
        [class*="st-key-metric_header_"] > div {
            overflow: visible !important;
            width: 100% !important;
        }

        [class*="st-key-metric_header_"] .mcard-titulo {
            font-family: var(--bk-font) !important;
            font-size: var(--bk-base) !important;
            color: var(--bk-text) !important;
            text-transform: uppercase !important;
            font-weight: var(--bk-w-bold) !important;
        }

        [class*="st-key-metric_header_"] .mcard-icon {
            display: flex !important;
            align-items: center !important;    
            justify-content: center !important; 

            width: 1em;
            height: 1em;
            color: var(--bk-primary) !important; /* Ícones ganham a cor de destaque */
        }

        /* ─── INFO & TOOLTIP (CORREÇÃO DE LAYOUT) ─── */
        
        /* Forçar o container do Streamlit a permitir que o tooltip "vaze" */
        [data-testid="stVerticalBlock"]:has(> [class*="st-key-metric_card_"]) {
            overflow: visible !important;
        }

        /* Tooltip adaptável */
        .mcard-tooltip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            z-index: 999999 !important; 
            bottom: 110%; 
            right: 10px;
            
            /* Cores e desfoque herdam do contexto do tema */
            background: color-mix(in srgb, var(--bk-surface-2) 95%, transparent) !important;
            backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            -webkit-backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            
            border: var(--bk-border-w) solid var(--bk-border) !important;
            padding: var(--bk-sp-sm) var(--bk-sp-md) !important;
            border-radius: var(--bk-radius-sm) !important;
            box-shadow: var(--bk-shadow-md) !important;
            color: var(--bk-text) !important;
            font-family: var(--bk-font) !important;
            font-size: var(--bk-sm) !important;
            
            pointer-events: none;
            transition: all 0.25s ease;
            transform: translateY(5px);
        }

        /* Seta do Tooltip baseada nas cores da borda do tema */
        .mcard-tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            right: 14px;
            border-width: 6px;
            border-style: solid;
            border-color: var(--bk-border) transparent transparent transparent !important;
        }

        .mcard-info {
            position: relative !important;
            overflow: visible !important;
            z-index: 101 !important;
        }

        .mcard-info:hover .mcard-tooltip {
            visibility: visible !important;
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    """