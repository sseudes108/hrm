from system.control.config import hex_to_rgba
from system.view.components.helper import get_base64_icon

def get_button_css(theme, colors):
    icon = get_base64_icon(theme)
    return f"""
        [class*="st-key-toggle_theme_btn_container_"] {{
            z-index: 1001 !important;
            margin: 0 !important;      /* Remove margens padrão que empurram o texto */
            padding: 0 !important;     /* Remove paddings extras */
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        [class*="st-key-toggle_theme_btn_container_"] button {{
            background:  {hex_to_rgba(colors['surface'], 0.5)};
            background-image: url('data:image/svg+xml;base64,{icon}') !important;
            background-repeat: no-repeat !important;
            background-position: center !important;

            border: 1px solid {hex_to_rgba(colors['text'], 0.3)};
            border-radius: 50%;

            width: 40px;
            height: 40px;
            
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        [class*="st-key-toggle_theme_btn_container_"]:hover button {{
            border-color: {hex_to_rgba(colors['border_focus'], 0.4)} !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }}

        [class*="st-key-toggle_theme_btn_container_"]:active button {{
            transform: translateY(0) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
        }}

        button {{
            transition: all 0.3s ease !important;
        }}
    """