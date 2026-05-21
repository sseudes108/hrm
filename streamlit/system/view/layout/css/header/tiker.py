"""
styles/header/tiker.py — Bankai 
CSS da faixa de notícias animada (Ticker).
Totalmente estático, consumindo os tokens estruturais e de efeitos do :root.
"""

def get_tiker_css() -> str:
    return """
        [class*="st-key-container_header_"] .ticker-wrap {
            overflow: hidden;
            /* Troca do hex_to_rgba pelo color-mix nativo */
            background-color: color-mix(in srgb, var(--bk-surface-2) 30%, transparent) !important;
            
            /* Herança do desfoque genérico definido no tema ativo */
            backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            -webkit-backdrop-filter: blur(var(--bk-backdrop-blur)) !important;
            
            height: 2.5em;
            width: 100%;
            border-radius: var(--bk-radius-md) !important; /* Amarrado ao token de borda md */
            z-index: 998;
            
            display: flex;
            align-items: center;
        }

        [class*="st-key-container_header_"] .ticker-move {
            display: inline-block;
            white-space: nowrap;
            padding-left: 10px; 
            animation: header_news_ticker 30s linear infinite;
            
            /* Variáveis globais do :root */
            color: var(--bk-text) !important;
            font-size: var(--bk-sub) !important; /* var(--bk-sub) já traz o 'px' do base */
            font-family: var(--bk-font) !important;
            font-weight: var(--bk-w-normal) !important;
        }

        @keyframes header_news_ticker {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        [class*="st-key-container_header_"] .ticker-wrap:hover .ticker-move {
            animation-play-state: paused;
            cursor: pointer;
        }
    """