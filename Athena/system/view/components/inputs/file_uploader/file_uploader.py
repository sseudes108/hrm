import streamlit as st
from system.view.components._keys import scoped_key

def draw(context, label, input_id, *, accepted_types=("csv",), accept_multiple_files=False):
    """Renderiza upload com chaves isoladas por aplicação."""
    with st.container(key=scoped_key(context, "co_file_uploader", input_id)):
        file_uploaded = st.file_uploader(
            label=label,
            type=list(accepted_types),
            accept_multiple_files=accept_multiple_files,
            key=scoped_key(context, "file_uploader", input_id),
        )

    return file_uploaded
