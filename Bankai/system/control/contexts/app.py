import streamlit as st
import system.control.managers.layout as layout_man

class AppContext:
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

    def update_filter(self, column: str, value: str, rerun:bool = True):
        if self.active_filters.get(column) != value:
            self.active_filters[column] = value
            if rerun:
                st.rerun()
            return True
        return False

    def remove_filter(self, column: str, rerun: bool = True):
        if column in self.active_filters:
            del self.active_filters[column]
            if rerun:
                st.rerun()
            return True
        return False

    def clear_all(self):
        self.active_filters = {}
        self.show_details = False
        st.rerun()

    def update_mode(self, new_mode: str):
        """Altera o modo visual e recarrega o JSON correspondente SEM resetar os filtros"""
        if self.mode != new_mode:
            self.mode = new_mode
            
            # A mágica acontece aqui: busca o novo JSON (light ou dark) dinamicamente
            # usando o rglob pelo app_name atual da classe
            self.theme = layout_man.get_theme(self.app_name, mode=new_mode)
            
            # Força o Streamlit a redesenhar a tela com as novas cores,
            # mas mantendo esta mesma instância da classe viva na sessão com os filtros!
            st.rerun()