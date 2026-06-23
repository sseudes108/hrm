import pandas as pd
import streamlit as st
from system.view.components.layout import fixes
from system.core.log.view import infos
from apps.engines.athena.core.calculadora import page as calculadora

def _formatar_bloco_para_hora(bloco: int, sla_minutos: int) -> str:
    """Traduz o índice numérico (ex: 16) para string de hora (ex: '08:00')."""
    minutos_totais = int(bloco) * sla_minutos
    horas = (minutos_totais // 60) % 24
    minutos = minutos_totais % 60
    return f"{horas:02d}:{minutos:02d}"

def draw(df_escala_agrupado: pd.DataFrame, sla_minutos: int):
    
    # Validação segura
    if df_escala_agrupado is None or df_escala_agrupado.empty:
        with st.container(height=565, border=False):
            infos.draw(message="Aguardando dados do quadro.")
            return

    # Usamos o container com scroll (height fixo) para não estourar a tela do dashboard
    with st.container(height=565, border=False):       
        for idx, row in df_escala_agrupado.iterrows():
            
            # 2. Extração dos dados do grupo
            quantidade = row['quantidade']
            turno = row['turno_aplicado']
            
            ent = row['str_entrada']
            alm_ini = row['str_almoco_inicio']
            sai = row['str_saida']
            
            # 3. Criação da Linha
            spc1, col_info, col_add, col_rmv, col_del, spc2 = st.columns([0.1, 5, 0.5, 0.5, 0.5, 0.1], vertical_alignment="center", gap='xxsmall')
            
            with col_info:
                # O HTML agora mostra "X Analistas" em destaque
                html_content = f"""
                    <div style="line-height: 1.2;">
                        <strong>{quantidade} Analistas</strong> <span style="color: gray; font-size: 0.85em;">({turno})</span><br>
                        <span style="font-size: 0.9em;">Entrada: <b>{ent}</b> | Almoço: <b>{alm_ini}</b> | Saída: <b>{sai}</b></span>
                    </div>
                """
                st.html(html_content)

            with col_add:
                fixes.horizontal_spacer("0.1em")
                if st.button(
                    label=" ", 
                    icon=":material/add:",
                    key=f"btn_add_{idx}_athena", 
                    use_container_width=True
                    ):
                    calculadora.adicionar_analista(row)
                    st.rerun() 
                    
            with col_rmv:
                fixes.horizontal_spacer("0.1em")
                if st.button(
                    label=" ", 
                    icon=":material/remove:",
                    key=f"btn_rmv_{idx}_athena", 
                    use_container_width=True):
                    calculadora.remover_analista(row)
                    st.rerun()

            with col_del:
                fixes.horizontal_spacer("0.1em")
                if st.button(
                    label=" ", 
                    icon=":material/delete:",
                    key=f"btn_del_{idx}_athena", 
                    use_container_width=True):
                    calculadora.deletar_grupo(row)
                    st.rerun()
            
            html_divisor = "<hr style='margin: 0.5em 0px; border-color: rgba(139,148,158,0.15);'>"
            st.html(html_divisor)