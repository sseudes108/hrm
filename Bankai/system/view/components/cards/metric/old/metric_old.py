import streamlit as st
import pandas as pd
from system.view.components.cards import card
from system.core.managers.charts import sparkline
from system.core.log.view import warnings
from dataclasses import dataclass

@dataclass
class MetricSparkLineConfig:
    df:pd.DataFrame
    x_column:str
    y_column:str
    click_type:str = "categoric"

@dataclass
class MetricValue:
    title:str
    subtitle:str
    value:str
    delta:str
    delta_class:str = "success"
    delta_icon:str = "🔼"
    has_highlight: bool = True,
    hl_title: str = None,
    hl_value: str = None

def _draw_component(metric_value, model, chart_data, chart_config, context):
    values_col, grafic_col = st.columns([0.3, 0.7], gap="xxsmall")

    with values_col:
        st.markdown(
            f"""
                <div class="metric-value-container">
                    <div class="metric-value-main">
                        {metric_value.value}
                    </div>
                    <div class="metric-delta {metric_value.delta_class}">
                        <span class="metric-delta-text">
                            {metric_value.delta}
                        </span>
                        <span class="metric-delta-icon">
                            {metric_value.delta_icon}
                        </span>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )
    
    with grafic_col:
        if model == "sparkline":
            sparkline.draw(
                df=chart_data.head(7),
                sparkline_color=metric_value.delta_class,
                title=metric_value.title,
                subtitle=metric_value.title,
                column_x=chart_config.x_column,
                column_y=chart_config.y_column,
                context=context,
                click_type=chart_config.click_type
            )

def _draw_component_action(has_highlight, hl_title, hl_value):
    if has_highlight:
        sub_html = f'<div class="bk-card-highlight-value">{hl_value}</div>'
        custom_header = f"""            
            <div class="bk-card-highlight">
                <div class="bk-card-highlight-label">{hl_title}</div>
                {sub_html}
            </div>
        """
        st.markdown(custom_header, unsafe_allow_html=True)

def draw(
    context,
    model:str = "simple", #sparkline
    metric_value:MetricValue = None,
    sparkline_config:MetricSparkLineConfig = None,
):
    app_name = context.app_name
    if metric_value is None:
        error.draw(
            app_name=app_name, title="error_metric_value", alert="error",
            message="metric_value não pode ser None!"
        )
        return

    if metric_value.has_highlight:
        if metric_value.hl_title is None or metric_value.hl_value is None:
            error.draw(
                app_name=app_name, title="error_metric_value", alert="error",
                message="Highlight ativado. hl_title e hl_value não podem ser None!"
            )
            return

    if model == "sparkline" and sparkline_config is None:
        error.draw(
            app_name=app_name, title="error_sparkline_config", alert="error",
            message="Metrica Sparkline. sparkline_config não pode ser None!"
        )
        return
    
    if model == "sparkline":
        if sparkline_config.df.empty:
            warnings.draw(
                message="sparkline_config.df não pode ser empty!", alert="error", 
            )
            return
        
        chart_data = sparkline_config.df
        chart_config = sparkline_config
    else:
        chart_data = {}
        chart_config = {}

    
    card.draw(
        card.CardConfig(
            card_id=f"metric_{app_name}_{metric_value.title}_{model}",
            context=context, model="metric", title=metric_value.title,
            subtitle=metric_value.subtitle, has_action=True, has_title=True
        ), card.CardRenderConfig(
            content=lambda: _draw_component(
                metric_value, model, chart_data, chart_config, context
            ), right_side=lambda: _draw_component_action(
                metric_value.has_highlight, metric_value.hl_title, metric_value.hl_value
            )
        )
    )