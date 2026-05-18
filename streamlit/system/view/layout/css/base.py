"""
styles/css_base.py — Bankai Template
Variáveis CSS globais (:root), reset, fundo do app e scrollbar.
É o primeiro CSS a ser injetado — todos os outros dependem das variáveis definidas aqui.
"""

def get_css_base(theme: dict) -> str:
    c  = theme["colors"]
    ty = theme["typography"]
    sp = theme["spacing"]
    b  = theme["borders"]

    return f"""

        /* ── :root — variáveis globais do tema ── */
        :root {{

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
            font-family:      var(--bk-font);
            font-size:        var(--bk-base);
            color:            var(--bk-text);
            line-height:      var(--bk-lh);
        }}

        /* Remove o fundo branco padrão do Streamlit */
        .stApp > header {{
            background-color: transparent;
        }}

        .block-container {{
            padding-top:    var(--bk-sp-xs);
            padding-bottom: var(--bk-sp-sm);
            max-width:      100% !important;   /* <-- adicione isso */
            padding-left:   var(--bk-sp-lg);  /* ajuste as margens laterais */
            padding-right:  var(--bk-sp-lg);  /* conforme seu layout */
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