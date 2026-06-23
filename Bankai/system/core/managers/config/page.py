from system.view.pages import error

def run(target_app, context):

    if target_app == "athena":
        from apps.engines import athena
        athena.main(context)

    elif target_app == "gicons":
        from apps.sandbox import g_icons
        g_icons.main(context)
        
    else:
        error.main(target_app)