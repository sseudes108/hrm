import streamlit as st
import system.control.managers.layout as layout_man

class AppContext:
    """
    Contexto global da aplicação — instanciado uma única vez no session_state
    e compartilhado entre todas as páginas e componentes do app.

    Responsabilidades:
        - Guardar e atualizar o estado de navegação (página e subpágina ativas)
        - Gerenciar filtros ativos aplicados às visualizações
        - Controlar o tema visual (modo claro/escuro) sem resetar o estado

    Uso:
        Nunca instanciar diretamente nas páginas. Sempre recuperar via:
        `context = state_man.get_context(app_name)`
    """

    def __init__(self, 
            app_name: str, 
            theme: dict = None,
            mode: str = "dark",
        ):
        self.app_name = app_name
        self.mode = mode
        self.active_filters = {}
        self.show_details = False
        self.theme = theme if theme else {}
        self.current_page = 1
        self.current_subpage = 1

        self._processed_events = {}

    ## FILTERS

    def update_filter(self, column: str, value: str, rerun: bool = True):
        """Adiciona ou atualiza um filtro ativo. Reroda o app se o valor mudou."""
        if self.active_filters.get(column) != value:
            self.active_filters[column] = value
            if rerun:
                st.rerun()
            return True
        return False

    def remove_filter(self, column: str, rerun: bool = True):
        """Remove um filtro ativo pelo nome da coluna."""
        if column in self.active_filters:
            del self.active_filters[column]
            if rerun:
                st.rerun()
            return True
        return False

    def clear_all(self):
        """Limpa todos os filtros e reseta o estado de detalhes."""
        self.active_filters = {}
        self.show_details = False

    ## CHARTS

    def get_last_event_ts(self, column: str):
        """Retorna o timestamp do último evento processado para uma coluna."""
        return self._processed_events.get(column)
        
    def set_last_event_ts(self, column: str, ts: int):
        """Salva o timestamp do último evento processado."""
        self._processed_events[column] = ts

    ## THEME

    def update_mode(self, new_mode: str):
        """
        Altera o modo visual (dark/light) e recarrega o tema correspondente
        sem resetar filtros ou navegação.
        """
        if self.mode != new_mode:
            self.mode = new_mode
            self.theme = layout_man.get_theme(self.app_name, mode=new_mode)

    ## NAVIGATION

    def set_page(self, page: int):
        """
        Navega para uma página principal.
        Reseta current_subpage para None — subpáginas de outras páginas
        não devem permanecer ativas ao trocar de contexto.
        """
        self.current_page = page
        self.current_subpage = 1

    def set_subpage(self, subpage: int):
        """
        Navega para uma subpágina mantendo a página pai intacta.
        Não dispara st.rerun — o Streamlit reroda automaticamente após o on_click.
        """
        self.current_subpage = subpage