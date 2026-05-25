import streamlit as st

def draw_empty_element(size_px):
    """Cria um bloco vazio na tela com a altura exata em pixels."""
    st.markdown(f'<div style="height: {size_px}px; width: 100%;"></div>', unsafe_allow_html=True)

def draw_bg_element(size_px: int, color_name: str = "transparent"):
    """
    Cria um bloco visual temporário para testes de layout e espaçamento.
    Cores disponíveis por nome: 'primary', 'secondary', 'bg', 'gray' ou qualquer Hex/Nome CSS puro.
    """
    # Mapeamento rápido das suas cores temáticas para teste visual
    theme_colors = {
        "rosa": "#ff007f",     # Rosa Bankai / Neon
        "ciano": "#00f0ff",   # Cyan
        "azul": "#1c1cc0",          # Cor do Card Dark
        "verde": "#16C000",        # Cinza para demarcar bloco
        "transparent": "transparent"
    }
    
    # Se o nome estiver no dicionário, usa o hex. Se não, assume que você passou uma cor CSS (ex: 'red' ou '#fff')
    final_color = theme_colors.get(color_name.lower(), color_name)
    # Desenha o bloco puro e limpo
    html = f'<div style="height: {size_px}px; width: 100%; background-color: {final_color};"></div>'
    st.markdown(html, unsafe_allow_html=True)