import pandas as pd
import streamlit as st

from system.control.managers import hash as hash_man

from system.view.layout import fixes

def draw(app_name:str, titulo:str, df:pd.DataFrame):
    key = hash_man.get_hash_key(app_name, titulo)

    with st.container(key=f"table_deltas_card_{key}", height=600):

        head_cols = st.columns([5, 10 ,1], gap='xxsmall', vertical_alignment="center")

        with st.container(key=f"table_deltas_header_{key}"):
            with head_cols[0]:
                with st.container(key=f"table_deltas_header_right_{key}", vertical_alignment="center"):
                    st.write("Esquerda (Título)")

            with head_cols[1]:
                with st.container(key=f"table_deltas_header_middle_{key}", vertical_alignment="center"):
                    filter_cols = st.columns(4)

                    with filter_cols[0]:
                        st.selectbox("1", [1,2,3], key=1)

                    with filter_cols[1]:
                        st.selectbox("2", [1,2,3], key=2)

                    with filter_cols[2]:
                        st.selectbox("3", [1,2,3], key=3)

                    with filter_cols[3]:
                        st.selectbox("4", [1,2,3], key=4)

                    st.write("Meio")

            with head_cols[2]:
                with st.container(key=f"table_deltas_header_left_{key}", vertical_alignment="center"):
                    st.write("💀")
        
        with st.container(key=f"table_deltas_body_{key}"):
            fixes.draw_bg_element(880, "azul")