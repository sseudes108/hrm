from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "dados_fraude.csv")
STATUS_ORDER = ["Fraude", "Reprovada", "Aprovada", "Pendenciada"]

app = FastAPI(title="Sharingan Fraud Detection API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class Proposta(BaseModel):
    id: int
    cliente: str
    valor: float
    status: str
    lat: float
    lng: float
    risco_score: int
    ibge: int
    municipio: str
    uf: str
    estado: str
    regiao: str
    occurred_at: str


def load_dataframe() -> pd.DataFrame:
    """Adaptador de fonte de dados. Troque este corpo por uma consulta PostgreSQL no futuro."""
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    return pd.read_csv(CSV_PATH)


def status_rows(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return [
            {"status": status, "count": 0, "total_value": 0.0, "average_risk": 0.0}
            for status in STATUS_ORDER
        ]
    grouped = df.groupby("status", dropna=False).agg(
        count=("id", "size"), total_value=("valor", "sum"), average_risk=("risco_score", "mean")
    )
    rows = []
    for status in STATUS_ORDER:
        values = grouped.loc[status] if status in grouped.index else None
        rows.append({
            "status": status,
            "count": int(values["count"]) if values is not None else 0,
            "total_value": float(values["total_value"]) if values is not None else 0.0,
            "average_risk": round(float(values["average_risk"]), 1) if values is not None else 0.0,
        })
    return rows


def build_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"total": 0, "total_value": 0.0, "high_risk_count": 0, "high_risk_rate": 0.0, "by_status": status_rows(df)}
    high_risk_count = int((df["risco_score"] >= 80).sum())
    return {
        "total": int(len(df)),
        "total_value": float(df["valor"].sum()),
        "high_risk_count": high_risk_count,
        "high_risk_rate": round(high_risk_count / len(df) * 100, 1),
        "by_status": status_rows(df),
    }


@app.get("/stats")
@app.get("/dashboard/summary")
async def get_summary():
    return build_summary(load_dataframe())


@app.get("/analytics")
async def get_analytics():
    df = load_dataframe()
    if df.empty:
        return {"summary": build_summary(df), "trend": [], "top_municipalities": []}

    df = df.copy()
    df["occurred_at"] = pd.to_datetime(df["occurred_at"])
    df["period"] = df["occurred_at"].dt.strftime("%d/%m")
    recent_periods = sorted(df["period"].unique(), key=lambda period: pd.to_datetime(period, format="%d/%m"), reverse=True)[:14]
    trend = df[df["period"].isin(recent_periods)].groupby("period").agg(
        proposals=("id", "size"), value=("valor", "sum"), high_risk=("risco_score", lambda values: int((values >= 80).sum()))
    ).reset_index()
    top_municipalities = df.groupby(["municipio", "uf"]).agg(
        proposals=("id", "size"), value=("valor", "sum"), average_risk=("risco_score", "mean")
    ).sort_values(["average_risk", "value"], ascending=False).head(8).reset_index()
    return {
        "summary": build_summary(df),
        "trend": [
            {"period": row.period, "proposals": int(row.proposals), "value": round(float(row.value), 2), "high_risk": int(row.high_risk)}
            for row in trend.assign(sort_date=pd.to_datetime(trend["period"], format="%d/%m")).sort_values("sort_date").itertuples()
        ],
        "top_municipalities": [
            {"municipio": row.municipio, "uf": row.uf, "proposals": int(row.proposals), "value": float(row.value), "average_risk": round(float(row.average_risk), 1)}
            for row in top_municipalities.itertuples()
        ],
    }


@app.get("/propostas", response_model=List[Proposta])
async def get_propostas(limit: int = 100):
    return load_dataframe().head(max(1, min(limit, 5000))).to_dict(orient="records")


@app.get("/investigations", response_model=List[Proposta])
async def get_investigations(limit: int = 30):
    df = load_dataframe()
    if df.empty:
        return []
    ranked = df.sort_values(["risco_score", "valor"], ascending=[False, False]).head(max(1, min(limit, 100)))
    return ranked.to_dict(orient="records")


@app.get("/states/summary")
async def get_states_summary():
    df = load_dataframe()
    if df.empty:
        return []
    grouped = df.groupby(["uf", "estado", "regiao"]).agg(
        proposals=("id", "size"), value=("valor", "sum"),
        frauds=("status", lambda values: int((values == "Fraude").sum())),
        high_risk=("risco_score", lambda values: int((values >= 80).sum())),
    ).reset_index()
    return [
        {"uf": row.uf, "state": row.estado, "region": row.regiao, "proposals": int(row.proposals), "value": float(row.value), "frauds": int(row.frauds), "high_risk": int(row.high_risk)}
        for row in grouped.sort_values("frauds", ascending=False).itertuples()
    ]
