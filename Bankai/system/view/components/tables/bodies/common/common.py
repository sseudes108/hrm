import streamlit as st
import pandas as pd

import system.control.managers.hash as hash_man

def draw_body(df:pd.DataFrame, key):
    key_hash = hash_man.get_hash(key)
    st.dataframe(
        df, 
        hide_index=True,
        height="content",
        key=f"{key}_{key_hash}_common_table_body"
    )