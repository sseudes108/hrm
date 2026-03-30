import streamlit as st
import Control.Managers.json_manager as JsonMan
from Control.Managers import design_manager as DesignMan
from Control.Managers import image_manager as ImageMan
from datetime import datetime

def get_cor_destaque(cliente):
    """
    Busca a cor de destaque no novo modelo de JSON (Gaveta por Cliente).
    """
    config_cliente = JsonMan.load_json("Control/Config/clientes.json", cliente)
    
    # 2. Retorna a cor_destaque se existir, senão o azul padrão
    # Nota: como config_cliente já é o dict do cliente, basta dar um .get()
    return config_cliente.get("cor_destaque", "#4A90E2")

def draw_borda_topo(cliente):
    cor = DesignMan.get_cor_destaque(cliente)
    st.markdown(f"""
        <div style="
            height: 4px; 
            background-color: {cor}; 
            border-radius: 10px 10px 0 0; 
            margin-bottom: 0px; /* Removido o negativo */
            position: relative;
            z-index: 1;
        "></div>
    """, unsafe_allow_html=True)

def get_clock_emoji():
    now = datetime.now()
    hora = now.hour % 12
    if hora == 0: hora = 12
    minuto = now.minute

    relogios = {
        1: ("🕐", "🕜"), 2: ("🕑", "🕝"), 3: ("🕒", "🕞"),
        4: ("🕓", "🕟"), 5: ("🕔", "🕠"), 6: ("🕕", "🕡"),
        7: ("🕖", "🕢"), 8: ("🕗", "🕣"), 9: ("🕘", "🕤"),
        10: ("🕙", "🕥"), 11: ("🕚", "🕦"), 12: ("🕛", "🕧")
    }

    if 15 <= minuto < 45:
        return relogios[hora][1]
    elif minuto >= 45:
        proxima_hora = (hora % 12) + 1
        return relogios[proxima_hora][0]
    else:
        return relogios[hora][0]


def draw_header(cliente, dashboard):
    # 1. Configurações do Cliente
    cliente_id = cliente
    if cliente == "Itau":
        cliente_id = "Itaú"

    config = JsonMan.load_json("Control/Config/clientes.json", cliente)
    cor_primaria = config.get("cor_destaque", "#4A90E2")

    # 2. Converte o Logo para Base64 
    caminho_logo = f"source/imagens/untitled.PNG"
    try:
        logo_b64 = ImageMan.image_to_base64(caminho_logo)
    except:
        # Fallback caso a imagem não exista
        logo_b64 = "" 

    # 3. Renderiza o Header
    st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {cor_primaria} 0%, rgba(255,255,255,0) 100%);
            padding: 4px; border-radius: 12px; margin-bottom: 25px;
        ">
            <div style="background-color: #f0f2f6; padding: 10px 25px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 18px;">
                    <div style="background: white; padding: 5px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: center;">
                        <img src="{logo_b64}" style="height: 100px; width: 100px; object-fit: contain;">
                    </div>
                    <div>
                        <h1 style="margin: 0; color: #1f2937; font-size: 1.8rem; font-weight: 800;">
                            {cliente_id} <span style="font-weight: 300; color: #6b7280;">| {dashboard}</span>
                        </h1>
                    </div>
                </div>
                <div style="text-align: right; color: #4b5563; font-weight: 600;">
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 1.1rem;">
                        <span>📅 {datetime.now().strftime("%d/%m/%Y")}</span>
                        <span style="color: {cor_primaria}; font-size: 1.3rem;">•</span>
                        <span>{get_clock_emoji()} {datetime.now().strftime("%H:00")}</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)