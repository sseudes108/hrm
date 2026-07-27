"""Caso de uso da rota inicial."""

from bankai.domain import ApplicationStatus


def get_home_status() -> ApplicationStatus:
    """Obtém os dados necessários para apresentar a rota inicial."""
    return ApplicationStatus(name="Bankai", is_ready=True)
