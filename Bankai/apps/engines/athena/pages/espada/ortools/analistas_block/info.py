import streamlit as st
import pandas as pd
from system.core.log.view import infos

def draw(df_escala, payload):
    _draw_component(df_escala, payload)

def _minuto_para_hora(minuto: int) -> str:
    if pd.isna(minuto): return "--:--"
    h = (int(minuto) // 60) % 24
    m = int(minuto) % 60
    return f"{h:02d}:{m:02d}"

def _draw_component(df_escala: pd.DataFrame, payload):
    
    if df_escala is None or df_escala.empty:
        infos.draw(message="Aguardando dados do quadro.")
        return

    # ==========================================
    # 1. RECUPERAÇÃO DO PAYLOAD E CÁLCULOS EXATOS
    # ==========================================
    sla_minutos = getattr(payload, 'sla', 60) 
    
    # Capacidade por minuto da operação
    tamanho_bloco_segundos = sla_minutos * 60
    capacidade_por_bloco = int(tamanho_bloco_segundos / payload.tma) if payload.tma > 0 else 0
    cap_por_minuto = capacidade_por_bloco / float(sla_minutos)

    # Como não estamos usando o agrupado, o tamanho do DF é o total de pessoas
    total_analistas = len(df_escala)
    
    # CAPTURANDO OS 4 PONTOS CRÍTICOS (Usando as novas colunas min_)
    primeira_entrada = _minuto_para_hora(df_escala['min_entrada'].min())
    ultima_entrada   = _minuto_para_hora(df_escala['min_entrada'].max())
    
    primeira_saida   = _minuto_para_hora(df_escala['min_saida'].min())
    ultima_saida     = _minuto_para_hora(df_escala['min_saida'].max())
    
    # Cálculos de Carga em MINUTOS com Módulo 1440 (24h)
    delta_trabalho = (df_escala['min_saida'] - df_escala['min_entrada']) % 1440
    delta_almoco = (df_escala['min_alm_fim'] - df_escala['min_alm_inicio']) % 1440
    
    carga_minutos = delta_trabalho - delta_almoco
    carga_minutos = carga_minutos.apply(lambda x: max(0, x)) # Trava anti-negativo
    
    # Capacidade Total agora é perfeitamente proporcional!
    capacidade_total = int(round((carga_minutos * cap_por_minuto).sum()))
    
    # Horas de Operação
    primeiro_minuto = df_escala['min_entrada'].min()
    ultimo_minuto = df_escala['min_saida'].max()
    delta_operacao = (ultimo_minuto - primeiro_minuto) % 1440
    
    if delta_operacao == 0 and total_analistas > 0:
        delta_operacao = 1440
        
    horas_operacao = delta_operacao / 60.0
    cap_media_hora = int(capacidade_total / horas_operacao) if horas_operacao > 0 else 0

    # Formatação (ex: 1.500)
    str_cap_total = f"{capacidade_total:,}".replace(",", ".")
    str_cap_media = f"{cap_media_hora:,}".replace(",", ".")

    # ==========================================
    # 2. RENDERIZAÇÃO HTML
    # ==========================================
    
    html_info = f"""
    <div style="color: var(--bk-text); font-size: 0.95em; line-height: 2; padding: 0.2rem 0;">
        <div>
            <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">Total Analistas:</span>
            <span style="font-weight: 700; margin-left: 6px; color: var(--bk-primary);">{total_analistas}</span>
        </div>
        <div>
            <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">Capacidade Total:</span>
            <span style="font-weight: 700; margin-left: 6px;">{str_cap_total} propostas</span>
        </div>
        <div>
            <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">Média / Hora:</span>
            <span style="font-weight: 700; margin-left: 6px;">{str_cap_media} propostas</span>
        </div>
        
        <hr style="border-color: rgba(139,148,158,0.15); margin: 0.3rem 0; max-width: 80%;">
        
        <div style="display: flex; gap: 8px;">
            <div>
                <div>
                    <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">1ª Entrada:</span>
                    <span style="font-weight: 700; margin-left: 6px;">{primeira_entrada}</span>
                </div>
                <div>
                    <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">Últ. Entrada:</span>
                    <span style="font-weight: 700; margin-left: 6px;">{ultima_entrada}</span>
                </div>
            </div>
            <div>
                <div>
                    <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">1ª Saída:</span>
                    <span style="font-weight: 700; margin-left: 6px;">{primeira_saida}</span>
                </div>
                <div>
                    <span style="color: var(--bk-text-muted); font-size: 0.81em; font-weight: 600; text-transform: uppercase;">Últ. Saída:</span>
                    <span style="font-weight: 700; margin-left: 6px;">{ultima_saida}</span>
                </div>
            </div>
        </div>
    </div>
    """
    
    st.html(html_info)