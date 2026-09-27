"""fm ideas: tool-less brainstorm children (claude -p with no tools and no MCP), one per lens, in parallel."""
import json
import os
import time

from helpers import ForemanTestCase, read_text

import fmcore as c

STUB = r'''#!/usr/bin/env python3
import json, os, sys, time
args = sys.argv[1:]
lens = next(l for l in args if l.startswith("Lens: ")).split("\n")[0][6:] if any(a.startswith("Lens: ") for a in args) else "?"
stdin = sys.stdin.read()
lens = next((l for l in stdin.splitlines() if l.startswith("Lens: ")), "Lens: ?")[6:]
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin, "cwd": os.getcwd(), "t": time.time()}) + "\n")
time.sleep(float(os.environ.get("STUB_SLEEP", "0")))
if lens == os.environ.get("STUB_FAIL_LENS"):
    sys.exit(3)
phrases = ["apple banana cherry", "delta echo foxtrot", "golf hotel india", "juliet kilo lima", "mike november oscar"]
vary = " " + phrases[stdin.count(chr(10) + '- ') // 2 % 5] if os.environ.get("STUB_VARY") else ""
print(f"- **Idea for {lens}{vary}** — FEATURE — value 4 — effort S — risk low")
'''


class Ideas(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.pack = os.path.join(self.tmp, "pack.md")
        with open(self.pack, "w") as f:
            f.write("Project: a tiny calculator app.\nUser: super improve it\n")
        self.fm("init")

    def calls(self):
        return [json.loads(l) for l in read_text(self.log).splitlines()]

    def test_super_brainstorm_rounds_build_on_earlier_ideas_until_dry(self):
        # T-0071: each round sees every idea so far and is asked only for new ones; a round with nothing new ends it
        two = ["--lens", "user value", "--lens", "bold bets"]
        res = json.loads(self.fm("ideas", "--pack", self.pack, *two, "--rounds", "4", "--json", env=self.env).stdout)
        self.assertEqual(res["rounds"], 2, "round 2 repeated round 1: dry")
        later = [x for x in self.calls() if "Ideas so far" in x["stdin"]]
        self.assertTrue(later and "Idea for user value" in later[0]["stdin"])
        self.assertIn("Idea for bold bets", read_text(os.path.join(res["dir"], "ideas.md")))
        res = json.loads(self.fm("ideas", "--pack", self.pack, *two, "--rounds", "3", "--dry", "1", "--json",
                                 env=dict(self.env, STUB_VARY="1")).stdout)
        self.assertEqual(res["rounds"], 3)
        self.assertEqual(read_text(os.path.join(res["dir"], "ideas.md")).count("- "), 6)

    def test_one_toolless_child_per_lens_in_parallel(self):
        env = dict(self.env, STUB_SLEEP="1")
        start = time.time()
        res = json.loads(self.fm("ideas", "--pack", self.pack, "--lens", "reliability", "--lens", "bold bets",
                                 "--json", env=env).stdout)
        self.assertLess(time.time() - start, 1.9, "children run concurrently")
        calls = self.calls()
        self.assertEqual(len(calls), 2)
        for call in calls:
            a = call["args"]
            self.assertEqual(a[a.index("--tools") + 1], "")
            self.assertIn("--strict-mcp-config", a)
            self.assertEqual(a[a.index("--setting-sources") + 1], "project,local", "no user plugins/hooks leak in")
            self.assertEqual(json.loads(a[a.index("--mcp-config") + 1]), {"mcpServers": {}})
            self.assertIn("-p", a)
            self.assertIsNone(c.find_project(call["cwd"]), "children run outside any Foreman project")
        self.assertEqual(sorted(r["lens"] for r in res["results"]), ["bold bets", "reliability"])
        for r in res["results"]:
            self.assertIn(f"Idea for {r['lens']}", read_text(r["file"]))
        self.assertIn("super improve it", calls[0]["stdin"], "context pack goes in on stdin (no argv size limit)")
        self.assertNotIn("super improve it", " ".join(calls[0]["args"]))

    def test_missing_claude_is_a_clear_error(self):
        empty = os.path.join(self.tmp, "empty-bin")
        os.makedirs(empty)
        env = dict(self.env, PATH=empty)  # fm itself runs via sys.executable; no `claude` anywhere on PATH
        p = self.fm("ideas", "--pack", self.pack, "--lens", "reliability", env=env, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("claude", p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_lenses_with_the_same_slug_get_separate_files(self):
        res = json.loads(self.fm("ideas", "--pack", self.pack, "--lens", "ünïcode", "--lens", "日本",
                                 "--json", env=self.env).stdout)
        self.assertEqual(len({r["file"] for r in res["results"]}), 2)

    def test_failed_lens_is_reported_and_others_kept(self):
        env = dict(self.env, STUB_FAIL_LENS="performance")
        p = self.fm("ideas", "--pack", self.pack, "--lens", "performance", "--lens", "simplicity", env=env, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("performance", p.stderr)
        out = os.path.join(c.find_project(self.repo).dir, "research")
        files = [f for _, _, fs in os.walk(out) for f in fs]
        self.assertTrue(any("simplicity" in f for f in files))

    def test_default_lenses(self):
        self.fm("ideas", "--pack", self.pack, env=self.env)
        self.assertEqual(len(self.calls()), 4)  # T-0061: four by default
