import uuid
import streamlit as st
from streamlit_echarts import st_echarts

def chart_card(theme, fig, title=None, subtitle=None, value=None, value_sub=None,height="300px", key=None):
    if key is None:
        key = f"card_{hash(title) if title else uuid.uuid4().hex[:6]}"
    
    c = theme["colors"]
    ty = theme["typography"]
    h_str = str(height) if "px" in str(height) or "%" in str(height) else f"{height}px"

    header_html = ""
    if any([title, subtitle, value]):
        title_part = f'<h3 style="margin:0; color:{c["text"]}; font-size:{ty["size_subtitle"]}px; font-weight:{ty["weight_bold"]};">{title}</h3>' if title else ""
        sub_part = f'<p style="margin:0; color:{c["text_muted"]}; font-size:{ty["size_sm"]}px;">{subtitle}</p>' if subtitle else ""
        val_part = f'<div class="metric-value"><strong>{value}</strong></div>' if value else ""
        val_sub_part = f'<p style="margin:0; color:{c["text_muted"]}; font-size:{ty["size_sm"]}px;">{value_sub}</p>' if subtitle else ""

        header_html = f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2em; width: 100%;">
                <div style="flex-grow: 1;">{title_part}{sub_part}</div>
                <div style="flex-grow: 0;">{val_part}{val_sub_part}</div>
            </div>
        """

    with st.container(key=f"chart_container_{key}"):
        if header_html:
            st.markdown(header_html, unsafe_allow_html=True)
        
        st_echarts(options=fig, height=h_str, key=f"echart_{key}")