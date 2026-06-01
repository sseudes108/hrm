import io
import pandas as pd
import streamlit as st

from system.view.components.cards import card, CardConfig
from system.control.contexts import AppContext
from system.view.layout import fixes

def draw(df: pd.DataFrame, title:str, subtitle:str, context:AppContext, height:int = 500, sort_by:str = None):
    card.draw(
        CardConfig(
            context.app_name, card_id=f"table_{context.app_name}_{title}",
            has_title=True, title=title, subtitle=subtitle, has_action=True
        ), 
        render_content=lambda: _draw_component(df, context, title, height, sort_by),
        render_action=lambda: _btn_baixar_excel(df, context, title)
    )

def _btn_baixar_excel(df: pd.DataFrame, context: AppContext, title: str):
    
    # 1. Criação do arquivo Excel em Memória
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    excel_data = buffer.getvalue()
    
    # 2. A CHAVE MÁGICA: Tem que ter "wrap_btn_" pro seu CSS global capturar!
    wrapper_key = f"wrap_btn_{context.app_name}_{title}"

    # 3. Renderiza o botão
    with st.container(key=wrapper_key):
        st.download_button(
            label="📥 Excel", 
            data=excel_data,
            file_name=f'{title.replace(" ", "_")}_Dados.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            key=f"btn_excel_{context.app_name}_{title}"
        )

def _draw_component(df: pd.DataFrame, context:AppContext, title:str, height: int, sort_by: str = None):
    """
    Desenha uma tabela estática 100% renderizada com o tema do Bankai.
    """
    # 1. Tira o height do Streamlit! Deixa ele crescer livremente.
    with st.container(key=f"co_table_{context.app_name}_{title}"):
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=True)
        
        html_table = df.to_html(index=False, classes="bk-table", escape=False)
        
        # 2. Injeta a altura (max-height) e o scroll vertical (overflow-y) direto na div!
        html_content = f"""
        <div class="bk-table-wrapper" style="max-height: {height}px; overflow-y: auto;">
            {html_table}
        </div>
        """
        
        st.markdown(html_content, unsafe_allow_html=True)
    fixes.draw_empty_element(20)