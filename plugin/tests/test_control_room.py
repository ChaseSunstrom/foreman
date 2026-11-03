"""T-1660: fm settings chords, a probe of which key chords this terminal delivers to fm code."""
import unittest

from helpers import ForemanTestCase


class Chords(ForemanTestCase):
    """T-1660: fm settings keys: each press as fm code's own decoder reads it, so a binding is known to arrive."""

    def test_each_press_is_named_as_tui_toml_names_it(self):
        from sampo import settings
        self.assertEqual(settings.describe_press("\x01"), "ctrl+a")
        self.assertEqual(settings.describe_press("\x1b[15~"), "f5")
        self.assertEqual(settings.describe_press("\x1bOP"), "f1")
        self.assertIn("esc then x", settings.describe_press("\x1bx"))  # alt+x: two keys to fm code
        self.assertIn("not delivered", settings.describe_press("\x1b[1;5C"))  # ctrl+right: a sequence it skips
        self.assertIn("\\x1b[1;5C", settings.describe_press("\x1b[1;5C"))
        self.assertEqual(settings.describe_press("q"), "q")

    def test_the_probe_loop_stops_on_q_and_says_each_press(self):
        from sampo import settings
        chunks = iter(["\x01", "\x1b[15~", "q"])
        lines = []
        settings.key_probe(lambda: next(chunks, None), lines.append)
        self.assertEqual([x for x in lines if x.startswith("  ")], ["  ctrl+a", "  f5"])

    def test_without_a_terminal_it_says_so(self):
        import subprocess
        import sys
        from helpers import FM
        p = subprocess.run([sys.executable, FM, "settings", "chords"], stdin=subprocess.DEVNULL, capture_output=True,
                           text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("terminal", p.stderr)


if __name__ == "__main__":
    unittest.main()
