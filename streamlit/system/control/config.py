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

def get_theme(app_name: str, mode: str = "dark") -> dict:
    """
    Busca o arquivo JSON do tema estruturado dentro do diretório do app específico.
    Caminho real: ROOT / apps / <categoria> / {app_name} / themes / {mode}.json
    """
    # 1. Encontra o diretório atual onde este script está rodando
    current_path = Path(__file__).resolve()
    
    # 2. Sobe na árvore de diretórios até encontrar a raiz real 'Bankai'
    # Isso evita ficar adivinhando quantos ".parent" usar
    root_path = None
    for parent in current_path.parents:
        if parent.name.lower() == "bankai":
            root_path = parent
            break
            
    # Se não achar a pasta 'Bankai' pelo nome, usa o fallback clássico de subir 3 níveis
    if not root_path:
        root_path = current_path.parent.parent.parent

    # 3. Agora sim, miramos na pasta 'apps' que está na raiz do projeto
    apps_root = root_path / "apps"
    
    # 4. Busca recursiva focando na pasta do app e no arquivo de modo (dark/light)
    theme_files = list(apps_root.rglob(f"{app_name}/themes/{mode}.json"))
    
    # 5. Se encontrou o arquivo, carrega e retorna
    if theme_files:
        path = theme_files[0]
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    # 6. FALLBACK SEGURO: Busca dinâmica do tema padrão da Bankai
    fallback_files = list(apps_root.rglob(f"bankai/themes/{mode}.json"))
    if fallback_files:
        with open(fallback_files[0], "r", encoding="utf-8") as f:
            return json.load(f)
            
    raise FileNotFoundError(
        f"Tema '{mode}.json' para o módulo '{app_name}' (e nem o fallback da Bankai) "
        f"foi encontrado dentro de '{apps_root}'."
    )