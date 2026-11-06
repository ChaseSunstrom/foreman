"""T-3252: perf_bench.py records what a CLI call costs and how test runs share the machine, as one JSON line."""
import json
import os
import subprocess
import sys
import unittest

from helpers import ForemanTestCase

HERE = os.path.dirname(os.path.abspath(__file__))


class Bench(ForemanTestCase):
    def test_a_quick_bench_writes_one_row_with_every_number(self):
        out = os.path.join(self.tmp, "bench.jsonl")
        got = subprocess.run([sys.executable, os.path.join(HERE, "perf_bench.py"), "--runners", "2", "--calls", "1",
                              "--modules", "test_guard_debris", "--note", "quick", "--out", out],
                             capture_output=True, text=True, timeout=600)
        self.assertEqual(got.returncode, 0, got.stdout[-2000:] + got.stderr[-2000:])
        with open(out, encoding="utf-8") as f:
            rows = [json.loads(line) for line in f]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        for key in ("at", "cpus", "load_start", "alone_s", "together_s", "load_peak", "runners", "green"):
            self.assertIn(key, row)
        self.assertEqual((row["runners"], row["note"], row["green"]), (2, "quick", True))
        self.assertIn("python", row["cli_ms"])
        self.assertIn("task show", row["cli_ms"])
        self.assertGreater(row["cli_ms"]["task show"], 0)


if __name__ == "__main__":
    unittest.main()
