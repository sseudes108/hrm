import math
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from typing import Literal, Optional

from system.core.contexts import AppContext
from system.view.components.cards import card


# ── Fallback & Validação ───────────────────────────────────────────────────────

def _fallback_df() -> pd.DataFrame:
    return pd.DataFrame({
        'horario':    list(range(24)),
        'quantidade': [0] * 24
    })


def _validate(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return _fallback_df()
    if 'horario' not in df.columns or 'quantidade' not in df.columns:
        return _fallback_df()
    return df


# ── Extração de Tokens do Tema ─────────────────────────────────────────────────

def _tokens(context: AppContext) -> dict:
    """
    Extrai os tokens visuais do tema do AppContext.
    Retorna um dict com as chaves que o builder precisa.
    Caso algum token não exista no tema, usa fallback seguro.
    """
    theme       = context.theme
    chart_cfg   = theme.get("chart",       {})
    echarts_cfg = chart_cfg.get("echarts", {})
    colors      = theme.get("colors",      {})
    ty          = theme.get("typography",  {})

    return {
        # Cores do eixo / grid
        "axis_label_color":  echarts_cfg.get("axis_label_color",  "#8b949e"),
        "axis_line_color":   echarts_cfg.get("axis_line_color",   "rgba(139,148,158,0.15)"),
        "split_line_color":  echarts_cfg.get("split_line_color",  "rgba(139,148,158,0.05)"),

        # Tooltip
        "tooltip_bg":        echarts_cfg.get("tooltip_bg",        "transparent"),
        "tooltip_border":    echarts_cfg.get("tooltip_border",    "rgba(197,163,101,0.3)"),
        "tooltip_text":      echarts_cfg.get("tooltip_text",      "#e6e9ec"),

        # Tipografia
        "font_family":       ty.get("font_family",  "sans-serif"),
        "font_size":         ty.get("size_base",    13),

        # Palette temática — fallback para o par Atena Dark característico
        "color_demand":      colors.get("danger",  "#b04c4c"),
        "color_capacity":    colors.get("primary", "#c5a365"),
    }


# ── Construtor de Opções ───────────────────────────────────────────────────────

def _build_options(
    x_axis:     list,
    y_demand:   list, # Agora recebe list de dicts {"value": x, "pessoas": y}
    y_capacity: list, # Agora recebe list de dicts {"value": x, "pessoas": y}
    tokens:     dict,
    step:       Literal["start", "middle", "end"],
    show_area:  bool,
    str_dem:    str,
    str_cap:    str,
    str_pct:    str
) -> dict:

    # Atualizado para buscar o 'value' dentro de item.data se for um objeto
    tooltip_formatter = JsCode("""
        function(params) {
            let html = '<div style="margin-bottom:6px;font-size:1.05em;font-weight:bold;">🕐 Hora ' + params[0].name + '</div>';
            params.forEach(function(item) {
                let val = (item.data && item.data.value !== undefined) ? item.data.value : item.value;
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
    
    # Formata a etiqueta na bolinha: Mostra a Qtd de Pessoas apenas se > 0
    label_formatter = JsCode("""
        function(params) {
            if (params.data && params.data.pessoas > 0) {
                return params.data.pessoas;
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

    series_demand = {
        "name":       "Demanda",
        "type":       "line",
        "step":       step,
        "data":       y_demand,
        "smooth":     False,
        "symbol":     "circle",
        "symbolSize": 5,
        "itemStyle":  {"color": tokens["color_demand"]},
        "lineStyle":  {"width": 2, "color": tokens["color_demand"]},
        "label": {
            "show": True,
            "position": "top", # Fica em cima da linha
            "distance": 6,
            "fontSize": 10,
            "color": tokens["color_demand"],
            "formatter": label_formatter
        }
    }

    series_capacity = {
        "name":       "Capacidade",
        "type":       "line",
        "step":       step,
        "data":       y_capacity,
        "smooth":     False,
        "symbol":     "circle",
        "symbolSize": 5,
        "itemStyle":  {"color": tokens["color_capacity"]},
        "lineStyle":  {"width": 2, "color": tokens["color_capacity"]},
        "label": {
            "show": True,
            "position": "bottom", # Fica embaixo da linha para não sobrepor a demanda
            "distance": 6,
            "fontSize": 10,
            "color": tokens["color_capacity"],
            "formatter": label_formatter
        }
    }

    if show_area:
        r, g, b = _hex_to_rgb(tokens["color_capacity"])
        series_capacity["areaStyle"] = {"color": f"rgba({r},{g},{b},0.08)"}

    return {
        "backgroundColor": "transparent",
        
        # O Componente Title foi usado para ancorar os totais na direita
        "title": {
            "text": f"{{dem|Demanda:}} {{val|{str_dem}}}\n{{cap|Capacidade:}} {{val|{str_cap}}} {{pct|{str_pct}}}",
            "right": "4%",
            "top": 0,
            "textStyle": {
                "fontFamily": tokens["font_family"],
                "fontSize": tokens["font_size"],
                "lineHeight": 22,
                "rich": {
                    "dem": {"color": tokens["color_demand"]},
                    "cap": {"color": tokens["color_capacity"]},
                    "val": {"color": tokens["tooltip_text"], "fontWeight": "bold"},
                    "pct": {"color": tokens["axis_label_color"], "fontSize": 11}
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
        # Legenda empilhada na esquerda
        "legend": {
            "data":      ["Demanda", "Capacidade"],
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
        "series": [series_demand, series_capacity],
    }


# ── Utilitário ─────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Converte #rrggbb para (r, g, b). Fallback em caso de erro."""
    try:
        h = hex_color.lstrip("#")
        if len(h) == 6:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except Exception:
        pass
    return (197, 163, 101)  # bronze atena como fallback


# ── API Pública ────────────────────────────────────────────────────────────────

def draw(
    context:     AppContext,
    title:str,
    subtitle:str,
    capacidade_por_bloco: int, # <--- PARÂMETRO OBRIGATÓRIO INSERIDO
    df_demand:   Optional[pd.DataFrame] = None,
    df_capacity: Optional[pd.DataFrame] = None,
    step:        Literal["start", "middle", "end"] = "end",
    show_area:   bool  = True,
    height:      str   = "300px",
    grafico: str = "demanda"
):
    df_dem = _validate(df_demand)
    df_cap = _validate(df_capacity)

    x_axis = df_dem['horario'].astype(str).tolist()
    
    # Prevenção de divisão por zero na conversão de pessoas
    cap_bloco_segura = max(1, capacidade_por_bloco)

    # Conversão das listas brutas para dicionários do ECharts
    y_demand = []
    total_dem = 0
    for val in df_dem['quantidade'].tolist():
        total_dem += val
        pessoas = math.ceil(val / cap_bloco_segura)
        y_demand.append({"value": val, "pessoas": pessoas})
        
    y_capacity = []
    total_cap = 0
    for val in df_cap['quantidade'].tolist():
        total_cap += val
        pessoas = round(val / cap_bloco_segura)
        y_capacity.append({"value": val, "pessoas": pessoas})

    # Cálculo dos Totais Gerais
    pct_cap   = (total_cap / total_dem * 100) if total_dem > 0 else 0.0

    # Formatação Padrão BR (ex: 198.546)
    str_dem = f"{int(total_dem):,}".replace(",", ".")
    str_cap = f"{int(total_cap):,}".replace(",", ".")
    str_pct = f"({pct_cap:.2f}%)"

    tokens  = _tokens(context)
    options = _build_options(
        x_axis, y_demand, y_capacity, tokens, step, show_area,
        str_dem, str_cap, str_pct
    )

    card.draw(
        card.CardConfig(
            card_id=f"step_{grafico}_{title}", context=context,
            model="chart", hover=False, has_title=True, title=title, subtitle=subtitle,
            icon=":material/inventory:"
        ), card.CardRenderConfig(
            content=lambda:st_echarts(options=options, height=height)
        )
    )