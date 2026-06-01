from system.view.components.cards import card, CardConfig
import streamlit as st

def warning(app_name:str, title:str, message:str):
    card.draw(
        CardConfig(
            app_name=app_name, 
            card_id=f"error_pie_neg_{app_name}_{title}",
            model="base"
        ), render_content=lambda: _draw_warning(message)
    )

def _draw_warning(message: str):
    """
    Desenha um card de alerta customizado usando o sistema de design do Bankai.
    """

    html_content = f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 16px;
        background: var(--bk-surface);
        border: 1px solid var(--bk-border, var(--bk-surface_2));
        border-left: 4px solid #f59e0b; /* Laranja/Amarelo padrão de alerta */
        border-radius: var(--bk-radius-md);
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: var(--bk-shadow-sm);
        color: var(--bk-text);
        font-family: inherit;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 1.5rem; display: flex; align-items: center; justify-content: center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
        </div>
        <div style="font-size: 0.95em; line-height: 1.5; font-weight: 500;">
            {message}
        </div>
    </div>
    """

    st.markdown(html_content, unsafe_allow_html=True)