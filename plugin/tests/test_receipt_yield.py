"""T-2655: the drive's receipt adds yield per dollar beside spend, and never divides by zero."""
import unittest

import helpers  # noqa: F401  (puts plugin/lib on the path)
from sampo import contract as con


class ReceiptYield(unittest.TestCase):
    def test_three_tasks_for_a_dollar_fifty(self):
        s = con.yield_text(3, 1.5)
        self.assertIn("$0.50 a task", s)
        self.assertIn("2.0 tasks a dollar", s)

    def test_zero_spend_or_zero_tasks_print_no_ratio(self):
        self.assertEqual(con.yield_text(3, 0), "")
        self.assertEqual(con.yield_text(0, 1.5), "")
        self.assertEqual(con.yield_text(0, 0), "")
        self.assertEqual(con.yield_text(2, None), "")


if __name__ == "__main__":
    unittest.main()
