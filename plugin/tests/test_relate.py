"""fm relate (T-0383): dependencies between open tasks inferred, not typed — an id one task mentions, and a tool-less
child's 'T-B -> T-A: why' and 'group: …' lines — stored as inferred_deps and group, honoured by the queue and the
inbox, and undone by --clear. Runs on its own once a day when 3+ open tasks are new."""
import json
import os
import time

from helpers import ForemanTestCase

STUB = r'''#!/usr/bin/env python3
import json, os, sys
stdin = sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": sys.argv[1:], "stdin": stdin}) + "\n")
print(json.dumps({"result": open(os.environ["STUB_REPLY"]).read(), "total_cost_usd": 0.01}))
'''

REPLY = """T-0001 -> T-0004: the export reads what the parser writes
- T-0007 -> T-0006: the timeout fix needs the client
T-0004 -> T-0001: a cycle, dropped
T-0003 -> T-0042: an unknown id, dropped
T-0003 -> T-0003: a self edge, dropped
group: T-0002 T-0005 — the settings page
"""


class _Stubbed(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log, reply = os.path.join(self.tmp, "stub.log"), os.path.join(self.tmp, "reply.txt")
        with open(reply, "w") as f:
            f.write(REPLY)
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log, "STUB_REPLY": reply,
                    "CLAUDE_CONFIG_DIR": os.path.join(self.tmp, "cc")}
        self.fm("init")

    def calls(self):
        if not os.path.exists(self.log):
            return []
        with open(self.log) as f:
            return [json.loads(x) for x in f]

    def inbox(self):
        return [q["id"] for q in json.loads(self.fm("state", "--json").stdout)["inbox"]]

    def queue(self):
        return [q["id"] for q in json.loads(self.fm("queue", "--json").stdout)["order"]]

    def seven(self):
        for title, typ in (("export the report as CSV", "FEATURE"), ("settings page layout", "FEATURE"),
                           ("rename the CLI", "FEATURE"), ("parse the report", "FEATURE"),
                           ("settings page crashes on save", "FIX"), ("add the API client", "FEATURE"),
                           ("the API client times out", "FIX")):
            self.fm("capture", title, "--type", typ, "--tier", "M", "--source", "user")
        for tid in ("T-0006", "T-0007"):
            self.fm("task", "set", tid, "status=planned")


class Mentions(_Stubbed):
    def test_an_id_one_task_mentions_goes_first(self):
        self.fm("capture", "export the report as CSV, reading what T-0003 parses", "--tier", "M")
        self.fm("capture", "rename the CLI", "--tier", "M")
        self.fm("capture", "parse the report", "--tier", "M")
        self.assertEqual(self.inbox(), ["T-0001", "T-0002", "T-0003"])
        self.fm("relate", "--no-child", env=self.env)
        self.assertEqual(self.inbox(), ["T-0003", "T-0001", "T-0002"])
        self.assertIn("inferred_deps: [T-0003]", self.fm("task", "show", "T-0001").stdout)
        self.assertEqual(self.calls(), [])  # mentions are free: no child


class Child(_Stubbed):
    def test_child_edges_and_groups_reorder_the_queue_and_inbox(self):
        self.seven()
        self.assertEqual(self.inbox(), ["T-0005", "T-0001", "T-0002", "T-0003", "T-0004"])
        self.assertEqual(self.queue(), ["T-0007", "T-0006"])
        out = self.fm("relate", env=self.env).stdout
        self.assertIn("2 edge", out)
        self.assertEqual(self.inbox(), ["T-0005", "T-0002", "T-0004", "T-0001", "T-0003"])  # a group stays together
        self.assertEqual(self.queue(), ["T-0006", "T-0007"])
        call = self.calls()[0]
        self.assertIn("--tools", call["args"])  # tool-less
        self.assertIn("T-0004 [FEATURE M] Parse the report", call["stdin"])
        self.assertIn("the timeout fix needs the client", self.fm("queue").stdout)  # the reason, shown
        self.assertIn("inferred_deps: [T-0004]", self.fm("task", "show", "T-0001").stdout)
        for tid in ("T-0003", "T-0004"):  # unknown id, self edge and cycle dropped
            self.assertNotIn("inferred_deps", self.fm("task", "show", tid).stdout)
        self.assertIn("group: the settings page", self.fm("task", "show", "T-0005").stdout)

    def test_clear_undoes_it(self):
        self.seven()
        self.fm("relate", env=self.env)
        self.fm("relate", "--clear", env=self.env)
        self.assertEqual(self.inbox(), ["T-0005", "T-0001", "T-0002", "T-0003", "T-0004"])
        self.assertEqual(self.queue(), ["T-0007", "T-0006"])
        for tid in ("T-0001", "T-0005", "T-0007"):
            brief = self.fm("task", "show", tid).stdout
            self.assertNotIn("inferred_", brief)
            self.assertNotIn("group:", brief)

    def test_a_sensitive_project_keeps_its_words_out_of_any_child(self):
        self.seven()
        self.fm("sensitive", "on")
        self.fm("relate", env=self.env)
        self.assertEqual(self.calls(), [])


class Due(_Stubbed):
    def test_once_a_day_and_only_with_three_new_open_tasks(self):
        self.fm("capture", "one", "--tier", "M")
        self.fm("capture", "two", "--tier", "M")
        self.assertIn("not due", self.fm("relate", "--if-due", env=self.env).stdout)
        self.fm("capture", "three", "--tier", "M")
        self.fm("relate", "--if-due", env=self.env)
        self.assertEqual(len(self.calls()), 1)
        for t in ("four", "five", "six"):
            self.fm("capture", t, "--tier", "M")
        self.assertIn("not due", self.fm("relate", "--if-due", env=self.env).stdout)  # once a day
        self.assertEqual(len(self.calls()), 1)
        import fmcore as c
        import fmrelate
        meta = c.read_meta(c.find_project(self.repo))
        self.assertFalse(fmrelate.due(meta, ["T-0004", "T-0005", "T-0006"]))  # ran today
        meta["relate_day"] = "2000-01-01"
        self.assertTrue(fmrelate.due(meta, ["T-0004", "T-0005", "T-0006"]))  # tomorrow: three new
        self.assertFalse(fmrelate.due(meta, ["T-0001", "T-0005", "T-0006"]))  # T-0001 was seen

    def wait_for_run(self):
        for _ in range(100):  # detached: the command returned before the run did
            if self.calls() and "inferred_deps" in self.fm("task", "show", "T-0001").stdout:
                return
            time.sleep(0.1)
        self.fail("no background fm relate ran")

    def test_session_start_runs_it_in_the_background(self):
        self.seven()
        self.hook("SessionStart", {"source": "startup", "session_id": "new-session"},
                  env=dict(self.env, FOREMAN_NO_BACKGROUND=""))
        self.wait_for_run()

    def test_an_intake_of_three_runs_it_in_the_background(self):
        self.fm("intake", input="FEATURE: export the report as CSV\nFEATURE: settings page layout\n"
                                "FEATURE: rename the CLI\nFEATURE: parse the report\n",
                env=dict(self.env, FOREMAN_NO_BACKGROUND=""))
        self.wait_for_run()
