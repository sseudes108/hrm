"""Catálogo executável dos gráficos adicionais do Zanpakutou Framework."""

from typing import Any

import pandas as pd
import streamlit as st

from bankai.application.accounts import filter_accounts, get_accounts
from system.core.managers.charts import (
    boxplot,
    heatmap,
    nightingale,
    radar,
    scatter,
    sunburst,
)
from system.view.components.tables import ColumnConfig
from system.view.components.tables import ranking as ranking_table
from system.view.components.tables import status as status_table
from system.view.components.tables import summary as summary_table


def render(context: Any) -> None:
    accounts = _catalog_data(filter_accounts(get_accounts(), context.state.active_filters))
    st.subheader("Catálogo de gráficos")
    st.caption(
        "Exemplos funcionais dos modelos avançados. Os mesmos managers podem ser usados por qualquer aplicação do framework."
    )

    left, right = st.columns(2, gap="xxsmall")
    with left:
        scatter.draw(
            accounts.sample(min(1500, len(accounts)), random_state=42),
            title="Scatter — saldo por perfil de cliente",
            column_x="customer_id",
            column_y="balance",
            category_column="status",
            context=context,
            chart_id="catalog_scatter",
            update_context=True,
            filter_column="customer_id"
        )
    with right:
        radar.draw(
            _radar_data(accounts),
            title="Radar — perfil por tipo de conta",
            label_column="account_type",
            indicator_columns=["saldo_medio", "contas_mil", "agencias", "clientes_mil"],
            context=context,
            chart_id="catalog_radar",
            update_context=True,
            filter_column="account_type"
        )

    left, right = st.columns(2, gap="xxsmall")
    with left:
        boxplot.draw(
            accounts,
            title="Box plot — distribuição de saldo",
            category_column="account_type",
            value_column="balance",
            context=context,
            chart_id="catalog_boxplot",
        )
    with right:
        heatmap.draw(
            accounts,
            title="Heatmap — saldo por ano e status",
            column_x="open_year",
            column_y="status",
            value_column="balance",
            context=context,
            chart_id="catalog_heatmap",
        )

    left, right = st.columns(2, gap="xxsmall")
    with left:
        sunburst.draw(
            accounts,
            title="Sunburst — carteira hierárquica",
            path_columns=["status", "account_type", "branch_group"],
            value_column="balance",
            context=context,
            chart_id="catalog_sunburst",
        )
    with right:
        nightingale.draw(
            accounts,
            title="Nightingale — volume por status",
            category_column="status",
            context=context,
            chart_id="catalog_nightingale",
            update_context=True,
            click_type="categoric_click",
        )

    st.subheader("Tabelas HTML")
    st.caption("Padrões para rankings, resumos executivos e status operacional.")
    _render_tables(context, accounts)


def _catalog_data(accounts: pd.DataFrame) -> pd.DataFrame:
    data = accounts.copy()
    data["open_year"] = data["open_date"].dt.year.astype(str)
    data["branch_group"] = "Grupo " + (data["branch_id"] % 8 + 1).astype(str)
    return data


def _radar_data(accounts: pd.DataFrame) -> pd.DataFrame:
    return (
        accounts.groupby("account_type", as_index=False)
        .agg(
            saldo_medio=("balance", "mean"),
            contas_mil=("account_id", lambda values: len(values) / 1000),
            agencias=("branch_id", "nunique"),
            clientes_mil=("customer_id", lambda values: values.nunique() / 1000),
        )
    )


def _render_tables(context: Any, accounts: pd.DataFrame) -> None:
    branch_ranking = (
        accounts.groupby("branch_id", as_index=False)["balance"].sum()
        .nlargest(8, "balance")
        .assign(branch=lambda frame: "Agência " + frame["branch_id"].astype(str))
    )
    status_summary = accounts.groupby("status", as_index=False).agg(
        accounts=("account_id", "size"), balance=("balance", "sum")
    )
    type_summary = accounts.groupby("account_type", as_index=False).agg(
        accounts=("account_id", "size"), average_balance=("balance", "mean")
    )

    left, right = st.columns(2, gap="xxsmall")
    with left:
        ranking_table.draw(
            branch_ranking, context=context, table_id="catalog_branch_ranking",
            label_column="branch", value_column="balance", title="Ranking de agências",
        )
    with right:
        status_table.draw(
            status_summary, context=context, table_id="catalog_status",
            label_column="status", status_column="status", value_column="balance",
            title="Status da carteira",
        )

    summary_table.draw(
        type_summary,
        context=context,
        table_id="catalog_account_types",
        title="Resumo por tipo de conta",
        columns=[
            ColumnConfig("account_type", "Tipo de conta"),
            ColumnConfig("accounts", "Contas", "integer", "right"),
            ColumnConfig("average_balance", "Saldo médio", "currency", "right"),
        ],
    )
