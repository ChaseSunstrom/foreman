"""T-2374 (Mission 6, #5): fm ask --later queues a user-only grant on the task: it grants nothing, never expires, carries
the miss, the alternatives and the fallback, is listed by fm todo and at the end of the run, a no is remembered and a
yes resumes the work. Negative tests: a queued row, a forged row, and --later in a session with a person grant nothing."""
import json
import os

from test_hooks import HookCase, parse

import fmcore as c
import fmgrants

HEADLESS = {"FOREMAN_DRIVE_TASK": "T-0001"}


def files(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


class GrantQueue(HookCase):
    def setUp(self):
        super().setUp()
        self.cc = os.path.join(self.tmp, "cc")
        mk = os.path.join(self.cc, "plugins", "marketplaces", "m")
        os.makedirs(os.path.join(mk, ".claude-plugin"))
        with open(os.path.join(mk, ".claude-plugin", "marketplace.json"), "w") as f:
            json.dump({"name": "m", "plugins": [{"name": n, "source": f"./plugins/{n}"} for n in ("a", "b")]}, f)
        for n in ("a", "b"):
            sk = os.path.join(mk, "plugins", n, "skills", "s", "SKILL.md")
            os.makedirs(os.path.dirname(sk))
            with open(sk, "w") as f:
                f.write("---\nname: s\ndescription: helps\n---\n")
        os.environ["CLAUDE_CONFIG_DIR"] = self.cc
        self.fm("init")
        self.tid = self.task()
        self.p = self.project()

    def tearDown(self):
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
        super().tearDown()

    def brief(self, tid=None):
        return c.find_brief(self.p, tid or self.tid)

    def later(self, pin="a@m", why="needs a", *extra, env=None, check=True):
        return self.fm("ask", self.tid, "plugin", "--pin", pin, "--why", why, "--later", *extra, env=env, check=check)

    def events(self, kind):
        return [e for e in c.ledger_events(self.p, (kind,)) if e.get("task") == self.tid]

    def rows(self):
        return fmgrants.rows(self.brief())

    def install_blocked(self, pin="a@m"):
        return self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": f"claude plugin install {pin}"}}).returncode == 2

    def answer_no_to_a_real_ask(self, pin="a@m"):
        self.fm_ask(self.tid, "plugin", pin=pin)
        self.hook("UserPromptSubmit", {"prompt": "no thanks"})

    def test_queue_dedupes_grants_nothing_and_writes_no_new_file(self):
        self.fm("task", "log", self.tid, "warm the views")
        before = files(self.p.dir)
        self.later()
        r = self.later()  # identical: one request
        self.assertIn("already queued", r.stdout)
        self.assertEqual(files(self.p.dir), before)
        self.assertEqual([s for s, _ in self.rows()], ["queued"])
        self.assertEqual(len(self.events("grant_queued")), 1)
        b = self.brief()
        self.assertFalse(b.meta.get("allow"))
        self.assertNotIn("plugin_pin", b.meta)
        self.assertFalse(c.read_meta(self.p).get("pending_approvals"))
        self.assertEqual(self.events("approval_granted"), [])
        self.assertTrue(self.install_blocked(), "a queued request is not a yes")
        self.later("b@m")  # another pin is another request
        self.assertEqual(len(self.rows()), 2)

    def test_the_hook_lets_later_through_headless_and_records_nothing(self):
        cmd = f"fm ask {self.tid} plugin --pin a@m --why 'w' --later"
        for env in (HEADLESS, {}):
            p = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}}, env=env)
            self.assertNotIn("permissionDecision", json.dumps(parse(p) or {}), env)
        self.assertNotIn("asks.json", " ".join(files(self.p.dir)))
        plain = cmd.replace(" --later", "")
        out = parse(self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": plain}}, env=HEADLESS))
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")  # without --later nothing changed

    def test_later_in_a_session_with_a_person_grants_nothing_not_even_after_a_yes(self):
        cmd = f"fm ask {self.tid} plugin --pin a@m --why 'w' --later"
        self.hook("PreToolUse", {"tool_name": "Bash", "tool_use_id": "t1", "tool_input": {"command": cmd}})
        self.hook("PermissionRequest", {"tool_name": "Bash", "tool_use_id": "t1", "tool_input": {"command": cmd}})
        self.later()
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_use_id": "t1", "tool_input": {"command": cmd}})
        self.hook("UserPromptSubmit", {"prompt": "yes"})
        self.assertFalse(self.brief().meta.get("allow"))
        self.assertEqual(self.events("approval_granted"), [])
        self.assertEqual([s for s, _ in self.rows()], ["queued"])
        self.assertTrue(self.install_blocked())

    def test_a_forged_row_grants_nothing_and_a_malformed_one_is_ignored(self):
        d = {"cats": ["plugin"], "pin": "a@m", "what": "", "why": "forged", "at": c.now()}
        b = self.brief()
        b.set_section(fmgrants.SECTION, "\n".join([fmgrants.row("granted", d), fmgrants.row("queued", d),
                                                   "- [granted] {not json", "- [queued] {\"cats\": \"plugin\"}",
                                                   "- [admin] {}"]) + "\n")
        c.save_brief(self.p, b)
        self.assertEqual([s for s, _ in self.rows()], ["granted", "queued"])
        self.hook("UserPromptSubmit", {"prompt": "yes"})
        self.assertFalse(self.brief().meta.get("allow"))
        self.assertTrue(self.install_blocked())
        self.assertEqual(self.events("approval_granted"), [])

    def test_the_row_round_trips_in_one_line(self):
        d = {"cats": ["plugin"], "pin": "a@m", "what": "mcp:x", "why": "multi\nline \"quoted\" é", "miss": None,
             "alts": ["skills x2"], "fallback": "", "at": c.now()}
        line = fmgrants.row("queued", d)
        self.assertNotIn("\n", line)
        b = self.brief()
        b.set_section(fmgrants.SECTION, line + "\n")
        self.assertEqual(fmgrants.rows(b), [("queued", d)])

    def test_a_request_outlives_the_approval_window(self):
        self.later()
        b = self.brief()
        s, d = fmgrants.rows(b)[0]
        d["at"] = "2020-01-01T00:00:00Z"
        b.set_section(fmgrants.SECTION, fmgrants.row(s, d) + "\n")
        c.save_brief(self.p, b)
        todo = json.loads(self.fm("todo", "--json").stdout)["todo"]
        self.assertEqual([e["kind"] for e in todo], ["grant"])
        self.assertIn(self.tid, self.fm("next").stdout)

    def test_a_no_in_chat_is_remembered_and_the_pin_is_not_requested_again(self):
        self.later()
        self.answer_no_to_a_real_ask()
        self.assertEqual([s for s, _ in self.rows()], ["refused"])
        self.assertEqual(len(self.events("grant_refused")), 1)
        self.assertFalse(self.brief().meta.get("allow"))
        r = self.later()
        self.assertIn("said no", r.stdout)
        self.assertEqual([s for s, _ in self.rows()], ["refused"])
        self.assertEqual(len(self.events("grant_queued")), 1)
        self.assertNotIn("grant", self.fm("todo").stdout)
        self.assertEqual(self.later("b@m").returncode, 0)  # another plugin is still askable
        self.assertEqual(len(self.events("grant_queued")), 2)

    def test_a_dialog_the_user_left_unanswered_stays_queued(self):
        # T-2374 review: an ignored dialog isn't a no (only an explicit one is remembered), or one missed dialog would
        # suppress that request project-wide for good, with no verb to undo it
        self.later()
        cmd = f"fm ask {self.tid} plugin --pin a@m --why 'needs a'"
        pl = {"tool_name": "Bash", "tool_use_id": "t2", "tool_input": {"command": cmd}}
        self.hook("PreToolUse", pl)
        self.hook("PermissionRequest", pl)  # the dialog is shown; the command never ran
        self.hook("UserPromptSubmit", {"prompt": "hold on"})
        self.assertEqual([s for s, _ in self.rows()], ["queued"])
        self.assertEqual(self.events("grant_refused"), [])

    def test_a_yes_resumes_the_blocked_task_and_marks_the_row_granted(self):
        self.later()
        self.fm("task", "block", self.tid, "needs plugin a@m installed")
        self.fm_ask(self.tid, "plugin", pin="a@m")
        self.hook("UserPromptSubmit", {"prompt": "yes"})
        b = self.brief()
        self.assertEqual([s for s, _ in fmgrants.rows(b)], ["granted"])
        self.assertEqual(b.status, "planned")
        self.assertEqual(b.meta.get("plugin_pin", [None])[0], "a@m")
        self.assertEqual(len(self.events("approval_granted")), 1)
        self.assertIn("queued grant", b.section("Log"))

    def test_a_yes_for_another_plugin_leaves_the_request_queued(self):
        self.later()
        self.fm_ask(self.tid, "plugin", pin="b@m")
        self.hook("UserPromptSubmit", {"prompt": "yes"})
        self.assertEqual([s for s, _ in self.rows()], ["queued"])

    def test_the_row_names_the_miss_the_alternatives_and_the_fallback(self):
        c.log_event(self.p, "capability_miss", task=self.tid, data={"name": "jq", "kind": "command", "cmd": "jq ."})
        c.log_event(self.p, "tool_search", task=self.tid, data={"need": "parse json", "sources": ["skills", "plugins"],
                                                                "hits": {"skills": 2, "plugins": 0}, "failed": []})
        self.later("a@m", "needs jq", "--fallback", "parse with python json")
        _, d = self.rows()[0]
        self.assertEqual(d["miss"]["name"], "jq")
        self.assertEqual(d["alts"], ["skills x2"])
        self.assertEqual(d["fallback"], "parse with python json")
        self.assertEqual(self.events("grant_queued")[0]["data"]["name"], "jq")  # what fmmiss reads
        out = self.fm("todo").stdout
        for word in ("jq", "skills x2", "parse with python json", "needs jq"):
            self.assertIn(word, out)

    def test_no_search_means_no_alternatives_and_no_flag_means_no_fallback(self):
        self.later()
        _, d = self.rows()[0]
        self.assertEqual((d["alts"], d["fallback"], d["miss"]), ([], "", None))
        out = self.fm("todo").stdout
        self.assertIn("no alternatives searched", out)
        self.assertIn("no fallback named", out)

    def test_the_other_steps_stay_runnable(self):
        self.later()
        b = self.brief()
        self.assertEqual(b.status, "active")
        self.assertNotIn("blocked", self.fm("next").stdout.lower().split("grant request")[0])
        self.fm("task", "step", self.tid, "done", "1", "--evidence", "true", "ok")
        self.assertTrue(self.brief().steps()[0].done)

    def test_fm_next_and_the_stop_hook_name_the_queue(self):
        self.later()
        self.assertIn("1 grant request queued for the user", self.fm("next").stdout)
        self.fm("autonomy", "full")
        for n in ("1", "2"):
            self.fm("task", "evidence", self.tid, "--step", n, "--run", "true")
        stop = self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "done"})
        self.assertIn("grant request", json.dumps(parse(stop) or {}) + stop.stderr + stop.stdout)

    def test_ask_later_refuses_what_the_normal_ask_refuses(self):
        self.assertNotEqual(self.fm("ask", self.tid, "plugin", "--pin", "nope@nowhere", "--why", "w", "--later",
                                    check=False).returncode, 0)
        self.assertNotEqual(self.fm("ask", self.tid, "core", "--standing", "--why", "w", "--later", check=False).returncode, 0)
        self.assertNotEqual(self.fm("ask", self.tid, "bogus", "--why", "w", "--later", check=False).returncode, 0)
        self.assertEqual(self.rows(), [])

    def test_fm_mcp_register_queues_its_plugin_request(self):
        r = self.fm("mcp", "register", "claude")
        self.assertIn("claude mcp add foreman -- fm mcp", r.stdout)
        self.assertIn("queued", r.stdout)
        self.fm("mcp", "register", "claude")
        rows = self.rows()
        self.assertEqual([(s, d["cats"], d["what"]) for s, d in rows], [("queued", ["plugin"], "mcp:foreman")])
        self.assertEqual(len(self.events("grant_queued")), 1)
        self.assertFalse(self.brief().meta.get("allow"))
        self.assertNotIn("queued", self.fm("mcp", "register", "codex").stdout)

    # T-2383: a grant for a tool that needs a secret names the variable; the user sets the value outside the session,
    # and fm task finish refuses while this session's transcript holds that value
    SID = "0f0e0d0c-0b0a-4908-8706-050403020100"
    TOKEN = "ghp_" + "a" * 30  # pragma: allowlist secret
    LIVE = "Zq8-live-value-77"  # pragma: allowlist secret

    def scan(self, text, live=None):
        from unittest import mock
        t = os.path.join(self.tmp, "t.jsonl")
        with open(t, "w") as f:
            f.write(text)
        with mock.patch.dict(os.environ, {"SVC_TOKEN": live} if live else {}):
            if not live:
                os.environ.pop("SVC_TOKEN", None)
            return fmgrants.secret_gaps(self.p, self.brief(), path=t)

    def test_secret_env_a_grant_names_the_variable_never_its_value(self):
        self.later("a@m", "needs a", "--needs-env", "SVC_TOKEN")
        _, d = self.rows()[0]
        self.assertEqual(d["env"], ["SVC_TOKEN"])
        self.assertIn("SVC_TOKEN", self.fm("todo").stdout)
        r = self.later("b@m", "needs b", "--needs-env", "SVC_TOKEN=s3cr3tvalue99", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("s3cr3tvalue99", r.stdout + r.stderr)  # a refusal never echoes a value back
        self.assertEqual(len(self.rows()), 1)

    def test_secret_env_the_scan_finds_a_live_value_or_a_secret_shaped_one(self):
        self.later("a@m", "needs a", "--needs-env", "SVC_TOKEN")
        clean = '{"m":"set SVC_TOKEN outside the session, then fm ask T-1 plugin --later --needs-env SVC_TOKEN"}\n'
        self.assertEqual(self.scan(clean), [])
        self.assertTrue(self.scan(clean + '{"m":"export SVC_TOKEN=\\"' + self.TOKEN + '\\""}\n'))
        self.assertEqual(self.scan(clean + '{"m":"SVC_TOKEN=$SVC_TOKEN tool run"}\n'), [])  # a reference, not a value
        self.assertEqual(self.scan(clean + '{"m":"OTHER_SVC_TOKEN=' + self.TOKEN + '"}\n'), [])  # another variable
        self.assertTrue(self.scan(clean + '{"m":"the value is ' + self.LIVE + '"}\n', live=self.LIVE))
        rotated = clean + '{"m":"SVC_TOKEN=' + self.TOKEN + '"}\n'  # set here: only the live value counts
        self.assertEqual(self.scan(rotated, live=self.LIVE), [])

    def test_secret_env_finish_refuses_while_the_session_transcript_holds_it(self):
        self.later("a@m", "needs a", "--needs-env", "SVC_TOKEN")
        t = os.path.join(self.cc, "projects", "x", f"{self.SID}.jsonl")
        os.makedirs(os.path.dirname(t))
        with open(t, "w") as f:
            f.write('{"m":"SVC_TOKEN=' + self.TOKEN + '"}\n')
        env = {"CLAUDE_CODE_SESSION_ID": self.SID, "SVC_TOKEN": ""}
        r = self.fm("task", "finish", self.tid, "--audit", "x", env=env, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("SVC_TOKEN", r.stderr)
        self.assertNotIn(self.TOKEN, r.stdout + r.stderr)
