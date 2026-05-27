"""
styles/css_base.py — Bankai 
Variáveis CSS globais (:root), reset, fundo do app e scrollbar.
É o primeiro CSS a ser injetado — todos os outros dependem das variáveis definidas aqui.
"""

def create_base_css(theme: dict) -> str:
    c  = theme["colors"]
    ty = theme["typography"]
    sp = theme["spacing"]
    b  = theme["borders"]
    ef = theme["effects"] # <-- Adicionado aqui
    overlay = ef["surface_overlay"] # <-- Captura o bloco dinâmico
    lay = theme["layout"]

    # Define o estado das bordas tridimensionais
    border_edge = overlay["border_gradient"] if overlay["enabled"] else "none"
    inner_shadow = overlay["inner_shadow"] if overlay["enabled"] else "none"

    return f"""

        /* ── :root — variáveis globais do tema ── */
        :root {{
            /* 1. VARIÁVEIS DE LAYOUT*/
            --bk-header-h:      {lay['header_height']};
            --bk-header-icon:   {lay['icon_size']};

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
        }}

        /* ── Reset base ── */
        *, *::before, *::after {{
            box-sizing: border-box;
            margin:     0;
            padding:    0;
        }}

        /* ── App ── */
        .stApp {{
            background-color: var(--bk-bg);
            font-family:       var(--bk-font);
            font-size:        var(--bk-base);
            color:            var(--bk-text);
            line-height:      var(--bk-lh);


            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(11, 13, 20, 0.4); /* Ajuste a opacidade se precisar */
            z-index: -1;
        }}

        /* Remove o fundo branco padrão do Streamlit */
        .stApp > header {{
            background-color: transparent;
        }}

        .block-container {{
            margin-top: -2.8rem !important;
            padding-top:    var(--bk-sp-xs);
            padding-bottom: var(--bk-sp-sm);
            max-width:      100% !important;
            padding-left:   var(--bk-sp-lg);
            padding-right:  var(--bk-sp-lg);
        }}

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {{
            width:  6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: var(--bk-bg);
        }}
        ::-webkit-scrollbar-thumb {{
            background:    var(--bk-border);
            border-radius: var(--bk-radius-full);
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--bk-primary);
        }}

        /* ── Divider ── */
        hr {{
            border:  none;
            border-top: var(--bk-border-w) solid var(--bk-border);
            margin: var(--bk-sp-lg) 0;
        }}

    """