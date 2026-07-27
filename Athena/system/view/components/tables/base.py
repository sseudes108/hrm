"""Tabela HTML segura e tematizada para resumos de pequeno e médio porte."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from html import escape
from typing import Any, Literal

import pandas as pd
import streamlit as st

from system.view.components.cards import card
from system.view.components._keys import scoped_key
from .formatters import CellFormatter, format_cell


Alignment = Literal["left", "center", "right"]


@dataclass(frozen=True)
class ColumnConfig:
    key: str
    label: str
    formatter: str | CellFormatter = "text"
    align: Alignment = "left"

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("A coluna da tabela deve possuir uma chave.")
        if self.align not in {"left", "center", "right"}:
            raise ValueError("align deve ser left, center ou right.")


@dataclass(frozen=True)
class HtmlTableConfig:
    table_id: str
    columns: Sequence[ColumnConfig]
    title: str | None = None
    subtitle: str | None = None
    variant: str = "surface"
    padding: str = "normal"
    show_card: bool = True
    empty_message: str = "Nenhum registro para exibir."

    def __post_init__(self) -> None:
        if not self.table_id:
            raise ValueError("table_id é obrigatório.")
        if not self.columns:
            raise ValueError("Uma tabela HTML requer ao menos uma coluna.")


def draw(df: pd.DataFrame, config: HtmlTableConfig, context: Any) -> None:
    """Renderiza dados já preparados; não substitui tabelas nativas interativas."""
    content: Callable[[], None] = lambda: _draw_content(df, config, context)
    card.draw(
        card.CardConfig(
            card_id=f"table_{config.table_id}", context=context, model="base",
            variant=config.variant,
            padding=config.padding,
            show_card=config.show_card,
            hover=False,
            has_title=bool(config.title),
            title=config.title,
            subtitle=config.subtitle,
        ),
        card.CardRenderConfig(content=content),
    )


def _draw_content(df: pd.DataFrame, config: HtmlTableConfig, context: Any) -> None:
    key = scoped_key(context, "table", config.table_id)
    rows = _render_rows(df, config.columns)
    head = "".join(
        f'<th class="ui-table-align--{column.align}">{escape(column.label)}</th>'
        for column in config.columns
    )
    body = rows or f'<tr><td class="ui-table-empty" colspan="{len(config.columns)}">{escape(config.empty_message)}</td></tr>'
    st.html(f'<div class="ui-table-wrap" id="{escape(key)}"><table class="ui-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def _render_rows(df: pd.DataFrame, columns: Sequence[ColumnConfig]) -> str:
    missing = [column.key for column in columns if column.key not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes na tabela HTML: {missing}")
    rows = []
    for _, row in df.iterrows():
        cells = "".join(
            f'<td class="ui-table-align--{column.align}">{format_cell(row[column.key], column.formatter)}</td>'
            for column in columns
        )
        rows.append(f"<tr>{cells}</tr>")
    return "".join(rows)
