from streamlit_echarts import st_echarts

def render(options: dict, chart_config: dict):
    chart_type = chart_config.get("type", "chart")

    echarts_events = {
        "click": "function(params) { return { name: params.name, ts: Date.now() }; }"
    }

    clicked_value = st_echarts(
        options=options,
        events=echarts_events,
        height=f"{chart_config.get('height', 400)}px",
        key=f"{chart_type}_{chart_config['key']}"
    )

    return clicked_value

    # if not filter_column:
    #     return

    # last_selection_key = f"{chart_config["type"]}_column_last_sel"
    # last_selection = context.active_filters.get(last_selection_key, "")

    # if clicked_value and clicked_value.get("chart_event") is not None:
    #     event = clicked_value["chart_event"]

    #     selected = event["name"] if isinstance(event, dict) else event

    #     if last_selection == selected:
    #         context.remove_filter(last_selection_key, rerun=False)
    #         context.remove_filter(filter_column, rerun=True)
    #     else:
    #         context.update_filter(last_selection_key, selected, rerun=False)
    #         context.update_filter(filter_column, selected, rerun=True)