import streamlit as st
from system.control.contexts import AppContext

def main(context: AppContext):
    print("executando 2")
    st.success("p2")