"""Contrato e validação dos temas consumidos pela camada visual."""

from collections.abc import Mapping
from typing import Any

from .mapping import deep_merge
from .theme_defaults import SCHEMA_VERSION, THEME_DEFAULTS

CARD_VARIANTS = ("surface", "elevated", "outline", "minimal", "chart")
CARD_PADDINGS = ("none", "compact", "normal")


class ThemeValidationError(ValueError):
    """Indica que um tema não atende ao contrato visual compartilhado."""


def normalize_and_validate(theme: Mapping[str, Any], *, source: str) -> dict[str, Any]:
    """Aplica defaults de contrato e valida os tokens usados pelo sistema."""
    normalized = deep_merge(THEME_DEFAULTS, theme)
    _validate_mapping(normalized, "theme", source)

    _require(normalized, "meta.name", str, source)
    _require(normalized, "meta.schema_version", int, source)
    if normalized["meta"]["schema_version"] != SCHEMA_VERSION:
        raise ThemeValidationError(
            f"Tema '{source}': meta.schema_version deve ser {SCHEMA_VERSION}."
        )

    _require_many(
        normalized,
        {
            "layout.header_height": (str, int, float),
            "layout.logo_size": (str, int, float),
            "typography.font_family": str,
            "typography.font_family_mono": str,
            "typography.size_xs": _number,
            "typography.size_sm": _number,
            "typography.size_base": _number,
            "typography.size_subtitle": _number,
            "typography.size_title": _number,
            "typography.size_display": _number,
            "typography.weight_normal": _number,
            "typography.weight_medium": _number,
            "typography.weight_bold": _number,
            "typography.line_height": _number,
            "spacing.xs": (str, int, float),
            "spacing.sm": (str, int, float),
            "spacing.md": (str, int, float),
            "spacing.lg": (str, int, float),
            "spacing.xl": (str, int, float),
            "borders.width": (str, int, float),
            "borders.radius_sm": (str, int, float),
            "borders.radius_md": (str, int, float),
            "borders.radius_lg": (str, int, float),
            "borders.radius_full": (str, int, float),
            "borders.shadow_sm": str,
            "borders.shadow_md": str,
            "borders.shadow_lg": str,
            "icons.toggle": str,
            "effects.hover_y": (str, int, float),
            "effects.backdrop_blur": (str, int, float),
            "effects.glow_primary": str,
            "effects.glow_danger": str,
            "effects.gradient_primary": str,
            "effects.gradient_surface": str,
            "effects.surface_overlay.enabled": bool,
            "effects.surface_overlay.border_gradient": str,
            "effects.surface_overlay.inner_shadow": str,
            "chart.grid_color": str,
            "chart.font_color": str,
            "chart.echarts.tooltip_bg": str,
            "chart.echarts.tooltip_border": str,
            "chart.echarts.tooltip_text": str,
            "chart.echarts.axis_line_color": str,
            "chart.echarts.axis_label_color": str,
            "chart.echarts.split_line_color": str,
            "chart.echarts.glow_blur": _number,
            "chart.echarts.area_opacity_top": _number,
            "chart.echarts.area_opacity_base": _number,
            "chart.severity.critical": str,
            "chart.severity.warning": str,
            "chart.severity.normal": str,
            "chart.severity.stale": str,
            "chart.families.heatmap_low": str,
            "chart.families.heatmap_mid": str,
            "chart.families.heatmap_high": str,
            "chart.families.hierarchy_border": str,
            "chart.families.hierarchy_label": str,
            "components.button.background": str,
            "components.button.foreground": str,
            "components.button.border": str,
            "components.button.radius": str,
            "components.button.hover_background": str,
            "components.button.hover_foreground": str,
            "components.input.background": str,
            "components.input.border": str,
            "components.input.radius": str,
            "components.input.focus_border": str,
            "components.filter.card_min_height": str,
            "components.navigation.foreground": str,
            "components.navigation.hover_foreground": str,
            "components.navigation.active_foreground": str,
            "components.navigation.indicator": str,
            "components.metric.value_font": str,
            "components.metric.value_size": str,
            "components.metric.value_weight": str,
            "components.metric.value_color": str,
        },
        source,
    )

    for variant in CARD_VARIANTS:
        _require_many(
            normalized,
            {
                f"components.card.variants.{variant}.background": str,
                f"components.card.variants.{variant}.border": str,
                f"components.card.variants.{variant}.radius": str,
                f"components.card.variants.{variant}.shadow": str,
                f"components.card.variants.{variant}.hover_shadow": str,
                f"components.card.variants.{variant}.hover_transform": str,
            },
            source,
        )

    for padding in CARD_PADDINGS:
        _require(normalized, f"components.card.padding.{padding}", str, source)

    for color_name, color_value in _mapping_at(normalized, "colors", source).items():
        if not isinstance(color_value, str):
            raise ThemeValidationError(
                f"Tema '{source}': colors.{color_name} deve ser uma string."
            )

    color_scale = _at(normalized, "chart.colorscale_extended", source)
    if not isinstance(color_scale, list) or not all(isinstance(color, str) for color in color_scale):
        raise ThemeValidationError(
            f"Tema '{source}': chart.colorscale_extended deve ser uma lista de strings."
        )

    _validate_mapping(_at(normalized, "components", source), "components", source)
    return normalized


def _require_many(theme: Mapping[str, Any], requirements: dict[str, object], source: str) -> None:
    for path, expected_type in requirements.items():
        _require(theme, path, expected_type, source)


def _require(theme: Mapping[str, Any], path: str, expected_type: object, source: str) -> None:
    value = _at(theme, path, source)
    if isinstance(expected_type, type) or isinstance(expected_type, tuple):
        expected_types = expected_type if isinstance(expected_type, tuple) else (expected_type,)
        is_valid = isinstance(value, expected_types)
        expected_name = " ou ".join(item.__name__ for item in expected_types)
    else:
        is_valid = bool(expected_type(value))
        expected_name = "um número"

    if not is_valid:
        raise ThemeValidationError(
            f"Tema '{source}': {path} deve ser {expected_name}; recebido {type(value).__name__}."
        )


def _at(theme: Mapping[str, Any], path: str, source: str) -> Any:
    value: Any = theme
    for part in path.split("."):
        if not isinstance(value, Mapping) or part not in value:
            raise ThemeValidationError(f"Tema '{source}': chave obrigatória ausente: {path}.")
        value = value[part]
    return value


def _mapping_at(theme: Mapping[str, Any], path: str, source: str) -> Mapping[str, Any]:
    value = _at(theme, path, source)
    _validate_mapping(value, path, source)
    return value


def _validate_mapping(value: Any, path: str, source: str) -> None:
    if not isinstance(value, Mapping):
        raise ThemeValidationError(
            f"Tema '{source}': {path} deve ser um objeto JSON; recebido {type(value).__name__}."
        )


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
