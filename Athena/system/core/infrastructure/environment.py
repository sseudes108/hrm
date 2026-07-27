"""Inicialização explícita da configuração de ambiente."""

from pathlib import Path

from dotenv import load_dotenv


def load_environment(env_path: Path | None = None) -> bool:
    """Carrega um arquivo de ambiente opcional sem sobrescrever o processo.

    O bootstrap deve chamar esta função uma única vez. Módulos de
    infraestrutura apenas leem as variáveis já disponíveis no ambiente.
    """
    if env_path is not None and not env_path.is_file():
        return False
    return load_dotenv(dotenv_path=env_path, override=False)
