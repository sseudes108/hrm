from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os

# 1. Descobre onde o main.py está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Constrói o caminho para o CSV (voltando uma pasta do 'app' e entrando em 'data')
# O '..' significa "voltar uma pasta"
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "dados_fraude.csv")

app = FastAPI(title="Sharingan Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Proposta(BaseModel):
    id: int
    cliente: str
    valor: float
    status: str
    lat: float
    lng: float
    risco_score: int

def carregar_dados():
    # Agora usamos o caminho absoluto que construímos acima
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return df.to_dict(orient="records")
    else:
        print(f"ERRO: Arquivo não encontrado em {CSV_PATH}")
    return []

@app.get("/stats")
async def get_stats():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return {
            "total": len(df),
            "fraudes": len(df[df["status"] == "Fraude"]),
            "valor_total": float(df["valor"].sum()) # Forçando float para não dar erro de JSON
        }
    return {"erro": "Arquivo não encontrado"}

@app.get("/propostas", response_model=List[Proposta])
async def get_propostas(limit: int = 100):
    # Dica: Retornar 10.800 registros de uma vez pode travar o navegador.
    # Por isso, usamos um 'limit' padrão, mas você pode mudar.
    dados = carregar_dados()
    return dados[:limit]

