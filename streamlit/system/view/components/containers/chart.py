import streamlit as st
from streamlit_echarts import st_echarts
import uuid

def container(fig, type="plotly", height="350px"):
    key = f"metric_{uuid.uuid4().hex[:4]}"

    with st.container(key=f"chart_container_{key}"):

        if type == "plotly":
            st.plotly_chart(fig, width="stretch", key=key)

        elif type == "echarts":
            st_echarts(options=fig, height=height, key=key)