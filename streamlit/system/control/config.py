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
    
    # 4. Busca usando curinga para a categoria (ex: dashboards, engines, etc.)
    # O '*' substitui 'dashboards' ou qualquer outra pasta que venha antes do app
    theme_pattern = f"*/{app_name}/themes/{mode}.json"
    theme_files = list(apps_root.glob(theme_pattern))
    
    # 5. Se encontrou o arquivo real do app, carrega e retorna
    if theme_files:
        path = theme_files[0]
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    # 6. Se não encontrou (ex: o app específico não tem pasta de temas), 
    # busca o tema padrão na pasta 'bankai' independente de onde ela esteja
    fallback_files = list(apps_root.glob(f"*/bankai/themes/{mode}.json"))
    if fallback_files:
        with open(fallback_files[0], "r", encoding="utf-8") as f:
            return json.load(f)
            
    raise FileNotFoundError(
        f"Tema '{mode}.json' para o módulo '{app_name}' (e nem o fallback da Bankai) "
        f"foi encontrado dentro de '{apps_root}'."
    )