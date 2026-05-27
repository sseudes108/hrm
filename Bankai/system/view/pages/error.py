import streamlit as st

def run(invalid_app: str):
    """Renderiza uma página de erro estilizada para módulos inválidos ou restritos"""
    
    # Injeção de CSS para estilização premium e centralização
    st.markdown(
        """
        <style>
            /* Remove margens extras do Streamlit na página de erro */
            .block-container {
                padding-top: 5rem;
                padding-bottom: 5rem;
                max-width: 600px;
            }
            
            /* Container do Card de Erro */
            .error-card {
                background-color: #111111;
                border: 1px solid #222222;
                border-radius: 8px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            }
            
            /* Código do erro (404) ou Ícone */
            .error-code {
                font-size: 72px;
                font-weight: 700;
                color: #e50914; /* Vermelho escuro/alerta */
                margin-bottom: 10px;
                font-family: monospace;
            }
            
            /* Título principal */
            .error-title {
                color: #ffffff;
                font-size: 22px;
                font-weight: 600;
                margin-bottom: 15px;
            }
            
            /* Subtítulo descritivo */
            .error-desc {
                color: #888888;
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 25px;
            }
            
            /* Tag do módulo tentado */
            .module-tag {
                background-color: #1a1a1a;
                color: #aaaaaa;
                padding: 4px 10px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 13px;
                border: 1px solid #333333;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Renderização do Card de Erro usando HTML controlado
    st.markdown(
        f"""
        <div class="error-card">
            <div class="error-code">404</div>
            <div class="error-title">Módulo Não Encontrado</div>
            <div class="error-desc">
                O aplicativo solicitado não existe no ecossistema atual ou sua sessão não possui permissão para montá-lo na memória.
                <br><br>
                Tentativa de acesso: <span class="module-tag">--{invalid_app}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("") # Espaçador spacer
    
    # Botão de ação nativo do Streamlit, porém centralizado visualmente pelo container
    columns = st.columns([1, 2, 1])
    with columns[1]:
        if st.button("⚔️ Retornar à Bankai Central", use_container_width=True):
            # Força o redirecionamento limpando os argumentos ou resetando a sessão
            st.query_params.clear()
            # Como o seu app.py joga para 'bankai' por padrão no else, 
            # podemos apenas dar um rerun simulando uma nova entrada limpa
            st.rerun()