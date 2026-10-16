"""fm draft (T-1062): the top queued S task drafted by a headless claude in a throwaway worktree branch draft/T-x;
swept when the queue's top (or its brief) changes. Never merges."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c

STUB = r'''#!/usr/bin/env python3
import os
open("drafted.txt", "w").write(os.getcwd())
print('{"type": "result", "is_error": false, "total_cost_usd": 0.1, "result": "ok"}')
'''


class Draft(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"]}

    def branches(self):
        return subprocess.run(["git", "-C", self.repo, "branch", "--list", "draft/*", "--format=%(refname:short)"], capture_output=True,
                              text=True).stdout.split()

    def new(self, title, tier="S"):
        return json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", tier, "--ac", "ok :: true",
                                  "--step", "a", "--json").stdout)["id"]

    def test_nothing_to_draft_without_an_s_task(self):
        self.new("big", "L")
        out = json.loads(self.fm("draft", "--json", env=self.env).stdout)
        self.assertEqual(out["drafted"], None)
        self.assertEqual(self.branches(), [])

    def test_draft_then_stale_sweep(self):
        tid = self.new("small")
        out = json.loads(self.fm("draft", "--json", env=self.env).stdout)
        self.assertEqual(out["drafted"], tid)
        self.assertEqual(self.branches(), [f"draft/{tid}"])
        p = c.find_project(self.repo)
        fp = json.load(open(os.path.join(p.dir, "draft.json")))
        self.assertEqual(fp["task"], tid)
        self.assertTrue(fp["hash"])
        kept = json.loads(self.fm("draft", "--status", "--json").stdout)  # unchanged: kept
        self.assertEqual(kept["swept"], [])
        self.assertEqual(self.branches(), [f"draft/{tid}"])
        with open(next(b.path for b in c.load_briefs(p) if b.id == tid), "a") as f:  # the brief changes
            f.write("\nmore\n")
        swept = json.loads(self.fm("draft", "--status", "--json").stdout)
        self.assertEqual(swept["swept"], [tid])
        self.assertEqual(self.branches(), [])
        self.assertFalse(os.path.exists(os.path.join(p.dir, "draft.json")))

    def test_night_lists_a_draft_job(self):
        d = os.path.join(c.state_dir(), "sessions")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "s.json"), "w") as f:
            json.dump({"rate_limits": {"seven_day": {"used_percentage": 10}}}, f)
        tid = self.new("small")
        names = [j["name"] for j in json.loads(self.fm("night", "--dry-run", "--max-usd", "5", "--json").stdout)["jobs"]]
        self.assertIn(f"draft {tid}", names)
