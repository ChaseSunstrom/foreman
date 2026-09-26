"""Behavioural tests for the fm CLI (run as a subprocess against an isolated FOREMAN_HOME)."""
import json
import os
import threading
import unittest

from helpers import ForemanTestCase

import fmcore as c


class Init(ForemanTestCase):
    def test_init_prints_slug_and_state_is_empty(self):
        slug = self.fm("init").stdout.strip()
        self.assertEqual(slug, c.slug_for(self.repo))
        st = self.fm_json("state")
        self.assertEqual(st["project"], slug)
        self.assertIsNone(st["active"])
        self.assertEqual((st["queue"], st["inbox"]), ([], []))

    def test_commands_auto_register_git_repo(self):
        self.fm("capture", "something")
        self.assertIsNotNone(c.find_project(self.repo))

    def test_project_flag_and_env_select_project_outside_it(self):
        slug = self.fm("init").stdout.strip()
        elsewhere = os.path.join(self.tmp, "elsewhere")
        os.makedirs(elsewhere)
        self.assertEqual(self.fm_json("state", "-p", slug, cwd=elsewhere)["project"], slug)
        self.assertEqual(self.fm_json("state", cwd=elsewhere, env={"FOREMAN_PROJECT": slug})["project"], slug)
        p = self.fm("state", cwd=elsewhere, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("fm init", p.stderr)


class CaptureAndIntake(ForemanTestCase):
    def test_capture_creates_captured_brief_and_inbox_view(self):
        out = self.fm("capture", "export report as CSV", "--type", "FEATURE", "--source", "discovered").stdout
        self.assertIn("T-0001", out)
        b = c.find_brief(c.find_project(self.repo), "T-0001")
        self.assertEqual((b.status, b.type, b.meta["source"]), ("captured", "FEATURE", "discovered"))
        inbox = open(os.path.join(c.find_project(self.repo).dir, "INBOX.md")).read()
        self.assertIn("T-0001", inbox)
        self.assertEqual([i["id"] for i in self.fm_json("state")["inbox"]], ["T-0001"])

    def test_intake_block_creates_briefs_in_canonical_order(self):
        block = ("FEATURE: export CSV @src/reports\nFIX: login timeout\nCLEAN!: dedupe date helpers\n"
                 "PERF?: first paint 4s\nSECURITY: review upload\nCONTEXT: Django app\nDONE-WHEN: tests pass\n")
        res = json.loads(self.fm("intake", "--json", input=block).stdout)
        self.assertEqual([i["type"] for i in res["created"]], ["FEATURE", "FIX", "CLEAN", "PERFORMANCE", "SECURITY"])
        self.assertEqual([i["type"] for i in res["order"]], ["CLEAN", "PERFORMANCE", "SECURITY", "FIX", "FEATURE"])
        p = c.find_project(self.repo)
        feat = c.find_brief(p, res["created"][0]["id"])
        self.assertEqual(feat.meta["scope"], ["src/reports"])
        self.assertIn("Django app", feat.section("Raw request"))
        self.assertIn("tests pass", feat.section("Raw request"))
        clean = c.find_brief(p, res["created"][2]["id"])
        self.assertEqual(clean.priority, "urgent")
        self.assertTrue(c.find_brief(p, res["created"][3]["id"]).meta.get("explore"))

    def test_intake_ref_becomes_dependency(self):
        self.fm("task", "new", "Base work", "--type", "CLEAN", "--tier", "S")
        res = json.loads(self.fm("intake", "--json", input="FEATURE: build on it #T-0001\n").stdout)
        b = c.find_brief(c.find_project(self.repo), res["created"][0]["id"])
        self.assertEqual(b.meta["depends_on"], ["T-0001"])

    def test_parallel_captures_get_unique_ids(self):
        outs = []

        def run(i):
            outs.append(self.fm("capture", f"item {i}").stdout)

        self.fm("init")
        threads = [threading.Thread(target=run, args=(i,)) for i in range(8)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        ids = sorted(b.id for b in c.load_briefs(c.find_project(self.repo)))
        self.assertEqual(ids, [f"T-{i:04d}" for i in range(1, 9)])


class TaskLifecycle(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Fix login timeout", "--type", "FIX", "--tier", "S", "--scope", "src/auth/**")
        self.p = c.find_project(self.repo)

    def brief(self, tid="T-0001"):
        return c.find_brief(self.p, tid)

    def test_new_task_is_planned_with_scope(self):
        b = self.brief()
        self.assertEqual((b.status, b.type, b.tier, b.meta["scope"]), ("planned", "FIX", "S", ["src/auth/**"]))
        self.assertEqual(self.fm_json("task", "show", "T-0001")["id"], "T-0001")

    def test_step_done_without_evidence_is_refused(self):
        self.fm("task", "step", "T-0001", "add", "write failing test")
        p = self.fm("task", "step", "T-0001", "done", "1", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("evidence", p.stderr)
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest -k slow", "1 failed as expected")
        self.assertTrue(self.brief().steps()[0].done)

    def test_evidence_then_step_done(self):
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "step", "T-0001", "add", "b")
        self.fm("task", "evidence", "T-0001", "--step", "1", "pytest", "3 passed")
        self.fm("task", "step", "T-0001", "done", "1")
        steps = self.brief().steps()
        self.assertEqual([(s.done, s.current) for s in steps], [(True, False), (False, True)])

    def test_task_done_requires_everything(self):
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "ac", "T-0001", "add", "login works on 3G", "--verify", "pytest -k slow")
        p = self.fm("task", "done", "T-0001", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("step 1", p.stderr)
        self.assertIn("criterion 1", p.stderr)
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        self.fm("task", "ac", "T-0001", "check", "1", "--evidence", "pytest -k slow", "1 passed")
        self.fm("task", "done", "T-0001")
        self.assertEqual(self.brief().status, "done")
        events = [e["event"] for e in c.ledger_tail(self.p)]
        self.assertIn("task_done", events)

    def test_focus_is_exclusive(self):
        self.fm("task", "new", "Second", "--type", "CLEAN", "--tier", "S")
        self.fm("focus", "T-0001")
        self.fm("focus", "T-0002")
        self.assertEqual((self.brief("T-0001").status, self.brief("T-0002").status), ("planned", "active"))
        self.assertEqual(self.fm_json("state")["active"]["id"], "T-0002")

    def test_set_fields_and_allow(self):
        self.fm("task", "set", "T-0001", "tier=M", "priority=urgent", "--allow", "core", "--allow", "publish")
        b = self.brief()
        self.assertEqual((b.tier, b.priority, b.meta["allow"]), ("M", "urgent", ["core", "publish"]))
        self.fm("task", "set", "T-0001", "--section", "Execution prompt", "--text", "Do X then Y.")
        self.assertIn("Do X then Y.", self.brief().section("Execution prompt"))

    def test_set_rejects_unknown_status_and_protected_fields(self):
        self.assertEqual(self.fm("task", "set", "T-0001", "status=weird", check=False).returncode, 1)
        self.assertEqual(self.fm("task", "set", "T-0001", "id=T-9999", check=False).returncode, 1)
        self.assertEqual(self.fm("task", "set", "T-0001", "status=done", check=False).returncode, 1)

    def test_block_drop_defer(self):
        self.fm("task", "block", "T-0001", "waiting on API key")
        b = self.brief()
        self.assertEqual(b.status, "blocked")
        self.assertIn("waiting on API key", b.section("Log"))
        self.assertEqual(self.fm_json("state")["blocked"][0]["id"], "T-0001")
        self.fm("task", "defer", "T-0001")
        self.assertEqual(self.brief().status, "deferred")
        self.fm("task", "drop", "T-0001", "not needed")
        self.assertEqual(self.brief().status, "dropped")

    def test_unknown_task_exit_1(self):
        self.assertEqual(self.fm("task", "show", "T-0404", check=False).returncode, 1)

    def test_checkpoint_and_resume(self):
        self.fm("task", "step", "T-0001", "add", "reproduce")
        self.fm("focus", "T-0001")
        with open(os.path.join(self.repo, "x.py"), "w") as f:
            f.write("x = 1\n")
        self.fm("checkpoint", "--note", "Half-way through the retry helper")
        sec = self.brief().section("Resume here")
        self.assertIn("Half-way through the retry helper", sec)
        self.assertIn("<!-- auto -->", sec)
        self.assertIn("x.py", sec)
        r = self.fm_json("resume")
        self.assertEqual((r["id"], r["step"]["n"]), ("T-0001", 1))
        self.assertIn("Half-way", r["resume"])
        self.assertIn("checkpoint", [e["event"] for e in c.ledger_tail(self.p)])

    def test_resume_with_nothing_active(self):
        self.assertIsNone(self.fm_json("resume")["id"])


class StateViews(ForemanTestCase):
    def test_state_md_is_bounded(self):
        self.fm("init")
        for i in range(30):
            self.fm("task", "new", f"task {i}", "--type", "FIX", "--tier", "S")
            self.fm("capture", f"idea {i}")
        text = open(os.path.join(c.find_project(self.repo).dir, "STATE.md")).read()
        self.assertLessEqual(len(text.splitlines()), 60)

    def test_state_line(self):
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S")
        self.fm("task", "step", "T-0001", "add", "one")
        self.fm("task", "step", "T-0001", "add", "two")
        self.fm("focus", "T-0001")
        line = self.fm("state", "--line").stdout.strip()
        self.assertIn("T-0001 FIX 1/2", line)
        self.assertEqual(len(line.splitlines()), 1)

    def test_queue_json_with_cycle(self):
        self.fm("task", "new", "a", "--type", "FIX", "--tier", "S", "--depends", "T-0002")
        self.fm("task", "new", "b", "--type", "FIX", "--tier", "S", "--depends", "T-0001")
        self.fm("task", "new", "c", "--type", "CLEAN", "--tier", "S")
        q = self.fm_json("queue")
        self.assertEqual(q["order"][0]["id"], "T-0003")
        self.assertEqual(q["cycles"], [["T-0001", "T-0002"]])

    def test_log_event(self):
        self.fm("init")
        self.fm("log", "baseline", '{"tests": "40 passed"}')
        e = c.ledger_tail(c.find_project(self.repo))[-1]
        self.assertEqual((e["event"], e["data"]), ("baseline", {"tests": "40 passed"}))


class SensitiveAndDrive(ForemanTestCase):
    def test_sensitive_on_off_preserves_other_settings(self):
        os.makedirs(os.path.join(self.repo, ".claude"))
        path = os.path.join(self.repo, ".claude", "settings.local.json")
        with open(path, "w") as f:
            json.dump({"env": {"A": "1"}}, f)
        self.fm("sensitive", "on")
        data = json.load(open(path))
        self.assertEqual(data["permissions"]["defaultMode"], "default")
        self.assertEqual(data["env"], {"A": "1"})
        self.assertTrue(c.read_meta(c.find_project(self.repo))["sensitive"])
        self.fm("sensitive", "off")
        data = json.load(open(path))
        self.assertNotIn("defaultMode", data.get("permissions", {}))
        self.assertEqual(data["env"], {"A": "1"})
        self.assertFalse(c.read_meta(c.find_project(self.repo))["sensitive"])

    def test_drive_toggle(self):
        self.fm("init")
        self.fm("drive", "off")
        self.assertFalse(c.read_meta(c.find_project(self.repo))["drive"])
        self.fm("drive", "on")
        self.assertTrue(c.read_meta(c.find_project(self.repo))["drive"])


if __name__ == "__main__":
    unittest.main()
