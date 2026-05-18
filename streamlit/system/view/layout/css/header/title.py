def get_title_css(colors, typography):
    return f"""
        [class*="st-key-container_header_"] {{            
            position: absolute !important; 
            left: 0 !important;
            top: 0 !important;

            height: 72px; /* Mantenha a altura que definimos antes */
            z-index: 1000;
        }}

        [class*="st-key-container_header_"] .custom-header {{
            margin-top: 0.4em; !important;
        }}

        [class*="st-key-container_header_"] .header-title {{
            margin: 0 !important;      /* Remove margens padrão que empurram o texto */
            padding: 0 !important;     /* Remove paddings extras */
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            color: {colors['text']} !important;
            font-size: {typography['size_title']}px !important;
            font-family: {typography['font_family']} !important;
            font-weight: {typography['weight_bold']} !important;

            line-height: 1 !important;
        }}

    """