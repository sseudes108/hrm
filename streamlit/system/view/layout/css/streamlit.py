def get_css_settings():
    # return ""
    return f"""
        /* Esconder header padrão do Streamlit */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}

        /* Esconder botão controlador da sidebar */
        button[data-testid="collapsedControl"] {{
            display: none !important;
        }}
    """