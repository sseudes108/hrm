from system.core.applications import ApplicationDefinition

def run(application: ApplicationDefinition, context) -> None:
    """Delega a renderização à aplicação já carregada pelo bootstrap."""
    application.render(context)
