from system.view.components.layout.navigator import navigator
from system.view.components.renderers import page

from apps.engines.athena.pages.espada.ortools import page as ortools

SUBPAGES = {
    1: ortools,
    # 2: wip,
    # 3: escalas
}

def get_subpage(context):
    return SUBPAGES.get(context.current_subpage or 1, ortools)

def main(context):
    navigator.draw(
        context=context, is_sub=True, nav_pages=[
            "Ortools", "Wip", "Escalas"
        ]
    )

    page_to_render = get_subpage(context)
    page.render(page_to_render, context)