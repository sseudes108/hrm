import os
import pandas as pd
import streamlit as st
from psycopg2 import pool
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()

# ==========================================
# 1. GERENCIADOR DO POOL DE CONEXÕES
# ==========================================
# st.cache_resource garante que o pool seja criado apenas UMA VEZ 
# e compartilhado entre todos os reloads e usuários da aplicação.
def iniciar_pool():
    usuario = os.getenv('DB_USER')
    senha = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    porta = os.getenv('DB_PORT', '5432')
    banco = os.getenv('DB_NAME')

    if not all([usuario, senha, host, banco]):
        raise ValueError("Credenciais ausentes. Verifique o arquivo .env.")

    try:
        # Cria um pool com no mínimo 1 e no máximo 10 conexões simultâneas.
        # ThreadedConnectionPool é obrigatório no Streamlit pois ele é multithread.
        connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=banco,
            user=usuario,
            password=senha,
            host=host,
            port=porta
        )
        print("✅ Pool de conexões do PostgreSQL criado com sucesso!")
        return connection_pool

    except Exception as e:
        st.error(f"❌ Falha ao criar o pool de conexões: {e}")
        return None

# Instancia o pool globalmente
db_pool = iniciar_pool()

# ==========================================
# 2. FUNÇÃO DE CONSULTA (USANDO O POOL)
# ==========================================
# st.cache_data faz o cache do RESULTADO da query. 
# Se a query for igual, ele não vai até o banco, economizando processamento.
# O ttl (Time to Live) define a validade do cache em segundos.
def consultar_banco(query: str) -> pd.DataFrame:
    """
    Pega uma conexão do pool, executa a query SQL, 
    retorna um DataFrame e devolve a conexão ao pool.
    """
    if not db_pool:
        st.error("O pool de conexões não está disponível.")
        return pd.DataFrame()

    conn = None
    try:
        # 1. "Pega emprestado" uma conexão livre do pool
        conn = db_pool.getconn()
        
        # 2. Executar a query
        with conn.cursor() as cur:
            cur.execute(query)
            dados = cur.fetchall()
            colunas = [desc[0] for desc in cur.description]
            
        # 3. Monta o DataFrame
        df = pd.DataFrame(dados, columns=colunas)
        
        # Converte tipos decimais do banco para float do Pandas/Streamlit
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass 
        
        return df

    except Exception as e:
        st.error(f"Erro ao consultar o banco de dados: {e}")
        return pd.DataFrame()
        
    finally:
        # 4. GARANTIA: "Devolve" a conexão para o pool independente de erro ou sucesso
        if conn is not None:
            db_pool.putconn(conn)


# ==========================================
# Exemplo de uso na interface
# ==========================================
if __name__ == "__main__":
    st.title("Lakshmi Data Core")
    
    # Query de teste puxando os dados do Airflow
    query_mercado = """
        SELECT ativo, mercado, tempo_grafico, data_hora, fechamento 
        FROM public.mercado_historico 
        ORDER BY data_hora DESC 
        LIMIT 5;
    """
    
    df_mercado = consultar_banco(query_mercado)
    st.dataframe(df_mercado)