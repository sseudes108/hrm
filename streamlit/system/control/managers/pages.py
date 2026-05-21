from apps.dashboards.bankai.bankai import main as bankai
from apps.engines.shebattle.shebattle import main as shebattle
from system.view.pages.error import show_error_page

def run(target_app, context):
    if target_app == "bankai":
        bankai(context)

    elif target_app == "shebattle":
        shebattle(context)
        
    else:
        show_error_page(target_app)
