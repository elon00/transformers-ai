"""Exercise the actual local telemetry service, including invalid public inputs."""
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("morphic", Path(__file__).resolve().parents[1] / "src/transformers_morphic_service.py")
service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(service)


class MorphicServiceTests(unittest.TestCase):
    def setUp(self):
        self.agent = service.TransformersMorphicAgent()

    def test_real_dispatch_fields_and_quantity(self):
        result = self.agent.transform_and_roll_out("Earth Relay", 500)
        self.assertEqual(result["destination"], "Earth Relay")
        self.assertEqual(result["energon_consumed"], 225.0)
        self.assertRegex(result["allspark_hash"], r"^0x[0-9a-f]{32}$")

    def test_destination_is_trimmed(self):
        self.assertEqual(self.agent.transform_and_roll_out("  Earth  ", 1)["destination"], "Earth")

    def test_bad_quantities_are_rejected_before_telemetry(self):
        for value in (0, -1, 1.5, "1", True, None, 1_000_001, float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.agent.transform_and_roll_out("Earth", value)

    def test_bad_destinations_are_rejected(self):
        for value in ("", " ", None, 123, "Earth\nMoon", "a" * 257):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.agent.transform_and_roll_out(value, 1)

    def test_quantity_bounds_are_accepted(self):
        for value in (1, 1_000_000):
            with self.subTest(value=value):
                self.assertEqual(self.agent.transform_and_roll_out("Earth", value)["energon_consumed"], value * .45)

    def test_rejected_input_does_not_generate_a_dispatch(self):
        with patch.object(service.time, "time", side_effect=AssertionError("telemetry must not run")):
            with self.assertRaises(ValueError):
                self.agent.transform_and_roll_out("Earth", -100)

    def test_custom_commander_and_faction_are_preserved(self):
        result = service.TransformersMorphicAgent("Test Commander", "Test Faction").transform_and_roll_out("Earth", 1)
        self.assertEqual((result["commander"], result["faction"]), ("Test Commander", "Test Faction"))


if __name__ == "__main__":
    unittest.main()
