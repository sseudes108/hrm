import streamlit as st
from collections.abc import Callable, Mapping
from typing import Any

class AppContext:
    """
    Contexto técnico compartilhado entre o bootstrap e a aplicação.

    Responsabilidades:
        - Expor tema, modo visual e largura da tela
        - Referenciar o estado criado e possuído pela aplicação

    O estado de domínio, filtros e navegação não pertencem a esta classe.
    """

    def __init__(self, 
            app_name: str, 
            theme: dict = None,
            mode: str = "dark",
            theme_loader: Callable[[str], Mapping[str, Any]] | None = None,
            theme_mode_persister: Callable[[str], None] | None = None,
            state: Any = None,
        ):
        self.app_name = app_name
        self.mode = mode
        self.theme = theme if theme else {}
        self._theme_loader = theme_loader
        self._theme_mode_persister = theme_mode_persister
        self.state = state
        self.screen_width = 1920  # default desktop até JS resolver

    ## THEME

    def update_mode(self, new_mode: str):
        """
        Altera o modo visual (dark/light) e recarrega o tema correspondente
        sem resetar filtros ou navegação.
        """
        normalized_mode = new_mode.strip().lower()
        if self.mode != normalized_mode:
            if self._theme_loader is None:
                raise RuntimeError("Nenhum carregador de tema foi configurado para esta aplicação.")
            loaded_theme = dict(self._theme_loader(normalized_mode))
            self.mode = normalized_mode
            self.theme = loaded_theme
            if self._theme_mode_persister is not None:
                self._theme_mode_persister(normalized_mode)

    def set_theme_loader(self, theme_loader: Callable[[str], Mapping[str, Any]]) -> None:
        """Atualiza a origem de temas sem acoplar o contexto a uma aplicação."""
        self._theme_loader = theme_loader

    def set_theme_mode_persister(
        self,
        theme_mode_persister: Callable[[str], None] | None,
    ) -> None:
        """Atualiza o destino da preferência sem conhecer seu meio físico."""
        self._theme_mode_persister = theme_mode_persister

    def set_state(self, state: Any) -> None:
        """Vincula o estado que pertence à aplicação ativa."""
        self.state = state

    @property
    def is_mobile(self) -> bool:
        return self.screen_width < 640

    @property  
    def is_tablet(self) -> bool:
        return 640 <= self.screen_width < 1024
