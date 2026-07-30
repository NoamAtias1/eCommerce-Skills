import importlib.util
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).parents[1] / "scripts" / "monitor.py"
SPEC = importlib.util.spec_from_file_location("brand_monitor", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MONITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MONITOR)


class ParseMonitorInputTests(unittest.TestCase):
    def test_parses_documented_json_configuration(self):
        config = MONITOR.parse_monitor_input(
            '{"brand":"YourBrand","competitors":["CompA","CompB"]}',
        )

        self.assertEqual(config.brand, "YourBrand")
        self.assertEqual(config.competitors, ("CompA", "CompB"))
        self.assertEqual(config.lang, "en")

    def test_preserves_plain_brand_input(self):
        config = MONITOR.parse_monitor_input("Your Brand", lang="zh")

        self.assertEqual(config.brand, "Your Brand")
        self.assertEqual(config.competitors, ())
        self.assertEqual(config.lang, "zh")

    def test_rejects_unsupported_json_fields(self):
        with self.assertRaisesRegex(ValueError, "unsupported JSON field.*platforms"):
            MONITOR.parse_monitor_input(
                '{"brand":"YourBrand","platforms":["reddit"]}',
            )

    def test_rejects_invalid_competitor_entries(self):
        with self.assertRaisesRegex(
            ValueError,
            "'competitors' must be a list of non-empty strings",
        ):
            MONITOR.parse_monitor_input(
                '{"brand":"YourBrand","competitors":["CompA",""]}',
            )

    def test_uses_demo_defaults_only_for_demo_mode(self):
        config = MONITOR.parse_monitor_input(None, demo=True)

        self.assertEqual(config.brand, "TechBrand")
        self.assertEqual(config.competitors, ("CompetitorA", "CompetitorB"))
        self.assertEqual(config.lang, "en")


if __name__ == "__main__":
    unittest.main()
