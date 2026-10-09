"""Observability, replay and trust (T-0674): fm explain (T-0464), fm task show --story (T-0483) and
fm recall --ask (T-0484), all read from the logs Foreman already keeps."""
import json
import os
import re
import time

from helpers import ForemanTestCase

import fmcore as c


class TrustCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def new(self, title, tier="S", focus=False):
        tid = json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", tier, "--ac", "works :: true",
                                 "--step", "do it", "--json").stdout)["id"]
        if tier != "S":
            for sec in ("Interpretation", "Approach (options → choice → why)"):
                self.fm("task", "set", tid, "--section", sec, "--text", f"{title}: planned")
        if focus:
            self.fm("focus", tid)
        return tid

    def finish(self, tid, lesson=None):
        self.fm("focus", tid)
        self.fm("task", "step", tid, "done", "1", "--evidence", "pytest -k login", "1 passed")
        self.fm("task", "ac", tid, "check", "1", "--evidence", "true", "ok")
        for lens in ("self", "intent", "edge"):
            self.fm("task", "audit", tid, lens, f"{lens} read", "ok")
        self.fm("task", "set", tid, "--section", "Docs impact", "--text", "none: test")
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
        return self.fm("task", "done", tid, *(["--lesson", lesson] if lesson else []), check=False)

    def project(self):
        return c.find_project(self.repo)

    def ledger_add(self, path, **rec):
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(dict({"ts": c.now(), "session_id": None, "project": self.project().slug}, **rec)) + "\n")


class ExplainBlock(TrustCase):
    def test_a_guard_block_is_explained_with_its_rule_inputs_and_ledger(self):
        tid = self.new("Ship the release", focus=True)
        p = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "npm publish --tag next"}})
        self.assertEqual(p.returncode, 2)
        out = self.fm("explain").stdout
        self.assertIn("guard block", out.lower())
        self.assertRegex(out, r"publish:[a-z-]+")  # the rule that fired
        self.assertIn("npm publish --tag next", out)  # its input: the command as the guard saw it
        self.assertIn(f"fm task set {tid} --allow publish", out)  # the rule in the guard's own words
        self.assertIn(f"focus {tid}", out)  # the ledger events behind it
        self.assertIn("no grant", out.lower())
        data = self.fm_json("explain", "block")
        self.assertEqual(data["kind"], "block")
        self.assertEqual(data["task"], tid)
        self.assertTrue(data["rule"].startswith("publish:"))
        self.assertIn("npm publish", data["inputs"]["command"])
        self.assertTrue(any(e["event"] == "focus" for e in data["ledger"]))

    def test_a_drive_decision_is_explained_with_its_settings_and_breaker(self):
        tid = self.new("Fix login", focus=True)
        self.fm("drive", "on")
        p = self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Continuing with the fix next.",
                               "session_id": "sess-1"})
        self.assertIn(f"Foreman drive: {tid}", json.loads(p.stdout)["reason"])
        # another project's later drive record with the same task id is not this project's decision
        with open(os.path.join(self.home, "state", "events.jsonl"), "a") as f:
            f.write(json.dumps({"ts": c.now(), "kind": "drive_wait", "session_id": "other", "project": "elsewhere-1",
                                "task": tid, "running": ["b1"]}) + "\n")
        br = os.path.join(self.home, "state", "logs", "breaker.json")
        os.makedirs(os.path.dirname(br), exist_ok=True)
        with open(br, "w") as f:
            json.dump({"Stop": {"fails": 3, "until": time.time() + 600}}, f)
        out = self.fm("explain", "drive").stdout
        self.assertIn("drive", out.lower())
        self.assertIn(tid, out)
        self.assertIn("work remains", out)  # the rule behind a plain continuation
        self.assertNotIn("drive_wait", out)
        self.assertIn("drive on", out)  # the setting it read, from the ledger
        self.assertIn("Stop paused until", out)  # the hook breaker
        data = self.fm_json("explain")
        self.assertEqual((data["kind"], data["decision"]), ("drive", "drive"))
        self.assertEqual(data["inputs"]["task"], tid)

    def test_a_stop_evidence_gate_is_a_drive_decision_too(self):
        tid = self.new("Fix login", focus=True)
        self.fm("drive", "off")
        self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "All done, the fix is implemented.",
                           "session_id": "sess-1"})
        out = self.fm("explain", "drive").stdout
        self.assertIn("stop_gate", out)
        self.assertIn("no evidence", out)
        self.assertIn(tid, out)

    def test_nothing_on_record_says_so(self):
        self.assertIn("Nothing to explain", self.fm("explain").stdout)


class StoryView(TrustCase):
    def test_a_finished_task_reads_as_chapters_with_times(self):
        tid = self.new("Fix login timeout", tier="M")
        self.fm("task", "log", tid, "the token refresh was the slow part")
        self.finish(tid, lesson="retry the refresh with backoff")
        out = self.fm("task", "show", tid, "--story").stdout
        heads = [h for h in ("Plan", "Steps", "Evidence", "Reviews", "Close") if re.search(rf"(?m)^{h}\b", out)]
        self.assertEqual(heads, ["Plan", "Steps", "Evidence", "Reviews", "Close"], out)
        self.assertLess(out.index("Plan"), out.index("Steps"))
        self.assertLess(out.index("Reviews"), out.index("Close"))
        self.assertRegex(out, r"\d\d:\d\d")
        self.assertIn("pytest -k login", out)  # evidence
        self.assertIn("edge", out)  # a review lens
        self.assertIn("token refresh", out)  # a note
        self.assertIn("Fix login timeout", out.splitlines()[0])

    def test_edits_are_one_line_and_archived_months_count(self):
        tid = self.new("Fix login", focus=True)
        p = self.project()
        for f in ("a.py", "a.py", "b.py"):
            self.ledger_add(os.path.join(p.dir, "ledger.jsonl"), task=tid, event="touched",
                            data={"file": os.path.join(self.repo, f), "tool": "Edit"})
        os.makedirs(os.path.join(p.dir, "archive"), exist_ok=True)
        self.ledger_add(os.path.join(p.dir, "archive", f"ledger-{c.now()[:7]}.jsonl"), task=tid, event="note",
                        data={"text": "from the rolled ledger"})
        out = self.fm("task", "show", tid, "--story").stdout
        self.assertIn("edited 2 file(s)", out)
        self.assertEqual(out.count("touched"), 0, out)
        self.assertIn("from the rolled ledger", out)

    def test_json_story_has_chapters_and_events(self):
        tid = self.new("Fix login", focus=True)
        data = self.fm_json("task", "show", tid, "--story")
        self.assertEqual(data["id"], tid)
        names = [ch["name"] for ch in data["chapters"]]
        self.assertIn("Plan", names)
        plan = data["chapters"][names.index("Plan")]
        self.assertTrue(plan["events"] and all(e["ts"] for e in plan["events"]))
        self.assertIn("task_new", [e["event"] for e in plan["events"]])


class AskMemory(TrustCase):
    def setUp(self):
        super().setUp()
        self.login = self.new("Fix login timeout on slow wifi", tier="M")
        self.finish(self.login, lesson="the timeout was in session renewal; retry the token refresh with backoff")
        self.export = self.new("Export the report as CSV")
        self.fm("task", "log", self.export, "the flaky export check came from the UTC offset in the fixture")
        self.fm("decide", "Report exports use UTF-8 with a BOM", "--why", "spreadsheet apps misread plain UTF-8")
        self.fm("research", "add", "csv-notes",
                input=f"# CSV\nThe spreadsheet import quirks were measured in {self.export}.\n\nUnrelated paragraph.\n")

    def test_an_answer_cites_the_task_behind_a_ledger_note(self):
        out = self.fm("recall", "--ask", "why was the export flaky?").stdout
        first = next(x for x in out.splitlines() if x.startswith("1."))
        self.assertIn(self.export, first)
        self.assertIn("UTC offset", first)
        self.assertIn("not instructions", out)
        self.assertRegex(out, rf"(?m)^Cited tasks: .*{self.export}")

    def test_a_lesson_answers_how_something_was_fixed(self):
        out = self.fm("recall", "--ask", "how was the login timeout fixed, renewal backoff?").stdout
        first = next(x for x in out.splitlines() if x.startswith("1."))
        self.assertIn(self.login, first)
        self.assertIn("backoff", out)

    def test_decisions_and_research_are_searched_and_cite_task_ids(self):
        data = self.fm_json("recall", "--ask", "spreadsheet BOM for UTF-8 exports")
        labels = " ".join(h["label"] for h in data["hits"])
        self.assertIn("decision", labels)
        self.assertIn("csv-notes", labels)
        research = next(h for h in data["hits"] if "csv-notes" in h["label"] and "spreadsheet" in h["text"])
        self.assertIn(self.export, research["cites"])
        self.assertIn(self.export, data["cited"])

    def test_no_matching_words_says_so(self):
        self.assertIn("Nothing in this project's memory", self.fm("recall", "--ask", "kubernetes helm chart?").stdout)
