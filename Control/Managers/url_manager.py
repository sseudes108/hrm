import streamlit as st

def validar_acesso(cliente_url, lista_permitida):
    """
    Retorna True se o cliente existe na lista (case-insensitive),
    caso contrário retorna False.
    """
    if not cliente_url:
        return False
    
    # Normaliza para comparação: remove espaços e coloca em minúsculo
    cliente_limpo = cliente_url.strip().lower()
    
    # Transforma toda a lista permitida em minúsculo para garantir o match
    permitidos_lower = [c.lower() for c in lista_permitida]
    
    return cliente_limpo in permitidos_lower