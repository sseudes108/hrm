import streamlit as st
import time
import random

def draw_page():
    # Estilo Minimalista e Elegante (Dark Mode Corporativo)
    st.markdown("""
<style>
/* Fundo grafite profundo, quase preto, muito limpo */
.main {
    background-color: #0f1117 !important;
}
header, footer, [data-testid="stSidebar"] { visibility: hidden; display: none; }

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;300;400&family=Fira+Code:wght@300&display=swap');

.easter-container {
    font-family: 'Inter', sans-serif;
    text-align: center;
    padding-top: 8vh;
    position: relative;
    z-index: 2;
}

/* O Número Sagrado: Efeito Glitch Colorido */
.number-108 {
    font-family: 'Inter', sans-serif;
    font-size: 8rem;
    font-weight: 700;
    letter-spacing: -3px;
    position: relative;
    display: inline-block;
    color: #FFD700;
    text-shadow: 
        0.05em 0 0 rgba(255, 215, 0, 0.8),
        -0.025em -0.05em 0 rgba(255, 105, 180, 0.6),
        0.025em 0.05em 0 rgba(138, 43, 226, 0.5),
        0 0 20px rgba(255, 215, 0, 0.3);
    animation: glitch-108 2s infinite linear alternate-reverse;
}

@keyframes glitch-108 {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

.sub-text {
    font-family: 'Fira Code', monospace;
    font-size: 0.75rem;
    color: #636c7e;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: -15px;
    opacity: 0.8;
}

/* Texto reflexivo próximo ao input */
.reflection-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: #8a92a6;
    font-weight: 300;
    line-height: 1.8;
    margin: 25px 0 15px 0;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}

.reflection-text i {
    color: #a0a8b8;
    font-weight: 400;
}

/* Input Minimalista: Sem bordas pesadas */
.stTextInput>div>div>input {
    background-color: transparent !important;
    color: #ffffff !important;
    border: none !important;
    border-bottom: 1px solid #3b4252 !important;
    border-radius: 0 !important;
    text-align: center !important;
    font-family: 'Fira Code', monospace !important;
    transition: 0.3s ease;
    width: 220px !important;
    margin: 10px auto 0 auto;
    font-size: 0.9rem;
}

.stTextInput>div>div>input::placeholder {
    color: #4a5568 !important;
    font-style: italic;
}

.stTextInput>div>div>input:focus {
    border-bottom: 1px solid #FFD700 !important;
    box-shadow: none !important;
}

/* Esconde o label do input */
label[data-testid="stWidgetLabel"] { display: none; }

/* Frase dos antigos no canto inferior esquerdo */
.ancient-footer {
    position: fixed;
    bottom: 25px;
    left: 30px;
    font-family: 'Fira Code', monospace;
    font-size: 0.7rem;
    color: #3b4252;
    font-style: italic;
    font-weight: 300;
    line-height: 1.6;
    opacity: 0.6;
    z-index: 1;
    text-align: left;
    max-width: 280px;
}

/* Botão minimalista */
.stButton>button {
    background: transparent !important;
    color: #636c7e !important;
    border: 1px solid #3b4252 !important;
    border-radius: 4px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: 0.2s ease !important;
    margin-top: 15px !important;
}

.stButton>button:hover {
    border-color: #FFD700 !important;
    color: #FFD700 !important;
}

</style>
""", unsafe_allow_html=True)

    # Frases místicas aleatórias
    frases_misticas = [
        ("A verdade reside no silêncio do coração.", "🏹"),
        ("O que procuras já está dentro de ti.", "🗝️"),
        ("Nem todos que vagam estão perdidos.", "🌌"),
        ("O conhecimento é a chave, a sabedoria é a porta.", ""),
        ("Às vezes, o vazio é a resposta.", "🌑"),
        ("O espelho revela mais do que esconde.", "🪞"),
        ("Cada pergunta é um passo na escuridão.", "🕯️"),
        ("O guardião reconhece os dignos.", "🛡️"),
        ("O tempo é um círculo, não uma linha.", "⭕"),
        ("Escute o que não é dito.", "👁️"),
        ("A porta se abre apenas uma vez.", "🪬"),
        ("Você está mais perto do que imagina.", "🌀"),
        ("O segredo não é o que você busca, mas por quê.", "🎭"),
        ("Silêncio é a linguagem dos sábios.", "🤫"),
        ("A resposta está na pergunta que você não fez.", "❓"),
    ]

    # Estrutura da Página
    st.markdown('<div class="easter-container">', unsafe_allow_html=True)
    
    # O centro do Easter Egg
    st.markdown('<h1 class="number-108">108</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">ERROR 403 // RESTRICTED ACCESS</p>', unsafe_allow_html=True)
    
    # Texto reflexivo próximo ao input
    st.markdown("""
        <p class="reflection-text">
            Você busca o que está oculto, mas não traz a chave.<br>
            Muitos batem à porta, mas poucos são convidados a entrar.<br><br>
            <i>"Eu protejo o que importa mais."</i>
        </p>
    """, unsafe_allow_html=True)
    
    # Campo de input centralizado e sutil
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        prop = st.text_input("", placeholder="o que você procura?", key="oracle_key")
        
        if prop:
            # Seleciona frase aleatória
            frase, emoji = random.choice(frases_misticas)
            st.toast(frase, icon=emoji)
            time.sleep(1.5)

    # Frase dos antigos no canto inferior esquerdo
    st.markdown("""
        <div class="ancient-footer">
            "Guarde a verdade no seu coração,<br>
            mantenha a boca fechada.<br><br>
            Somos nós, por quem os sinos dobram."
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Efeito de vinheta sutil (foco central)
    st.markdown("""
        <div style="
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background: radial-gradient(circle, transparent 42%, rgba(15,17,23,0.5) 100%);
            pointer-events: none; z-index: 1;
        "></div>
    """, unsafe_allow_html=True)