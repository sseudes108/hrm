import streamlit as st

def draw(app_name, label, input_id):
    with st.container(key=f"co_file_uploader_{app_name}_{input_id}"):
        file_uploaded = st.file_uploader(
            label=label, type="csv", accept_multiple_files=False
        )

    return file_uploaded