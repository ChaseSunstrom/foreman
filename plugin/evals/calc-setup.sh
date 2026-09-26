#!/usr/bin/env bash
# Shared scaffold for the behavioural cases: a tiny calculator app with a CLI and tests, committed to git.
set -euo pipefail
cat > calc.py <<'PY'
def add(a, b):
    return a + b


def div(a, b):
    return a / b
PY
cat > cli.py <<'PY'
import argparse

import calc


def main(argv=None):
    ap = argparse.ArgumentParser(prog="calc")
    ap.add_argument("op", choices=["add", "div"])
    ap.add_argument("a", type=float)
    ap.add_argument("b", type=float)
    args = ap.parse_args(argv)
    print(getattr(calc, args.op)(args.a, args.b))


if __name__ == "__main__":
    main()
PY
mkdir -p tests
touch tests/__init__.py  # plain `python -m unittest` discovers the tests
cat > tests/test_calc.py <<'PY'
import unittest

import calc


class Calc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(2, 3), 5)

    def test_div(self):
        self.assertEqual(calc.div(6, 3), 2)
PY
git init -q -b main .
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "calculator app"
