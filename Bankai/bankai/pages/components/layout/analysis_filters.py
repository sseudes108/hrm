"""Barra de filtros exclusiva da rota de análise de contas."""

from typing import Any

import streamlit as st

from bankai.application.accounts import get_accounts
from system.view.components.filters.date import date
from system.view.components.filters.select import select
from system.view.components.inputs.text import text_input


def draw(context: Any) -> None:
    """Renderiza filtros de data, seleção e texto, sincronizados ao estado Bankai."""
    accounts = get_accounts()
    date_column, status_column, type_column, query_column = st.columns(4, gap="small")

    with date_column:
        date.draw_start_end(accounts, "open_date", "analysis", context, has_card=True)
    with status_column:
        select.draw(accounts, "status", "analysis", context, has_card=True)
    with type_column:
        select.draw(accounts, "account_type", "analysis", context, has_card=True)
    with query_column:
        query = text_input.draw(
            context=context,
            label="Conta, cliente ou agência",
            input_id="analysis_account_query",
            default=str(context.state.active_filters.get("account_query", "")),
        )
        context.state.update_filter("account_query", query, rerun=False)
