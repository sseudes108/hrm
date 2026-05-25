import streamlit as st
from system.control.contexts import AppContext
from system.control.managers import layout as layout_man

from system.view.components.layout import header
from system.view.components.layout import navigator

def draw_header():
    header_config = {
        "model": "nav",
        "has_card": True,
        "hover": True,
        "app_name": "lakshmi",
        "title": "lakshmi",
        "subtitle": "goddess of prosperity",
        "logo_left": "png"
    }
    header.draw(header_config)

def draw_navigator():
    navi_config = {
        "app_name": "lakshmi",
        "model": "bg",
        "has_card": False,
        "nav_pages":[
            "Adi",
            "Dhana",
            "Vidya",
            "Veera",
            "Gaja",
            "Santana",
            "Dhanya",
            "Vijaya"
        ]
    }
    return navigator.draw(navi_config)

def main(context:AppContext):
    layout_man.set_bg("apps/engines/lakshmi/layout/bg-palacio.png")

    draw_header()
    nav_pages = draw_navigator()

    with nav_pages[0]:
        st.success("Teste")

if __name__ == "__main__":
    main()