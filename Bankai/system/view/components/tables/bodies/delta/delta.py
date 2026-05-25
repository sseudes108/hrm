import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. GERAÇÃO E PROCESSAMENTO (Mantidos iguais)
# ==========================================
def gerar_dados_simulados():
    np.random.seed(42)
    ferramentas = ["Zangetsu", "Senbonzakura", "Kyoka Suigetsu", "Hyorinmaru", "Ryujin Jakka"]
    meses = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
    data = []
    for f in ferramentas:
        for m in meses:
            data.append({
                "ferramenta": f,
                "periodo": m,
                "quantidade": np.random.randint(500, 2000),
                "sla": np.random.uniform(80.0, 99.9),
                "tma_segundos": np.random.randint(120, 600)
            })
    return pd.DataFrame(data)

def processar_deltas(df: pd.DataFrame):
    df = df.sort_values(by=["ferramenta", "periodo"]).reset_index(drop=True)
    df['qtd_prev'] = df.groupby('ferramenta')['quantidade'].shift(1)
    df['sla_prev'] = df.groupby('ferramenta')['sla'].shift(1)
    df['tma_prev'] = df.groupby('ferramenta')['tma_segundos'].shift(1)
    
    df['qtd_delta'] = df['quantidade'] - df['qtd_prev']
    df['sla_delta'] = df['sla'] - df['sla_prev']
    df['tma_delta'] = df['tma_segundos'] - df['tma_prev']
    return df

# ==========================================
# 2. SVGs E BADGES (O Novo Motor Visual)
# ==========================================
def format_tma(segundos):
    if pd.isna(segundos): return "-"
    m = int(segundos) // 60
    s = int(segundos) % 60
    return f"{m:02d}:{s:02d}"

# SVGs puros e minimalistas (stroke-width: 3 para ficarem gordinhos e legíveis pequenos)
SVG_UP = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
SVG_DOWN = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>'

def html_badge(valor, tipo_metrica):
    """Cria a caixinha translúcida (badge) com o SVG dentro"""
    if pd.isna(valor) or valor == 0:
        return "<span class='badge badge-neutral'>-</span>"
        
    is_up = valor > 0
    svg = SVG_UP if is_up else SVG_DOWN
    valor_abs = abs(valor)
    
    # LÓGICA DE CORES: TMA subir é ruim (bad). Qtd/SLA subir é bom (good).
    if tipo_metrica == 'tma':
        badge_class = "badge-bad" if is_up else "badge-good"
        texto = format_tma(valor_abs)
    elif tipo_metrica == 'sla':
        badge_class = "badge-good" if is_up else "badge-bad"
        texto = f"{valor_abs:.1f}%"
    else:
        badge_class = "badge-good" if is_up else "badge-bad"
        texto = f"{int(valor_abs)}"
        
    return f"<div class='badge {badge_class}'>{svg} {texto}</div>"

# ==========================================
# 3. RENDERIZAÇÃO DA TABELA HTML
# ==========================================
def desenhar_tabela_html(df: pd.DataFrame):
    periodos = sorted(df['periodo'].unique())
    ferramentas = sorted(df['ferramenta'].unique())

    html = "<table class='matrix-table'><thead><tr><th style='text-align: left;'>Ferramenta</th>"
    
    # Cabeçalho dos Períodos
    for p in periodos:
        html += f"<th>{p}</th>"
    html += "</tr></thead><tbody>"

    # Corpo da Tabela
    for f in ferramentas:
        html += f"<tr><td class='ferramenta-col'>{f}</td>" # Usei a classe do CSS em vez de style inline
        
        for p in periodos:
            row = df[(df['ferramenta'] == f) & (df['periodo'] == p)]
            if not row.empty:
                r = row.iloc[0]
                
                # Monta a célula empilhando 3 blocos horizontais (Rótulo | Valor | Badge)
                bloco_qtd = f"<div class='metric-row'><span class='metric-label'>QTD</span> <span class='metric-val'>{int(r['quantidade'])}</span> {html_badge(r['qtd_delta'], 'qtd')}</div>"
                bloco_sla = f"<div class='metric-row'><span class='metric-label'>SLA</span> <span class='metric-val'>{r['sla']:.1f}%</span> {html_badge(r['sla_delta'], 'sla')}</div>"
                bloco_tma = f"<div class='metric-row'><span class='metric-label'>TMA</span> <span class='metric-val'>{format_tma(r['tma_segundos'])}</span> {html_badge(r['tma_delta'], 'tma')}</div>"
                
                html += f"<td><div class='cell-content'>{bloco_qtd}{bloco_sla}{bloco_tma}</div></td>"
            else:
                html += "<td>-</td>"
                
        html += "</tr>"
        
    html += "</tbody></table>"
    
    # Renderiza o HTML final
    st.markdown(html, unsafe_allow_html=True)
    
def draw_body(df, key):
    df_bruto = gerar_dados_simulados()
    df_processado = processar_deltas(df_bruto)
    with st.container(key=f"body_delta_{key}"):
        desenhar_tabela_html(df_processado)