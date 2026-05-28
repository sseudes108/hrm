## imports internos devido a loop de dependencia circular
from apps.dashboards import run_bankai
from apps.engines import (
    run_lakshmi
)
from system.view.pages import run_error_page
from system.control.contexts import AppContext

def run(target_app, context:AppContext):
    if target_app == "bankai":
        run_bankai(context)

    elif target_app == "lakshmi":
        context.update_mode("light")
        run_lakshmi(context)
        
    else:
        run_error_page(target_app)