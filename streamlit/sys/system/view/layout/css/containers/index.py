"""
styles/containers/index.py — Bankai 
Unificador do CSS dos containers principais do dashboard.
"""
from system.view.layout.css.containers.charts import get_css_charts
from system.view.layout.css.containers.tables import get_css_tables

def get_css_containers() -> str:
    return f"""
        {get_css_charts()}
        {get_css_tables()}
    """