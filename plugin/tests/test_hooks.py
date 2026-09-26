"""Hook handler tests: run plugin/hooks/hook <Event> with JSON payloads against an isolated FOREMAN_HOME."""
import json
import os
import unittest

from helpers import ForemanTestCase, read_text

import fmcore as c


def parse(proc):
    out = proc.stdout.strip()
    return json.loads(out) if out.startswith("{") else None


class HookCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.env_file = os.path.join(self.tmp, "claude_env")
        open(self.env_file, "w").close()

    def project(self):
        return c.find_project(self.repo)

    def task(self, title="Fix login", type_="FIX", tier="S", steps=("reproduce", "fix"), focus=True, scope=None):
        args = ["task", "new", title, "--type", type_, "--tier", tier]
        for s in scope or []:
            args += ["--scope", s]
        tid = json.loads(self.fm(*args, "--json").stdout)["id"]
        for s in steps:
            self.fm("task", "step", tid, "add", s)
        self.fm("task", "ac", tid, "add", "works", "--verify", "pytest")
        if tier in ("M", "L"):
            for sec in ("Interpretation", "Approach (options → choice → why)"):
                self.fm("task", "set", tid, "--section", sec, "--text", "planned")
        if focus:
            self.fm("focus", tid)
        return tid

    def ctx_of(self, proc):
        data = parse(proc) or {}
        return (data.get("hookSpecificOutput") or {}).get("additionalContext", "")

    def hooks_log(self):
        path = os.path.join(self.home, "state", "logs", "hooks.log")
        return read_text(path) if os.path.exists(path) else ""

    def events(self):
        with open(os.path.join(self.home, "state", "events.jsonl")) as f:
            return [json.loads(l) for l in f]


class SessionStart(HookCase):
    def run_ss(self, source="startup"):
        return self.hook("SessionStart", {"source": source}, env={"CLAUDE_ENV_FILE": self.env_file})

    def test_registers_project_and_injects_factual_state(self):
        self.fm("init")
        tid = self.task()
        self.fm("capture", "export CSV", "--type", "FEATURE")
        p = self.run_ss()
        self.assertEqual(p.returncode, 0, p.stderr)
        ctx = self.ctx_of(p)
        self.assertIn(tid, ctx)
        self.assertIn("step 1/2", ctx)
        self.assertIn("Inbox: 1", ctx)
        self.assertLessEqual(len(ctx), 2000)
        self.assertNotRegex(ctx, r"(?i)\b(you must|always|never|do not)\b")
        self.assertIn("\x1b]0;", parse(p)["terminalSequence"])

    def test_exports_session_and_project_to_env_file(self):
        self.run_ss()
        env = read_text(self.env_file)
        self.assertIn("FOREMAN_SESSION_ID=sess-1", env)
        self.assertIn(f"FOREMAN_PROJECT={c.slug_for(self.repo)}", env)
        self.assertIsNotNone(self.project(), "git repo auto-registered")

    def test_full_autonomy_is_reported(self):
        self.fm("init")
        self.fm("autonomy", "full")
        self.assertIn("Autonomy: full", self.ctx_of(self.run_ss()))

    def test_budget_holds_with_large_queue(self):
        self.fm("init")
        for i in range(40):
            self.fm("task", "new", f"a fairly long task title number {i} " + "x" * 60, "--type", "FIX", "--tier", "S")
            self.fm("capture", f"idea {i} " + "y" * 80)
        self.assertLessEqual(len(self.ctx_of(self.run_ss())), 2000)

    def test_sensitive_and_other_session_are_reported(self):
        self.fm("init")
        self.fm("sensitive", "on")
        self.hook("UserPromptSubmit", {"prompt": "hi", "session_id": "other-session"})
        ctx = self.ctx_of(self.run_ss())
        self.assertIn("Sensitive", ctx)
        self.assertIn("other-se", ctx)

    def test_non_git_unregistered_dir_gets_nothing(self):
        plain = os.path.join(self.tmp, "plain")
        os.makedirs(plain)
        p = self.hook("SessionStart", {"source": "startup", "cwd": plain}, env={"CLAUDE_ENV_FILE": self.env_file})
        self.assertEqual((p.returncode, p.stdout.strip()), (0, ""))

    def test_fails_open_on_corrupt_state(self):
        self.fm("init")
        with open(os.path.join(self.project().dir, "meta.json"), "w") as f:
            f.write("{not json")
        p = self.run_ss()
        self.assertEqual(p.returncode, 0)
        self.assertIn("SessionStart", self.hooks_log())


class UserPromptSubmit(HookCase):
    def test_intake_block_is_summarised(self):
        self.fm("init")
        ctx = self.ctx_of(self.hook("UserPromptSubmit", {"prompt": "FIX: a\nFEATURE!: b\nCLEAN?: c\nCONTEXT: d"}))
        self.assertIn("3 intake items", ctx)
        self.assertIn("FEATURE!", ctx)
        self.assertLessEqual(len(ctx), 400)

    def test_active_task_and_override_are_reported(self):
        self.fm("init")
        tid = self.task()
        ctx = self.ctx_of(self.hook("UserPromptSubmit", {"prompt": "NOW: prod is down"}))
        self.assertIn("NOW", ctx)
        self.assertIn(f"{tid} FIX step 1/2", ctx)

    def test_open_ended_request_points_at_brainstorm(self):
        self.fm("init")
        self.assertIn("brainstorm", self.ctx_of(self.hook("UserPromptSubmit", {"prompt": "super improve it"})))
        self.assertNotIn("brainstorm", self.ctx_of(self.hook("UserPromptSubmit", {"prompt": "fix the login timeout"})))

    def test_pause_and_resume_toggle_drive_pause(self):
        self.fm("init")
        self.hook("UserPromptSubmit", {"prompt": "pause"})
        self.assertTrue(c.read_meta(self.project())["paused"])
        self.hook("UserPromptSubmit", {"prompt": "resume"})
        self.assertFalse(c.read_meta(self.project())["paused"])


class AutonomyWords(HookCase):
    def test_full_auto_and_standard_words_switch_autonomy(self):
        self.fm("init")
        ctx = self.ctx_of(self.hook("UserPromptSubmit", {"prompt": "full auto"}))
        self.assertEqual(c.read_meta(self.project())["autonomy"], "full")
        self.assertIn("Autonomy: full", ctx)
        self.hook("UserPromptSubmit", {"prompt": "Standard autonomy."})
        self.assertEqual(c.read_meta(self.project())["autonomy"], "standard")
        self.hook("UserPromptSubmit", {"prompt": "use the standard library for the full auto-save"})
        self.assertEqual(c.read_meta(self.project())["autonomy"], "standard", "only the whole message switches")


class Approvals(HookCase):
    """fm ask records a request; only the user's next prompt (a hook, never a command) decides it."""

    def ask(self, tid, *cats, session="sess-1"):
        self.fm("ask", tid, *cats, "--why", "needs it", env={"FOREMAN_SESSION_ID": session})

    def allow(self, tid):
        return c.find_brief(self.project(), tid).meta.get("allow") or []

    def pending(self):
        return c.read_meta(self.project()).get("pending_approvals") or []

    def test_yes_grants_and_is_recorded(self):
        self.fm("init")
        tid = self.task()
        self.ask(tid, "core")
        ctx = self.ctx_of(self.hook("UserPromptSubmit", {"prompt": "Yes, go ahead"}))
        self.assertEqual(self.allow(tid), ["core"])
        self.assertIn(f"approved core for {tid}", ctx)
        self.assertEqual(self.pending(), [])
        granted = [e for e in c.ledger_tail(self.project()) if e["event"] == "approval_granted"]
        self.assertEqual((len(granted), granted[0]["task"]), (1, tid))

    def test_other_replies_clear_without_granting(self):
        self.fm("init")
        tid = self.task()
        for reply in ("what would that change?", "no", "yesterday it worked", "not yet"):
            self.ask(tid, "core")
            ctx = self.ctx_of(self.hook("UserPromptSubmit", {"prompt": reply}))
            self.assertEqual(self.allow(tid), [], reply)
            self.assertEqual(self.pending(), [], reply)
            self.assertIn("not granted", ctx)

    def test_reply_in_another_session_does_not_decide(self):
        self.fm("init")
        tid = self.task()
        self.ask(tid, "core", session="sess-1")
        self.hook("UserPromptSubmit", {"prompt": "yes", "session_id": "sess-2"})
        self.assertEqual((self.allow(tid), len(self.pending())), ([], 1))

    def test_pasted_yes_does_not_count(self):
        self.fm("init")
        tid = self.task()
        self.ask(tid, "core")
        self.hook("UserPromptSubmit", {"prompt": "<pasted_content id=a>yes</pasted_content> what is this?"})
        self.assertEqual(self.allow(tid), [])

    def test_one_yes_grants_every_pending_request(self):
        self.fm("init")
        t1 = self.task()
        t2 = self.task("Other", focus=False)
        self.ask(t1, "core")
        self.ask(t2, "publish", "git-destructive")
        self.hook("UserPromptSubmit", {"prompt": "ok"})
        self.assertEqual((self.allow(t1), self.allow(t2)), (["core"], ["publish", "git-destructive"]))

    def test_busy_state_says_the_reply_was_not_recorded(self):
        self.fm("init")
        tid = self.task()
        self.ask(tid, "core")
        with c.lock(self.project().dir):  # another writer holds the project lock the whole time
            p = self.hook("UserPromptSubmit", {"prompt": "yes"}, timeout=20)
        self.assertEqual(p.returncode, 0)
        self.assertIn("not recorded", self.ctx_of(p))
        self.assertEqual((self.allow(tid), len(self.pending())), ([], 1), "nothing granted, request still pending")

    def test_expired_request_is_dropped(self):
        self.fm("init")
        tid = self.task()
        self.ask(tid, "core")
        p = self.project()
        meta = c.read_meta(p)
        meta["pending_approvals"][0]["at"] = "2020-01-01T00:00:00Z"
        c.write_meta(p, meta)
        self.hook("UserPromptSubmit", {"prompt": "yes"})
        self.assertEqual((self.allow(tid), self.pending()), ([], []))


class PreToolUse(HookCase):
    def pre(self, tool, tool_input):
        return self.hook("PreToolUse", {"tool_name": tool, "tool_input": tool_input})

    def test_dangerous_command_is_denied_with_reason(self):
        self.fm("init")
        tid = self.task()
        p = self.pre("Bash", {"command": "npm publish"})
        self.assertEqual(p.returncode, 2)
        out = parse(p)["hookSpecificOutput"]
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertIn(f"fm task set {tid} --allow publish", out["permissionDecisionReason"])
        self.assertIn("guard_block", [e["kind"] for e in self.events()])

    def test_authorized_command_passes(self):
        self.fm("init")
        tid = self.task()
        self.fm("task", "set", tid, "--allow", "publish")
        p = self.pre("Bash", {"command": "npm publish"})
        self.assertEqual(p.returncode, 0)
        self.assertIsNone(((parse(p) or {}).get("hookSpecificOutput") or {}).get("permissionDecision"))

    def test_safe_command_passes_silently(self):
        p = self.pre("Bash", {"command": "pytest -q"})
        self.assertEqual((p.returncode, p.stdout.strip()), (0, ""))

    def test_corrupt_brief_does_not_disable_guard(self):
        self.fm("init")
        tid = self.task()
        self.fm("task", "set", tid, "--allow", "publish")
        with open(c.find_brief(self.project(), tid).path, "w") as f:
            f.write("garbage without frontmatter")
        self.assertEqual(self.pre("Bash", {"command": "npm publish"}).returncode, 2)
        self.assertEqual(self.pre("Bash", {"command": "ls"}).returncode, 0)

    def test_guard_fails_closed_on_malformed_input(self):
        p = self.pre("Bash", "not-a-dict")
        self.assertEqual(p.returncode, 2)
        self.assertIn("guard", p.stderr.lower())

    def test_state_file_write_is_denied(self):
        self.fm("init")
        target = os.path.join(self.project().dir, "STATE.md")
        self.assertEqual(self.pre("Write", {"file_path": target, "content": "x"}).returncode, 2)

    def test_out_of_scope_edit_gets_one_note(self):
        self.fm("init")
        tid = self.task(scope=["src/auth/**"])
        path = os.path.join(self.repo, "docs", "x.md")
        first = self.ctx_of(self.pre("Edit", {"file_path": path, "old_string": "a", "new_string": "b"}))
        self.assertIn(f"outside {tid} scope", first)
        self.assertLessEqual(len(first), 200)
        again = self.pre("Edit", {"file_path": path, "old_string": "a", "new_string": "b"})
        self.assertEqual(self.ctx_of(again), "")
        inside = os.path.join(self.repo, "src", "auth", "login.py")
        self.assertEqual(self.ctx_of(self.pre("Write", {"file_path": inside, "content": "x"})), "")


class PostToolUse(HookCase):
    def test_edit_records_touched_file_and_event(self):
        self.fm("init")
        tid = self.task()
        path = os.path.join(self.repo, "app.py")
        p = self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path}, "tool_response": {},
                                      "duration_ms": 12})
        self.assertEqual(p.returncode, 0)
        touched = [e for e in c.ledger_tail(self.project()) if e["event"] == "touched"]
        self.assertEqual((touched[-1]["task"], touched[-1]["data"]["file"]), (tid, path))
        ev = self.events()[-1]
        self.assertEqual((ev["kind"], ev["tool"], ev["ms"]), ("tool", "Edit", 12))

    def test_failure_event(self):
        self.fm("init")
        self.hook("PostToolUseFailure", {"tool_name": "Bash", "tool_input": {"command": "false"}, "error": "Exit code 1"})
        ev = self.events()[-1]
        self.assertEqual((ev["kind"], ev["ok"]), ("tool_fail", False))


class PreCompact(HookCase):
    def test_checkpoints_active_task_and_never_blocks(self):
        self.fm("init")
        tid = self.task()
        p = self.hook("PreCompact", {"trigger": "auto", "custom_instructions": None})
        self.assertEqual((p.returncode, p.stdout.strip()), (0, ""))
        self.assertIn("<!-- auto -->", c.find_brief(self.project(), tid).section("Resume here"))

    def test_corrupt_state_still_exits_zero(self):
        self.fm("init")
        self.task()
        with open(os.path.join(self.project().dir, "meta.json"), "w") as f:
            f.write("][")
        self.assertEqual(self.hook("PreCompact", {"trigger": "manual"}).returncode, 0)


class Stop(HookCase):
    def stop(self, msg, active=False, session="sess-1"):
        return self.hook("Stop", {"stop_hook_active": active, "last_assistant_message": msg, "session_id": session})

    def decision(self, p):
        return (parse(p) or {}).get("decision")

    def test_premature_done_blocks_once_per_step(self):
        self.fm("init")
        tid = self.task()
        self.fm("drive", "off")
        p = self.stop("All done, the fix is implemented.")
        self.assertEqual(self.decision(p), "block")
        self.assertIn(f"{tid} step 1/2 has no recorded verification evidence", parse(p)["reason"])
        self.assertIsNone(self.decision(self.stop("Done.")))

    def test_stop_hook_active_never_evidence_blocks(self):
        self.fm("init")
        self.task()
        self.fm("drive", "off")
        self.assertIsNone(self.decision(self.stop("Finished!", active=True)))

    def test_negated_claim_and_recorded_evidence_pass(self):
        self.fm("init")
        tid = self.task()
        self.fm("drive", "off")
        self.assertIsNone(self.decision(self.stop("This is not done yet; tests still fail.")))
        self.fm("task", "evidence", tid, "--step", "1", "pytest -k repro", "1 failed as expected")
        self.assertIsNone(self.decision(self.stop("Step 1 is done.")))

    def test_drive_blocks_while_work_remains(self):
        self.fm("init")
        tid = self.task()
        p = self.stop("Continuing with the retry helper next.")
        self.assertEqual(self.decision(p), "block")
        self.assertIn(f"Foreman drive: {tid}", parse(p)["reason"])

    def test_drive_allows_stop_when_asking_the_user(self):
        self.fm("init")
        self.task()
        self.assertIsNone(self.decision(self.stop("Should I use the existing logger or add a new one?")))

    def test_drive_allows_stop_when_paused_off_or_idle(self):
        self.fm("init")
        self.assertIsNone(self.decision(self.stop("Nothing to do.")))
        self.task()
        self.hook("UserPromptSubmit", {"prompt": "pause"})
        self.assertIsNone(self.decision(self.stop("Paused.")))
        self.hook("UserPromptSubmit", {"prompt": "resume"})
        self.fm("drive", "off")
        self.assertIsNone(self.decision(self.stop("ok")))

    def test_drive_allows_stop_when_approval_needed(self):
        self.fm("init")
        tid = self.task(tier="L", focus=False)  # unapproved L can't be focused in standard autonomy
        self.assertIsNone(self.decision(self.stop("Here is the plan for the L-tier change.")))
        self.fm("task", "set", tid, "approved=true")
        self.assertEqual(self.decision(self.stop("Plan approved, starting.")), "block")

    def test_drive_allows_stop_without_progress(self):
        self.fm("init")
        self.task()
        self.assertEqual(self.decision(self.stop("working")), "block")
        self.assertIsNone(self.decision(self.stop("still working", active=True)))

    def test_drive_continues_after_progress(self):
        self.fm("init")
        tid = self.task()
        self.assertEqual(self.decision(self.stop("working")), "block")
        self.fm("task", "evidence", tid, "--step", "1", "pytest", "red as expected")
        self.assertEqual(self.decision(self.stop("working more", active=True)), "block")

    def test_full_autonomy_keeps_going_past_questions_and_unapproved_plans(self):
        self.fm("init")
        self.fm("autonomy", "full")
        self.task(tier="L")
        p = self.stop("Should I use the existing logger or add a new one?")
        self.assertEqual(self.decision(p), "block")
        self.assertIn("fm decide", parse(p)["reason"])

    def test_full_autonomy_skips_work_waiting_on_the_user_and_stops_when_only_that_is_left(self):
        self.fm("init")
        self.fm("autonomy", "full")
        t1 = self.task()
        self.fm("ask", t1, "core", env={"FOREMAN_SESSION_ID": "sess-1"})
        self.assertIsNone(self.decision(self.stop("T-0001 needs your approval for core.")))
        t2 = self.task("Other", focus=False)
        p = self.stop("Waiting on core for T-0001.")
        self.assertEqual(self.decision(p), "block")
        self.assertIn(t2, parse(p)["reason"])
        self.assertIn(f"waiting on the user: {t1}", parse(p)["reason"])

    def test_standard_autonomy_yields_while_an_approval_is_pending(self):
        self.fm("init")
        tid = self.task()
        self.fm("ask", tid, "publish", env={"FOREMAN_SESSION_ID": "sess-1"})
        self.assertIsNone(self.decision(self.stop("Continuing with the release notes.")))

    def test_stop_sets_terminal_title(self):
        self.fm("init")
        self.task()
        self.fm("drive", "off")
        self.assertIn("\x1b]0;foreman", parse(self.stop("ok"))["terminalSequence"])


class TaskCompleted(HookCase):
    def test_mirrored_step_without_evidence_is_refused(self):
        self.fm("init")
        tid = self.task()
        p = self.hook("TaskCompleted", {"task_id": "1", "task_subject": f"{tid} step 1: reproduce"})
        self.assertEqual(p.returncode, 2)
        self.assertIn("evidence", p.stderr)
        self.fm("task", "evidence", tid, "--step", "1", "pytest", "red")
        self.assertEqual(self.hook("TaskCompleted", {"task_id": "1", "task_subject": f"{tid} step 1: reproduce"}).returncode, 0)

    def test_unrelated_task_passes(self):
        self.assertEqual(self.hook("TaskCompleted", {"task_id": "2", "task_subject": "tidy up"}).returncode, 0)


class Subagents(HookCase):
    def test_start_and_stop_are_recorded(self):
        self.fm("init")
        self.task()
        self.hook("SubagentStart", {"agent_id": "a1", "agent_type": "foreman:fm-recon"})
        self.hook("SubagentStop", {"agent_id": "a1", "agent_type": "foreman:fm-recon", "stop_hook_active": False,
                                   "agent_transcript_path": "/x/agent-a1.jsonl", "last_assistant_message": "found 3 things"})
        self.assertEqual([e["kind"] for e in self.events()][-2:], ["subagent_start", "subagent_stop"])
        ev = [e for e in c.ledger_tail(self.project()) if e["event"] == "subagent"][-1]
        self.assertEqual(ev["data"]["agent_type"], "foreman:fm-recon")


class MessageDisplay(HookCase):
    def disp(self, index, delta, final=False):
        return self.hook("MessageDisplay", {"turn_id": "t", "message_id": "m", "index": index, "final": final, "delta": delta})

    def test_badge_on_first_batch_only(self):
        self.fm("init")
        tid = self.task()
        first = parse(self.disp(0, "Here is the plan:\n"))["hookSpecificOutput"]["displayContent"]
        self.assertRegex(first, rf"^\[{tid} FIX · 1/2 · \d\d:\d\d\] Here is the plan:")
        self.assertEqual(self.disp(1, "more text\n").stdout.strip(), "")

    def test_secrets_masked_on_screen(self):
        out = parse(self.disp(3, "key is sk-ant-api03-abcdefghijklmnop\n"))["hookSpecificOutput"]["displayContent"]
        self.assertNotIn("abcdefghijklmnop", out)

    def test_no_badge_when_idle(self):
        self.fm("init")
        self.assertEqual(self.disp(0, "hello\n").stdout.strip(), "")


class NotificationAndEnd(HookCase):
    def test_notification_emits_desktop_sequence(self):
        self.fm("init")
        p = self.hook("Notification", {"message": "Claude needs your permission", "notification_type": "permission_prompt"})
        self.assertIn("\x1b]777;notify;", parse(p)["terminalSequence"])

    def test_session_end_touches_last_active(self):
        self.fm("init")
        before = c.read_meta(self.project())["last_active"]
        self.assertEqual(self.hook("SessionEnd", {"reason": "other"}).returncode, 0)
        self.assertGreaterEqual(c.read_meta(self.project())["last_active"], before)

    def test_unknown_event_is_harmless(self):
        self.assertEqual(self.hook("SomethingNew", {}).returncode, 0)


if __name__ == "__main__":
    unittest.main()
