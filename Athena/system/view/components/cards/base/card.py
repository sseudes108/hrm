import streamlit as st
from dataclasses import dataclass, field
from typing import Callable, Literal, Optional
from html import escape

from system.core.managers.config import hash as hash_man
from system.core.contexts import AppContext

# Defina os modelos válidos de card (ajuste conforme os tipos que você tem no sistema)
VALID_CARD_MODELS = {"base", "header", "wrapper", "metric", "chart", "filter"}
VALID_CARD_PADDINGS = {"none", "compact", "normal"}
CardTitleCase = Literal["none", "upper", "capitalize"]
CardTitleAlign = Literal["left", "center", "right"]
VALID_TITLE_CASES = {"none", "upper", "capitalize"}
VALID_TITLE_ALIGNS = {"left", "center", "right"}

@dataclass
class CardConfig:
    card_id: str        # Identificador único DESTE card (ex: "sales_summary", "main_header")
    context: AppContext | None = None
    model: str = "base"
    variant: str = "surface"
    padding: str = "normal"
    show_card:bool = True
    has_title: bool = False
    title: Optional[str] = None
    subtitle: Optional[str] = None
    icon: Optional[str] = None
    hover: bool = True
    title_case: CardTitleCase = "none"
    title_align: CardTitleAlign = "left"

    # A chave será gerada pelo sistema, não deve ser passada na criação
    key: str = field(init=False) 

    def __post_init__(self):
        # 1. Valida o modelo do card
        if self.model not in VALID_CARD_MODELS:
            raise ValueError(f"model inválido para card: '{self.model}'. Escolha entre: {VALID_CARD_MODELS}")
        if not self.variant or not self.variant.isidentifier():
            raise ValueError("variant deve ser um identificador CSS simples e não vazio")
        available_variants = (
            self.context.theme.get("components", {})
            .get("card", {})
            .get("variants", {})
            if self.context is not None and hasattr(self.context, "theme")
            else {}
        )
        if available_variants and self.variant not in available_variants:
            raise ValueError(f"variant de card não existe no tema ativo: '{self.variant}'")
        if self.padding not in VALID_CARD_PADDINGS:
            raise ValueError(f"padding inválido para card: '{self.padding}'. Escolha entre: {VALID_CARD_PADDINGS}")
        if self.title_case not in VALID_TITLE_CASES:
            raise ValueError(f"title_case inválido: '{self.title_case}'. Escolha entre: {VALID_TITLE_CASES}")
        if self.title_align not in VALID_TITLE_ALIGNS:
            raise ValueError(f"title_align inválido: '{self.title_align}'. Escolha entre: {VALID_TITLE_ALIGNS}")
        if self.context is None:
            raise ValueError("context é obrigatório para criar um card")

        # 2. Cria a chave combinando as strings base para garantir unicidade total
        raw_string = (
            f"{self.context.app_name}_{self.card_id}_{self.model}_{self.variant}_"
            f"{self.padding}_{self.title_case}_{self.title_align}"
        )
        
        # Gera o hash e anexa um prefixo claro para facilitar o debug no CSS do navegador
        self.key = f"{hash_man.get_hash(raw_string)}"

@dataclass
class CardRenderConfig:
    content: Callable[[], None]
    custom_title_html: Optional[str] = None
    right_side_html: Optional[str] = None

def draw(config: CardConfig, render: CardRenderConfig):
    if render.content is None:
        from system.core.log.view import warnings

        warnings.draw(
            alert="error", message="Render Content is None", context=config.context
        )
        return
    
    comportamento = "hover" if config.hover else "static"
    bg = "bg" if config.show_card else "nobg"
    chave_container = (
        f"co_card_{config.model}_{bg}_{config.variant}_pad_{config.padding}_"
        f"titlecase_{config.title_case}_titlealign_{config.title_align}_"
        f"{comportamento}_{config.key}"
    )

    with st.container(key=chave_container):

        if config.has_title:
            if render.right_side_html:
                title_col, r_html_col = st.columns([0.8, 0.2], gap="small")
            else:
                title_col, r_html_col = st.columns([1, 0.01])
            
            with title_col:
                if render.custom_title_html:
                    st.html(render.custom_title_html)

                elif config.title:
                    # 🚀 LÓGICA DO ÍCONE
                    icon_html = ""
                    if config.icon:
                        if config.icon.startswith(":material/"):
                            icon_name = config.icon.replace(":material/", "").replace(":", "")
                            # Usamos a cor do texto padrão ou primary, você pode ajustar no style
                            icon_html = f'<span class="material-symbols-rounded" style="font-size: 1.15em; color: var(--ui-colors-text-muted);">{escape(icon_name)}</span>'
                        else:
                            icon_html = f'<span>{escape(config.icon)}</span>'

                    title = escape(config.title)
                    subtitle = escape(config.subtitle) if config.subtitle else ""
                    sub_html = f'<div class="ui-card-subtitle">{subtitle}</div>' if subtitle else ''
                    
                    custom_header = f"""            
                        <div class="ui-card-header">
                            <div class="ui-card-title">{icon_html}{title}</div>
                            {sub_html}
                        </div>
                    """
                    st.html(custom_header)
                
            with r_html_col:
                if render.right_side_html:
                    with st.container(key="co_cd_right_html_"):
                        st.html(render.right_side_html)

        return render.content()
