import json
import os

def save_json(path_save, novo_conteudo, cliente):
    # 1. Carrega o que já existe para não apagar dados de outros clientes
    dados_existentes = {}
    if os.path.exists(path_save):
        with open(path_save, "r") as f:
            try:
                dados_existentes = json.load(f)
            except json.JSONDecodeError:
                dados_existentes = {}

    # 2. Atualiza apenas a chave do cliente específico
    dados_existentes[cliente] = novo_conteudo

    # 3. Salva de volta
    with open(path_save, "w") as f:
        json.dump(dados_existentes, f, indent=4)

def load_json(path_load, cliente):
    if os.path.exists(path_load):
        with open(path_load, "r") as f:
            try:
                todos_os_dados = json.load(f)
                return todos_os_dados.get(cliente, {})
            except json.JSONDecodeError:
                return {}
    return {}