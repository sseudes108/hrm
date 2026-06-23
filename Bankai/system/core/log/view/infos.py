import streamlit as st

def draw(message:str, alert:str = "info"):
    _draw_component(alert, message)

def _draw_component(alert:str, message:str):
    if alert == "info":
        _draw_info(message)
    else:
        _draw_info(message) # Se no futuro você criar _draw_warning, _draw_error, é só plugar aqui!

def _draw_info(message: str):
    """
    Desenha um card de informação customizado usando o sistema de design do Bankai.
    """
    html_content = f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 16px;
            /* Fundo azul translúcido (8% de opacidade) que se adapta ao Light/Dark mode */
            background: rgba(59, 130, 246, 0.08); 
            /* Borda sutil acompanhando a paleta (25% de opacidade) */
            border: 1px solid rgba(59, 130, 246, 0.25); 
            /* Borda esquerda contínua e forte para manter o DNA do alerta */
            border-left: 4px solid var(--bk-info, #3b82f6); 
            border-radius: var(--bk-radius-md, 8px);
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: var(--bk-shadow-sm);
            color: var(--bk-text);
            font-family: inherit;
            transition: all 0.3s ease;
        ">
            <span class="material-symbols-rounded" style="color: var(--bk-info, #3b82f6); font-size: 28px;">
                info
            </span>
            
            <div style="
                font-size: 0.95em;
                line-height: 1.5;
                font-weight: 500;
            ">
                {message}
            </div>
        </div>
    """
    
    st.html(html_content)