import streamlit as st
from system.control.contexts import AppContext

def main(context: AppContext):
    print("executando 3")
    st.success("p3")