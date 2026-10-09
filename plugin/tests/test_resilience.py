"""T-0679: resilience, state and simplicity — first versions: a chaos test over the task lifecycle, fm usage --prune,
fm wiring, a doctor check that the views match the briefs, and a mutation script for the guard's checks."""
import datetime
import json
import os
import random
import subprocess
import sys
from unittest import mock

from helpers import PLUGIN, ForemanTestCase, read_text

import fmcli
import fmcore as c


class Chaos(ForemanTestCase):
    def test_random_lifecycles_crashed_at_a_random_write_stay_consistent(self):
        self.fm("init")
        p = c.find_project(self.repo)
        rng, here = random.Random(int(os.environ.get("FOREMAN_CHAOS_SEED", "20261009"))), os.getcwd()  # other seeds: an env var
        os.chdir(self.repo)
        seen = set()
        try:
            for i in range(80):
                ids = [b.id for b in c.load_briefs(p)]
                tid = rng.choice(ids) if ids else None
                argv = rng.choice([
                    ["task", "new", f"t{i}", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s"],
                    ["capture", f"idea {i}"],
                    *([["focus", tid], ["task", "evidence", tid, "--step", "1", "--run", "true"],
                       ["task", "finish", tid, "--run", "true", "--audit", "self check"], ["task", "block", tid, "x"],
                       ["task", "defer", tid, "later"], ["task", "drop", tid, "no"],
                       ["task", "set", tid, "status=planned"]] if tid else [])])
                before = {b.id: b.status for b in c.load_briefs(p)}
                left = [rng.randint(1, 8) if rng.random() < 0.4 else 10 ** 6]
                real = c.write_atomic

                def crashing(path, text):
                    left[0] -= 1
                    if left[0] <= 0:
                        raise OSError("chaos: the write never happened")
                    return real(path, text)
                with mock.patch.object(c, "write_atomic", crashing), \
                        mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                    try:
                        fmcli.main(argv)
                    except BaseException:
                        pass
                after = {b.id: b.status for b in c.load_briefs(p)}  # always loads
                for t, st in after.items():
                    if t in before and before[t] != st:
                        seen.add((before[t], st))
                        self.assertIn(st, c.TRANSITIONS[before[t]], f"{t}: {before[t]} → {st} via {argv}")
        finally:
            os.chdir(here)
        c.regen_views(p)
        self.assertTrue(seen, "the run changed some statuses")


class Prune(ForemanTestCase):
    def test_commands_never_run_are_listed_as_trim_candidates(self):
        self.fm("init")
        slug = c.find_project(self.repo).slug
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a") as f:
            f.write(json.dumps({"ts": ts, "kind": "tool", "tool": "Bash", "target": "fm queue", "project": slug}) + "\n")
        before = sorted(os.listdir(os.path.join(PLUGIN, "lib")))
        out = self.fm("usage", "--prune").stdout
        self.assertIn("orders", out)
        self.assertNotIn(" queue,", out.split("Not run")[1] if "Not run" in out else out)
        self.assertIn("fm capture", out)
        self.assertIn("CLEAN", out)
        self.assertEqual(sorted(os.listdir(os.path.join(PLUGIN, "lib"))), before, "nothing is deleted")


class Wiring(ForemanTestCase):
    def test_one_screen_of_what_is_wired(self):
        self.fm("init")
        self.fm("autonomy", "full")
        out = self.fm("wiring").stdout
        for want in ("version", "hooks", "PreToolUse", "autonomy full", "drive", "standing", "trust", "pause", "budget"):
            self.assertIn(want, out, want)


class ViewsRepair(ForemanTestCase):
    def test_doctor_sees_stale_views_and_repair_regenerates_them(self):
        self.fm("init")
        self.fm("task", "new", "One", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        p = c.find_project(self.repo)
        line = os.path.join(p.dir, "state.line")
        with open(line, "w") as f:
            f.write("garbage\n")
        self.assertIn("views", self.fm("doctor", check=False).stdout)
        self.fm("doctor", "--repair", check=False)
        self.assertNotEqual(read_text(line), "garbage\n")
        self.assertNotIn("views don't match", self.fm("doctor", check=False).stdout)


class Mutation(ForemanTestCase):
    SCRIPT = os.path.join(PLUGIN, "tests", "mutate_guard.py")

    def test_mutants_are_listed_and_one_is_judged(self):
        listed = subprocess.run([sys.executable, self.SCRIPT, "--list", "--max", "5"], capture_output=True, text=True)
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertGreaterEqual(len([x for x in listed.stdout.splitlines() if "fmguard.py:" in x]), 1)
        ran = subprocess.run([sys.executable, self.SCRIPT, "--max", "1", "--seed", "3"], capture_output=True, text=True,
                             timeout=600)
        self.assertEqual(ran.returncode, 0, ran.stderr)
        self.assertRegex(ran.stdout, r"(killed|survived)")
