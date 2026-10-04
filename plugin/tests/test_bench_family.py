"""Bench family (T-0280): judged cases for work without tests (T-0231), plugin duels (T-0240), replays on an earlier
Foreman (T-0241), the user's steers as judged cases (T-0242) and a shadow-user soak (T-0243)."""
import json
import os
import shutil
import subprocess

from helpers import ForemanTestCase, read_text

import fmcore as c

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
stdin = sys.stdin.read()
system = args[args.index("--append-system-prompt") + 1] if "--append-system-prompt" in args else ""
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin, "system": system}) + "\n")
if "--plugin-dir" in args:  # a replayed session
    if os.environ.get("STUB_PLANT"):  # a session that leaves git config for whoever runs git here next
        import subprocess
        subprocess.run(["git", "config", "core.fsmonitor", "touch " + os.environ["STUB_PLANT"]])
        subprocess.run(["git", "config", "core.hooksPath", os.path.dirname(os.environ["STUB_PLANT"])])
    if os.environ.get("STUB_FAIL"):
        print(json.dumps({"type": "result", "is_error": True, "total_cost_usd": 0.1, "result": "crashed"}))
        sys.exit(1)
    if os.environ.get("STUB_DOCS"):
        with open("README.md", "a") as f:
            f.write("\nUsage: run calc.\n")
    cost = float(os.environ.get("STUB_COST_WITH_RIVAL", 0.4)) if args.count("--plugin-dir") > 1 else 0.4
    sid = None if os.environ.get("STUB_NO_SID") else "s-1"
    print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": cost, "num_turns": 5, "session_id": sid,
                      "result": "Done. Run `make` yourself to finish."}))
elif "You play the user" in system:
    print(json.dumps({"result": "REPEAT: I said never hand me commands to run\nNEXT: run make yourself please",
                      "total_cost_usd": 0.01}))
else:  # the judge
    score = os.environ.get("STUB_SCORE", "4")
    print(json.dumps({"result": f"SCORE: {score}\n- the usage section is clear\n- one example is missing",
                      "total_cost_usd": 0.01}))
'''


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, check=True).stdout.strip()


class _Bench(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.fm("init")
        self.write("calc.py", "def double(x):\n    return x + x + 1\n")
        self.write("README.md", "# calc\n")
        git(self.repo, "add", "calc.py", "README.md")
        git(self.repo, "commit", "-qm", "calc")
        self.calc = self.finished("double() is off by one", "PYTHONPATH=. python3 tests/test_calc.py")
        self.write("calc.py", "def double(x):\n    return x * 2\n")
        self.write("tests/test_calc.py", "from calc import double\nassert double(3) == 6, double(3)\nprint('ok')\n")
        git(self.repo, "add", "-A", "calc.py", "tests")
        git(self.repo, "commit", "-qm", f"double() is right ({self.calc})")
        self.docs = self.finished("Document how to run calc", None, steer="never hand the user commands to run")
        self.write("README.md", "# calc\n\nUsage: python3 -c 'from calc import double'\n")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-qm", f"calc usage ({self.docs})")

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def finished(self, title, verify, steer=None):
        ac = ["--ac", f"fixed :: {verify}"] if verify else ["--ac", "the README says how to run calc"]
        tid = json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", *ac, "--step", "do it",
                                 "--json").stdout)["id"]
        self.fm("task", "set", tid, "--section", "Raw request", "--text", f"> {title}")
        self.fm("focus", tid)
        if steer:
            self.fm("task", "log", tid, f"steer: {steer}")
        self.fm("task", "step", tid, "done", "1", "--evidence", "x", "ok")
        self.fm("task", "ac", tid, "check", "1", "--evidence", "x", "ok")
        self.fm("task", "audit", tid, "self", "x", "ok")
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
        self.fm("task", "done", tid)
        return tid

    def calls(self):
        return [json.loads(x) for x in read_text(self.log).splitlines()]

    def sessions(self):
        return [x for x in self.calls() if "--plugin-dir" in x["args"]]


class Judged(_Bench):
    def test_a_docs_only_task_is_judged(self):
        built = json.loads(self.fm("bench", "build", "--judged", "--json", env=self.env).stdout)
        case = next(x for x in built["cases"] if x["id"] == self.docs)
        self.assertTrue(case["judge"])
        self.assertIn("the README says how to run calc", " ".join(case["rubric"]))
        self.assertIn(self.calc, [x["id"] for x in built["cases"]])  # tested work stays a tested case
        res = json.loads(self.fm("bench", "run", "--ids", self.docs, "--label", "j", "--json",
                                 env=dict(self.env, STUB_DOCS="1")).stdout)
        got = res["cases"][0]
        self.assertEqual((got["score"], got["pass"]), (4, True))
        judge = [x for x in self.calls() if "--plugin-dir" not in x["args"]][-1]
        self.assertIn("Usage: run calc", judge["stdin"])  # the replay's own change is what's judged
        self.assertIn("Run `make` yourself", judge["stdin"])  # and its final reply
        self.assertIn("never hand the user commands", judge["stdin"])  # the user's taste is in the rubric
        shown = self.fm("bench", "show", "j", env=self.env).stdout
        self.assertIn("score 4/5", shown)
        self.assertIn("judge: the usage section is clear", shown)
        self.assertEqual(json.loads(self.fm("ui", "--json").stdout)["bench"]["last"]["score"], 4.0)
        low = json.loads(self.fm("bench", "run", "--ids", self.docs, "--label", "low", "--json",
                                 env=dict(self.env, STUB_SCORE="2"), check=False).stdout)
        self.assertEqual((low["cases"][0]["score"], low["cases"][0]["pass"]), (2, False))  # below 4 fails

    def test_without_judged_a_docs_task_is_skipped(self):
        built = json.loads(self.fm("bench", "build", "--json", env=self.env).stdout)
        self.assertNotIn(self.docs, [x["id"] for x in built["cases"]])
        self.fm("bench", "build", "--judged", env=self.env)
        again = json.loads(self.fm("bench", "build", "--json", env=self.env).stdout)  # review: a plain rebuild keeps them
        self.assertIn(self.docs, [x["id"] for x in again["cases"]])

    def test_git_config_a_session_leaves_runs_nothing(self):
        # review: the judge's git add/diff ran in the worktree a bypass-mode session had configured
        self.fm("bench", "build", "--judged", env=self.env)
        marker = os.path.join(self.tmp, "planted", "ran")
        os.makedirs(os.path.dirname(marker))
        for hook in ("pre-commit", "post-checkout", "fsmonitor-watchman"):
            with open(os.path.join(self.tmp, "planted", hook), "w") as f:
                f.write(f"#!/bin/sh\ntouch {marker}\n")
            os.chmod(os.path.join(self.tmp, "planted", hook), 0o755)
        try:
            self.fm("bench", "run", "--ids", self.docs, "--label", "p", env=dict(self.env, STUB_PLANT=marker), check=False)
            self.fm("bench", "run", "--ids", self.calc, "--label", "q", env=dict(self.env, STUB_PLANT=marker), check=False)
        finally:
            git(self.repo, "config", "--unset", "core.fsmonitor")
            git(self.repo, "config", "--unset", "core.hooksPath")
        self.assertFalse(os.path.exists(marker))

    def test_the_change_is_fenced_and_a_failed_session_isnt_judged(self):
        self.fm("bench", "build", "--judged", env=self.env)
        self.fm("bench", "run", "--ids", self.docs, "--label", "j", env=dict(self.env, STUB_DOCS="1"))
        judge = [x for x in self.calls() if "--plugin-dir" not in x["args"]][-1]
        self.assertIn("<diff>", judge["stdin"])
        self.assertIn("</reply>", judge["stdin"])
        n = len(self.calls())
        res = json.loads(self.fm("bench", "run", "--ids", self.docs, "--label", "k", "--json",
                                 env=dict(self.env, STUB_FAIL="1"), check=False).stdout)
        self.assertFalse(res["cases"][0]["pass"])
        self.assertEqual(len(self.calls()), n + 1)  # the session only: no judge paid for a crashed run


class Duel(_Bench):
    def setUp(self):
        super().setUp()
        rival = os.path.join(self.tmp, "rival")  # T-0294: a duel's rival must be an installed plugin
        cc = os.path.join(self.tmp, "cc")
        os.makedirs(os.path.join(cc, "plugins"))
        with open(os.path.join(cc, "plugins", "installed_plugins.json"), "w") as f:
            json.dump({"version": 2, "plugins": {"rival@m": [{"scope": "user", "installPath": rival}]}}, f)
        self.env = dict(self.env, CLAUDE_CONFIG_DIR=cc)

    def test_both_arms_and_the_gate(self):
        self.fm("bench", "build", env=self.env)
        rival = os.path.join(self.tmp, "rival")
        os.makedirs(os.path.join(rival, ".claude-plugin"))
        with open(os.path.join(rival, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "rival"}')
        res = json.loads(self.fm("bench", "duel", rival, "--json", env=self.env).stdout)
        dirs = [[a[i + 1] for i, x in enumerate(a) if x == "--plugin-dir"] for a in (s["args"] for s in self.sessions())]
        self.assertEqual(dirs, [[c.PLUGIN_ROOT], [c.PLUGIN_ROOT, rival]])
        self.assertTrue(res["gate"]["lines"][0].startswith(res["without"]))
        for label in (res["without"], res["with"]):
            self.assertTrue(os.path.exists(os.path.join(c.find_project(self.repo).dir, "bench", "results",
                                                        label + ".json")))
        with_ = json.loads(read_text(os.path.join(c.find_project(self.repo).dir, "bench", "results",
                                                  res["with"] + ".json")))
        self.assertEqual(with_["extra"], [rival])  # the results say what ran beside Foreman
        self.assertIn("no difference", self.fm("bench", "duel", rival, env=self.env).stdout)
        view = json.loads(self.fm("ui", "--json").stdout)
        self.assertIn("no difference", view["bench"]["verdicts"][0]["verdict"])  # the pane's bench card
        self.assertEqual(view["bench"]["verdicts"][0]["kind"], "duel")

    def test_a_losing_contender_says_why(self):
        self.fm("bench", "build", env=self.env)
        rival = os.path.join(self.tmp, "rival")
        os.makedirs(os.path.join(rival, ".claude-plugin"))
        with open(os.path.join(rival, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "rival"}')
        out = self.fm("bench", "duel", rival, "--json", env=dict(self.env, STUB_COST_WITH_RIVAL="2.0")).stdout
        self.assertIn("rival hurts here: cost per case up 400%", json.loads(out)["verdict"])

    def test_a_folder_that_is_not_a_plugin_is_refused(self):
        self.fm("bench", "build", env=self.env)
        p = self.fm("bench", "duel", self.tmp, env=self.env, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(os.path.exists(self.log))


class Versions(_Bench):
    def test_an_earlier_foreman_and_this_one(self):
        self.fm("bench", "build", env=self.env)
        src = os.path.join(self.tmp, "src")
        shutil.copytree(c.PLUGIN_ROOT, os.path.join(src, "plugin"),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tests", "evals"))
        git(self.tmp, "init", "-q", src)
        git(src, "add", "-A")
        git(src, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "old foreman")
        rev = git(src, "rev-parse", "HEAD")
        res = json.loads(self.fm("bench", "versions", "HEAD", "--source", src, "--json", env=self.env).stdout)
        old, new = (s["args"][s["args"].index("--plugin-dir") + 1] for s in self.sessions())
        self.assertTrue(old.endswith(os.sep + "plugin") and "fm-bench-" in old, old)
        self.assertEqual(new, c.PLUGIN_ROOT)
        self.assertIn(rev[:10], res["old"])
        self.assertIn("→", res["gate"]["lines"][0])
        self.assertEqual(git(src, "worktree", "list").count("\n"), 0)  # the old version's worktree is gone


class Court(_Bench):
    def test_steers_become_judged_cases(self):
        res = json.loads(self.fm("bench", "court", "--json", env=self.env).stdout)
        case = res["cases"][0]
        self.assertEqual(case["score"], 4)
        cases = json.loads(read_text(os.path.join(c.find_project(self.repo).dir, "bench", "cases.json")))
        court = [x for x in cases if x["id"].startswith("R-")]
        self.assertEqual(len(court), 1)
        self.assertIn("never hand the user commands", court[0]["rubric"][0])
        self.assertEqual(court[0]["prompt"], "Document how to run calc")
        judge = [x for x in self.calls() if "--plugin-dir" not in x["args"]][-1]
        self.assertIn("never hand the user commands", judge["stdin"])


class Soak(_Bench):
    def test_a_two_turn_conversation_with_the_shadow_user(self):
        self.fm("bench", "build", env=self.env)
        res = json.loads(self.fm("bench", "soak", "--ids", self.calc, "--turns", "2", "--json", env=self.env).stdout)
        got = res["cases"][0]
        self.assertIn("never hand me commands", " ".join(got["complaints"]))
        first, second = self.sessions()
        self.assertNotIn("--no-session-persistence", first["args"])  # a conversation needs its session kept
        self.assertEqual(second["args"][second["args"].index("--resume") + 1], "s-1")
        self.assertIn("run make yourself please", " ".join(second["args"]))
        shadow = [x for x in self.calls() if "You play the user" in x["system"]]
        self.assertEqual(len(shadow), 2)
        self.assertIn("never hand the user commands", shadow[0]["stdin"])  # the user's own steers
        self.assertIn("Run `make` yourself", shadow[0]["stdin"])
        self.assertTrue(os.path.exists(res["path"]))
        shown = self.fm("bench", "show", res["label"], env=self.env).stdout
        self.assertIn("had to repeat: I said never hand me commands", shown)
        self.assertEqual(json.loads(self.fm("ui", "--json").stdout)["bench"]["last"]["repeats"], 2)  # once per turn

    def test_a_soak_needs_the_guard_a_session_id_and_sane_numbers(self):
        self.fm("bench", "build", env=self.env)
        bare = os.path.join(self.tmp, "bare")
        os.makedirs(os.path.join(bare, ".claude-plugin"))
        with open(os.path.join(bare, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "bare"}')
        import fmbench
        with self.assertRaises(ValueError):  # refused inside soak_case, whoever calls it
            fmbench.soak_case(c.find_project(self.repo), {"id": "x", "base": "HEAD", "prompt": "x"}, bare)
        self.assertFalse(os.path.exists(self.log))
        for bad in (["--budget", "nan"], ["--max", "0"], ["--turns", "0"]):
            p = self.fm("bench", "soak", *bad, env=self.env, check=False)
            self.assertNotEqual(p.returncode, 0, bad)
        res = json.loads(self.fm("bench", "soak", "--ids", self.calc, "--json", env=dict(self.env, STUB_NO_SID="1")).stdout)
        self.assertIn("session id", res["cases"][0]["error"])
        self.assertFalse(res["cases"][0]["pass"])
