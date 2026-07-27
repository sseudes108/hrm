"""APIs de alto nível para gráficos analíticos além de linha, barra e pizza."""

from typing import Callable, Literal

import pandas as pd

from system.core.contexts import AppContext
from system.core.log.view import warnings
from system.core.managers.chart_data import (
    ChartDataError,
    group_pie,
    prepare_boxplot,
    prepare_heatmap,
    prepare_radar,
    prepare_scatter,
    prepare_sunburst,
)
from system.core.managers.charts.interactions import ChartClickType, apply_click_filter
from system.core.managers.charts.payload import attach_filter_values
from system.view.components.charts.echarts import chart
from system.view.components.charts.echarts.config import (
    BaseChartConfig,
    BoxplotSeriesConfig,
    GridConfig,
    HeatmapSeriesConfig,
    LegendConfig,
    NightingaleSeriesConfig,
    RadarSeriesConfig,
    ScatterSeriesConfig,
    SunburstSeriesConfig,
    ToolboxConfig,
    TooltipConfig,
)


Aggregation = Literal["sum", "mean", "min", "max", "count"]


def scatter(
    df: pd.DataFrame, *, title: str, column_x: str, column_y: str,
    context: AppContext, size_column: str | None = None,
    category_column: str | None = None, chart_id: str | None = None,
    height: str = "330px", update_context: bool = False,
    click_type: ChartClickType = "categoric_click", filter_column: str | None = None,
) -> None:
    target_column = filter_column or category_column or column_x
    data = _prepare(
        lambda: prepare_scatter(
            df, column_x=column_x, column_y=column_y,
            size_column=size_column, category_column=category_column,
            extra_columns=[target_column],
        ),
        context,
    )
    if data is None:
        return
    if click_type not in {"date", "date_click"}:
        data = attach_filter_values(
            data, df, filter_column=target_column,
            match_columns=[column_x, column_y, *( [category_column] if category_column else [])],
        )
    clicked = _render(
        context=context, model="scatter", title=title, chart_id=chart_id,
        height=height,
        series=ScatterSeriesConfig(column_x, column_y, size_column, category_column),
        tooltip=TooltipConfig(trigger="item"), grid=GridConfig(bottom="12%"),
        data=data,
    )
    _apply_interaction(
        df, context, target_column, clicked,
        click_type, update_context, event_column=category_column or column_x,
    )


def radar(
    df: pd.DataFrame, *, title: str, label_column: str,
    indicator_columns: list[str], context: AppContext, chart_id: str | None = None,
    height: str = "360px", update_context: bool = False,
    click_type: ChartClickType = "categoric_click", filter_column: str | None = None,
) -> None:
    data = _prepare(
        lambda: prepare_radar(df, label_column=label_column, indicator_columns=indicator_columns),
        context,
    )
    if data is None or data.empty:
        _empty(context, title)
        return
    if click_type not in {"date", "date_click"}:
        data = attach_filter_values(data, df, filter_column=filter_column or label_column, match_columns=[label_column])
    max_values = {
        column: max(1.0, float(data[column].max()) * 1.15)
        for column in indicator_columns
    }
    clicked = _render(
        context=context, model="radar", title=title, chart_id=chart_id, height=height,
        series=RadarSeriesConfig(label_column, indicator_columns, max_values),
        tooltip=TooltipConfig(trigger="item"), data=data,
    )
    _apply_interaction(
        df, context, filter_column or label_column, clicked, click_type,
        update_context, event_column=label_column,
    )


def boxplot(
    df: pd.DataFrame, *, title: str, category_column: str, value_column: str,
    context: AppContext, chart_id: str | None = None, height: str = "330px",
    update_context: bool = False, click_type: ChartClickType = "categoric_click",
    filter_column: str | None = None,
) -> None:
    data = _prepare(
        lambda: prepare_boxplot(df, category_column=category_column, value_column=value_column),
        context,
    )
    if data is None or data.empty:
        _empty(context, title)
        return
    if click_type not in {"date", "date_click"}:
        data = attach_filter_values(data, df, filter_column=filter_column or category_column, match_columns=[category_column])
    clicked = _render(
        context=context, model="boxplot", title=title, chart_id=chart_id, height=height,
        series=BoxplotSeriesConfig(category_column, value_column),
        tooltip=TooltipConfig(trigger="item"), grid=GridConfig(bottom="18%"), data=data,
    )
    _apply_interaction(
        df, context, filter_column or category_column, clicked, click_type,
        update_context, event_column=category_column,
    )


def heatmap(
    df: pd.DataFrame, *, title: str, column_x: str, column_y: str,
    value_column: str, context: AppContext, aggregation: Aggregation = "sum",
    chart_id: str | None = None, height: str = "350px", update_context: bool = False,
    click_type: ChartClickType = "categoric_click", filter_column: str | None = None,
) -> None:
    data = _prepare(
        lambda: prepare_heatmap(
            df, column_x=column_x, column_y=column_y,
            value_column=value_column, aggregation=aggregation,
        ),
        context,
    )
    if data is None or data.empty:
        _empty(context, title)
        return
    if click_type not in {"date", "date_click"}:
        data = attach_filter_values(data, df, filter_column=filter_column or column_x, match_columns=[column_x, column_y])
    clicked = _render(
        context=context, model="heatmap", title=title, chart_id=chart_id, height=height,
        series=HeatmapSeriesConfig(column_x, column_y, value_column),
        tooltip=TooltipConfig(trigger="item"), grid=GridConfig(bottom="20%"), data=data,
    )
    _apply_interaction(
        df, context, filter_column or column_x, clicked, click_type,
        update_context, event_column=column_x,
    )


def sunburst(
    df: pd.DataFrame, *, title: str, path_columns: list[str], value_column: str,
    context: AppContext, chart_id: str | None = None, height: str = "380px",
    update_context: bool = False, click_type: ChartClickType = "categoric_click",
    filter_column: str | None = None,
) -> None:
    data = _prepare(
        lambda: prepare_sunburst(
            df, path_columns=path_columns, value_column=value_column,
            filter_column=filter_column if click_type not in {"date", "date_click"} else None,
        ),
        context,
    )
    if not data:
        _empty(context, title)
        return
    clicked = _render(
        context=context, model="sunburst", title=title, chart_id=chart_id, height=height,
        series=SunburstSeriesConfig(path_columns, value_column),
        tooltip=TooltipConfig(trigger="item"), data=data,
    )
    if filter_column:
        _apply_interaction(
            df, context, filter_column, clicked, click_type, update_context,
            event_column=filter_column,
        )


def nightingale(
    df: pd.DataFrame, *, title: str, category_column: str, context: AppContext,
    value_column: str | None = None, aggregation: Aggregation = "sum",
    chart_id: str | None = None, height: str = "350px", update_context: bool = False,
    click_type: ChartClickType = "categoric_click", filter_column: str | None = None,
) -> None:
    data = _prepare(
        lambda: group_pie(
            df, category_column=category_column, value_column=value_column,
            aggregation=aggregation,
        ),
        context,
    )
    if data is None or data.empty:
        _empty(context, title)
        return
    if (data["value"] < 0).any():
        warnings.draw("Nightingale não aceita valores negativos.", alert="warning", context=context)
        return
    if click_type not in {"date", "date_click"}:
        data = attach_filter_values(data, df, filter_column=filter_column or category_column, match_columns=[category_column])
    clicked = _render(
        context=context, model="nightingale", title=title, chart_id=chart_id, height=height,
        series=NightingaleSeriesConfig(category_column, "value", ["20%", "72%"], ["50%", "44%"]),
        tooltip=TooltipConfig(trigger="item"), legend=LegendConfig(orientation="horizontal", top="82%"),
        data=data,
    )
    _apply_interaction(
        df, context, filter_column or category_column, clicked, click_type,
        update_context, event_column=category_column,
    )


def _render(
    *, context: AppContext, model: str, title: str, chart_id: str | None,
    height: str, series: object, data: object, tooltip: TooltipConfig,
    grid: GridConfig | None = None, legend: LegendConfig | None = None,
) -> object:
    return chart.draw(
        BaseChartConfig(
            app_name=context.app_name, context=context, model=model, title=title,
            theme=context.theme, series=series, chart_id=chart_id, height=height,
            has_card_title=True, card_variant="chart", card_padding="normal",
            tooltip=tooltip, grid=grid or GridConfig(), legend=legend or LegendConfig(),
            toolbox=ToolboxConfig(magic=None, top="0%"),
        ),
        data,
        context,
    )


def _prepare(factory: Callable[[], object], context: AppContext):
    try:
        return factory()
    except ChartDataError as exc:
        warnings.draw(str(exc), alert="error", context=context)
        return None


def _empty(context: AppContext, title: str) -> None:
    warnings.draw(f"O gráfico '{title}' não possui dados para exibir.", alert="info", context=context)


def _apply_interaction(
    df: pd.DataFrame,
    context: AppContext,
    column: str | None,
    event_data: object,
    click_type: ChartClickType,
    enabled: bool,
    event_column: str | None = None,
) -> None:
    if enabled:
        apply_click_filter(
            df=df,
            context=context,
            column=column,
            event_column=event_column,
            event_data=event_data if isinstance(event_data, dict) else None,
            click_type=click_type,
        )
