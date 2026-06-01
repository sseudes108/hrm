import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()

@st.cache_data
def consultar_banco(query: str) -> pd.DataFrame:
    """
    Conecta ao banco de dados PostgreSQL usando credenciais de variáveis 
    de ambiente, executa uma query SQL e retorna um DataFrame do Pandas.
    """
    # 1. Resgatar as credenciais com segurança
    usuario = os.getenv('DB_USER')
    senha = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    porta = os.getenv('DB_PORT', '5432') # Usa 5432 como padrão se não achar no .env
    banco = os.getenv('DB_NAME')

    # Validação rápida de segurança para evitar erros difíceis de rastrear
    if not all([usuario, senha, host, banco]):
        raise ValueError("Credenciais ausentes. Verifique o arquivo .env.")

    # 2. Criar a string de conexão e a engine
    string_conexao = f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}'
    engine = create_engine(string_conexao)

    # 3. Executar a query e gerar o DataFrame
    df = pd.read_sql(query, con=engine)
    
    return df

# ==========================================
# Exemplo de como usar a função na prática:
# ==========================================
if __name__ == "__main__":
    # Sua query SQL
    minha_query = """
        SELECT order_id, customer_name, sales 
        FROM public.superstore_sales 
        WHERE sales > 1000
        ORDER BY sales DESC
        LIMIT 5;
    """
    
    # Chama a função passando a query
    df_vendas_altas = consultar_banco(minha_query)
    
    # Exibe o resultado
    print(df_vendas_altas)