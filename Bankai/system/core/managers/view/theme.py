import json
from pathlib import Path

def _deep_merge(base: dict, override: dict) -> dict:
    """
    Merge recursivo — override sobrescreve folhas do base,
    mas preserva chaves do base que não existem no override.
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def get_theme(app_name: str, mode: str = "dark") -> dict:
    current_path = Path(__file__).resolve()

    # Encontra a raiz do projeto (Bankai)
    root_path = None
    for parent in current_path.parents:
        if parent.name.lower() == "bankai":
            root_path = parent
            break
            
    if not root_path:
        root_path = current_path.parent.parent.parent

    def _load_search(target_app: str, file_name: str) -> dict | None:
        """
        Usa busca recursiva (rglob) para encontrar o arquivo de tema, 
        independentemente de estar em books, dashboards, engines ou sandbox.
        """
        # Procura em qualquer lugar por: <target_app>/theme/<file_name>
        pattern = f"**/{target_app}/theme/{file_name}"
        
        # O rglob vasculha a partir do root_path
        files = list(root_path.rglob(pattern))
        
        if files:
            with open(files[0], "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    # Tenta carregar base e mode do app específico, com fallback para bankai
    base  = _load_search(app_name, "base.json")  or _load_search("bankai", "base.json")
    theme = _load_search(app_name, f"{mode}.json") or _load_search("bankai", f"{mode}.json")

    if not base:
        raise FileNotFoundError(f"base.json não encontrado para '{app_name}' nem no fallback.")
    if not theme:
        raise FileNotFoundError(f"'{mode}.json' não encontrado para '{app_name}' nem no fallback.")

    return _deep_merge(base, theme)