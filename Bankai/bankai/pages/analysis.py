"""Dashboard analítico de contas construído sobre ``accounts.csv``."""

from typing import Any

import pandas as pd
import streamlit as st

from bankai.application.accounts import filter_accounts, get_accounts
from bankai.pages.components.layout import analysis_filters
from system.core.managers.charts import bar, line, pie
from system.view.components.cards.metric import metric
from system.view.components.layout import fixes


def render(context: Any) -> None:
    """Renderiza KPIs, distribuição e evolução das contas filtradas."""
    analysis_filters.draw(context)
    with st.container(
        height=800,
        border=False,
        key=f"co_page_analysis_content_{context.app_name}",
    ):
        _render_content(context)


def _render_content(context: Any) -> None:
    accounts = filter_accounts(get_accounts(), context.state.active_filters)

    _render_kpis(context, accounts)
    _render_charts(context, accounts)
    _render_table(accounts, context)

def _render_kpis(context: Any, accounts: pd.DataFrame) -> None:
    fixes.horizontal_spacer("5px")
    total_balance = accounts["balance"].sum()
    average_balance = accounts["balance"].mean() if not accounts.empty else 0.0
    active_share = (accounts["status"].eq("Active").mean() * 100) if not accounts.empty else 0.0
    branches = accounts["branch_id"].nunique()

    columns = st.columns([1.2, 1, 0.7, 0.7], gap="xxsmall")
    metrics = (
        ("Saldo sob gestão", f"R$ {total_balance:,.2f}", "Soma dos saldos filtrados", "balance", "green"),
        ("Saldo médio", f"R$ {average_balance:,.2f}", "Média por conta", "average", "black"),
        ("Contas ativas", f"{active_share:.1f}%", "Participação da base ativa", "active", "black"),
        ("Agências", str(branches), "Contas filtradas", "branches", "black"),
    )
    for column, (title, value, subtitle, identifier, color) in zip(columns, metrics):
        with column:
            metric.draw(
                context=context,
                title=title,
                value=value,
                subtitle=subtitle,
                metric_id=f"analysis_{identifier}",
                padding="compact",
                value_color=color, variant="surface"
            )

def _render_charts(context: Any, accounts: pd.DataFrame) -> None:
    fixes.horizontal_spacer()
    if accounts.empty:
        st.info("Nenhuma conta corresponde aos filtros selecionados.")
        return

    top_branches = (
        accounts.groupby("branch_id", as_index=False)["balance"].sum()
        .nlargest(10, "balance")
        .assign(branch_label=lambda frame: "Agência " + frame["branch_id"].astype(str))
    )

    left, right = st.columns(2, gap="xxsmall")
    with left:
        line.draw(
            df=accounts,
            title="Evolução do saldo por abertura",
            subtitle="Soma mensal das contas abertas",
            column_x="open_date",
            columns_y=["balance"],
            context=context,
            agg_func="sum",
            date_frequency="M",
            update_context=True,
            card_hover=False,
            card_variant="surface",
            height="330px",
            card_title_case="capitalize",
            card_title_align="left"
        )
    with right:
        pie.draw(
            title="Distribuição por status",
            subtitle="Quantidade de contas",
            df=accounts,
            column_pie="status",
            context=context,
            update_context=True,
            click_type="categoric_click",
            card_hover=False,
            card_variant="chart",
            height="330px",
        )

    fixes.horizontal_spacer()
    bar.draw(
        df=top_branches,
        title="Top 10 agências por saldo",
        subtitle="Soma dos saldos filtrados",
        column_x="branch_label",
        filter_column="branch_id",
        columns_y=["balance"],
        context=context,
        agg_func="sum",
        update_context=True,
        card_hover=False,
        click_type="categoric_click",
        card_variant="chart",
        height="340px",
    )

def _render_table(accounts: pd.DataFrame, context) -> None:
    fixes.horizontal_spacer()
    st.subheader("Amostra das contas filtradas")
    preview = accounts.sort_values("balance", ascending=False).head(100).copy()
    preview["open_date"] = preview["open_date"].dt.date
    st.dataframe(preview, width='stretch', hide_index=True)
