"""Geração consistente de chaves para widgets e containers Streamlit."""

from system.core.managers.config import hash as hash_man


def scoped_key(context, component: str, identifier: str) -> str:
    """Cria uma chave estável, única por aplicação e segura para seletores CSS."""
    if not identifier:
        raise ValueError("identifier não pode ser vazio")
    raw = f"{context.app_name}:{component}:{identifier}"
    return f"{component}_{context.app_name}_{hash_man.get_hash(raw)}"
