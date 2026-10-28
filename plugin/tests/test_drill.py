"""T-1669: fm drill runs a scripted day in a temp home with faults planted mid-day (a torn ledger and journal, a stale
lock, a broken lane, a corrupt state file, an unreadable journal) and passes only when every fault is found by fm fsck
or fm verify-ledger, or healed, and nothing crashed. And the fixes its first runs forced: a corrupt or unreadable
state file is named in one line, never a traceback, and an append after a torn tail starts on a line of its own."""
import json
import os
import shutil
import unittest
from unittest import mock

from helpers import ForemanTestCase, read_text

import fmcore as c
import fmdrill


def tree(root):
    return sorted(os.path.relpath(os.path.join(d, n), root) for d, _, ns in os.walk(root) for n in ns)


class Drill(ForemanTestCase):
    def test_a_seed_replays_the_same_plan(self):
        self.assertEqual(fmdrill.plan(7, 3), fmdrill.plan(7, 3))
        plans = {json.dumps(fmdrill.plan(s, 3)) for s in range(8)}
        self.assertGreater(len(plans), 1, "seeds differ")
        kinds = [f["kind"] for f in fmdrill.plan(7, 3)]
        self.assertEqual(len(set(kinds)), 3)
        self.assertTrue(set(kinds) <= set(fmdrill.KINDS))
        with self.assertRaises(ValueError):
            fmdrill.plan(1, 2)

    def test_a_drill_passes_names_its_faults_and_leaves_the_home_alone(self):
        before = tree(self.home)
        p = self.fm("drill", "--seed", "5", "--json", check=False)
        got = json.loads(p.stdout)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertTrue(got["ok"])
        self.assertEqual(got["seed"], 5)
        self.assertEqual(len(got["faults"]), 3)
        for f in got["faults"]:
            self.assertIn(f["verdict"], ("found", "healed", "skipped"), f)
        self.assertEqual(got["crashes"], [])
        self.assertEqual(tree(self.home), before)
        self.assertFalse(os.path.exists(got["home"]), "a passing drill removes its temp home")

    def test_every_kind_at_once_still_passes(self):
        p = self.fm("drill", "--seed", "11", "--faults", "6", check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        for kind in fmdrill.KINDS:
            self.assertIn(kind, p.stdout)
        self.assertIn("fm drill --seed 11 --faults 6", p.stdout, "the replay command")

    def test_a_missed_fault_fails_and_keeps_the_home(self):
        with mock.patch.object(fmdrill, "_verdict", return_value=("missed", "planted, not found")):
            r = fmdrill.drill(5, 3)
        self.addCleanup(shutil.rmtree, r["home"], True)
        self.assertFalse(r["ok"])
        self.assertTrue(os.path.isdir(r["home"]), "a failed drill keeps its home to look at")
        self.assertIn("✗", fmdrill.render(r))
        self.assertIn("FAILED", fmdrill.render(r))

    def test_a_traceback_is_a_crash(self):
        self.assertIsNone(fmdrill.crash("fm status", 4, "", "fm: state looks corrupt: x"))
        self.assertIn("fm status", fmdrill.crash("fm status", 1, "", "Traceback (most recent call last):\n  x\n"))


class StateErrors(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.fm("task", "new", "A thing", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.log = os.path.join(self.home, "state", "logs", "hooks.log")

    def test_only_a_state_file_permission_error_is_a_state_error(self):
        import fmhooks
        self.assertIsNone(fmhooks._state_error(PermissionError(13, "denied", "/etc/shadow")), "not state: the breaker")
        self.assertIn("permission denied", fmhooks._state_error(
            PermissionError(13, "denied", os.path.join(c.state_dir(), "events.jsonl"))))

    def test_a_corrupt_meta_json_is_named_never_a_traceback(self):
        meta = os.path.join(self.p.dir, "meta.json")
        with open(meta, "w") as f:
            f.write('{"cut')
        p = self.fm("status", check=False)
        self.assertEqual(p.returncode, 4, p.stderr)
        self.assertIn(meta, p.stderr)
        self.assertIn("fm fsck", p.stderr)
        self.assertNotIn("Traceback", p.stderr)
        out = self.hook("UserPromptSubmit", {"prompt": "fix the thing"}).stdout
        ctx = json.loads(out)["hookSpecificOutput"]["additionalContext"]
        self.assertIn(meta, ctx)
        self.assertNotIn("Traceback", read_text(self.log))
        self.assertIn("meta.json", read_text(self.log))
        found = json.loads(self.fm("fsck", "--json", check=False).stdout)
        self.assertIn(("corrupt state", meta), [(f["kind"], f["path"]) for f in found["findings"]])

    @unittest.skipIf(os.geteuid() == 0, "root reads any file")
    def test_an_unreadable_ledger_is_named_never_a_traceback(self):
        ledger = os.path.join(self.p.dir, "ledger.jsonl")
        os.chmod(ledger, 0)
        try:
            p = self.fm("task", "log", "T-0001", "x", check=False)
            self.hook("UserPromptSubmit", {"prompt": "fix the thing"})
        finally:
            os.chmod(ledger, 0o644)
        self.assertEqual(p.returncode, 4, p.stderr)
        self.assertIn(ledger, p.stderr)
        self.assertIn("permission denied", p.stderr)
        self.assertNotIn("Traceback", p.stderr)
        self.assertNotIn("Traceback", read_text(self.log) if os.path.exists(self.log) else "")

    def test_an_append_after_a_torn_tail_starts_its_own_line(self):
        events = os.path.join(self.home, "state", "events.jsonl")
        with open(events, "a") as f:
            f.write('{"ev": "cut')
        self.hook("UserPromptSubmit", {"prompt": "fix the thing"})
        lines = read_text(events).splitlines()
        i = lines.index('{"ev": "cut')
        self.assertGreater(len(lines), i + 1)
        for ln in lines[i + 1:]:
            json.loads(ln)
        path = os.path.join(self.tmp, "x.jsonl")
        c.append_line(path, '{"a": 1}\n')
        c.append_line(path, '{"b": 2}\n')
        self.assertEqual(read_text(path), '{"a": 1}\n{"b": 2}\n', "a whole tail gets no blank line")


if __name__ == "__main__":
    unittest.main()
