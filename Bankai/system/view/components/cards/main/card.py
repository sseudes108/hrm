import streamlit as st
from dataclasses import dataclass, field
from typing import Optional
import system.control.managers.hash as hash_man

# Defina os modelos válidos de card (ajuste conforme os tipos que você tem no sistema)
VALID_CARD_MODELS = {"base", "header", "metric", "chart"}

@dataclass
class CardConfig:
    app_name: str       # Necessário para o escopo global
    card_id: str        # Identificador único DESTE card (ex: "sales_summary", "main_header")
    model: str = "base"
    show_card:bool = True
    has_title: bool = False
    title: Optional[str] = None
    subtitle: Optional[str] = None
    hover: bool = False
    has_action: bool = False

    # A chave será gerada pelo sistema, não deve ser passada na criação
    key: str = field(init=False) 

    def __post_init__(self):
        # 1. Valida o modelo do card
        if self.model not in VALID_CARD_MODELS:
            raise ValueError(f"model inválido para card: '{self.model}'. Escolha entre: {VALID_CARD_MODELS}")

        # 2. Cria a chave combinando as strings base para garantir unicidade total
        raw_string = f"{self.app_name}_{self.card_id}_{self.model}"
        
        # Gera o hash e anexa um prefixo claro para facilitar o debug no CSS do navegador
        self.key = f"{hash_man.get_hash(raw_string)}"

# Adicione render_action=None nos parâmetros
def draw(config: CardConfig, render_content=None, render_action=None, *args, **kwargs):
    if render_content is None:
        st.error("Render Content is None")
        return

    comportamento = "hover" if config.hover else "static"
    bg = "bg" if config.show_card else "nobg"
    chave_container = f"co_card_{bg}_{comportamento}_{config.model}_{config.key}"

    with st.container(key=chave_container):
        
        # 🚀 NOVO CABEÇALHO DIVIDIDO
        if config.has_title and config.title:
            
            # Se tiver ação (botão), dividimos em duas colunas (80% pro título, 20% pro botão)
            if config.has_action and render_action:
                col_title, col_action = st.columns([0.8, 0.2], gap="small")
            else:
                # Se não tiver botão, usamos uma coluna falsa que ocupa 100% para manter o padrão
                col_title, col_action = st.columns([1, 0.01])
            
            with col_title:
                sub_html = f'<div class="bk-card-subtitle">{config.subtitle}</div>' if config.subtitle else ''
                custom_header = f"""            
                    <div class="bk-card-header" style="margin-bottom: 0px;">
                        <div class="bk-card-title">{config.title}</div>
                        {sub_html}
                    </div>
                """
                st.markdown(custom_header, unsafe_allow_html=True)
                
            with col_action:
                if config.has_action and render_action:
                    # Aqui o botão ou a métrica é renderizada!
                    render_action()
                    
        # Roda o conteúdo dinâmico (O Gráfico ou a Tabela)
        response = render_content(*args, **kwargs)

    return response