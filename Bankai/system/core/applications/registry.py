"""Registro e carregamento genéricos de aplicações."""

from importlib import import_module
from types import ModuleType

from .contracts import ApplicationDefinition


class ApplicationRegistry:
    """Mantém aplicações registradas sem depender de implementações concretas."""

    def __init__(self) -> None:
        self._applications: dict[str, ApplicationDefinition] = {}

    def register(self, application: ApplicationDefinition) -> ApplicationDefinition:
        """Registra uma aplicação e falha em caso de identificador duplicado."""
        if application.app_id in self._applications:
            raise ValueError(f"Aplicação já registrada: '{application.app_id}'.")

        self._applications[application.app_id] = application
        return application

    def get(self, app_id: str) -> ApplicationDefinition | None:
        """Retorna uma aplicação registrada, normalizando seu identificador."""
        return self._applications.get(app_id.strip().lower())

    def all(self) -> tuple[ApplicationDefinition, ...]:
        """Lista aplicações na ordem em que foram registradas."""
        return tuple(self._applications.values())

    def load_module(self, module_path: str) -> ApplicationDefinition:
        """Carrega e registra a definição exportada por um módulo de aplicação.

        O módulo informado deve exportar ``get_application()``, retornando uma
        ``ApplicationDefinition``. O caminho é fornecido pelo bootstrap; assim,
        este núcleo não possui referência a nomes de aplicações concretas.
        """
        module = import_module(module_path)
        application = self._extract_definition(module, module_path)
        registered = self.get(application.app_id)
        if registered is None:
            return self.register(application)

        # O watchdog do Streamlit pode reconstruir a fábrica do app sem
        # reconstruir este singleton. Substituir a definição evita manter
        # callbacks, tema ou configuração de autenticação da versão anterior.
        self._applications[application.app_id] = application
        return application

    @staticmethod
    def _extract_definition(
        module: ModuleType, module_path: str
    ) -> ApplicationDefinition:
        factory = getattr(module, "get_application", None)
        if not callable(factory):
            raise TypeError(
                f"O módulo '{module_path}' deve exportar get_application()."
            )

        application = factory()
        if not ApplicationRegistry._is_application_definition(application):
            raise TypeError(
                f"get_application() em '{module_path}' deve retornar "
                "ApplicationDefinition."
            )
        return application

    @staticmethod
    def _is_application_definition(application: object) -> bool:
        """Valida o contrato, inclusive durante hot-reloads do Streamlit.

        Em um hot-reload, módulos podem manter uma referência para a classe
        anterior de ``contracts.py``. O objeto continua sendo exatamente a
        mesma definição por contrato, mas falha em um ``isinstance`` estrito.
        A alternativa estrutural abaixo só aceita a mesma classe qualificada e
        todos os campos obrigatórios do contrato.
        """
        if isinstance(application, ApplicationDefinition):
            return True

        candidate_type = type(application)
        if (
            candidate_type.__name__ != ApplicationDefinition.__name__
            or candidate_type.__module__ != ApplicationDefinition.__module__
        ):
            return False

        required_callables = ("render", "load_theme", "state_factory")
        required_strings = ("app_id", "title", "initial_route", "default_mode")
        return (
            all(isinstance(getattr(application, name, None), str) for name in required_strings)
            and all(callable(getattr(application, name, None)) for name in required_callables)
            and hasattr(application, "auth")
        )


registry = ApplicationRegistry()
