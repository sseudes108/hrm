"""Defaults compartilhados do contrato visual dos temas."""

from typing import Any


SCHEMA_VERSION = 1

THEME_DEFAULTS: dict[str, Any] = {
    "meta": {"schema_version": SCHEMA_VERSION},
    "chart": {
        "families": {
            "heatmap_low": "#dbeafe",
            "heatmap_mid": "#3b82f6",
            "heatmap_high": "#1e3a8a",
            "hierarchy_border": "#ffffff",
            "hierarchy_label": "#ffffff",
        },
    },
    "components": {
        "button": {
            "background": "var(--ui-colors-border)",
            "foreground": "var(--ui-colors-text)",
            "border": "transparent",
            "radius": "var(--ui-borders-radius-md)",
            "hover_background": "var(--ui-colors-primary)",
            "hover_foreground": "var(--ui-colors-background)",
            "variants": {
                "primary": {
                    "background": "var(--ui-effects-gradient-primary)",
                    "foreground": "var(--ui-colors-background)",
                    "border": "var(--ui-borders-width) solid transparent",
                    "shadow": "var(--ui-borders-shadow-sm)",
                    "hover_background": "var(--ui-colors-primary-hover)",
                    "hover_foreground": "var(--ui-colors-background)",
                    "hover_border": "var(--ui-borders-width) solid transparent",
                    "hover_shadow": "var(--ui-effects-glow-primary)",
                },
                "secondary": {
                    "background": "var(--ui-colors-surface-2)",
                    "foreground": "var(--ui-colors-text)",
                    "border": "var(--ui-borders-width) solid var(--ui-colors-border)",
                    "shadow": "var(--ui-borders-shadow-sm)",
                    "hover_background": "var(--ui-colors-border)",
                    "hover_foreground": "var(--ui-colors-text)",
                    "hover_border": "var(--ui-borders-width) solid var(--ui-colors-border-focus)",
                    "hover_shadow": "0 0 0 transparent",
                },
                "ghost": {
                    "background": "transparent",
                    "foreground": "var(--ui-colors-text-muted)",
                    "border": "var(--ui-borders-width) solid transparent",
                    "shadow": "none",
                    "hover_background": "var(--ui-colors-surface-2)",
                    "hover_foreground": "var(--ui-colors-primary)",
                    "hover_border": "var(--ui-borders-width) solid var(--ui-colors-border)",
                    "hover_shadow": "none",
                },
            },
        },
        "input": {
            "background": "var(--ui-colors-surface)",
            "border": "var(--ui-borders-width) solid var(--ui-colors-border)",
            "radius": "var(--ui-borders-radius-md)",
            "focus_border": "var(--ui-colors-primary)",
        },
        "filter": {
            # Filtros de data e seleção têm widgets nativos de alturas
            # ligeiramente diferentes; este token os alinha pelo card.
            "card_min_height": "90px",
        },
        "navigation": {
            "foreground": "var(--ui-colors-text-muted)",
            "hover_foreground": "var(--ui-colors-secondary)",
            "active_foreground": "var(--ui-colors-text)",
            "indicator": "var(--ui-colors-border-focus)",
        },
        "metric": {
            "value_font": "var(--ui-typography-font-family-mono)",
            "value_size": "var(--ui-typography-size-display)",
            "value_weight": "var(--ui-typography-weight-bold)",
            "value_color": "var(--ui-colors-text)",
        },
        "card": {
            "padding": {
                "none": "0",
                "compact": "var(--ui-spacing-sm)",
                "normal": "var(--ui-spacing-md)",
            },
            "variants": {
                "surface": {
                    "background": "var(--ui-effects-gradient-surface)",
                    "border": "var(--ui-borders-width) solid var(--ui-colors-border)",
                    "radius": "var(--ui-borders-radius-md)",
                    "shadow": "var(--ui-borders-shadow-lg)",
                    "hover_shadow": "var(--ui-borders-shadow-lg), var(--ui-effects-glow-primary)",
                    "hover_transform": "translateY(var(--ui-effects-hover-y)) translateZ(0)",
                },
                "elevated": {
                    "background": "var(--ui-effects-gradient-surface)",
                    "border": "var(--ui-borders-width) solid var(--ui-colors-border)",
                    "radius": "var(--ui-borders-radius-lg)",
                    "shadow": "var(--ui-borders-shadow-lg)",
                    "hover_shadow": "var(--ui-borders-shadow-lg), var(--ui-effects-glow-primary)",
                    "hover_transform": "translateY(var(--ui-effects-hover-y)) translateZ(0)",
                },
                "outline": {
                    "background": "transparent",
                    "border": "var(--ui-borders-width) solid var(--ui-colors-border-focus)",
                    "radius": "var(--ui-borders-radius-md)",
                    "shadow": "none",
                    "hover_shadow": "0 0 0 1px var(--ui-colors-border-focus)",
                    "hover_transform": "translateY(0)",
                },
                "minimal": {
                    "background": "transparent",
                    "border": "none",
                    "radius": "0",
                    "shadow": "none",
                    "hover_shadow": "none",
                    "hover_transform": "translateY(0)",
                },
                "chart": {
                    "background": "var(--ui-effects-gradient-surface)",
                    "border": "var(--ui-borders-width) solid var(--ui-colors-border)",
                    "radius": "var(--ui-borders-radius-md)",
                    "shadow": "var(--ui-borders-shadow-md)",
                    "hover_shadow": "var(--ui-borders-shadow-md)",
                    "hover_transform": "translateY(0)",
                },
            },
        },
    },
}
