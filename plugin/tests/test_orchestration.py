"""T-0675: orchestration first versions — a handoff packet, host strain, a conflict brief, and a stall watchdog."""
import json
import os
import re
import subprocess
import time

from helpers import ForemanTestCase, read_text
from test_serve import ServeCase

import fmcore as c


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, check=True).stdout


class Packet(ForemanTestCase):
    def test_a_blocked_task_packs_into_one_handoff(self):
        self.fm("init")
        self.fm("task", "new", "Fix the flaky login", "--type", "FIX", "--tier", "S", "--ac",
                "login passes 20 times :: true", "--step", "find the race", "--focus")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "echo flaky once in 5")
        self.fm("task", "hypo", "T-0001", "add", "the token refresh races the redirect", "--probe", "log both timings")
        self.fm("task", "block", "T-0001", "needs the staging key to reproduce")
        out = os.path.join(self.tmp, "packet.md")
        printed = self.fm("task", "packet", "T-0001", "--out", out).stdout
        text = read_text(out)
        for want in ("Fix the flaky login", "login passes 20 times", "find the race", "flaky once in 5",
                     "needs the staging key", "token refresh races the redirect", "Next probe", "log both timings"):
            self.assertIn(want, text, want)
        self.assertIn(out, printed)


class HostHealth(ForemanTestCase):
    def test_a_strained_host_gets_no_new_lane(self):
        self.fm("init")
        self.fm("task", "new", "One", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        r = self.fm("lane", "new", "T-0001", check=False, env={"FOREMAN_HOST": "load=64,cpus=4,mem_mb=4000"})
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("load", r.stderr)
        r = self.fm("lane", "new", "T-0001", check=False, env={"FOREMAN_HOST": "load=1,cpus=4,mem_mb=200"})
        self.assertIn("memory", r.stderr)
        self.fm("lane", "new", "T-0001", env={"FOREMAN_HOST": "load=1,cpus=4,mem_mb=4000"})

    def test_strain_reads_the_real_host(self):
        why = c.host_strain()
        self.assertTrue(why is None or isinstance(why, str))


class ConflictBrief(ForemanTestCase):
    def test_a_conflicting_merge_leaves_a_brief_and_the_way_to_resolve_it(self):
        self.fm("init")
        with open(os.path.join(self.repo, "shared.py"), "w") as f:
            f.write("x = 1\n")
        git(self.repo, "add", "shared.py")
        git(self.repo, "commit", "-qm", "base")
        self.fm("task", "new", "Change x", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        lane = json.loads(self.fm("lane", "new", "T-0001", "--json").stdout)
        with open(os.path.join(lane["path"], "shared.py"), "w") as f:
            f.write("x = 2\n")
        git(lane["path"], "commit", "-qam", "lane change")
        with open(os.path.join(self.repo, "shared.py"), "w") as f:
            f.write("x = 3\n")
        git(self.repo, "commit", "-qam", "main change")
        r = self.fm("lane", "merge", "T-0001", check=False)
        self.assertNotEqual(r.returncode, 0)
        brief = re.search(r"(\S+\.conflict\.md)", r.stderr)
        self.assertTrue(brief, r.stderr)
        text = read_text(brief.group(1))
        self.assertIn("shared.py", text)
        self.assertIn("x = 2", text)
        self.assertIn("x = 3", text)
        self.assertIn("Change x", text)
        self.assertIn(f"git -C {lane['path']} merge", r.stderr + text)
        self.assertEqual(git(self.repo, "status", "--porcelain").strip(), "", "the main checkout is left clean")


class Stall(ServeCase):
    def test_a_session_whose_transcript_stops_moving_is_stopped_and_logged(self):
        self.fm("task", "new", "one", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "fix it")
        self.stub("claude", 'd="$HOME/.claude/projects/$(pwd | sed "s/[^A-Za-z0-9]/-/g")"\nmkdir -p "$d"\n'
                            'echo "{}" > "$d/s.jsonl"\nsleep 30\n')
        t0 = time.monotonic()
        p = self.fm("run", "--max", "1", "--stall", "0.05", check=False, env=self.env())  # 3 s
        self.assertLess(time.monotonic() - t0, 25, "stopped well before the 30 s sleep and the 60 min limit")
        self.assertIn("stalled", p.stdout + p.stderr)
        events = [e for e in c.ledger_tail(c.find_project(self.repo), 50) if e.get("event") == "run_stalled"]
        self.assertTrue(events)

    def test_a_session_it_cant_observe_is_never_stopped_for_stalling(self):
        self.fm("task", "new", "one", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "fix it")
        self.stub("claude", "sleep 4\n")  # writes no transcript: no signal, so no stall
        p = self.fm("run", "--max", "1", "--stall", "0.02", check=False, env=self.env())
        self.assertNotIn("stalled", p.stdout + p.stderr)
