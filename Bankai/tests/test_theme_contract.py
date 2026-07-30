"""Testes do contrato de temas sem dependência do runtime Streamlit."""

import unittest
import os
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from system.core.managers.view import theme
from system.core.managers.config import theme_preferences
from system.core.managers.view.theme_schema import ThemeValidationError
from system.core.managers.view.theme_tokens import compile_css_variables
from system.core.managers.view.css import render_theme_tokens
from system.view.components.cards.base.card import CardConfig
from system.view.components.button.button import ButtonConfig
from system.view.components.layout.navigator.navigator import NavigationItem, NavigatorConfig
from system.view.components._keys import scoped_key
from system.core.contexts import require_filter_state
from system.core.managers.chart_data import (
    ChartDataError,
    group_pie,
    group_series,
    prepare_boxplot,
    prepare_heatmap,
    prepare_radar,
    prepare_scatter,
    prepare_sunburst,
    add_period_column,
    prepare_axis_data,
)
from system.view.components.tables.base import ColumnConfig, _render_rows
from system.view.components.tables.formatters import format_cell
from system.core.managers.charts.interactions import apply_click_filter
from system.core.managers.charts.payload import FILTER_VALUE_KEY, attach_filter_values
from system.core.managers.filters import apply_filters
from system.core.auth.captcha import MathCaptcha
from system.core.auth.locks import AttemptLockout
from system.core.auth.passwords import hash_password, verify_password
from system.core.auth.tokens import issue_token, verify_token
from system.core.managers.database.psql import _validate_identifier
from system.core.applications.contracts import ApplicationDefinition
from system.core.applications.registry import ApplicationRegistry
from system.core.auth import AuthConfig
from system.core.contexts.app_context import AppContext
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
THEME_DIRECTORY = ROOT / "bankai" / "theme"


class ThemeContractTests(unittest.TestCase):
    def test_bankai_light_theme_is_valid(self) -> None:
        loaded = theme.load(THEME_DIRECTORY / "base.json", THEME_DIRECTORY / "light.json")
        self.assertEqual(loaded["meta"]["schema_version"], 1)
        self.assertEqual(
            loaded["components"]["card"]["variants"]["surface"]["radius"],
            "var(--ui-borders-radius-md)",
        )

    def test_bankai_dark_theme_is_valid(self) -> None:
        loaded = theme.load(THEME_DIRECTORY / "base.json", THEME_DIRECTORY / "dark.json")
        self.assertEqual(loaded["colors"]["primary"], "#ff6a00")

    def test_component_defaults_fill_a_new_theme(self) -> None:
        loaded = theme.load(THEME_DIRECTORY / "base.json", THEME_DIRECTORY / "light.json")
        loaded["components"] = {"button": {"radius": "24px"}}

        from system.core.managers.view.theme_schema import normalize_and_validate
        normalized = normalize_and_validate(loaded, source="example")

        self.assertEqual(normalized["components"]["button"]["radius"], "24px")
        self.assertEqual(normalized["components"]["input"]["background"], "var(--ui-colors-surface)")
        self.assertIn("minimal", normalized["components"]["card"]["variants"])

    def test_component_tokens_must_be_strings(self) -> None:
        loaded = theme.load(THEME_DIRECTORY / "base.json", THEME_DIRECTORY / "light.json")
        invalid = deepcopy(loaded)
        invalid["components"]["button"]["background"] = 42

        from system.core.managers.view.theme_schema import normalize_and_validate
        with self.assertRaisesRegex(ThemeValidationError, "components.button.background"):
            normalize_and_validate(invalid, source="example")

    def test_theme_provides_three_button_variants(self) -> None:
        loaded = theme.load(THEME_DIRECTORY / "base.json", THEME_DIRECTORY / "dark.json")

        self.assertEqual(
            set(loaded["components"]["button"]["variants"]),
            {"primary", "secondary", "ghost"},
        )
        compiled = compile_css_variables(loaded)
        self.assertIn("--ui-components-button-variants-primary-background:", compiled)

    def test_error_identifies_missing_token(self) -> None:
        with self.assertRaisesRegex(ThemeValidationError, "typography.font_family"):
            theme_schema = {
                "meta": {"name": "Example"},
                "layout": {"header_height": "48px", "logo_size": "24"},
            }
            from system.core.managers.view.theme_schema import normalize_and_validate
            normalize_and_validate(theme_schema, source="example")

    def test_compiler_exposes_custom_component_token(self) -> None:
        compiled = compile_css_variables(
            {"components": {"card": {"variants": {"elevated": {"radius": "24px"}}}}}
        )
        self.assertIn("--ui-components-card-variants-elevated-radius: 24px;", compiled)

    def test_css_manager_emits_only_generic_tokens(self) -> None:
        rendered = render_theme_tokens({"typography": {"font_family": "Inter"}})
        self.assertIn("--ui-typography-font-family: Inter;", rendered)
        self.assertNotIn("--bk-", rendered)

    def test_card_variant_is_exposed_in_its_configuration(self) -> None:
        context = type("Context", (), {"app_name": "example"})()
        card = CardConfig(card_id="summary", context=context, variant="outline")
        self.assertEqual(card.variant, "outline")
        self.assertIn(card.padding, {"none", "compact", "normal"})

    def test_card_rejects_unknown_padding(self) -> None:
        context = type("Context", (), {"app_name": "example"})()
        with self.assertRaisesRegex(ValueError, "padding inválido"):
            CardConfig(card_id="summary", context=context, padding="wide")

    def test_card_exposes_title_controls(self) -> None:
        context = type("Context", (), {"app_name": "example"})()
        card = CardConfig(
            card_id="summary",
            context=context,
            title_case="capitalize",
            title_align="center",
        )
        self.assertEqual(card.title_case, "capitalize")
        self.assertEqual(card.title_align, "center")

    def test_theme_provides_chart_card_variant(self) -> None:
        loaded = theme.load(THEME_DIRECTORY / "base.json", THEME_DIRECTORY / "dark.json")
        self.assertIn("chart", loaded["components"]["card"]["variants"])
        self.assertEqual(loaded["components"]["filter"]["card_min_height"], "90px")

    def test_filter_card_model_is_available_for_aligned_filter_wrappers(self) -> None:
        context = type("Context", (), {"app_name": "example"})()
        card = CardConfig(card_id="filters", context=context, model="filter", show_card=False)
        self.assertEqual(card.model, "filter")
        self.assertFalse(card.show_card)

    def test_navigator_configuration_is_route_based(self) -> None:
        items = [NavigationItem(route="home", label="Home")]
        config = NavigatorConfig(
            app_name="example",
            model="tabs",
            items=items,
            active_route="home",
            on_navigate=lambda route: None,
        )
        self.assertEqual(config.items[0].route, "home")

    def test_component_keys_are_namespaced_by_application(self) -> None:
        context = type("Context", (), {"app_name": "example"})()
        self.assertNotEqual(
            scoped_key(context, "input_text", "name"),
            scoped_key(context, "input_select", "name"),
        )
        self.assertTrue(scoped_key(context, "input_text", "name").startswith("input_text_example_"))

    def test_button_configuration_exposes_stable_keys_and_variants(self) -> None:
        context = type("Context", (), {"app_name": "example", "theme": {}})()
        primary = ButtonConfig(context=context, button_id="save", label="Salvar")
        ghost = ButtonConfig(
            context=context,
            button_id="save",
            label="Salvar",
            variant="ghost",
        )

        self.assertEqual(primary.widget_key, ghost.widget_key)
        self.assertIn("co_button_primary_example_", primary.container_key)
        self.assertIn("co_button_ghost_example_", ghost.container_key)
        with self.assertRaisesRegex(ValueError, "variant inválida"):
            ButtonConfig(
                context=context,
                button_id="save",
                label="Salvar",
                variant="danger",
            )

    def test_theme_preference_round_trip_is_scoped_by_application(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            preference_path = Path(temporary_directory) / "preferences.json"
            theme_preferences.save_theme_mode("bankai", "dark", path=preference_path)
            theme_preferences.save_theme_mode("athena", "light", path=preference_path)

            self.assertEqual(
                theme_preferences.load_theme_mode("bankai", "light", path=preference_path),
                "dark",
            )
            self.assertEqual(
                theme_preferences.load_theme_mode("athena", "dark", path=preference_path),
                "light",
            )

            preference_path.write_text("{json inválido", encoding="utf-8")
            self.assertEqual(
                theme_preferences.load_theme_mode("bankai", "light", path=preference_path),
                "light",
            )

            preference_path.write_text('{"theme_modes": []}', encoding="utf-8")
            self.assertEqual(
                theme_preferences.load_theme_mode("bankai", "dark", path=preference_path),
                "dark",
            )

    def test_app_context_persists_only_an_actual_theme_change(self) -> None:
        persisted_modes = []
        context = AppContext(
            app_name="example",
            theme={"mode": "dark"},
            mode="dark",
            theme_loader=lambda mode: {"mode": mode},
            theme_mode_persister=persisted_modes.append,
        )

        context.update_mode(" LIGHT ")
        context.update_mode("light")

        self.assertEqual(context.mode, "light")
        self.assertEqual(context.theme, {"mode": "light"})
        self.assertEqual(persisted_modes, ["light"])

    def test_filter_state_contract_reports_a_clear_error(self) -> None:
        context = type("Context", (), {"state": object()})()
        with self.assertRaisesRegex(TypeError, "active_filters"):
            require_filter_state(context)

    def test_chart_grouping_validates_columns_before_aggregation(self) -> None:
        frame = pd.DataFrame({"month": ["2026-01", "2026-01"], "value": [10, 20]})
        grouped = group_series(
            frame,
            column_x="month",
            columns_y=["value"],
            aggregation="sum",
        )
        self.assertEqual(grouped.loc[0, "value"], 30)
        with self.assertRaises(ChartDataError):
            group_series(
                frame,
                column_x="missing",
                columns_y=["value"],
                aggregation="sum",
            )

    def test_pie_grouping_validates_columns_before_access(self) -> None:
        frame = pd.DataFrame({"status": ["active", "closed"]})

        with self.assertRaises(ChartDataError):
            group_pie(frame, category_column="missing")

    def test_advanced_chart_data_contracts(self) -> None:
        frame = pd.DataFrame(
            {
                "group": ["A", "A", "B"],
                "subgroup": ["X", "Y", "X"],
                "x": [1, 2, 3],
                "y": [10, 20, 30],
                "value": [5, 7, 11],
            }
        )
        self.assertEqual(len(prepare_scatter(frame, column_x="x", column_y="y")), 3)
        self.assertEqual(len(prepare_radar(frame, label_column="group", indicator_columns=["x", "y"])), 2)
        self.assertEqual(len(prepare_boxplot(frame, category_column="group", value_column="value")), 2)
        self.assertEqual(len(prepare_heatmap(frame, column_x="group", column_y="subgroup", value_column="value")), 3)
        self.assertEqual(len(prepare_sunburst(frame, path_columns=["group", "subgroup"], value_column="value")), 2)

    def test_period_axis_preparation_keeps_the_original_filter_column(self) -> None:
        frame = pd.DataFrame({"open_date": ["2026-01-03", "2026-02-12"], "value": [1, 2]})
        enriched = add_period_column(frame, source_column="open_date", frequency="M")
        self.assertIn("open_month", enriched.columns)
        self.assertEqual(enriched["open_month"].tolist(), ["2026-01", "2026-02"])
        prepared, axis_column = prepare_axis_data(frame, column_x="open_date", date_frequency="M")
        self.assertEqual(axis_column, "open_month")
        self.assertIn("open_date", prepared.columns)

    def test_html_table_formatters_are_safe_and_localized(self) -> None:
        self.assertEqual(format_cell(1234.5, "currency"), "R$ 1.234,50")
        self.assertEqual(format_cell(-2.5, "trend"), '<span class="ui-table-trend ui-table-trend--negative">↓ 2,5%</span>')
        self.assertIn("&lt;script&gt;", format_cell("<script>", "text"))
        self.assertIn("ui-table-badge--success", format_cell("Active", "badge"))

    def test_html_table_rows_validate_columns_and_escape_values(self) -> None:
        frame = pd.DataFrame({"name": ["<admin>"], "value": [10]})
        rows = _render_rows(frame, [ColumnConfig("name", "Nome"), ColumnConfig("value", "Valor", "integer")])
        self.assertIn("&lt;admin&gt;", rows)
        self.assertIn("10", rows)
        with self.assertRaisesRegex(ValueError, "ausentes"):
            _render_rows(frame, [ColumnConfig("missing", "Ausente")])

    def test_dataframe_filter_manager_applies_and_ignores_unknown_columns(self) -> None:
        frame = pd.DataFrame(
            {
                "status": ["Active", "Closed", "Active"],
                "opened": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03"]),
            }
        )
        filtered = apply_filters(
            frame,
            {"status": "Active", "opened": [pd.Timestamp("2026-01-03").date()] * 2, "missing": "ignored"},
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["opened"].date().isoformat(), "2026-01-03")

    def test_chart_click_toggles_context_filter_without_missing_column_errors(self) -> None:
        class State:
            def __init__(self):
                self.active_filters = {}
                self.events = {}

            def update_filter(self, column, value, rerun=True):
                self.active_filters[column] = value
                return True

            def remove_filter(self, column, rerun=True):
                return self.active_filters.pop(column, None) is not None

            def get_last_event_ts(self, column):
                return self.events.get(column)

            def set_last_event_ts(self, column, timestamp):
                self.events[column] = timestamp

        context = type("Context", (), {"state": State()})()
        frame = pd.DataFrame({"status": ["Active", "Closed"]})
        event = {"name": "Closed", "componentType": "series", "ts": 10}
        self.assertTrue(apply_click_filter(df=frame, context=context, column="status", event_data=event))
        self.assertEqual(context.state.active_filters["status"], "Closed")
        self.assertFalse(apply_click_filter(df=frame, context=context, column="missing", event_data=event))

        event["ts"] = 11
        self.assertTrue(apply_click_filter(df=frame, context=context, column="status", event_data=event))
        self.assertNotIn("status", context.state.active_filters)

    def test_chart_click_maps_display_label_to_real_filter_column(self) -> None:
        class State:
            def __init__(self):
                self.active_filters = {}
                self.events = {}

            def update_filter(self, column, value, rerun=True):
                self.active_filters[column] = value
                return True

            def remove_filter(self, column, rerun=True):
                return self.active_filters.pop(column, None) is not None

            def get_last_event_ts(self, column):
                return self.events.get(column)

            def set_last_event_ts(self, column, timestamp):
                self.events[column] = timestamp

        context = type("Context", (), {"state": State()})()
        frame = pd.DataFrame({"branch_id": [78, 12], "branch_label": ["Agência 78", "Agência 12"]})
        applied = apply_click_filter(
            df=frame,
            context=context,
            column="branch_id",
            event_column="branch_label",
            event_data={"name": "Agência 78", "componentType": "series", "ts": 1},
        )
        self.assertTrue(applied)
        self.assertEqual(context.state.active_filters["branch_id"], 78)
        raw_accounts = pd.DataFrame({"branch_id": [78, 12, 78], "balance": [1, 2, 3]})
        self.assertEqual(len(apply_filters(raw_accounts, context.state.active_filters)), 2)

    def test_chart_payload_uses_the_filter_column_value_for_aggregated_points(self) -> None:
        class State:
            def __init__(self):
                self.active_filters = {}
                self.events = {}

            def update_filter(self, column, value, rerun=True):
                self.active_filters[column] = value
                return True

            def remove_filter(self, column, rerun=True):
                return self.active_filters.pop(column, None) is not None

            def get_last_event_ts(self, column):
                return self.events.get(column)

            def set_last_event_ts(self, column, timestamp):
                self.events[column] = timestamp

        source = pd.DataFrame({
            "status": ["Active", "Active", "Closed"],
            "customer_id": [101, 202, 303],
            "balance": [10, 20, 30],
        })
        display = source.groupby("status", as_index=False)["balance"].sum()
        enriched = attach_filter_values(
            display, source, filter_column="customer_id", match_columns=["status"],
        )
        active_value = enriched.loc[enriched["status"] == "Active", FILTER_VALUE_KEY].iloc[0]
        self.assertEqual(active_value, [101, 202])

        context = type("Context", (), {"state": State()})()
        applied = apply_click_filter(
            df=source,
            context=context,
            column="customer_id",
            event_column="status",
            event_data={
                "name": "Active",
                "data": {FILTER_VALUE_KEY: active_value},
                "componentType": "series",
                "ts": 1,
            },
        )
        self.assertTrue(applied)
        self.assertEqual(context.state.active_filters["customer_id"], [101, 202])
        self.assertEqual(len(apply_filters(source, context.state.active_filters)), 2)

    def test_chart_payload_filters_a_scatter_point_by_its_real_identifier(self) -> None:
        class State:
            active_filters = {}

            def update_filter(self, column, value, rerun=True):
                self.active_filters[column] = value
                return True

            def remove_filter(self, column, rerun=True):
                return self.active_filters.pop(column, None) is not None

            def get_last_event_ts(self, column):
                return None

            def set_last_event_ts(self, column, timestamp):
                pass

        context = type("Context", (), {"state": State()})()
        source = pd.DataFrame({"customer_id": [42, 84], "status": ["Active", "Active"]})
        applied = apply_click_filter(
            df=source,
            context=context,
            column="customer_id",
            event_column="status",
            event_data={
                "data": {FILTER_VALUE_KEY: 42}, "componentType": "series", "ts": 1,
            },
        )
        self.assertTrue(applied)
        self.assertEqual(context.state.active_filters["customer_id"], 42)

    def test_date_click_expands_month_labels_to_a_date_range(self) -> None:
        class State:
            active_filters = {}

            def update_filter(self, column, value, rerun=True):
                self.active_filters[column] = value
                return True

            def remove_filter(self, column, rerun=True):
                return self.active_filters.pop(column, None) is not None

            def get_last_event_ts(self, column):
                return None

            def set_last_event_ts(self, column, timestamp):
                pass

        context = type("Context", (), {"state": State()})()
        frame = pd.DataFrame({"opened": pd.to_datetime(["2026-02-03", "2026-03-01"])})
        applied = apply_click_filter(
            df=frame,
            context=context,
            column="opened",
            event_data={"name": "2026-02", "componentType": "series", "ts": 1},
            click_type="date_click",
        )
        self.assertTrue(applied)
        self.assertEqual(context.state.active_filters["opened"], [pd.Timestamp("2026-02-01").date(), pd.Timestamp("2026-02-28").date()])

    def test_auth_hash_tokens_lockout_and_captcha_contracts(self) -> None:
        stored_hash = hash_password("password-segura", salt=b"0123456789abcdef")
        self.assertTrue(verify_password("password-segura", stored_hash))
        self.assertFalse(verify_password("senha-incorreta", stored_hash))

        os.environ["TEST_AUTH_SECRET"] = "secret-for-tests"
        token = issue_token(username="admin", app_id="bankai", secret_env="TEST_AUTH_SECRET", lifetime_days=1)
        self.assertEqual(verify_token(token, app_id="bankai", secret_env="TEST_AUTH_SECRET")["sub"], "admin")
        self.assertIsNone(verify_token(token, app_id="athena", secret_env="TEST_AUTH_SECRET"))

        lockout = AttemptLockout()
        self.assertEqual(lockout.record_failure("admin", max_attempts=2, lockout_seconds=60), 0)
        self.assertEqual(lockout.failure_count("admin"), 1)
        self.assertEqual(lockout.record_failure("admin", max_attempts=2, lockout_seconds=60), 60)
        self.assertGreater(lockout.is_locked("admin"), 0)
        self.assertEqual(lockout.failure_count("admin"), 0)
        self.assertEqual(MathCaptcha(7, 3, "-").answer, 4)

    def test_sql_identifiers_reject_injection_syntax(self) -> None:
        _validate_identifier("app_users")
        with self.assertRaises(ValueError):
            _validate_identifier("app_users; DROP TABLE app_users")

    def test_registry_accepts_a_reloaded_application_definition_contract(self) -> None:
        """O hot-reload mantém o contrato mesmo quando a identidade da classe muda."""
        ReloadedDefinition = type(
            "ApplicationDefinition",
            (),
            {"__module__": ApplicationDefinition.__module__},
        )
        reloaded = ReloadedDefinition()
        reloaded.app_id = "example"
        reloaded.title = "Example"
        reloaded.initial_route = "home"
        reloaded.default_mode = "light"
        reloaded.render = lambda context: None
        reloaded.load_theme = lambda mode: {}
        reloaded.state_factory = lambda app_id: object()
        reloaded.auth = AuthConfig()

        self.assertTrue(ApplicationRegistry._is_application_definition(reloaded))
        self.assertFalse(ApplicationRegistry._is_application_definition(object()))


if __name__ == "__main__":
    unittest.main()
