"""T-2653: every nonzero exit from fmcli.main prints exactly one runnable `Next:` line and keeps its exit code."""
import argparse
import contextlib
import io
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import fmcli
import fmcore as c


def run_raising(exc):
    def boom(args):
        raise exc

    fake = mock.Mock()
    fake.parse_args.return_value = argparse.Namespace(cmd="x", fn=boom)
    err = io.StringIO()
    with mock.patch.object(fmcli, "_parser_for", return_value=fake), \
            mock.patch.object(fmcli, "_task_shape", side_effect=lambda p, a: a), \
            mock.patch.object(fmcli, "_options_first", side_effect=lambda p, a: a), \
            mock.patch.object(fmcli, "_sync_in"), \
            mock.patch.dict(os.environ, {"FOREMAN_WORKER_OF": ""}), \
            contextlib.redirect_stderr(err):
        rc = fmcli.main(["x"])
    return rc, err.getvalue()


class ExitNext(unittest.TestCase):
    def check(self, exc, code):
        rc, err = run_raising(exc)
        self.assertEqual(rc, code)
        nexts = [l for l in err.splitlines() if l.startswith("Next: ")]
        self.assertEqual(len(nexts), 1, err)
        self.assertRegex(nexts[0], r"^Next: (fm |retry)")

    def test_policy(self):
        self.check(c.PolicyError("no"), 2)

    def test_lock(self):
        self.check(c.LockTimeout("busy"), 3)

    def test_corrupt(self):
        self.check(c.CorruptState("bad"), 4)

    def test_value(self):
        self.check(ValueError("x"), 4)

    def test_usage_keeps_its_own(self):
        e = fmcli.UsageError("u")
        e.then = "fm help"
        rc, err = run_raising(e)
        self.assertEqual((rc, err.count("Next:")), (1, 1))


if __name__ == "__main__":
    unittest.main()
