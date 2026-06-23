def reset_st_base() -> str:
    return """
        /* Esconder header padrão do Streamlit */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Esconder botão controlador da sidebar */
        button[data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Remover margens e colar conteudo no topo */
        .block-container {
            margin-top:     -1.6em !important;
            padding-top:    0 !important;
            padding-bottom: 0 !important;
            max-width:      100% !important;
            padding-left:   0 !important;
            padding-right:  0 !important;
        }
        
        /* Remover o gap entre os elementos base do container */
        .st-emotion-cache-tn0cau {
            gap: 0 !important;
        }
    """

def set_bankai_base(theme: dict) -> str:
    c  = theme["colors"]
    ty = theme["typography"]
    sp = theme["spacing"]
    b  = theme["borders"]
    ef = theme["effects"]
    overlay = ef["surface_overlay"]
    lay = theme["layout"]

    # Define o estado das bordas tridimensionais
    border_edge = overlay["border_gradient"] if overlay["enabled"] else "none"
    inner_shadow = overlay["inner_shadow"] if overlay["enabled"] else "none"
    
    # Prepara o import da fonte (se existir no JSON)
    font_url = ty.get("font_url", "")
    import_font = f"@import url('{font_url}');" if font_url else ""

    return f"""
        /* ── IMPORTAÇÃO DE FONTES EXTERNAS (Deve ser a 1ª linha) ── */
        {import_font}
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

        /* ── :root — variáveis globais do tema ── */
        :root {{
            /* 1. VARIÁVEIS DE LAYOUT*/
            --bk-header-h:       {lay['header_height']};
            --bk-header-icon:    {lay['logo_size']};
            --bk-navig-top-mg:  {lay.get('navigator_top_margin', '0px')};

            /* Cores */
            --bk-bg:           {c['background']};
            --bk-surface:      {c['surface']};
            --bk-surface-2:    {c['surface_2']};

            --bk-primary:      {c['primary']};
            --bk-primary-h:    {c['primary_hover']};
            --bk-secondary:    {c['secondary']};
            --bk-accent:       {c['accent']};

            --bk-text:         {c['text']};
            --bk-text-muted:   {c['text_muted']};
            --bk-text-dis:     {c['text_disabled']};

            --bk-border:       {c['border']};
            --bk-border-focus: {c['border_focus']};

            --bk-success:      {c['success']};
            --bk-warning:      {c['warning']};
            --bk-danger:       {c['danger']};
            --bk-info:         {c['info']};

            /* Tipografia */
            --bk-font:         {ty['font_family']};
            --bk-font-mono:    {ty['font_family_mono']};
            --bk-lh:           {ty['line_height']};

            --bk-xs:           {ty['size_xs']}px;
            --bk-sm:           {ty['size_sm']}px;
            --bk-base:         {ty['size_base']}px;
            --bk-sub:          {ty['size_subtitle']}px;
            --bk-title:        {ty['size_title']}px;
            --bk-display:      {ty['size_display']}px;

            --bk-w-normal:     {ty['weight_normal']};
            --bk-w-medium:     {ty['weight_medium']};
            --bk-w-bold:       {ty['weight_bold']};

            /* Espaçamento */
            --bk-sp-xs:        {sp['xs']};
            --bk-sp-sm:        {sp['sm']};
            --bk-sp-md:        {sp['md']};
            --bk-sp-lg:        {sp['lg']};
            --bk-sp-xl:        {sp['xl']};

            /* Bordas e sombras */
            --bk-border-w:     {b['width']};
            --bk-radius-sm:    {b['radius_sm']};
            --bk-radius-md:    {b['radius_md']};
            --bk-radius-lg:    {b['radius_lg']};
            --bk-radius-full:  {b['radius_full']};
            --bk-shadow-sm:    {b['shadow_sm']};
            --bk-shadow-md:    {b['shadow_md']};
            --bk-shadow-lg:    {b['shadow_lg']};

            /* Efeitos Estruturais Genéricos */
            --bk-hover-y:         {ef['hover_y']};
            --bk-backdrop-blur:   {ef['backdrop_blur']};
            --bk-glow-primary:    {ef['glow_primary']};
            --bk-glow-danger:     {ef['glow_danger']};
            --bk-grad-primary:    {ef['gradient_primary']};
            --bk-grad-surface:    {ef['gradient_surface']};
            
            /* Acabamento Tridimensional Dinâmico */
            --bk-card-border-edge: {border_edge};
            --bk-card-inner-shadow: {inner_shadow};
            --bk-shadow-inset:     {ef.get('shadow_inset', 'none')};

            /* 🚀 NOVA VARIÁVEL: Prepara o terreno para imagens de fundo específicas */
            --bk-bg-image: none;
        }}

        /* ─── FORÇAR TIPOGRAFIA GLOBAL (Com Exceções Múltiplas) ─── */
        html, body, 
        [class*="st-"]:not(.material-symbols-rounded):not(code):not(pre):not([data-testid="stIconMaterial"]), 
        [class*="st-"] *:not(.material-symbols-rounded):not(code):not(pre):not([data-testid="stIconMaterial"]) {{
            font-family: var(--bk-font) !important;
        }}

        /* ─── BLINDAGEM ABSOLUTA DOS ÍCONES MATERIAL ─── */
        .material-symbols-rounded,
        [class*="material-symbols"],
        [data-testid="stIconMaterial"] {{
            font-family: 'Material Symbols Rounded' !important;
            
            /* Eixos obrigatórios para renderizar o ícone (opsz ajustado para 28) */
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 28 !important;
            font-weight: 400 !important;
            font-style: normal !important;
            
            /* Força a ligatura */
            font-variant-ligatures: normal !important;
            font-feature-settings: "liga" 1 !important;
            -webkit-font-feature-settings: "liga" 1 !important;
            
            /* Proteções contra herança */
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
            
            /* 🚀 CENTRALIZAÇÃO ABSOLUTA (Flexbox + Vertical Align) */
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            vertical-align: middle !important;
            line-height: 1 !important;
            margin-left: 0.5rem;

            font-size: 20px !important;
        }}
        
        /* ─── CÓDIGO FONTE ─── */
        code, pre, code *, pre * {{
            font-family: var(--bk-font-mono) !important;
        }}

        /* ─── FORÇAR O FUNDO DO STREAMLIT A OBEDECER O TEMA ─── */
        .stApp, .stApp > header {{
            background-color: var(--bk-bg) !important;
            /* 🚀 AGORA ELE LÊ A VARIÁVEL EM VEZ DE BLOQUEAR TUDO */
            background-image: var(--bk-bg-image) !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            color: var(--bk-text) !important;
        }}

        /* ─── CUSTOMIZAÇÃO DA BARRA DE ROLAGEM (Para imersão total) ─── */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: var(--bk-bg);
        }}
        ::-webkit-scrollbar-thumb {{
            background: var(--bk-border);
            border-radius: var(--bk-radius-full);
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--bk-primary);
        }}

        /* ─── REMOVER RODAPÉ E ELEMENTOS INÚTEIS DO STREAMLIT ─── */
        footer {{ visibility: hidden; }}
        #MainMenu {{ visibility: hidden; }}
    """