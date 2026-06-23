import math
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from typing import Literal, Optional

from system.core.contexts import AppContext
from system.view.components.cards import card


# ── Fallback & Validação ───────────────────────────────────────────────────────

def _fallback_df() -> pd.DataFrame:
    return pd.DataFrame({
        'horario':     list(range(24)),
        'acumulo':     [0] * 24,
        'estouro_sla': [0] * 24
    })


def _validate(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return _fallback_df()
    if 'horario' not in df.columns or 'acumulo' not in df.columns:
        return _fallback_df()
    return df


# ── Extração de Tokens do Tema ─────────────────────────────────────────────────

def _tokens(context: AppContext) -> dict:
    theme       = context.theme
    chart_cfg   = theme.get("chart",       {})
    echarts_cfg = chart_cfg.get("echarts", {})
    colors      = theme.get("colors",      {})
    ty          = theme.get("typography",  {})

    return {
        "axis_label_color":  echarts_cfg.get("axis_label_color",  "#8b949e"),
        "axis_line_color":   echarts_cfg.get("axis_line_color",   "rgba(139,148,158,0.15)"),
        "split_line_color":  echarts_cfg.get("split_line_color",  "rgba(139,148,158,0.05)"),

        "tooltip_bg":        echarts_cfg.get("tooltip_bg",        "transparent"),
        "tooltip_border":    echarts_cfg.get("tooltip_border",    "rgba(197,163,101,0.3)"),
        "tooltip_text":      echarts_cfg.get("tooltip_text",      "#e6e9ec"),

        "font_family":       ty.get("font_family",  "sans-serif"),
        "font_size":         ty.get("size_base",    13),

        # Cores Específicas para Fila e Estouro
        "color_queue":       colors.get("warning", "#d29922"), # Âmbar/Dourado para fila normal
        "color_breach":      colors.get("danger",  "#b04c4c"), # Vermelho para estouro de SLA
    }


# ── Construtor de Opções ───────────────────────────────────────────────────────

def _build_options(
    x_axis:      list,
    y_acumulo:   list, 
    y_estouro:   list, 
    tokens:      dict,
    step:        Literal["start", "middle", "end"],
    show_area:   bool,
    str_pico:    str,
    str_estouro: str
) -> dict:

    # Tooltip simplificada para exibir volumes brutos
    tooltip_formatter = JsCode("""
        function(params) {
            let html = '<div style="margin-bottom:6px;font-size:1.05em;font-weight:bold;">🕐 Hora ' + params[0].name + '</div>';
            params.forEach(function(item) {
                let val = item.value;
                let fmt = (typeof val === 'number')
                    ? val.toLocaleString('pt-BR', {minimumFractionDigits:0, maximumFractionDigits:2})
                    : val;
                html += '<div style="display:flex;justify-content:space-between;gap:32px;line-height:1.8;">'
                      + '<div>' + item.marker + ' ' + item.seriesName + '</div>'
                      + '<div style="font-weight:bold;">' + fmt + '</div>'
                      + '</div>';
            });
            return html;
        }
    """)
    
    # Rótulo de Estouro (Só exibe se houver estouro > 0 para não poluir o gráfico)
    label_formatter_estouro = JsCode("""
        function(params) {
            if (params.value > 0) {
                return params.value;
            }
            return '';
        }
    """)

    axis_style = {
        "axisLine":  {"lineStyle": {"color": tokens["axis_line_color"]}},
        "axisLabel": {"color": tokens["axis_label_color"],
                      "fontFamily": tokens["font_family"],
                      "fontSize": tokens["font_size"]},
        "splitLine": {"lineStyle": {"color": tokens["split_line_color"]}},
    }

    series_acumulo = {
        "name":       "Fila (Acúmulo)",
        "type":       "line",
        "step":       step,
        "data":       y_acumulo,
        "smooth":     False,
        "symbol":     "circle",
        "symbolSize": 5,
        "itemStyle":  {"color": tokens["color_queue"]},
        "lineStyle":  {"width": 2, "color": tokens["color_queue"]},
    }

    series_estouro = {
        "name":       "Estouro SLA",
        "type":       "line",
        "step":       step,
        "data":       y_estouro,
        "smooth":     False,
        "symbol":     "circle",
        "symbolSize": 6,
        "itemStyle":  {"color": tokens["color_breach"]},
        "lineStyle":  {"width": 2, "color": tokens["color_breach"]},
        "label": {
            "show": True,
            "position": "top",
            "distance": 6,
            "fontSize": 10,
            "fontWeight": "bold",
            "color": tokens["color_breach"],
            "formatter": label_formatter_estouro
        }
    }

    if show_area:
        r_q, g_q, b_q = _hex_to_rgb(tokens["color_queue"])
        series_acumulo["areaStyle"] = {"color": f"rgba({r_q},{g_q},{b_q},0.15)"}
        
        r_b, g_b, b_b = _hex_to_rgb(tokens["color_breach"])
        series_estouro["areaStyle"] = {"color": f"rgba({r_b},{g_b},{b_b},0.35)"}

    return {
        "backgroundColor": "transparent",
        
        # O Componente Title com as métricas focadas em Gargalos
        "title": {
            "text": f"{{q|Pico da Fila:}} {{val|{str_pico}}}\n{{b|Total Estouros:}} {{val|{str_estouro}}}",
            "right": "4%",
            "top": 0,
            "textStyle": {
                "fontFamily": tokens["font_family"],
                "fontSize": tokens["font_size"],
                "lineHeight": 22,
                "rich": {
                    "q": {"color": tokens["color_queue"]},
                    "b": {"color": tokens["color_breach"]},
                    "val": {"color": tokens["tooltip_text"], "fontWeight": "bold"}
                }
            }
        },
        "tooltip": {
            "trigger":         "axis",
            "axisPointer":     {"type": "line"},
            "backgroundColor": tokens["tooltip_bg"],
            "borderColor":     tokens["tooltip_border"],
            "borderWidth":     1,
            "textStyle": {
                "color":      tokens["tooltip_text"],
                "fontFamily": tokens["font_family"],
                "fontSize":   tokens["font_size"],
            },
            "formatter": tooltip_formatter,
        },
        "legend": {
            "data":      ["Fila (Acúmulo)", "Estouro SLA"],
            "orient":    "vertical",
            "left":      "2%",
            "top":       0,
            "itemGap":   10,
            "textStyle": {"color": tokens["axis_label_color"],
                          "fontFamily": tokens["font_family"]},
        },
        "grid": {
            "left":         "2%",
            "right":        "4%",
            "bottom":       "0%",
            "top":          "22%", 
            "containLabel": True,
        },
        "xAxis": {
            "type":        "category",
            "data":        x_axis,
            "boundaryGap": False,
            "axisLine":    axis_style["axisLine"],
            "splitLine":   axis_style["splitLine"],
            "axisLabel":   dict(axis_style["axisLabel"], rotate=45, interval=0),
        },
        "yAxis": {
            "type": "value",
            **axis_style,
        },
        "series": [series_acumulo, series_estouro],
    }


# ── Utilitário ─────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    try:
        h = hex_color.lstrip("#")
        if len(h) == 6:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except Exception:
        pass
    return (210, 153, 34)  # Warning/Amber como fallback


# ── API Pública ────────────────────────────────────────────────────────────────

def draw(
    context:     AppContext,
    title:       str,
    subtitle:    str,
    df_fluxo:    Optional[pd.DataFrame] = None, # <--- Recebe o DF de Fila
    step:        Literal["start", "middle", "end"] = "end",
    show_area:   bool  = True,
    height:      str   = "300px",
    grafico:     str   = "acumulo"
):
    df_f = _validate(df_fluxo)

    x_axis    = df_f['horario'].astype(str).tolist()
    y_acumulo = df_f['acumulo'].tolist()
    
    # Tratamento caso a coluna estouro_sla não exista (fallback seguro)
    y_estouro = df_f['estouro_sla'].tolist() if 'estouro_sla' in df_f.columns else [0] * len(df_f)

    # Cálculo dos Indicadores Principais de Gargalo
    pico_fila = max(y_acumulo) if y_acumulo else 0
    total_estouros = sum(y_estouro) if y_estouro else 0

    # Formatação (ex: 1.546)
    str_pico = f"{int(pico_fila):,}".replace(",", ".")
    str_estouro = f"{int(total_estouros):,}".replace(",", ".")

    tokens  = _tokens(context)
    options = _build_options(
        x_axis, y_acumulo, y_estouro, tokens, step, show_area,
        str_pico, str_estouro
    )

    card.draw(
        card.CardConfig(
            card_id=f"step_{grafico}_{title}", context=context,
            model="chart", hover=False, has_title=True, title=title, subtitle=subtitle,
             icon=":material/storage:"
        ), card.CardRenderConfig(
            content=lambda:st_echarts(options=options, height=height)
        )
    )