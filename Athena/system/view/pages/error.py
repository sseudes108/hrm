import streamlit as st

def main(invalid_app: str):
    """Renderiza uma página de erro estilizada para módulos inválidos ou restritos"""
    
    # Injeção de CSS para estilização premium e centralização
    css = f"""
        <style>
            /* Remove margens extras do Streamlit na página de erro */
            .block-container {{
                padding-top: 5rem;
                padding-bottom: 5rem;
                max-width: 600px;
            }}
            
            /* Container do Card de Erro */
            .error-card {{
                background-color: var(--ui-colors-surface, Canvas);
                border: 1px solid var(--ui-colors-border, GrayText);
                border-radius: 8px;
                padding: 40px;
                text-align: center;
                box-shadow: var(--ui-borders-shadow-lg, none);
            }}
            
            /* Código do erro (404) ou Ícone */
            .error-code {{
                font-size: 72px;
                font-weight: 700;
                color: var(--ui-colors-danger, LinkText);
                margin-bottom: 10px;
                font-family: monospace;
            }}
            
            /* Título principal */
            .error-title {{
                color: var(--ui-colors-text, CanvasText);
                font-size: 22px;
                font-weight: 600;
                margin-bottom: 15px;
            }}
            
            /* Subtítulo descritivo */
            .error-desc {{
                color: var(--ui-colors-text-muted, GrayText);
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 25px;
            }}
            
            /* Tag do módulo tentado */
            .module-tag {{
                background-color: var(--ui-colors-background, Canvas);
                color: var(--ui-colors-text-muted, GrayText);
                padding: 4px 10px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 13px;
                border: 1px solid var(--ui-colors-border, GrayText);
            }}
        </style>
    """
    st.html(css)

    # Renderização do Card de Erro usando HTML controlado
    error_card = f"""
        <div class="error-card">
            <div class="error-code">404</div>
            <div class="error-title">Módulo Não Encontrado</div>
            <div class="error-desc">
                O aplicativo solicitado não existe no ecossistema atual ou sua sessão não possui permissão para montá-lo na memória.
                <br><br>
                Tentativa de acesso: <span class="module-tag">--{invalid_app}</span>
            </div>
        </div>
    """
    st.html(error_card)
    st.write("") # Espaçador spacer
    # Botão de ação nativo do Streamlit, porém centralizado visualmente pelo container
    columns = st.columns([1, 2, 1])
    with columns[1]:
        if st.button("⚔️ Retornar à aplicação padrão", width='stretch'):
            # Força o redirecionamento limpando os argumentos ou resetando a sessão
            st.query_params.clear()
            # O bootstrap usa a aplicação padrão ao reiniciar sem parâmetros.
            st.rerun()
