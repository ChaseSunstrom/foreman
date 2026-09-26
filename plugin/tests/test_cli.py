"""Behavioural tests for the fm CLI (run as a subprocess against an isolated FOREMAN_HOME)."""
import json
import os
import threading
import unittest

from helpers import ForemanTestCase, read_text, read_json

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
        inbox = read_text(os.path.join(c.find_project(self.repo).dir, "INBOX.md"))
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
        p = self.fm("task", "done", "T-0001", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("audit missing: self", p.stderr)
        self.fm("task", "audit", "T-0001", "self", "lens checklist", "no findings")
        self.fm("task", "done", "T-0001")
        self.assertEqual(self.brief().status, "done")
        events = [e["event"] for e in c.ledger_tail(self.p)]
        self.assertIn("task_done", events)

    def test_audit_older_than_the_last_edit_is_stale(self):
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        self.fm("task", "audit", "T-0001", "self", "checklist", "ok")
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:  # an Edit recorded by the hook later on
            f.write(json.dumps({"ts": "2999-01-01T00:00:00Z", "task": "T-0001", "event": "touched",
                                "data": {"file": "x.py", "tool": "Edit"}}) + "\n")
        p = self.fm("task", "done", "T-0001", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("after the last change", p.stderr)
        self.assertEqual(self.fm("task", "audit", "T-0001", "vibes", "x", "y", check=False).returncode, 1)

    def test_focus_is_exclusive(self):
        self.fm("task", "new", "Second", "--type", "CLEAN", "--tier", "S")
        self.fm("focus", "T-0001")
        self.fm("focus", "T-0002")
        self.assertEqual((self.brief("T-0001").status, self.brief("T-0002").status), ("planned", "active"))
        self.assertEqual(self.fm_json("state")["active"]["id"], "T-0002")

    def test_set_fields_and_allow(self):
        self.fm("task", "set", "T-0001", "tier=M", "priority=urgent", "--allow", "publish")
        b = self.brief()
        self.assertEqual((b.tier, b.priority, b.meta["allow"]), ("M", "urgent", ["publish"]))
        self.fm("task", "set", "T-0001", "--section", "Execution prompt", "--text", "Do X then Y.")
        self.assertIn("Do X then Y.", self.brief().section("Execution prompt"))

    def test_cli_never_grants_core_or_unauthorizable_categories(self):
        # However fm is reached (renamed binary, symlink, python -m), core only comes from the user's reply to fm ask.
        for cat in ("core", "state-direct", "self-authorize", "bogus"):
            p = self.fm("task", "set", "T-0001", "--allow", cat, check=False)
            self.assertNotEqual(p.returncode, 0, cat)
            self.assertIn("fm ask", p.stderr + p.stdout if cat == "core" else "fm ask")
        self.assertEqual(self.brief().meta.get("allow") or [], [])

    def test_abbreviated_options_are_rejected(self):
        # The guard matches `--allow core` literally; an abbreviation must not reach the same code path (T-0010).
        for spelling in (["--allo", "core"], ["--al=core"], ["--all", "core"]):
            p = self.fm("task", "set", "T-0001", *spelling, check=False)
            self.assertEqual(p.returncode, 2, spelling)
        self.assertEqual(self.brief().meta.get("allow") or [], [])
        self.assertEqual(self.fm("capture", "x", "--sour", "self", check=False).returncode, 2)

    def test_ask_records_a_pending_approval_without_granting(self):
        p = self.fm("ask", "T-0001", "core", "publish", "--why", "edit the guard", env={"FOREMAN_SESSION_ID": "s1"})
        self.assertIn("yes", p.stdout.lower())
        pend = c.read_meta(self.p)["pending_approvals"]
        self.assertEqual([(a["task"], a["allow"], a["why"], a["session"]) for a in pend],
                         [("T-0001", ["core", "publish"], "edit the guard", "s1")])
        self.assertEqual(self.brief().meta.get("allow") or [], [])
        self.fm("ask", "T-0001", "core", "--why", "again")
        self.assertEqual(len(c.read_meta(self.p)["pending_approvals"]), 1, "one pending request per task")

    def test_session_comes_from_claude_code_first(self):
        # FOREMAN_SESSION_ID (CLAUDE_ENV_FILE) goes stale on resume; Claude Code's own variable doesn't.
        self.fm("ask", "T-0001", "core", env={"CLAUDE_CODE_SESSION_ID": "cc-1", "FOREMAN_SESSION_ID": "stale"})
        self.assertEqual(c.read_meta(self.p)["pending_approvals"][0]["session"], "cc-1")

    def test_ask_rejects_unknown_and_unauthorizable_categories(self):
        for cat in ("bogus", "state-direct", "self-authorize"):
            self.assertEqual(self.fm("ask", "T-0001", cat, check=False).returncode, 1, cat)
        self.assertEqual(self.fm("ask", "T-0099", "core", check=False).returncode, 1)

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

    def test_log_appends_a_note_without_replacing_the_section(self):
        self.fm("task", "log", "T-0001", "steer: use the existing logger instead of print")
        self.fm("task", "log", "T-0001", "second note")
        log = self.brief().section("Log")
        self.assertIn("steer: use the existing logger instead of print", log)
        self.assertIn("second note", log)
        self.assertIn("created", log, "earlier lines are kept")
        self.assertIn("note", [e["event"] for e in c.ledger_tail(self.p)])

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
        text = read_text(os.path.join(c.find_project(self.repo).dir, "STATE.md"))
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
        data = read_json(path)
        self.assertEqual(data["permissions"]["defaultMode"], "default")
        self.assertEqual(data["env"], {"A": "1"})
        self.assertTrue(c.read_meta(c.find_project(self.repo))["sensitive"])
        self.fm("sensitive", "off")
        data = read_json(path)
        self.assertNotIn("defaultMode", data.get("permissions", {}))
        self.assertEqual(data["env"], {"A": "1"})
        self.assertFalse(c.read_meta(c.find_project(self.repo))["sensitive"])

    def test_drive_toggle(self):
        self.fm("init")
        self.fm("drive", "off")
        self.assertFalse(c.read_meta(c.find_project(self.repo))["drive"])
        self.fm("drive", "on")
        self.assertTrue(c.read_meta(c.find_project(self.repo))["drive"])


class NextAction(ForemanTestCase):
    def test_next_names_the_one_required_action(self):
        self.fm("init")
        self.assertIn("queue is empty", self.fm("next").stdout)
        self.fm("task", "new", "Fix login", "--type", "FIX", "--tier", "S")
        self.assertIn("missing acceptance criterion, step", self.fm("next").stdout)
        self.fm("task", "ac", "T-0001", "add", "works", "--verify", "pytest")
        self.fm("task", "step", "T-0001", "add", "reproduce")
        self.assertIn("fm focus T-0001", self.fm("next").stdout)
        res = self.fm_json("next")
        self.assertEqual((res["task"], res["stage"]), ("T-0001", "ready"))


class Autonomy(ForemanTestCase):
    def test_autonomy_defaults_to_standard_and_switches(self):
        self.fm("init")
        self.assertEqual(self.fm_json("state")["autonomy"], "standard")
        self.assertIn("standard", self.fm("autonomy").stdout)
        self.fm("autonomy", "full")
        self.assertEqual(self.fm_json("state")["autonomy"], "full")
        self.assertEqual(self.fm("autonomy", "reckless", check=False).returncode, 2)


class DecisionsResearchSelf(ForemanTestCase):
    def test_decide_appends_a_table_row_and_logs(self):
        self.fm("init")
        self.fm("decide", "Use Python stdlib for fm", "--why", "jq missing; python on PATH", "--rejected", "sh+jq")
        text = read_text(os.path.join(c.find_project(self.repo).dir, "decisions.md"))
        self.assertRegex(text, r"\| \d{4}-\d\d-\d\d \| Use Python stdlib for fm \| jq missing; python on PATH \| sh\+jq \|")
        self.assertIn("decision", [e["event"] for e in c.ledger_tail(c.find_project(self.repo))])

    def test_decide_escapes_pipes(self):
        self.fm("init")
        self.fm("decide", "a | b", "--why", "c|d")
        text = read_text(os.path.join(c.find_project(self.repo).dir, "decisions.md"))
        self.assertIn("a \\| b", text)

    def test_research_add_from_stdin_and_file(self):
        self.fm("init")
        self.fm("research", "add", "auth-recon", input="## Findings\n- src/auth.py:12 retries missing\n")
        path = os.path.join(c.find_project(self.repo).dir, "research", "auth-recon.md")
        self.assertIn("retries missing", read_text(path))
        src = os.path.join(self.tmp, "notes.md")
        with open(src, "w") as f:
            f.write("token=abcd1234efgh leaked\n")
        self.fm("research", "add", "notes", "--file", src)
        saved = read_text(os.path.join(c.find_project(self.repo).dir, "research", "notes.md"))
        self.assertNotIn("abcd1234efgh", saved)

    def test_research_name_must_be_safe(self):
        self.fm("init")
        self.assertEqual(self.fm("research", "add", "../escape", input="x", check=False).returncode, 1)

    def test_capture_self_targets_the_foreman_repo_project(self):
        own = os.path.join(self.home)  # FOREMAN_HOME is itself a git repo in this test
        import subprocess
        subprocess.run(["git", "init", "-q", own], check=True)
        out = self.fm("capture", "stop gate too chatty", "--source", "self", "--self").stdout
        self.assertIn("T-0001", out)
        p = c.find_project(own)
        self.assertEqual(c.find_brief(p, "T-0001").meta["source"], "self")
        self.assertIsNone(c.find_project(self.repo))


if __name__ == "__main__":
    unittest.main()
