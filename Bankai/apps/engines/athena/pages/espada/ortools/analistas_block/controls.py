import streamlit as st
from apps.engines.athena.pages.espada.ortools.inputs import CATALOGO_TURNOS
from apps.engines.athena.core.calculadora import page as calculadora
from system.view.components.inputs.select import select
from system.view.components.inputs.text import text_input
from system.view.components.inputs.number import number_input
from system.view.components.layout import fixes
from system.core.log.system import log

# Passamos o payload da página pai para termos acesso ao sla_minutos
def draw(context, payload):
    _draw_component(context, payload)

def _draw_component(context, payload):
    opcoes_nomes = [turno.nome for turno in CATALOGO_TURNOS.values()]
    
    # Como é um multiselect, ele retorna uma lista. Assumiremos a primeira escolha se houver.
    turnos_selecionados_nomes = select.draw(
        context=context, input_id="ortools_turnos_select_control_inp",
        label="TURNO", options=opcoes_nomes
    )
    
    turno_escolhido = turnos_selecionados_nomes[0] if turnos_selecionados_nomes else opcoes_nomes[0]

    entrada_col, almoco_col, saida_col = st.columns(3, gap="xxsmall")
    with entrada_col:
        entrada = text_input.draw(
            context=context, label="ENT.", input_id="ortools_entrada_ctn", default="08:00"
        )

    with almoco_col:
        almoco = text_input.draw(
            context=context, label="ALM.", input_id="ortools_almoço_ctn", default="12:00"
        )

    with saida_col:
        saida = text_input.draw(
            context=context, label="SAI.", input_id="ortools_saida_ctn", default="17:48"
        )

    col_rmv, col_add = st.columns([3,1], gap="xxsmall")
    with col_rmv:
        qtd = number_input.draw(
            context=context, label="QUANTIDADE", 
            input_id="ortools_qtd_ctn_inp", default=1, max_v=27
        )

    with col_add:
        fixes.horizontal_spacer("0.01em")
        if st.button(
            label=" ", 
            icon=":material/add:",
            key=f"btn_add_cnt_athena", 
            use_container_width=True
        ):
            # # ==========================================
            # # LOGS DE DEBUG (O que está chegando da UI?)
            # # ==========================================
            # log.log(f"Botão ADD Clicado!", t="debug", emoji="🖱️")
            # log.log(f"Turno: '{turno_escolhido}' | Qtd: {qtd}", t="debug", emoji="🕹️")
            # log.log(f"Strings -> Entrada: '{entrada}' | Almoço: '{almoco}' | Saída: '{saida}'", t="debug", emoji="⏱️")
            # # ==========================================

            # Passa todos os parâmetros da tela para a calculadora converter e injetar no state!
            calculadora.adicionar_analistas_customizados(
                turno_nome=turno_escolhido,
                entrada_str=entrada,
                almoco_ini_str=almoco,
                saida_str=saida,
                qtd=int(qtd),
                sla_minutos=payload.sla
            )
            st.rerun()