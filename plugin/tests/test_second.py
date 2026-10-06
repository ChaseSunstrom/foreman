"""fm second (T-0276): one primitive for an independent second read — a plan on another model (T-0233), a review's
findings rebutted (T-0232), the last session read for what was missed (T-0235), installed review skills per lens
(T-0230)."""
import json
import os

from helpers import ForemanTestCase

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
stdin = sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin}) + "\n")
system = args[args.index("--append-system-prompt") + 1] if "--append-system-prompt" in args else ""
if "plan" in system.lower():
    text = ("## Objections\n- HIGH: the cache has no invalidation step — stale tokens survive logout\n"
            "- LOW: step 3 duplicates step 2\nVerdict: revise — add invalidation before building")
else:
    text = "## Missed\n- export the report as CSV — asked twice, no task or answer followed\n"
print(json.dumps({"result": text, "total_cost_usd": 0.01}))
'''


class _Stubbed(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.cc = os.path.join(self.tmp, "cc")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log, "CLAUDE_CONFIG_DIR": self.cc}
        self.fm("init")

    def calls(self):
        with open(self.log) as f:
            return [json.loads(x) for x in f]


class Plan(_Stubbed):
    def test_a_rival_model_reviews_the_plan(self):
        tid = json.loads(self.fm("task", "new", "Cache the session token", "--type", "FEATURE", "--tier", "L",
                                 "--ac", "tokens are cached :: true", "--step", "add the cache", "--interpretation",
                                 "keep tokens in memory", "--approach", "dict vs redis → dict", "--json").stdout)["id"]
        out = self.fm("second", "plan", tid, env=self.env).stdout
        self.assertIn("Verdict: revise", out)
        brief = self.fm("task", "show", tid).stdout
        self.assertIn("## Plan review", brief)
        self.assertIn("no invalidation step", brief)
        call = self.calls()[0]
        self.assertIn("dict vs redis", call["stdin"])
        self.assertEqual(call["args"][call["args"].index("--model") + 1], "sonnet")  # not the main model
        self.assertIn("--tools", call["args"])


class Debate(_Stubbed):
    def test_a_rebuttal_brief_embeds_the_review(self):
        tid = json.loads(self.fm("capture", "x", "--json").stdout)["id"]
        review = os.path.join(self.tmp, "review.md")
        with open(review, "w") as f:
            f.write("## adversary: changes needed\n- HIGH fmx.py:12 the token is logged\n")
        self.fm("research", "add", f"{tid}-review-1", "--file", review)
        out = self.fm("second", "debate", tid, "--review", f"{tid}-review-1").stdout
        path = next(w for w in out.split() if w.endswith(".debate.md"))
        with open(path) as f:
            brief = f.read()
        self.assertIn("the token is logged", brief)
        self.assertIn("CONFIRMED", brief)
        self.assertIn("foreman:fm-reviewer", out)

    def test_an_unknown_review_is_refused(self):
        tid = json.loads(self.fm("capture", "x", "--json").stdout)["id"]
        self.assertNotEqual(self.fm("second", "debate", tid, "--review", "nope", check=False).returncode, 0)


class Session(_Stubbed):
    def transcript(self, sid, messages, entrypoint=None):
        import fmcost
        d = fmcost.transcripts_dir(self.repo).replace(os.path.expanduser("~/.claude"), self.cc, 1)
        d = os.path.join(self.cc, "projects", os.path.basename(d))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"{sid}.jsonl"), "w") as f:
            for m in messages:
                f.write(json.dumps(dict({"type": "user", "message": {"role": "user", "content": m}},
                                        **({"entrypoint": entrypoint} if entrypoint else {}))) + "\n")
        return os.path.join(d, f"{sid}.jsonl")

    def test_Interactive_sessions_only(self):
        # T-0307: a newer SDK or claude -p run (a background review, a child) isn't a session the user typed in
        import time
        self.transcript("old-session", ["export the report as CSV please"], entrypoint="cli")
        for i, ep in enumerate(("sdk-py", "sdk-cli")):
            path = self.transcript(f"robot-{i}", ["Review this change for security vulnerabilities"], entrypoint=ep)
            os.utime(path, (time.time() + 10 + i, time.time() + 10 + i))
        self.fm("second", "session", env=dict(self.env, FOREMAN_SESSION_ID="new-session"))
        self.assertIn("export the report as CSV please", self.calls()[0]["stdin"])
        self.assertNotIn("security vulnerabilities", self.calls()[0]["stdin"])

    def test_a_missed_request_is_captured_once(self):
        self.transcript("old-session", ["export the report as CSV please", "<task-notification>x</task-notification>",
                                        "also export the report as CSV"])
        out = self.fm("second", "session", "--if-due", env=dict(self.env, FOREMAN_SESSION_ID="new-session")).stdout
        self.assertIn("export the report as CSV", out)
        inbox = self.fm("state").stdout
        self.assertIn("Export the report as CSV", inbox)
        self.assertIn("export the report as CSV please", self.calls()[0]["stdin"])
        self.assertNotIn("task-notification", self.calls()[0]["stdin"])
        again = self.fm("second", "session", "--if-due", env=dict(self.env, FOREMAN_SESSION_ID="new-session")).stdout
        self.assertIn("already", again.lower())
        self.assertEqual(len(self.calls()), 1)  # once a day

    def test_session_start_runs_it_in_the_background(self):
        import time
        self.transcript("old-session", ["export the report as CSV please"])
        self.hook("SessionStart", {"source": "startup", "session_id": "new-session"},
                  env=dict(self.env, FOREMAN_NO_BACKGROUND=""))
        for _ in range(100):  # detached: the hook returned before the review ran
            if "Export the report as CSV" in self.fm("state").stdout:
                break
            time.sleep(0.1)
        self.assertIn("Export the report as CSV", self.fm("state").stdout)

    def test_secrets_stay_out_and_captures_ask_first(self):
        secret = "sk-ant-api03-" + "A" * 40  # pragma: allowlist secret (a fake key for the redaction test)
        self.transcript("old-session", [f"export the report as CSV please, the key is {secret}"])
        self.fm("second", "session", env=dict(self.env, FOREMAN_SESSION_ID="new-session"))
        self.assertNotIn(secret, self.calls()[0]["stdin"])
        brief = self.fm("task", "show", "T-0001").stdout
        self.assertIn("explore: true", brief)

    def test_a_failed_review_is_recorded_and_claims_the_day(self):
        self.transcript("old-session", ["export the report as CSV please"])
        p = self.fm("second", "session", "--if-due", env=dict(self.env, PATH="/nonexistent"), check=False)
        self.assertNotEqual(p.returncode, 0)
        import fmcore as c
        proj = c.find_project(self.repo)
        self.assertEqual(c.read_meta(proj).get("second_session"), c.now()[:10])
        self.assertTrue(any(e.get("event") == "second_session" and "error" in (e.get("data") or {})
                            for e in c.ledger_tail(proj, 50)))

    def test_a_sensitive_project_is_skipped(self):
        self.transcript("old-session", ["export the report as CSV please"])
        self.fm("sensitive", "on")
        out = self.fm("second", "session", "--if-due", env=self.env).stdout
        self.assertIn("sensitive", out.lower())
        self.assertFalse(os.path.exists(self.log))


class Due(ForemanTestCase):
    def test_only_new_sessions_once_a_day_never_sensitive(self):
        import fmcore as c
        import fmhooks
        today = c.now()[:10]
        self.assertTrue(fmhooks.second_due({"source": "startup"}, {}))
        self.assertFalse(fmhooks.second_due({"source": "compact"}, {}))
        self.assertFalse(fmhooks.second_due({"source": "startup"}, {"second_session": today}))
        self.assertFalse(fmhooks.second_due({"source": "startup"}, {"sensitive": True}))
        self.assertFalse(fmhooks.second_due({"source": "startup"}, {}, busy=True))


class LensSkills(ForemanTestCase):
    def test_audit_prep_names_installed_review_skills_per_lens(self):
        cc = os.path.join(self.tmp, "cc")
        path = os.path.join(cc, "plugins", "cache", "m", "sec", "1.0")
        os.makedirs(os.path.join(path, "skills", "sec-scan"))
        with open(os.path.join(path, "skills", "sec-scan", "SKILL.md"), "w") as f:
            f.write("---\nname: sec-scan\ndescription: Security vulnerability review of a diff.\n---\nbody\n")
        os.makedirs(os.path.join(cc, "plugins"), exist_ok=True)
        with open(os.path.join(cc, "plugins", "installed_plugins.json"), "w") as f:
            json.dump({"version": 2, "plugins": {"sec@m": [{"scope": "user", "installPath": path}]}}, f)
        with open(os.path.join(cc, "settings.json"), "w") as f:
            json.dump({"enabledPlugins": {"sec@m": True}}, f)
        self.fm("init")
        tid = json.loads(self.fm("task", "new", "x", "--type", "FIX", "--tier", "M", "--ac", "x :: true", "--step", "x",
                                 "--interpretation", "x", "--approach", "x", "--json").stdout)["id"]
        self.fm("focus", tid)
        with open(os.path.join(self.repo, "a.py"), "w") as f:
            f.write("x = 1\n")
        out = self.fm("audit", "prep", tid, env={"CLAUDE_CONFIG_DIR": cc}).stdout
        self.assertIn("adversary: /sec:sec-scan, /security-review", out)
        self.assertIn(f"fm task audit {tid} adversary", out)
        data = json.loads(self.fm("audit", "prep", tid, "--json", env={"CLAUDE_CONFIG_DIR": cc}).stdout)
        self.assertEqual(data["lens_skills"]["adversary"][0], "/sec:sec-scan")

    def test_lens_tables_are_validated(self):
        from fmcore import routing_problem
        good = {"lens_words": {"adversary": ["security"]}, "lens_builtin": {"adversary": ["security-review"]}}
        self.assertIsNone(routing_problem(good))
        self.assertIsNotNone(routing_problem(dict(good, lens_words={"adversary": "security"})))
        self.assertIsNotNone(routing_problem(dict(good, lens_builtin={"adversary": ["x; rm -rf /tmp/y"]})))
