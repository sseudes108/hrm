import streamlit as st

def horizontal_spacer(height: str = "1em"):
    """
    Injeta um bloco invisível no fluxo do Streamlit para forçar um espaçamento.
    
    Args:
        height (str): Altura do espaço. Aceita 'em', 'rem', 'px', 'vh', etc. 
                      O padrão é '1em'.
    """
    # Usamos flex-shrink: 0 para garantir que o Streamlit não "esmague" 
    # esse elemento se a tela ficar apertada.
    st.html(f"<div style='height: {height}; width: 100%; flex-shrink: 0;'></div>")