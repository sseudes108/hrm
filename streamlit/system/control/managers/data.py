import streamlit as st
import json

def load_json(json_path: str) -> list:
    """Carrega o JSON uma única vez."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return []

def normalize_data(raw) -> list:
    """
    Garante que a saída seja sempre uma lista de dicts,
    independente de como o JSON está estruturado.
    """
    # Caso 1: já é lista de dicts → ok
    if isinstance(raw, list):
        result = []
        for item in raw:
            if isinstance(item, dict):
                result.append(item)   # {"nome": ..., "pais": ...}
            elif isinstance(item, str):
                result.append({"nome": item})  # lista de strings puras
        return result

    # Caso 2: dicionário raiz com uma chave que contém a lista
    # Ex: {"perfis": [{...}, {...}]}
    if isinstance(raw, dict):
        for key, value in raw.items():
            if isinstance(value, list):
                return normalize_data(value)  # recursivo com a lista encontrada
        # Caso 3: o próprio dict é um único registro
        return [raw]

    return []


def get_data():
    if "data" not in st.session_state:
        raw = load_json("data/she_base.json")
        data = normalize_data(raw)
    
    return data