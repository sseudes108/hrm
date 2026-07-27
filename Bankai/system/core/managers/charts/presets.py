"""Presets compartilhados pelos managers de gráficos."""

from typing import Literal

from streamlit_echarts import JsCode

from system.view.components.charts.echarts.config import TooltipConfig


ChartClickType = Literal["categoric_click", "date_click", "categoric", "date"]

_DATE_TOOLTIP = """
function(params) {
    let rawDate = params[0].name;
    let formattedDate = rawDate;
    if (rawDate && rawDate.indexOf('-') !== -1) {
        let datePart = rawDate.split('T')[0];
        let parts = datePart.split('-');
        if (parts.length === 3) {
            formattedDate = parts[2] + '/' + parts[1] + '/' + parts[0];
        }
    }
    let html = '<div style="margin-bottom: 6px; font-size: 1.05em; font-weight: bold;">📅'
        + formattedDate + '</div>';
    params.forEach(function(item) {
        let val = item.value;
        let formattedVal = (typeof val === 'number')
            ? val.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 2})
            : val;
        html += '<div style="display: flex; justify-content: space-between; align-items: center; gap: 32px; line-height: 1.6;">'
            + '<div>' + item.marker + ' ' + item.seriesName + '</div>'
            + '<div style="font-weight: bold;">' + formattedVal + '</div></div>';
    });
    return html;
}
"""


def axis_tooltip(click_type: ChartClickType) -> TooltipConfig:
    """Retorna o tooltip padrão para eixos categóricos ou temporais."""
    if click_type in {"date", "date_click"}:
        return TooltipConfig(trigger="axis", formatter=JsCode(_DATE_TOOLTIP))
    return TooltipConfig(trigger="axis")
