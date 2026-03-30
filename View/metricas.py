import streamlit as st

# def draw_metric_card(emoji: str, titulo: str, valor: str, cor_valor: str = "#000000"):
#     """
#     Renderiza um cartão de métrica personalizado no Streamlit usando HTML/CSS.
    
#     Args:
#         emoji (str): Ícone/Emoji representativo da métrica.
#         titulo (str): Título ou descrição da métrica.
#         valor (str): Valor numérico ou texto da métrica.
#         cor_valor (str): Cor hexadecimal para destacar o valor e a borda lateral.
#     """
    
#     html_content = f"""
#     <div style="
#         background-color: #ffffff; 
#         padding: 12px; 
#         border-radius: 8px; 
#         border: 1px solid #e6e9ef; 
#         border-left: 5px solid {cor_valor}; 
#         display: flex; 
#         align-items: center; 
#         justify-content: space-between; 
#         min-height: 75px; 
#         box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
#     ">
#         <div style="
#             display: flex;
#             align-items: center;
#             gap: 8px;
#             flex: 1;
#             min-width: 0;
#         ">
#             <span style="
#                 font-size: 1.2rem;
#                 flex-shrink: 0;
#             ">{emoji}</span>
#             <p style="
#                 margin: 0;
#                 font-size: 0.65rem;
#                 color: #5f6368;
#                 font-weight: 700;
#                 text-transform: uppercase;
#                 line-height: 1.2;
#                 word-wrap: break-word;
#             ">{titulo}</p>
#         </div>
#         <div style="
#             font-size: 1.4rem;
#             font-weight: 800;
#             color: {cor_valor};
#             margin-left: 10px;
#             flex-shrink: 0;
#             text-align: right;
#         ">{valor}</div>
#     </div>
#     """
    
#     st.markdown(html_content, unsafe_allow_html=True)
def draw_metric_card(emoji: str, titulo: str, valor: str, cor_valor: str = "#000000"):
    """
    Renderiza um cartão de métrica personalizado no Streamlit usando HTML/CSS.
    
    Args:
        emoji (str): Ícone/Emoji representativo da métrica.
        titulo (str): Título ou descrição da métrica.
        valor (str): Valor numérico ou texto da métrica.
        cor_valor (str): Cor hexadecimal para destacar o valor e a borda lateral.
    """
    
    html_content = f"""
    <div style="
        background-color: #ffffff; 
        padding: 12px; 
        border-radius: 8px; 
        border: 1px solid #e6e9ef; 
        border-left: 5px solid {cor_valor}; 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        min-height: 75px; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
            min-width: 0;
        ">
            <span style="
                font-size: 1.2rem;
                flex-shrink: 0;
            ">{emoji}</span>
            <p style="
                margin: 0;
                font-size: 0.65rem;
                color: #5f6368;
                font-weight: 700;
                text-transform: uppercase;
                line-height: 1.2;
                word-wrap: break-word;
            ">{titulo}</p>
        </div>
        <div style="
            font-size: 1.4rem;
            font-weight: 800;
            color: {cor_valor};
            margin-left: 10px;
            flex-shrink: 0;
            text-align: right;
        ">{valor}</div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)