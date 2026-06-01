import os
import pandas as pd
import streamlit as st
import psycopg2 # 🚀 Import nativo do Postgres
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()

@st.cache_data
def consultar_banco(query: str) -> pd.DataFrame:
    """
    Conecta ao banco de dados PostgreSQL usando psycopg2,
    executa uma query SQL e retorna um DataFrame do Pandas.
    """
    # 1. Resgatar as credenciais com segurança
    usuario = os.getenv('DB_USER')
    senha = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    porta = os.getenv('DB_PORT', '5432')
    banco = os.getenv('DB_NAME')

    # Validação rápida de segurança
    if not all([usuario, senha, host, banco]):
        raise ValueError("Credenciais ausentes. Verifique o arquivo .env.")

    conn = None
    try:
        # 2. Criar a conexão pura com o banco
        conn = psycopg2.connect(
            dbname=banco,
            user=usuario,
            password=senha,
            host=host,
            port=porta
        )
        
        # 3. Executar a query usando um cursor
        with conn.cursor() as cur:
            cur.execute(query)
            
            # Pega todas as linhas resultantes da query
            dados = cur.fetchall()
            
            # Pega o nome das colunas inspecionando o "description" do cursor
            colunas = [desc[0] for desc in cur.description]
            
        # 4. Monta o DataFrame silenciosamente
        df = pd.DataFrame(dados, columns=colunas)
        
        # O Psycopg2 traz números (NUMERIC) como 'decimal.Decimal', que quebra o ECharts.
        # Nós varremos as colunas e forçamos a conversão de objetos numéricos para float.
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    # Se for texto (Customer Name) ou Data, ele não consegue converter e cai aqui.
                    # Nós usamos o 'pass' para ignorar e seguir a vida.
                    pass 
        
        return df

    except Exception as e:
        # Repassa o erro para o Streamlit ajudar no debug
        st.error(f"Erro ao consultar o banco de dados: {e}")
        return pd.DataFrame() # Retorna DataFrame vazio para não quebrar a tela
        
    finally:
        # 5. GARANTIA: Fecha a conexão independente de sucesso ou falha
        if conn is not None:
            conn.close()

# ==========================================
# Exemplo de como usar a função na prática:
# ==========================================
if __name__ == "__main__":
    minha_query = """
        SELECT order_id, customer_name, sales 
        FROM public.superstore_sales 
        WHERE sales > 1000
        ORDER BY sales DESC
        LIMIT 5;
    """
    
    df_vendas_altas = consultar_banco(minha_query)
    print(df_vendas_altas)