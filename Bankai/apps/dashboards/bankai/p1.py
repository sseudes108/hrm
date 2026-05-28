import streamlit as st
from system.control.contexts import AppContext

def main(context: AppContext):
    st.success("p1")
    print("executando 1")