import streamlit as st
from dataclasses import dataclass
from system.control.contexts import AppContext

VALID_MODELS = ["tabs", "arrows"]

@dataclass
class NavigatorConfig:
    app_name: str
    model: str
    labels: list[str]

    def __post_init__(self):
        if self.model not in VALID_MODELS:
            st.error(f"navigator — model inválido: '{self.model}'. Escolha entre: {VALID_MODELS}")
            raise ValueError(f"model inválido: '{self.model}'")

        if not self.labels:
            st.error("navigator — 'labels' não pode ser vazio.")
            raise ValueError("labels não pode ser vazio")

def _inject_active_css(app_name: str, active_index: int):
    st.markdown(f"""
        <style>
        [data-testid="co_navigator_{app_name}"] > div > div:nth-child({active_index + 1}) button {{
            border-bottom: 2px solid #fff;
            color: #fff;
            font-weight: 500;
        }}
        </style>
    """, unsafe_allow_html=True)


def draw(config: NavigatorConfig, context:AppContext):
    _inject_active_css(config.app_name, context.current_page - 1)

    with st.container(key=f"co_navigator_{config.app_name}"):
        cols = st.columns(len(config.labels))
        for i, (col, label) in enumerate(zip(cols, config.labels)):
            with col:
                st.button(
                    label,
                    key=f"pag_{config.app_name}_p{i+1}",
                    on_click=lambda ctx, idx: setattr(ctx, "current_page", idx),
                    args=[context, i + 1],
                    use_container_width=True,
                )