"""Behavioural tests for the fm CLI (run as a subprocess against an isolated FOREMAN_HOME)."""
import json
import subprocess
import os
import re
import threading
import time
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

    def test_lines_between_items_belong_to_the_item_above(self):
        # T-0259: a 30-item block gave every item every item's CONTEXT and DONE-WHEN
        block = ("CONTEXT: shared repo note\nFEATURE: export CSV\nCONTEXT: reports.py\nDONE-WHEN: the CSV opens\n"
                 "FIX: login timeout\nCONTEXT: auth/session.py\nDONE-WHEN: login works on 3G\nSKIP: OAuth\n")
        res = json.loads(self.fm("intake", "--json", input=block).stdout)
        p = c.find_project(self.repo)
        feat, fix = (c.find_brief(p, x["id"]) for x in res["created"])
        for b in (feat, fix):
            self.assertIn("shared repo note", b.section("Raw request"), "lines before the first item are for all")
        self.assertIn("the CSV opens", feat.section("Raw request"))
        self.assertNotIn("login works", feat.section("Raw request"))
        self.assertNotIn("auth/session.py", feat.section("Raw request"))
        self.assertIn("login works on 3G", fix.section("Raw request"))
        self.assertNotIn("reports.py", fix.section("Raw request"))
        self.assertIn("OAuth", fix.section("Non-goals"))
        self.assertNotIn("OAuth", feat.section("Non-goals"))

    def test_intake_ref_becomes_dependency(self):
        self.fm("task", "new", "Base work", "--type", "CLEAN", "--tier", "S")
        res = json.loads(self.fm("intake", "--json", input="FEATURE: build on it #T-0001\n").stdout)
        b = c.find_brief(c.find_project(self.repo), res["created"][0]["id"])
        self.assertEqual(b.meta["depends_on"], ["T-0001"])

    def test_titles_cannot_carry_terminal_control_sequences(self):
        # round 4 (brainstorm, security): titles are printed by the dashboard, statusline and terminal title
        self.fm("capture", "evil\x1b]0;pwned\x07 title‮ here")
        self.fm("task", "new", "also\x1b[2J bad", "--type", "FIX", "--tier", "S")
        self.fm("task", "new", "planned\x1b]0;again\x07 one", "--type", "FIX", "--tier", "S", "--from", "T-0001")
        self.fm("capture", "\x1b[2J")
        for b in c.load_briefs(c.find_project(self.repo)):
            self.assertNotRegex(b.title, r"[\x00-\x1f\x7f‮]")
            self.assertTrue(b.title, "a title of only control characters falls back to 'untitled'")
        self.assertNotIn("\x1b]0;pwned", self.fm("watch", "--once").stdout)

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
        self.fm("task", "set", "T-0001", "--section", "Regression test", "--text", "none: fixture (T-0045 has its own)")
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

    def test_remote_is_granted_only_through_fm_ask(self):
        p = self.fm("task", "set", "T-0001", "--allow", "remote", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("fm ask", p.stderr)
        self.fm_ask("T-0001", "remote")
        self.assertEqual(c.read_meta(self.p)["pending_approvals"][0]["allow"], ["remote"])

    def test_docs_named_in_docs_impact_must_exist_and_be_current(self):
        self.fm("task", "new", "Add a flag", "--type", "FEATURE", "--tier", "M")
        self.fm("task", "step", "T-0002", "add", "a")
        self.fm("task", "step", "T-0002", "done", "1", "--evidence", "pytest", "ok")
        for name, text in (("README.md", "# app\nRun `./cli.py` with --verbose.\n"), ("NOTES.md", "See `./gone.py`.\n")):
            with open(os.path.join(self.repo, name), "w") as f:
                f.write(text)
        self.fm("task", "set", "T-0002", "--section", "Docs impact", "--text", "README.md: --verbose; docs/usage.md")

        def audited_done(check):
            for lens in ("intent", "edge"):
                self.fm("task", "audit", "T-0002", lens, "lens prompt", "ok")
            return self.fm("task", "done", "T-0002", "--lesson", "none: test", check=check)
        p = audited_done(False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("docs/usage.md, which doesn't exist", p.stderr)
        self.assertIn("README.md: path ./cli.py", p.stderr)
        self.assertNotIn("gone.py", p.stderr, "drift in docs the task didn't name is reported, not a blocker")
        open(os.path.join(self.repo, "cli.py"), "w").close()
        self.fm("task", "set", "T-0002", "--section", "Docs impact", "--text", "README.md: documents --verbose")
        self.assertIn("NOTES.md: path ./gone.py", audited_done(True).stdout)

    def test_audit_older_than_the_last_edit_is_stale(self):
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        self.fm("task", "audit", "T-0001", "self", "checklist", "ok")
        with open(os.path.join(self.repo, "x.py"), "w") as f:  # an edit after the audit…
            f.write("x = 2\n")
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:  # …as the hook records it
            f.write(json.dumps({"ts": "2999-01-01T00:00:00Z", "task": "T-0001", "event": "touched",
                                "data": {"file": "x.py", "tool": "Edit"}}) + "\n")
        p = self.fm("task", "done", "T-0001", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("re-audit", p.stderr)

    def test_evidence_recorded_after_the_audit_does_not_stale_it(self):
        # T-0020: the audit covered these exact files; recording more evidence (merge/push results) changes nothing
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        self.fm("task", "audit", "T-0001", "self", "checklist", "ok")
        time.sleep(1.1)  # timestamps have one-second resolution: the evidence must come later than the audit
        self.fm("task", "evidence", "T-0001", "--step", "1", "git push origin main", "pushed")
        self.fm("task", "done", "T-0001")
        self.assertEqual(self.brief().status, "done")
        self.assertEqual(self.fm("task", "audit", "T-0001", "vibes", "x", "y", check=False).returncode, 1)

    def test_next_agrees_with_the_done_gate_after_evidence_only_updates(self):
        # T-0028: fm next / the statusline can't afford a worktree id; evidence carries the one it was recorded at
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "ac", "T-0001", "add", "works")
        self.fm("focus", "T-0001")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        self.fm("task", "ac", "T-0001", "check", "1", "--evidence", "pytest", "ok")
        self.fm("task", "audit", "T-0001", "self", "checklist", "ok")
        time.sleep(1.1)
        self.fm("task", "evidence", "T-0001", "--step", "1", "git push origin main", "pushed")
        self.assertEqual(self.fm_json("next")["stage"], "closing")
        with open(os.path.join(self.repo, "x.py"), "w") as f:
            f.write("x = 2\n")
        time.sleep(1.1)
        self.fm("task", "evidence", "T-0001", "--step", "1", "pytest", "ok")  # files changed since the audit
        self.assertEqual(self.fm_json("next")["stage"], "auditing")

    def test_evidence_run_records_the_real_exit_and_output(self):
        # T-0024: typed results went wrong ("272 tests" for 267); run the command and record what it printed
        self.fm("task", "step", "T-0001", "add", "a")
        out = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "echo '3 passed'").stdout
        self.assertIn("3 passed", out)
        line = self.brief().evidence()[-1]
        for needle in ("echo '3 passed'", "exit 0", "3 passed"):
            self.assertIn(needle, line)
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "echo '1 failed'; exit 3", check=False)
        self.assertEqual(p.returncode, 3)
        self.assertIn("exit 3", self.brief().evidence()[-1])
        p = self.fm("task", "step", "T-0001", "done", "1", check=False)
        self.assertNotEqual(p.returncode, 0, "the newest evidence for the step is a failed run")
        self.assertIn("failed", p.stderr)
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "1")
        self.assertEqual(self.fm("task", "evidence", "T-0001", "--step", "1", "pytest", check=False).returncode, 1,
                         "a typed result is still required without --run")

    def test_focus_requires_a_plan(self):
        p = self.fm("focus", "T-0001", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("acceptance criterion", p.stderr)
        self.assertIn("step", p.stderr)
        self.fm("task", "ac", "T-0001", "add", "login works on 3G")
        self.fm("task", "step", "T-0001", "add", "reproduce")
        self.fm("focus", "T-0001")
        self.assertEqual(self.brief().status, "active")

    def test_unapproved_L_focus_depends_on_autonomy(self):
        self.fm("task", "new", "Big one", "--type", "FEATURE", "--tier", "L")
        for sec, text in (("Interpretation", "x"), ("Approach (options → choice → why)", "y")):
            self.fm("task", "set", "T-0002", "--section", sec, "--text", text)
        self.fm("task", "ac", "T-0002", "add", "works", "--verify", "pytest")
        self.fm("task", "step", "T-0002", "add", "build")
        p = self.fm("focus", "T-0002", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("approval", p.stderr)
        self.fm("autonomy", "full")
        self.fm("focus", "T-0002")

    def test_focus_is_exclusive(self):
        self.fm("task", "new", "Second", "--type", "CLEAN", "--tier", "S")
        for tid in ("T-0001", "T-0002"):
            self.fm("task", "ac", tid, "add", "works")
            self.fm("task", "step", tid, "add", "do it")
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
        p = self.fm_ask("T-0001", "core", "publish", why="edit the guard", session="s1")
        self.assertIn("yes", p.stdout.lower())
        pend = c.read_meta(self.p)["pending_approvals"]
        self.assertEqual([(a["task"], a["allow"], a["why"], a["session"]) for a in pend],
                         [("T-0001", ["core", "publish"], "edit the guard", "s1")])
        self.assertEqual(self.brief().meta.get("allow") or [], [])
        self.fm_ask("T-0001", "core", why="again", session="s1")
        self.assertEqual(len(c.read_meta(self.p)["pending_approvals"]), 1, "one pending request per task")

    def test_ask_not_seen_by_the_hook_is_refused(self):
        # Obfuscated or scripted fm ask: no trusted session, so nothing may be recorded (T-0009 adversary audit).
        p = self.fm("ask", "T-0001", "core", env={"CLAUDE_CODE_SESSION_ID": "victim"}, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("session", p.stderr)
        self.assertNotIn("pending_approvals", c.read_meta(self.p))

    def test_ask_session_comes_from_the_hook_not_the_environment(self):
        self.fm_ask("T-0001", "core", session="mine", env={"CLAUDE_CODE_SESSION_ID": "victim"})
        self.assertEqual(c.read_meta(self.p)["pending_approvals"][0]["session"], "mine")

    def test_audit_goes_stale_when_files_change_however_they_were_edited(self):
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        self.fm("task", "audit", "T-0001", "self", "checklist", "ok")
        path = os.path.join(self.repo, "README.md")
        original = read_text(path)
        with open(path, "a") as f:  # e.g. sed -i through Bash: no touched event
            f.write("changed after the audit\n")
        p = self.fm("task", "done", "T-0001", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("changed since", p.stderr)
        with open(path, "w") as f:
            f.write(original)
        self.fm("task", "done", "T-0001")

    def test_tier_cannot_be_lowered_once_work_has_evidence(self):
        self.fm("task", "set", "T-0001", "tier=M")
        self.fm("task", "step", "T-0001", "add", "a")
        self.fm("task", "evidence", "T-0001", "--step", "1", "pytest", "red")
        p = self.fm("task", "set", "T-0001", "tier=S", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("tier", p.stderr)
        self.fm("task", "set", "T-0001", "tier=L")
        self.assertEqual(self.brief().tier, "L")

    def test_ask_rejects_unknown_and_unauthorizable_categories(self):
        for cat in ("bogus", "state-direct", "self-authorize"):
            self.assertEqual(self.fm_ask("T-0001", cat, check=False).returncode, 1, cat)
        self.assertEqual(self.fm_ask("T-0099", "core", check=False).returncode, 1)

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
        self.fm("task", "ac", "T-0001", "add", "works")
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
        self.fm("task", "ac", "T-0001", "add", "works")
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


class OneCommandTask(ForemanTestCase):
    def test_task_new_with_ac_step_and_focus(self):
        self.fm("init")
        self.fm("task", "new", "Fix typo in README", "--type", "FIX", "--tier", "S",
                "--ac", "typo gone", "--step", "fix it", "--focus")
        b = c.find_brief(c.find_project(self.repo), "T-0001")
        self.assertEqual((b.status, len(b.acceptance()), len(b.steps())), ("active", 1, 1))


class Checks(ForemanTestCase):
    def test_a_gate_flaky_again_and_again_fails(self):
        # final review: a racy bug that passes half the time mustn't keep passing as "flaky"
        self.fm("init")
        flag = os.path.join(self.tmp, "odd")
        self.fm("check", "add", f"if [ -e {flag} ]; then rm {flag}; exit 0; else touch {flag}; exit 1; fi")
        codes = [self.fm("check", "--fresh", check=False) for _ in range(3)]
        self.assertEqual([p.returncode for p in codes], [0, 0, 1])
        self.assertIn("flaky again", codes[2].stdout)

    def test_a_pass_on_the_same_tree_is_reused_and_affected_runs_only_linked_tests(self):
        # round 5 (T-0063): the ~100 s suite ran twice per tree (step and criterion evidence); iterate on linked tests
        self.fm("init")
        log = os.path.join(self.tmp, "runs.log")
        self.fm("check", "add", f"echo full >> {log}")
        self.fm("check")
        out = self.fm("check").stdout
        self.assertIn("cached", out)
        self.assertEqual(read_text(log).count("full"), 1)
        with open(os.path.join(self.repo, "new.txt"), "w") as f:
            f.write("x\n")
        self.fm("check")
        self.fm("check", "--fresh")
        self.assertEqual(read_text(log).count("full"), 3)
        for rel in ("src/parser.py", "tests/test_parser.py", "tests/test_report.py", "src/report.py"):
            os.makedirs(os.path.join(self.repo, os.path.dirname(rel)), exist_ok=True)
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write("x = 1\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"],
                       check=True)
        self.fm("check", "affected", f"echo {{tests}} >> {log}")
        with open(os.path.join(self.repo, "src/parser.py"), "a") as f:
            f.write("y = 2\n")
        out = self.fm("check", "--affected").stdout
        self.assertIn("affected", out)
        self.assertIn("tests/test_parser.py", read_text(log))
        self.assertNotIn("tests/test_report.py", read_text(log))

    def test_a_flaky_gate_is_rerun_and_labelled_and_old_failures_are_told_apart(self):
        # T-0047: a failure that passes on a rerun is flaky; one that already failed before the task is pre-existing
        self.fm("init")
        flag = os.path.join(self.tmp, "ran-once")
        self.fm("check", "add", f"test -e {flag} || {{ touch {flag}; exit 1; }}")
        p = self.fm("check", check=False)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("flaky", p.stdout)
        self.assertRegex(p.stdout, r"\d+\.\d s")
        self.fm("check", "rm", "1")
        self.fm("check", "add", "exit 3")
        self.assertNotIn("pre-existing", self.fm("check", check=False).stdout)
        self.fm("task", "new", "Other work", "--type", "CLEAN", "--tier", "S", "--ac", "ok", "--step", "do", "--focus")
        p = self.fm("check", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("pre-existing", p.stdout)

    """T-0025: the project's gates in one command that can't be masked by a pipe."""

    def test_gates_run_together_and_any_failure_fails(self):
        self.fm("init")
        self.assertNotEqual(self.fm("check", check=False).returncode, 0, "no gates configured is not a pass")
        self.fm("check", "add", "echo suite ok")
        self.fm("check", "add", "echo 'lint: 2 errors'; exit 1")
        self.assertIn("echo suite ok", self.fm("check", "list").stdout)
        p = self.fm("check", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("✓ echo suite ok", p.stdout)
        self.assertIn("✗", p.stdout)
        self.assertIn("lint: 2 errors", p.stdout)
        self.fm("check", "rm", "2")
        self.assertIn("✓ echo suite ok", self.fm("check").stdout)

    def test_odd_output_missing_bash_and_no_timeout_are_handled(self):
        # round-1 edge audit: binary output, no bash on PATH, --timeout 0 ("no limit"), concurrent adds
        self.fm("init")
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S", "--step", "fix", "--ac", "works")
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", r"printf 'ok \377\376\n'", check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true", "--timeout", "0",
                                 check=False).returncode, 0)
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true", env={"PATH": self.tmp}, check=False)
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn("exit 127", c.find_brief(c.find_project(self.repo), "T-0001").evidence()[-1])
        threads = [threading.Thread(target=self.fm, args=("check", "add", f"echo {i}")) for i in range(6)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        self.assertEqual(len(c.read_meta(c.find_project(self.repo)).get("checks")), 6)

    def test_a_failing_gate_is_not_hidden_by_a_later_passing_one_or_by_typed_evidence(self):
        # round-1 adversary audit: only runs decide, and one fm check run is one verdict
        self.fm("init")
        self.fm("check", "add", "false")
        self.fm("check", "add", "true")
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S", "--step", "fix", "--ac", "works")
        self.assertEqual(self.fm("check", "--evidence", "T-0001", "--step", "1", check=False).returncode, 1)
        self.assertNotEqual(self.fm("task", "step", "T-0001", "done", "1", check=False).returncode, 0)
        self.fm("task", "evidence", "T-0001", "--step", "1", "pytest", "exit 0 · 5 passed [ran] [tree deadbeef0000]")
        self.assertNotEqual(self.fm("task", "step", "T-0001", "done", "1", check=False).returncode, 0,
                            "typed evidence can't clear a failed run")
        b = c.find_brief(c.find_project(self.repo), "T-0001")
        self.assertNotEqual(b.last_work_tree()[1], "deadbeef0000", "typed text can't forge a worktree id")
        self.fm("check", "rm", "1")
        self.fm("check", "--evidence", "T-0001", "--step", "1")
        self.fm("task", "step", "T-0001", "done", "1")

    def test_results_become_evidence(self):
        self.fm("init")
        self.fm("check", "add", "echo suite ok")
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S", "--step", "fix", "--ac", "works")
        self.fm("check", "--evidence", "T-0001", "--step", "1")
        line = c.find_brief(c.find_project(self.repo), "T-0001").evidence()[-1]
        self.assertIn("echo suite ok", line)
        self.assertIn("exit 0", line)
        self.fm("task", "step", "T-0001", "done", "1")


class NewTaskCriteria(ForemanTestCase):
    def test_ac_can_carry_its_verify_command(self):
        # T-0042: an M task made in one command must be focusable (every criterion needs a verify command)
        self.fm("task", "new", "Add export", "--type", "FEATURE", "--tier", "M", "--ac", "exports CSV :: pytest -k csv",
                "--step", "build it")
        for sec in ("Interpretation", "Approach (options → choice → why)"):
            self.fm("task", "set", "T-0001", "--section", sec, "--text", "planned")
        self.fm("focus", "T-0001")
        ac = c.find_brief(c.find_project(self.repo), "T-0001").acceptance()[0]
        self.assertEqual(ac.text, "exports CSV — verify with `pytest -k csv`")
        self.fm("task", "ac", "T-0001", "add", "quotes fields :: pytest -k quote")  # same form on ac add
        ac = c.find_brief(c.find_project(self.repo), "T-0001").acceptance()[1]
        self.assertEqual(ac.text, "quotes fields — verify with `pytest -k quote`")


class AuditPrep(ForemanTestCase):
    """T-0026: the diff since the task started, frozen, plus one ready reviewer brief per lens."""

    def test_split_writes_parallel_briefs_by_lens_group(self):
        # T-0216: an L review in up to three fresh contexts (claudekit-style), opt-in for usage
        self.fm("init")
        self.fm("task", "new", "Big change", "--type", "FEATURE", "--tier", "L", "--step", "do it")
        self.fm("task", "ac", "T-0001", "add", "works", "--verify", "true")
        for sec in ("Interpretation", "Approach (options → choice → why)"):
            self.fm("task", "set", "T-0001", "--section", sec, "--text", "planned")
        self.fm("task", "set", "T-0001", "approved=true")
        self.fm("focus", "T-0001")
        with open(os.path.join(self.repo, "big.py"), "w") as f:
            f.write("".join(f"X{i} = {i}\n" for i in range(900)))
        one = self.fm("audit", "prep", "T-0001").stdout
        self.assertIn("Run one foreman:fm-reviewer", one)
        self.assertIn("--split", one, "a big L diff gets the suggestion")
        out = self.fm("audit", "prep", "T-0001", "--split").stdout
        briefs = sorted(set(re.findall(r"\S+T-0001\.review-\d\.md", out)))
        self.assertEqual(len(briefs), 3, out)
        self.assertIn("in parallel", out)
        lenses = [re.findall(r"(?m)^## (\w+)$", read_text(b)) for b in briefs]
        self.assertEqual(sorted(sum(lenses, [])), sorted(["intent", "adversary", "edge", "operator", "maintainer"]))
        self.assertTrue(all(lenses), "no empty group")

    def test_prep_freezes_the_diff_and_prints_lens_briefs(self):
        self.fm("init")
        self.fm("task", "new", "Add --verbose", "--type", "FEATURE", "--tier", "L", "--step", "add it")
        self.fm("task", "ac", "T-0001", "add", "prints more with --verbose", "--verify", "pytest")
        for sec in ("Interpretation", "Approach (options → choice → why)"):
            self.fm("task", "set", "T-0001", "--section", sec, "--text", "planned")
        self.fm("task", "set", "T-0001", "approved=true")
        self.fm("focus", "T-0001")
        with open(os.path.join(self.repo, "cli.py"), "w") as f:
            f.write("VERBOSE = True\n")  # new, uncommitted and untracked
        out = self.fm("audit", "prep", "--print", "T-0001").stdout
        diff = next(w for w in out.split() if w.endswith("T-0001.diff"))
        self.assertIn("VERBOSE = True", read_text(diff))
        for lens, needle in (("intent", "prints more with --verbose"), ("adversary", "trying to break"),
                             ("edge", "environment"), ("operator", "real machine"), ("maintainer", "next year")):
            self.assertIn(needle, out, lens)
        only = self.fm("audit", "prep", "--print", "T-0001", "--lens", "adversary").stdout
        self.assertIn("trying to break", only)
        self.assertNotIn("next year", only)
        with open(os.path.join(self.repo, "blob.bin"), "wb") as f:
            f.write(b"\xff\xfe binary \x00\n")  # a diff that isn't UTF-8
        self.assertIn("trying to break", self.fm("audit", "prep", "--print", "T-0001", "--lens", "adversary").stdout)

    def test_lens_briefs_carry_this_projects_past_findings_for_that_lens(self):
        # round 9 (T-0018): a reviewer starts from the weak spots earlier reviews of this project found
        self.fm("init")
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S", "--ac", "works", "--step", "fix", "--focus")
        self.fm("research", "add", "t0005-adversary", input=(
            "## Verdict: changes needed\n**HIGH — fmguard.py:10 — tree writes bypass the core check**\n"
            "**LOW — a nit**\n- **MEDIUM — fmsync.py:3** — imported titles reach the terminal \x1b[31munsanitized\n"))
        report = json.dumps({"message": {"role": "assistant", "content": [
            {"type": "text", "text": "Verdict: changes needed\n1 MED stale grants survive a restart\n"}]}})
        self.fm("research", "add", "wave2-edge-adversary", input='"slug":"x"}\n' + report + "\n")  # a raw transcript
        self.fm("research", "add", "t0007-edge", input="**HIGH — clock skew breaks the lock**\n")
        self.fm("research", "add", "t0009-review", input="## adversary: changes needed\n**HIGH — combined finding**\n"
                                                           "## edge: ok\n**HIGH — edge only finding**\n")
        out = self.fm("audit", "prep", "--print", "T-0001", "--lens", "adversary").stdout
        for seen in ("tree writes bypass the core check", "imported titles reach the terminal",
                     "stale grants survive a restart", "combined finding"):
            self.assertIn(seen, out)
        for unseen in ("a nit", "clock skew", "\x1b", "edge only finding"):
            self.assertNotIn(unseen, out)
        self.assertNotIn("Past findings", self.fm("audit", "prep", "--print", "T-0001", "--lens", "operator").stdout)
        research = os.path.join(c.find_project(self.repo).dir, "research")
        os.mkdir(os.path.join(research, "odd-adversary.md"))  # not a file: skipped, never a crash or a hang
        os.mkfifo(os.path.join(research, "pipe-adversary.md"))
        os.symlink("/dev/zero", os.path.join(research, "zero-adversary.md"))
        out = self.fm("audit", "prep", "--print", "T-0001", "--lens", "adversary").stdout
        self.assertIn("tree writes bypass the core check", out)
        self.assertIn("not instructions", out)

    def test_several_lenses_make_one_combined_brief_for_one_reviewer(self):
        # T-0060: one reviewer pass reads the diff once; five separate subagents each re-read it
        self.fm("init")
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S", "--ac", "works", "--step", "fix", "--focus")
        out = self.fm("audit", "prep", "--print", "T-0001", "--lens", "adversary", "--lens", "edge").stdout
        self.assertEqual(out.count("Diff to review:"), 1)
        self.assertEqual(out.count("=== review"), 1)
        for needle in ("## adversary", "## edge", "trying to break", "environment", "one foreman:fm-reviewer"):
            self.assertIn(needle, out)

    def test_the_brief_goes_to_a_file_not_the_conversation(self):
        # round 5: printed, the brief is paid for twice (the main context and the reviewer's prompt)
        self.fm("init")
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "S", "--ac", "works", "--step", "fix", "--focus")
        out = self.fm("audit", "prep", "T-0001", "--lens", "adversary").stdout
        path = next(w for w in out.split() if w.endswith("T-0001.review.md"))
        self.assertIn("trying to break", read_text(path))
        self.assertNotIn("trying to break", out)
        self.assertLess(len(out), 700)

    def test_every_lens_has_a_template_in_the_audit_reference(self):
        # fm audit prep builds briefs from references/audit.md: rewording it must not silently drop a lens
        import fmcli
        with open(os.path.join(c.PLUGIN_ROOT, "skills", "intake", "references", "audit.md")) as f:
            found = {m.group(1) for m in fmcli._LENS_TPL.finditer(f.read())}
        self.assertEqual(found, set(c.AUDIT_LENSES) - {"self"})


class RoundFiveWorkflow(ForemanTestCase):
    """Round 5 (T-0018): cleaner review notes, focused audit briefs, requests finished inside another task."""

    def test_research_keeps_a_subagents_final_report_not_its_transcript(self):
        self.fm("init")
        transcript = os.path.join(self.tmp, "agent.output")
        lines = [{"type": "user", "message": {"role": "user", "content": "review this"}},
                 {"type": "assistant", "message": {"role": "assistant", "content": [
                     {"type": "tool_use", "name": "Read", "input": {"file_path": "x"}}]}},
                 {"type": "assistant", "message": {"role": "assistant", "content": [
                     {"type": "text", "text": "## Verdict: changes needed\n\n**HIGH** — x.py:3 — broken"}]}}]
        with open(transcript, "w") as f:
            f.write("\n".join(json.dumps(l) for l in lines) + "\n")
        path = self.fm_json("research", "add", "r1-edge", "--from-agent", transcript)["path"]
        text = read_text(path)
        self.assertTrue(text.startswith("## Verdict: changes needed"), text[:80])
        self.assertNotIn("tool_use", text)
        plain = os.path.join(self.tmp, "report.md")
        with open(plain, "w") as f:
            f.write("## Verdict: ok\n")
        self.assertIn("## Verdict: ok", read_text(self.fm_json("research", "add", "r2", "--from-agent", plain)["path"]))
        # final maintainer audit: a FIFO or device would hang the read, a directory would crash it
        os.mkfifo(os.path.join(self.tmp, "fifo"))
        for bad in ("/dev/zero", os.path.join(self.tmp, "fifo"), self.tmp):
            for flag in ("--from-agent", "--file"):
                with self.subTest(bad=bad, flag=flag):
                    p = self.fm("research", "add", "r3", flag, bad, check=False)
                    self.assertEqual(p.returncode, 1)
                    self.assertIn("regular file", p.stderr)

    def test_audit_prep_note_reaches_the_review_brief(self):
        self.fm("init")
        self.fm("task", "new", "Add sync", "--type", "FEATURE", "--tier", "L", "--step", "build it")
        self.fm("task", "ac", "T-0001", "add", "syncs", "--verify", "pytest")
        for sec in ("Interpretation", "Approach (options → choice → why)"):
            self.fm("task", "set", "T-0001", "--section", sec, "--text", "planned")
        self.fm("task", "set", "T-0001", "approved=true")
        self.fm("focus", "T-0001")
        out = self.fm("audit", "prep", "--print", "T-0001", "--note", "threat: a pulled .foreman/ is untrusted",
                      "--note", "round 3 only").stdout
        self.assertEqual(out.count("threat: a pulled .foreman/ is untrusted"), 1)  # one combined brief (T-0060)
        self.assertEqual(out.count("round 3 only"), 1)

    def test_a_request_done_inside_another_task_is_done_there(self):
        self.fm("init")
        self.fm("task", "new", "Umbrella", "--type", "FEATURE", "--tier", "S", "--step", "all of it", "--ac", "works")
        self.fm("capture", "export as CSV")
        p0 = self.fm("task", "drop", "T-0002", "--done-in", "T-0001", check=False)
        self.assertEqual(p0.returncode, 2, "the host must have done work (evidence), or nothing was done anywhere")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        out = self.fm("task", "drop", "T-0002", "--done-in", "T-0001").stdout
        self.assertIn("done in T-0001", out)
        p = c.find_project(self.repo)
        folded, host = c.find_brief(p, "T-0002"), c.find_brief(p, "T-0001")
        self.assertEqual((folded.status, folded.meta.get("done_in")), ("done", "T-0001"))
        self.assertIn("includes T-0002", host.section("Log"))
        self.assertNotEqual(self.fm("task", "drop", "T-0001", "--done-in", "T-0999", check=False).returncode, 0)
        self.assertNotEqual(self.fm("task", "drop", "T-0001", "--done-in", "T-0001", check=False).returncode, 0)
        # work that was started keeps its own gates: --done-in isn't a way around evidence and audits
        self.fm("capture", "another")
        p2 = self.fm("task", "drop", "T-0001", "--done-in", "T-0003", check=False)
        self.assertEqual(p2.returncode, 2)
        self.assertIn("started", p2.stderr)


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


class AskClosed(ForemanTestCase):
    """T-0302: a grant only works while its task is active, so a yes on a closed task would be a yes for nothing."""

    def test_a_closed_task_gets_no_dialog_and_no_request(self):
        self.fm("init")
        tid = json.JSONDecoder().raw_decode(self.fm("task", "new", "Release", "--type", "CLEAN", "--tier", "S", "--ac",
                                                    "ok :: true", "--step", "a", "--focus", "--json").stdout)[0]["id"]
        self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        cmd = f"fm ask {tid} plugin --why 'install it'"
        out = json.loads(self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("closed", out["hookSpecificOutput"]["permissionDecisionReason"])
        r = self.fm("ask", tid, "plugin", "--why", "install it", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("closed", r.stderr)
        self.assertFalse(c.read_meta(c.find_project(self.repo)).get("pending_approvals"))
        cmd = f"fm ask {tid} core --standing --why 'every task'"  # standing covers later tasks: any id will do
        out = json.loads(self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")


if __name__ == "__main__":
    unittest.main()
