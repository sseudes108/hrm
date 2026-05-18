from system.control.config import hex_to_rgba

def get_tiker_css(colors, typography):
    return f"""
        [class*="st-key-container_header_"] .ticker-wrap {{
            overflow: hidden;
            background-color: {hex_to_rgba(colors['surface_2'], 0.3)};
            backdrop-filter: blur(5px);
            height: 2.5em;
            width: 100%;
            border-radius: 8px;
            z-index: 998;
            
            display: flex;
            align-items: center;
        }}

        [class*="st-key-container_header_"] .ticker-move {{
            display: inline-block;
            white-space: nowrap;
            padding-left: 10px; 
            animation: header_news_ticker 30s linear infinite;
            color: {colors['text']};
            font-size: {typography['size_subtitle']}px !important;
            font-family: {typography['font_family']} !important;
            font-weight: {typography['weight_normal']} !important;
        }}

        @keyframes header_news_ticker {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}

        [class*="st-key-container_header_"] .ticker-wrap:hover .ticker-move {{
            animation-play-state: paused;
            cursor: pointer;
        }}
    """