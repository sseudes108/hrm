import streamlit as st
# Importa o seu método genérico com rglob que criamos antes
from system.control.config import get_theme 

class DashboardContext:
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

    def update_filter(self, column: str, value: str):
        if self.active_filters.get(column) != value:
            self.active_filters[column] = value
            st.rerun()
            return True
        return False

    def remove_filter(self, column: str):
        if column in self.active_filters:
            del self.active_filters[column]
            st.rerun()
            return True
        return False

    def clear_all(self):
        self.active_filters = {}
        self.show_details = False
        st.rerun()

    # --- O NOVO MÉTODO BLINDADO ---
    def update_mode(self, new_mode: str):
        """Altera o modo visual e recarrega o JSON correspondente SEM resetar os filtros"""
        if self.mode != new_mode:
            self.mode = new_mode
            
            # A mágica acontece aqui: busca o novo JSON (light ou dark) dinamicamente
            # usando o rglob pelo app_name atual da classe
            self.theme = get_theme(self.app_name, mode=new_mode)
            
            # Força o Streamlit a redesenhar a tela com as novas cores,
            # mas mantendo esta mesma instância da classe viva na sessão com os filtros!
            st.rerun()