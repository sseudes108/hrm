from system.view.components.cards import card
import streamlit as st

def draw(message:str, alert:str = "warning"):
    _draw_component(alert, message)

def _draw_component(alert:str, message:str):
    if alert == "warning":
        _draw_warning(message)
    else:
        _draw_error(message)

def _draw_warning(message: str):
    """
    Desenha um card de alerta customizado usando o sistema de design do Bankai.
    """
    html_content = f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 16px;
        /* Fundo laranja translúcido (8% de opacidade) */
        background: rgba(245, 158, 11, 0.08);
        /* Borda sutil (25% de opacidade) */
        border: 1px solid rgba(245, 158, 11, 0.25);
        /* Borda esquerda contínua e forte */
        border-left: 4px solid var(--bk-warning, #f59e0b);
        border-radius: var(--bk-radius-md, 8px);
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: var(--bk-shadow-sm);
        color: var(--bk-text);
        font-family: inherit;
        transition: all 0.3s ease;
    ">
        <span class="material-symbols-rounded" style="color: var(--bk-warning, #f59e0b); font-size: 28px;">
            warning
        </span>
        
        <div style="font-size: 0.95em; line-height: 1.5; font-weight: 500;">
            {message}
        </div>
    </div>
    """
    st.html(html_content)


def _draw_error(message: str):
    """
    Desenha um card de erro customizado usando o sistema de design do Bankai.
    """
    html_content = f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 16px;
            /* Fundo vermelho translúcido (8% de opacidade) */
            background: rgba(239, 68, 68, 0.08);
            /* Borda sutil (25% de opacidade) */
            border: 1px solid rgba(239, 68, 68, 0.25);
            /* Borda esquerda contínua e forte */
            border-left: 4px solid var(--bk-danger, #ef4444);
            border-radius: var(--bk-radius-md, 8px);
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: var(--bk-shadow-sm);
            color: var(--bk-text);
            font-family: inherit;
            transition: all 0.3s ease;
        ">
            <span class="material-symbols-rounded" style="color: var(--bk-danger, #ef4444); font-size: 28px;">
                error
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