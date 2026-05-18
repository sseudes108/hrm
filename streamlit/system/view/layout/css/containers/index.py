from system.view.layout.css.containers.charts import get_css_charts
from system.view.layout.css.containers.tables import get_css_tables
from system.view.layout.css.containers.metrics import get_css_metrics

def get_css_containers(theme):
    return f"""
        {get_css_charts(theme)}
        {get_css_tables(theme)}
    """
        # {get_css_metrics(theme)}
