import streamlit as st
from bankai.application.accounts import get_accounts
from system.view.components.cards import card
from system.view.components.filters.date import date

def draw(context):
    date.draw_start_end(
        get_accounts(), "open_date", "sidebar", context, has_card=True
    )