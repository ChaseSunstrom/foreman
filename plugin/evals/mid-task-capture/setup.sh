#!/usr/bin/env bash
# The calculator app, plus step 1 of an in-progress fix: the failing zero-divisor test (uncommitted).
set -euo pipefail
. "$(dirname "$0")/../calc-setup.sh"
cat >> tests/test_calc.py <<'PY'


class DivByZero(unittest.TestCase):
    def test_div_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            calc.div(1, 0)
PY
