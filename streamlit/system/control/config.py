import json
from pathlib import Path
import streamlit as st

def hex_to_rgba(hex_color, opacity):
    # Se por acaso vier um dicionário, tenta extrair a string
    if isinstance(hex_color, dict):
        hex_color = hex_color.get("color", "#ffffff") # fallback para branco
    
    hex_color = str(hex_color).lstrip("#")
    lv = len(hex_color)
    rgb = tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {opacity})"

def build_colorscale(colors: list[str], area_top: float, area_base: float) -> list[dict]:
    return [
        {
            "color":     c,
            "glow":      hex_to_rgba(c, 0.8),
            "area_top":  hex_to_rgba(c, area_top),
            "area_base": hex_to_rgba(c, area_base),
        }
        for c in colors
    ]

def set_theme(name: str):
    # garante que nunca receba um dict por engano
    if not isinstance(name, str):
        name = "bankai_dark"
    
    theme = load_theme(name)
    st.session_state.theme_name = name  # persiste o nome
    st.session_state.theme = theme      # persiste o objeto

def get_theme():
    return st.session_state.theme

def load_theme(name: str) -> dict:
    path = Path(__file__).parent.parent / "view" / "layout" / "themes" / f"{name}.json"

    with open(path, encoding="utf-8") as f:
        theme = json.load(f)

    ec = theme["chart"]["echarts"]
    theme["chart"]["colorscale"] = build_colorscale(
        theme["chart"]["colorscale"],
        area_top=ec["area_opacity_top"],
        area_base=ec["area_opacity_base"],
    )

    return theme