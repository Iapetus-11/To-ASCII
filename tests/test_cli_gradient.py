"""Tests for the --gradient option of the toascii CLI."""

import unittest

from click.testing import CliRunner

from toascii import gradients
from toascii.cli import cb_gradient, toascii_command


class GradientOptionTestCase(unittest.TestCase):
    def test_invalid_gradient_rejected(self):
        # An unknown gradient name must be rejected during option parsing
        # (exit code 2) instead of being silently used as the ASCII ramp.
        result = CliRunner().invoke(
            toascii_command,
            [
                "image",
                "x.png",
                "grayscaleconverter",
                "--gradient",
                "bogus",
                "--height",
                "20",
                "--width",
                "40",
            ],
        )
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Invalid value", result.output)

    def test_valid_gradients_map_to_ramps(self):
        self.assertEqual(cb_gradient(None, None, "low"), gradients.LOW)
        self.assertEqual(cb_gradient(None, None, "HIGH"), gradients.HIGH)
        self.assertEqual(cb_gradient(None, None, "oxxo"), gradients.OXXO)


if __name__ == "__main__":
    unittest.main()
