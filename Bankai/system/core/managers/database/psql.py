import os
from functools import lru_cache

import pandas as pd
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor


class DatabaseQueryError(RuntimeError):
    """Falha de infraestrutura durante a execução de uma consulta."""


class DatabaseConnectionError(DatabaseQueryError):
    """O banco não está disponível para uma operação que exige conexão."""


@lru_cache(maxsize=1)
def iniciar_pool() -> pool.ThreadedConnectionPool:
    """Cria o pool sob demanda usando o ambiente já carregado pelo bootstrap."""
    usuario = os.getenv('DB_USER')
    senha = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    porta = os.getenv('DB_PORT', '5432')
    banco = os.getenv('DB_NAME')

    if not all([usuario, senha, host, banco]):
        raise RuntimeError("Credenciais PostgreSQL ausentes no ambiente.")

    try:
        return pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=banco,
            user=usuario,
            password=senha,
            host=host,
            port=porta
        )
    except Exception as e:
        raise RuntimeError("Falha ao criar o pool PostgreSQL.") from e

# ==========================================
# 2. FUNÇÃO DE CONSULTA (USANDO O POOL)
# ==========================================
def consultar_banco(query: str) -> pd.DataFrame:
    """
    Pega uma conexão do pool, executa a query SQL, 
    retorna um DataFrame e devolve a conexão ao pool.
    """
    conn = None
    try:
        db_pool = iniciar_pool()
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

    except Exception as exc:
        raise DatabaseQueryError("Erro ao consultar o banco de dados.") from exc
        
    finally:
        # 4. GARANTIA: "Devolve" a conexão para o pool independente de erro ou sucesso
        if conn is not None:
            db_pool.putconn(conn)


def validate_connection() -> bool:
    """Verifica conectividade sem expor credenciais nem detalhes internos."""
    try:
        fetch_one("SELECT 1 AS connected")
        return True
    except DatabaseQueryError:
        return False


def fetch_one(query: str, params: tuple | dict | None = None) -> dict | None:
    """Executa uma consulta parametrizada e devolve uma única linha."""
    conn = None
    try:
        db_pool = iniciar_pool()
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            row = cur.fetchone()
        return dict(row) if row else None
    except Exception as exc:
        raise DatabaseConnectionError("Não foi possível consultar o banco de dados.") from exc
    finally:
        if conn is not None:
            db_pool.putconn(conn)


def insert_record(table: str, values: dict[str, object], *, returning: str | None = None) -> object | None:
    """Insere valores usando identificadores e parâmetros seguros do psycopg2.

    ``table``, colunas e ``returning`` são validados como identificadores SQL;
    valores nunca são interpolados na string da consulta.
    """
    if not values:
        raise ValueError("values não pode ser vazio.")
    _validate_identifier(table)
    for column in values:
        _validate_identifier(column)
    if returning is not None:
        _validate_identifier(returning)

    conn = None
    try:
        db_pool = iniciar_pool()
        conn = db_pool.getconn()
        columns = list(values)
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({placeholders})").format(
            table=sql.Identifier(table),
            columns=sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            placeholders=sql.SQL(", ").join(sql.Placeholder(column) for column in columns),
        )
        if returning is not None:
            query += sql.SQL(" RETURNING {column}").format(column=sql.Identifier(returning))
        with conn.cursor() as cur:
            cur.execute(query, values)
            result = cur.fetchone()[0] if returning is not None else None
        conn.commit()
        return result
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        raise DatabaseQueryError("Não foi possível inserir o registro.") from exc
    finally:
        if conn is not None:
            db_pool.putconn(conn)


def fetch_auth_user(table: str, username: str) -> dict | None:
    """Busca o hash de um usuário ativo com identificador SQL validado."""
    _validate_identifier(table)
    conn = None
    try:
        db_pool = iniciar_pool()
        conn = db_pool.getconn()
        query = sql.SQL(
            "SELECT username, password_hash FROM {table} "
            "WHERE username = %(username)s AND is_active = TRUE LIMIT 1"
        ).format(table=sql.Identifier(table))
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, {"username": username})
            row = cur.fetchone()
        return dict(row) if row else None
    except Exception as exc:
        raise DatabaseConnectionError("Não foi possível consultar usuários no banco de dados.") from exc
    finally:
        if conn is not None:
            db_pool.putconn(conn)


def _validate_identifier(identifier: str) -> None:
    if not identifier or not identifier.replace("_", "").isalnum() or identifier[0].isdigit():
        raise ValueError(f"Identificador SQL inválido: '{identifier}'.")
