import streamlit as st
from system.view.components.layout.header.views import brand, helper

def draw_title(header_config, context):
    brand.draw(context, header_config)

def get_component(header_config, context):
    # As colunas são criadas diretamente, pois já estamos "dentro" do container do Card.draw()
    header_cols = st.columns([2, 4, 0.5], gap='xxsmall', vertical_alignment="bottom")

    with header_cols[0]:
        draw_title(header_config, context)

    with header_cols[2]:
        helper.draw_tools(context)
