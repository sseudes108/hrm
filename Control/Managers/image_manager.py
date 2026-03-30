import base64
from io import BytesIO
from PIL import Image
import streamlit as st

@st.cache_data
def image_to_base64(image_input):
    """
    Converte um caminho de arquivo ou objeto PIL em string Base64.
    """
    # Se for um caminho de arquivo (string), abre a imagem
    if isinstance(image_input, str):
        img = Image.open(image_input)
    else:
        img = image_input

    buffered = BytesIO()
    # Salva a imagem no buffer em formato PNG
    img.save(buffered, format="PNG")
    
    # Codifica os bytes para base64 e transforma em string utf-8
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return f"data:image/png;base64,{img_str}"