"""Casos de uso para a análise de contas do Bankai."""

from typing import Any

import pandas as pd

from bankai.infrastructure.accounts import load_accounts
from system.core.managers.filters import apply_filters


def get_accounts() -> pd.DataFrame:
    """Entrega uma cópia para que a camada visual possa criar agregações locais."""
    return load_accounts().copy()


def filter_accounts(accounts: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    """Aplica os filtros opcionais mantidos no estado da aplicação."""
    filtered = apply_filters(accounts, filters)

    query = str(filters.get("account_query", "")).strip()
    if query:
        searchable = filtered[["account_id", "customer_id", "branch_id"]].astype(str)
        filtered = filtered.loc[searchable.apply(lambda row: row.str.contains(query, case=False, na=False).any(), axis=1)]

    return filtered.copy()