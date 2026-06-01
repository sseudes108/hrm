from system.control.contexts import AppContext

from system.view.layout                      import fixes
from system.view.components.renderers        import page
from system.view.components.layout.header    import header
from system.view.components.layout.navigator import navigator

from apps.dashboards.bankai.pages import date_input_lab

PAGES = {
    1: date_input_lab
}

def get_page(context: AppContext):
    return PAGES.get(context.current_page)

def main(context:AppContext):
    fixes.draw_empty_element(22)

    header.draw(
        title="bankai", subtitle="Zanpakuto Framework", 
        context=context, model="nav", nav_pages=["Date Input Lab"]
    )

    # navigator.draw(
    #     context=context, nav_pages=["Date Input Lab"]
    # )

    page_to_render = get_page(context)
    page.render(page_to_render, context)