def get_css_tables(theme: dict) -> str:
    c = theme["colors"]
    ty = theme["typography"]
    sp = theme["spacing"]
    b = theme["borders"]
    
    # Cores auxiliares para o efeito Glass
    glass_bg = "rgba(255, 255, 255, 0.05)"
    glass_border = "1px solid rgba(255, 255, 255, 0.1)"
    primary_rgba = c.get("primary", "#00ffa6")

    return f"""
        /* 1. CONTAINER PAI (O ENVELOPE DE VIDRO) */
        [class*="st-key-chart_container_table_"] {{
            background: {glass_bg} !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: {glass_border} !important;
            border-radius: {b['radius_md']} !important;
            margin-top: {sp['xs']} !important;
            padding: 0.1em !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
            transition: all 0.3s ease-in-out !important;
            margin-bottom: 20px !important;
        }}

        [class*="st-key-chart_container_table_"]:hover {{
            background:    {c['surface']} !important;
            transform:     translateY(0px);!important;
        }}

        /* 2. CONTAINER DE FILTROS (A LINHA DE INPUTS) */
        [class*="st-key-table_filters_row_"] {{
            background: rgba(0, 0, 0, 0) !important;
            border-radius: 8px !important;
            margin-top: 2em !important;
            margin-bottom: 0.2em !important;
            margin-left: 3em !important;
        }}

        /* Estilo dos Labels dos Filtros */
        [class*="st-key-table_filters_row_"] label p {{
            color: {c['text_muted']} !important;
            font-size: 0.7rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-weight: 600 !important;
        }}

        /* Inputs de Texto e Selectbox dentro da linha de filtros */
        [class*="st-key-table_filters_row_"] input, 
        [class*="st-key-table_filters_row_"] div[data-baseweb="select"] {{
            background-color: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 6px !important;
            transition: border-color 0.2s ease !important;
        }}

        [class*="st-key-table_filters_row_"] input:focus {{
            border-color: {primary_rgba} !important;
        }}

        /* 3. BOTÃO DE DOWNLOAD (EXPORTAR) */
        [class*="st-key-table_filters_row_"] button {{
            background-color: transparent !important;
            border: 1px solid {primary_rgba} !important;
            color: {primary_rgba} !important;
            font-weight: 500 !important;
            border-radius: {b['radius_sm']} !important;
            transition: all 0.2s !important;
            width: 100% !important;
        }}

        /* 4. AJUSTES DA TABELA HTML */
        [class*="st-key-chart_container_table_"] table {{
            margin-top: 0px !important;
            margin-left: 0px !important;
        }}

        /* Efeito de zebra nas linhas (opcional, mas ajuda na leitura) */
        [class*="st-key-chart_container_table_"] tr:nth-child(even) {{
            background: rgba(255, 255, 255, 0.01) !important;
        }}

        [class*="st-key-chart_container_table_"] tr:hover {{
            background: rgba(255, 255, 255, 0.03) !important;
            transform:     translateY(0px);!important;
        }}
    """