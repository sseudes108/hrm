"""Leitura local da base de contas usada pela demonstração Bankai."""

from functools import lru_cache
from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "accounts.csv"


@lru_cache(maxsize=1)
def load_accounts() -> pd.DataFrame:
    """Carrega e normaliza a base uma única vez por processo."""
    accounts = pd.read_csv(DATA_PATH, parse_dates=["open_date"])
    accounts["balance"] = pd.to_numeric(accounts["balance"], errors="coerce").fillna(0.0)
    return accounts