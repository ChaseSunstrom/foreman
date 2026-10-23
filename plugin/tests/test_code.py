"""T-1212: fm code, the harness-run loop. A scripted fake model server (OpenAI or Anthropic wire shape) answers every
request in order; fm code runs as a real subprocess on a throwaway repo with a seeded bug. No real model, no network."""
import http.server
import json
import os
import subprocess
import sys
import threading
import time

from helpers import FM, PLUGIN, ForemanTestCase, busy_factor, read_json, read_text, stub_corpus_replay

PLAN = {"type": "FIX", "tier": "S", "title": "Make calc.add add",
        "criteria": [{"text": "calc.add adds", "verify": "python3 test_calc.py"}], "steps": ["fix calc.add"]}
HANG = object()


class Fake:
    """Answers each POST with the next scripted reply (a dict: text and/or calls; in: the prompt tokens it reports, 5 unless given) in the profile's wire shape; HANG
    holds the request until release(); past the script it answers 400. Records every request body."""

    def __init__(self, kind, script):
        self.kind, self.script, self.seen = kind, list(script), []
        self.hung, self.release_ = threading.Event(), threading.Event()
        fake = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)))
                fake.seen.append(body)
                step = fake.script.pop(0) if fake.script else None
                if step is HANG:
                    fake.hung.set()
                    fake.release_.wait(10)
                    step = None
                data = json.dumps(fake.reply(step) if step else {"error": "script exhausted"}).encode()
                self.send_response(200 if step else 400)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}/v1"
        threading.Thread(target=self.srv.serve_forever, args=(0.02,), daemon=True).start()

    def reply(self, step):
        calls = [(f"c{len(self.seen)}_{i}", n, a) for i, (n, a) in enumerate(step.get("calls") or [])]
        if self.kind == "anthropic":
            content = ([{"type": "text", "text": step["text"]}] if step.get("text") else []) + [
                {"type": "tool_use", "id": i, "name": n, "input": a} for i, n, a in calls]
            stop = "max_tokens" if step.get("cut") else "tool_use" if calls else "end_turn"
            return {"content": content, "stop_reason": stop, "usage": {"input_tokens": step.get("in", 5), "output_tokens": 2}}
        msg = {"role": "assistant", "content": step.get("text")}
        if calls:
            msg["tool_calls"] = [{"id": i, "type": "function", "function": {"name": n, "arguments": json.dumps(a)}}
                                 for i, n, a in calls]
        stop = "length" if step.get("cut") else "tool_calls" if calls else "stop"
        return {"choices": [{"message": msg, "finish_reason": stop}],
                "usage": {"prompt_tokens": step.get("in", 5), "completion_tokens": 2}}

    def close(self):
        self.release_.set()
        self.srv.shutdown()
        self.srv.server_close()

    def said(self, i):
        """Everything request i sent, flattened to text: what the model was shown."""
        return json.dumps(self.seen[i])


def plan(p=None, prose="Here is the plan:\n"):
    return {"text": prose + "```json\n" + json.dumps(p or PLAN) + "\n```"}


def call(name, **args):
    return {"calls": [(name, args)]}


def text_action(name, **args):
    return {"text": "I'll do this:\n" + json.dumps(dict(args, action=name))}


CLOSE = {"text": json.dumps({"intent": "calc.add adds, as asked", "adversary": "negative numbers add too",
                             "docs": "none: internal fix", "lesson": "none: a one-character bug",
                             "why_not_caught": "none: test_calc.py is the test that catches it"})}


class CodeCase(ForemanTestCase):
    replayed = True  # T-1401: a fresh green guard corpus replay on record, so unattended runs aren't refused

    def setUp(self):
        super().setUp()
        if self.replayed:
            stub_corpus_replay(self.repo)
        with open(os.path.join(self.repo, "calc.py"), "w") as f:
            f.write("def add(a, b):\n    return a - b\n")
        with open(os.path.join(self.repo, "test_calc.py"), "w") as f:
            f.write("import calc\nassert calc.add(2, 3) == 5, calc.add(2, 3)\nprint('ok')\n")
        subprocess.run(["git", "-C", self.repo, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "seed the bug"], check=True)
        self.fake_home = os.path.join(self.tmp, "home")  # rm -rf ~ in a script can only ever reach this
        os.makedirs(self.fake_home)
        with open(os.path.join(self.fake_home, "keep"), "w") as f:
            f.write("x")
        self.fakes = []

    def tearDown(self):
        for f in self.fakes:
            f.close()
        super().tearDown()

    def serve(self, kind, *script, tools=True, name="fake"):
        f = Fake(kind, script)
        self.fakes.append(f)
        path = os.path.join(self.home, "models.json")
        conf = read_json(path) if os.path.exists(path) else {"profiles": {}}
        conf["profiles"][name] = {"kind": kind, "base_url": f.url, "model": "m1", "tools": tools}
        with open(path, "w") as fh:
            json.dump(conf, fh)
        return f

    def env(self, extra=None):
        xdg = {k: os.path.join(self.fake_home, d) for k, d in (  # T-1442: no ~/.config default can reach the real one
            ("XDG_CONFIG_HOME", ".config"), ("XDG_DATA_HOME", ".local/share"), ("XDG_STATE_HOME", ".local/state"),
            ("XDG_CACHE_HOME", ".cache"))}
        e = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1", HOME=self.fake_home, **{**xdg, **(extra or {})})
        e.pop("CLAUDE_CODE_SESSION_ID", None)
        return e

    def code(self, *args, check=True, env=None):
        p = subprocess.run([sys.executable, FM, "code", *args], cwd=self.repo, env=self.env(env), capture_output=True,
                           text=True, timeout=60 * busy_factor())  # T-1721: a hang guard; six builders' load tripped it
        if check and p.returncode:
            raise AssertionError(f"fm code exited {p.returncode}\nstdout:{p.stdout}\nstderr:{p.stderr}")
        return p

    def calc(self):
        return read_text(os.path.join(self.repo, "calc.py"))

    def task(self, tid="T-0001"):
        return self.fm_json("task", "show", tid)

    def last_commit(self):
        return subprocess.run(["git", "-C", self.repo, "show", "--stat", "--format=%s", "HEAD"], capture_output=True,
                              text=True).stdout

    def status(self):
        return subprocess.run(["git", "-C", self.repo, "status", "--porcelain"], capture_output=True, text=True).stdout


class CodeEnv(CodeCase):
    def test_xdg_dirs_stay_inside_the_temp_home(self):  # T-1442
        e = self.env()
        for k in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME"):
            self.assertTrue(e[k].startswith(self.fake_home + os.sep), (k, e[k]))
        outside = self.env({"XDG_CONFIG_HOME": "/elsewhere"})  # a test's own extra still wins
        self.assertEqual(outside["XDG_CONFIG_HOME"], "/elsewhere")


class EndToEnd(CodeCase):
    def run_fix(self, kind):
        f = self.serve(kind, plan(),
                       call("read", path="calc.py"),
                       call("run", cmd="rm -rf ~"),
                       call("edit", file="calc.py", old="a - b", new="a + b"),
                       call("done", summary="calc.add adds now"))
        r = self.code("make calc.add add instead of subtract", "--model", "fake")
        self.assertIn("return a + b", self.calc())
        self.assertEqual(self.task()["status"], "done", r.stdout)
        brief = read_text(self.task()["path"])
        self.assertRegex(brief, r"`python3 test_calc.py` → exit 0")
        self.assertIn("fm code (fake)", brief)  # the audit line names the model
        shown = self.last_commit()
        self.assertIn("T-0001", shown)
        self.assertIn("calc.py", shown)
        # the read's result went back: the model saw the file
        self.assertIn("return a - b", f.said(2))
        # rm -rf ~ never ran, and the guard's refusal is what the model read next
        self.assertTrue(os.path.exists(os.path.join(self.fake_home, "keep")))
        self.assertIn("Foreman guard", f.said(3))
        self.assertIn("refused", f.said(3))
        self.assertIn("calc.py", r.stdout)
        journal = os.path.join(os.path.dirname(os.path.dirname(self.task()["path"])), "code", "T-0001.jsonl")
        kinds = [json.loads(line)["kind"] for line in read_text(journal).splitlines()]
        self.assertEqual((kinds[0], kinds[-1]), ("start", "end"))
        return f

    def test_openai_shape_fixes_the_seeded_bug(self):
        self.run_fix("openai")

    def test_anthropic_shape_works_the_same(self):
        f = self.run_fix("anthropic")
        self.assertIn("tool_result", f.said(3))  # it really spoke the Anthropic wire shape

    def test_json_event_stream_and_no_api_key_reaches_a_command(self):
        f = self.serve("openai", plan(), call("run", cmd="echo key=${OPENAI_API_KEY:-unset}"),
                       call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        r = self.code("fix add", "--model", "fake", "--json", "--no-commit", env={"OPENAI_API_KEY": "sk-SECRET"})
        self.assertIn("key=unset", f.said(2))
        self.assertNotIn("sk-SECRET", json.dumps(f.seen))
        events = [json.loads(line) for line in r.stdout.splitlines()]
        self.assertTrue(all("event" in e for e in events))
        self.assertEqual(events[-1]["event"], "closed")
        self.assertIn("seed the bug", self.last_commit())  # --no-commit: closed, nothing committed
        self.assertIn("calc.py", self.status())


class Repairs(CodeCase):
    def test_malformed_plan_is_repaired_and_dry_plan_changes_nothing(self):
        bad = dict(PLAN, type="BUGFIX", criteria=[{"text": "adds"}])
        f = self.serve("openai", {"text": "Sure! " + json.dumps(bad)}, {"text": "no json at all"}, plan())
        r = self.code("fix add", "--model", "fake", "--dry-plan")
        self.assertIn("Make calc.add add", r.stdout)
        self.assertEqual(len(f.seen), 3)
        self.assertIn("BUGFIX", f.said(1))  # the error quoted back
        self.assertIn("no JSON object", f.said(2))
        self.assertEqual(self.status(), "")
        self.assertNotEqual(self.fm("task", "show", "T-0001", check=False).returncode, 0)  # no task made
        self.assertIn("return a - b", self.calc())

    def test_a_plan_never_repaired_stops_before_any_task(self):
        self.serve("openai", {"text": "nope"}, {"text": "nope"}, {"text": "nope"})
        r = self.code("fix add", "--model", "fake", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("plan", r.stderr + r.stdout)
        self.assertEqual(self.status(), "")

    def test_failing_verify_goes_back_and_a_second_fix_passes(self):
        # a model without native tools: every action is a JSON object in its text
        f = self.serve("openai", plan(),
                       text_action("edit", file="calc.py", old="a - b", new="a * b"),
                       text_action("done", summary="fixed?"),
                       text_action("edit", file="calc.py", old="a * b", new="a + b"),
                       text_action("done", summary="fixed"), tools=False)
        r = self.code("fix add", "--model", "fake")
        self.assertIn("return a + b", self.calc())
        self.assertEqual(self.task()["status"], "done", r.stdout)
        self.assertNotIn("tools", f.seen[1])
        self.assertIn("AssertionError: 6", f.said(3))  # the failing verify's output (a * b) went back to the model

    def test_verify_never_passing_blocks_the_task(self):
        self.serve("openai", plan(), *[call("done", summary="nothing") for _ in range(4)])
        r = self.code("fix add", "--model", "fake", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.task()["status"], "blocked")

    def test_escalate_takes_over_after_three_failed_rounds(self):
        self.serve("openai", plan(), *[call("done", summary="nothing") for _ in range(4)])
        strong = self.serve("anthropic", call("edit", file="calc.py", old="a - b", new="a + b"),
                            call("done", summary="fixed"), name="strong")
        r = self.code("fix add", "--model", "fake", "--escalate", "strong")
        self.assertEqual(self.task()["status"], "done", r.stdout)
        self.assertIn("fix round 4 (strong)", r.stdout)
        self.assertEqual(len(strong.seen), 2)

    def test_a_sensitive_repo_never_reaches_an_offsite_model(self):
        self.fm("init")
        self.fm("sensitive", "on")
        with open(os.path.join(self.home, "models.json"), "w") as fh:
            json.dump({"profiles": {"far": {"base_url": "https://models.example.invalid/v1", "model": "x"}}}, fh)
        r = self.code("fix add", "--model", "far", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("sensitive", r.stderr)

    def test_m_tier_asks_the_model_for_its_close_notes(self):
        f = self.serve("anthropic", plan(dict(PLAN, tier="M")),
                       call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"), CLOSE)
        r = self.code("fix add", "--model", "fake")
        self.assertEqual(self.task()["status"], "done", r.stdout)
        self.assertIn("negative numbers add too", read_text(self.task()["path"]))
        self.assertEqual(len(f.seen), 4)


class AnyRequest(CodeCase):
    """T-1320: fm code takes any request: a question gets an answer (no task, nothing changed), and a plan whose check
    can't run here goes back to the planner instead of ending the run."""

    def test_a_question_is_answered_from_the_files_and_changes_nothing(self):
        f = self.serve("openai", {"text": json.dumps({"answer": "it subtracts"})},
                       call("read", path="calc.py"),
                       call("edit", file="calc.py", old="a - b", new="a + b"),
                       call("done", summary="calc.add returns a - b (calc.py line 2): it subtracts, it doesn't add"))
        r = self.code("what does calc.add do?", "--model", "fake", "--json")
        events = [json.loads(line) for line in r.stdout.splitlines() if line.startswith("{")]
        answer = [e for e in events if e["event"] == "answer"]
        self.assertEqual(len(answer), 1, r.stdout)
        self.assertIn("calc.py line 2", answer[0]["text"])
        self.assertIn("return a - b", self.calc(), "a question changes nothing")
        self.assertIn("refused", f.said(3), "the edit was refused: this run only answers")
        self.assertNotEqual(self.fm("task", "show", "T-0001", check=False).returncode, 0, "no task for a question")

    def test_a_plan_that_also_says_answer_is_a_plan(self):
        both = dict(PLAN, answer="it subtracts")
        self.serve("openai", plan(both), call("edit", file="calc.py", old="a - b", new="a + b"),
                   call("done", summary="adds"))
        r = self.code("fix add", "--model", "fake", check=False)
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)

    def test_a_check_that_cant_run_here_goes_back_to_the_planner(self):
        bad = dict(PLAN, criteria=[{"text": "calc.add adds", "verify": "python3 -m nosuchmod_t1320 -q"}])
        f = self.serve("openai", plan(bad), plan(),
                       call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds"))
        r = self.code("fix add", "--model", "fake", check=False)
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)
        self.assertIn("nosuchmod_t1320", f.said(1), "why it can't run was quoted back")


class Resume(CodeCase):
    def kill_mid_run(self):
        first = self.serve("openai", plan(), call("read", path="calc.py"), HANG)
        p = subprocess.Popen([sys.executable, FM, "code", "fix add", "--model", "fake"], cwd=self.repo, env=self.env(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertTrue(first.hung.wait(30), "fm code never reached the hanging request")
            p.kill()
        finally:
            p.communicate(timeout=30)
        self.assertEqual(self.task()["status"], "active")

    def test_resume_after_a_killed_run_finishes_the_task(self):
        self.kill_mid_run()
        second = self.serve("openai", call("edit", file="calc.py", old="a - b", new="a + b"),
                            call("done", summary="fixed"))
        r = self.code("--resume", "--model", "fake")
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)
        self.assertIn("return a + b", self.calc())
        self.assertIn("return a - b", second.said(0))  # it picked up the conversation, read result and all
        self.assertEqual(len(second.seen), 2)  # no second plan, no second task
        self.assertNotEqual(self.fm("task", "show", "T-0002", check=False).returncode, 0)

    def test_a_kill_between_two_calls_answers_every_unanswered_one(self):
        marker = os.path.join(self.repo, "started")
        first = self.serve("openai", plan(), {"calls": [("read", {"path": "calc.py"}),
                                                        ("run", {"cmd": "touch started; sleep 3"}),
                                                        ("read", {"path": "test_calc.py"})]})
        p = subprocess.Popen([sys.executable, FM, "code", "fix add", "--model", "fake"], cwd=self.repo, env=self.env(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            for _ in range(300):
                if os.path.exists(marker) or p.poll() is not None:
                    break
                threading.Event().wait(0.05)
            p.kill()
        finally:
            p.communicate(timeout=30)
        self.assertTrue(os.path.exists(marker))
        second = self.serve("openai", *FIX)
        self.code("--resume", "--model", "fake")
        sent = second.seen[0]["messages"]
        results = {m["tool_call_id"]: m["content"] for m in sent if m["role"] == "tool"}
        self.assertEqual(len(results), 3, sent)
        self.assertIn("return a - b", results["c2_0"])
        self.assertIn("\nnot run (interrupted)", results["c2_1"])
        self.assertIn("\nnot run (interrupted)", results["c2_2"])
        self.assertEqual(self.task()["status"], "done")

    def test_resume_with_nothing_to_resume_says_so(self):
        r = self.code("--resume", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("nothing to resume", r.stderr)

    def test_claudes_continue_resumes_the_newest_unfinished_run(self):  # T-1399: claude -c
        self.kill_mid_run()
        self.serve("openai", *FIX)
        r = self.code("-c", "--model", "fake")
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)
        self.assertIn("resuming T-0001", r.stdout)


class ClaudeFlags(CodeCase):
    """T-1399: claude's own flags where the meaning matches: -p/--print is --plain, -c/--continue is --resume with no
    id, --output-format json is --json. fm's -p PROJECT still works before the verb (and --project after it)."""

    def test_print_is_plain_and_a_project_before_the_verb_stays_the_project(self):
        import fmcli
        parse = fmcli.build_parser().parse_args
        for flag in ("-p", "--print"):
            a = parse(["code", flag, "x", "--dry-plan"])
            self.assertEqual((a.plain, a.request, a.project, a.dry_plan), (True, ["x"], None, True), flag)
        for flag in ("-c", "--continue"):
            self.assertEqual(parse(["code", flag]).resume, "", flag)
        a = parse(["-p", "SLUG", "code", "x"])
        self.assertEqual((a.project, a.plain), ("SLUG", False))
        self.assertEqual(parse(["code", "--project", "SLUG", "x"]).project, "SLUG")
        slug = self.fm("init").stdout.strip()
        elsewhere = os.path.join(self.tmp, "elsewhere")
        os.makedirs(elsewhere)
        self.serve("openai", plan())
        r = subprocess.run([sys.executable, FM, "-p", slug, "code", "-p", "fix add", "--model", "fake", "--dry-plan"],
                           cwd=elsewhere, env=self.env(), capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Make calc.add add", r.stdout)
        self.assertEqual(self.status(), "")

    def test_output_format_json_is_json_and_any_other_is_refused(self):
        self.serve("openai", plan())
        r = self.code("fix add", "--model", "fake", "--output-format", "json", "--dry-plan")
        events = [json.loads(line) for line in r.stdout.splitlines()]
        self.assertEqual(events[-1]["event"], "plan", r.stdout)
        for value in ("stream-json", "text"):
            r = self.code("fix add", "--output-format", value, check=False)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("--json", r.stderr)


def journal_text(case, tid="T-0001"):
    return read_text(os.path.join(os.path.dirname(os.path.dirname(case.task(tid)["path"])), "code", f"{tid}.jsonl"))


FIX = [call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="fixed")]


class Review(CodeCase):
    def test_credentials_git_and_fifos_are_never_read_or_searched(self):
        with open(os.path.join(self.repo, ".env"), "w") as f:
            f.write("TOKEN_VALUE=hunter2hunter2\n")
        os.mkfifo(os.path.join(self.repo, "pipe"))
        f = self.serve("openai", plan(), call("read", path=".env"), call("read", path=".git/config"),
                       call("read", path="pipe"), call("search", pattern="hunter2"), *FIX)
        self.code("fix add", "--model", "fake")
        sent = json.dumps(f.seen)
        self.assertNotIn("hunter2hunter2", sent)
        self.assertNotIn("repositoryformatversion", sent)
        self.assertIn("pipe", f.said(4))  # the FIFO read answered (refused), it didn't hang

    def test_tool_results_and_the_journal_are_redacted(self):
        with open(os.path.join(self.repo, "notes.txt"), "w") as f:
            f.write("plain plainvalue12345 and ghp_abcdefghijklmnopqrstuvwxyz0123\n")
        f = self.serve("openai", plan(), call("read", path="notes.txt"), *FIX)
        self.code("fix add", "--model", "fake", env={"GROQ_API_KEY": "plainvalue12345"})
        for text in (json.dumps(f.seen), journal_text(self)):
            self.assertNotIn("plainvalue12345", text)
            self.assertNotIn("ghp_abcdefghijklmnopqrstuvwxyz0123", text)
        self.assertIn("plain", f.said(2))

    def test_a_reply_cut_at_the_output_limit_is_not_run(self):
        f = self.serve("openai", plan(), dict(call("write", file="calc.py", content="garbage"), cut=True), *FIX)
        self.code("fix add", "--model", "fake")
        self.assertIn("return a + b", self.calc())
        self.assertIn("cut off", f.said(2))
        self.assertEqual(f.seen[1]["max_tokens"], 8192)

    def test_a_verify_that_already_passes_is_sent_back_once(self):
        weak = dict(PLAN, criteria=[{"text": "it runs", "verify": "true"}])
        f = self.serve("openai", plan(weak), plan(), *FIX)
        r = self.code("fix add", "--model", "fake")
        self.assertIn("proves nothing", f.said(1))
        self.assertEqual(self.task()["status"], "done", r.stdout)

    def test_a_refused_verify_gets_one_replan_then_stops_before_any_task(self):
        bad = dict(PLAN, criteria=[{"text": "clean", "verify": "rm -rf ~"}])
        f = self.serve("openai", plan(bad), plan(bad))
        r = self.code("fix add", "--model", "fake", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("refused", f.said(1))
        self.assertTrue(os.path.exists(os.path.join(self.fake_home, "keep")))
        self.assertNotEqual(self.fm("task", "show", "T-0001", check=False).returncode, 0)

    def test_max_steps_stop_resumes_with_its_options(self):
        f = self.serve("openai", plan(), call("read", path="calc.py"), call("read", path="calc.py"))
        r = self.code("fix add", "--model", "fake", "--no-commit", "--max-steps", "2", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("--resume", r.stdout + r.stderr)
        self.assertEqual(self.task()["status"], "active")
        self.assertNotIn('"end"', journal_text(self))
        self.serve("openai", *FIX)
        r = self.code("--resume", "--max-steps", "6")
        self.assertEqual(self.task()["status"], "done", r.stdout)
        self.assertIn("seed the bug", self.last_commit())  # --no-commit came back from the journal
        self.assertEqual(len(f.seen), 3)

    def test_trim_keeps_the_last_six_results_whole(self):
        import fmcode
        msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "plan"}]
        for i in range(9):
            msgs += [{"role": "assistant", "content": "", "tool_calls": [{"id": f"c{i}", "name": "read", "args": {}}]},
                     {"role": "tool", "tool_call_id": f"c{i}", "content": f"result {i}\n" + "x" * 500}]
        view = fmcode.trim(msgs)
        self.assertEqual(len(view), len(msgs))
        self.assertEqual(view[:2], msgs[:2])
        tools = [m["content"] for m in view if m["role"] == "tool"]
        self.assertTrue(all(len(t) < 120 and t.startswith("(older result cut") for t in tools[:3]), tools[:3])
        self.assertEqual(tools[3:], [m["content"] for m in msgs if m["role"] == "tool"][3:])
        self.assertIn("x" * 500, msgs[3]["content"])  # the stored conversation is untouched


class Models(CodeCase):
    def test_models_lists_the_profiles(self):
        self.serve("openai")
        r = self.code("models")
        self.assertIn("fake", r.stdout)
        self.assertIn("m1", r.stdout)

    def test_unknown_model_is_a_plain_error(self):
        r = self.code("fix it", "--model", "nope", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("nope", r.stderr)
        self.assertNotIn("Traceback", r.stderr)


class TaskRun(CodeCase):
    """T-1330: fm code --task ID works a planned brief: its criteria and steps are the plan, so no planner call."""
    def brief(self, verify="python3 test_calc.py"):
        a = ["task", "new", "make calc.add add", "--type", "FIX", "--tier", "S", "--json", "--step", "fix calc.add"]
        a += ["--ac", f"calc.add adds :: {verify}"] if verify else []
        return json.loads(self.fm(*a).stdout)["id"]

    def test_a_planned_brief_is_worked_without_a_plan_call(self):
        tid = self.brief()
        f = self.serve("openai", call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds"))
        r = self.code("--task", tid, "--model", "fake", "--json", check=False)
        self.assertEqual(self.task(tid)["status"], "done", r.stdout + r.stderr)
        self.assertIn("return a + b", self.calc())
        self.assertIn("step 1", f.said(0), "the first call is the step, not a plan")
        ev = [json.loads(x) for x in r.stdout.splitlines() if x.startswith("{")]
        self.assertEqual([e.get("task") for e in ev if e["event"] == "start"], [tid])

    def test_it_refuses_a_task_it_cant_work_and_says_why(self):
        self.serve("openai", call("done", summary="x"))
        no_check = self.brief(verify=None)
        r = self.code("--task", no_check, "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no criterion", r.stderr)
        dropped = self.brief()
        self.fm("task", "drop", dropped, "not needed")
        r = self.code("--task", dropped, "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("dropped", r.stderr)
        r = self.code("--task", "T-9999", "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("T-9999", r.stderr)
        r = self.code("fix it too", "--task", no_check, "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0, "a request and --task can't both be the plan")

    def test_it_refuses_checks_it_cant_run_and_a_criterion_without_one(self):
        self.serve("openai", call("done", summary="x"))
        ran = []
        for verify, want in (("python3 -m no_such_module_xyz", "can't run here"), ("rm -rf ~", "refused")):
            tid = self.brief()  # fm task new refuses such a check; an edit or a synced brief can still hold one
            self.fm("task", "ac", tid, "edit", "1", "--verify", verify, check=False)
            if self.task(tid)["criteria"][0]["verify"] != verify:
                continue  # refused at the edit too: nothing for fm code to catch
            r = self.code("--task", tid, "--model", "fake", check=False)
            self.assertNotEqual(r.returncode, 0, verify)
            self.assertIn(want, r.stderr, verify)
            ran.append(verify)
        self.assertTrue(ran, "at least one bad check reached fm code")
        tid = self.brief()
        self.fm("task", "ac", tid, "add", "the README says so")  # no check: evidence would land on the wrong number
        r = self.code("--task", tid, "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("criterion 2", r.stderr)

    def test_an_earlier_unfinished_run_of_the_task_is_resumed_not_restarted(self):
        tid = self.brief()
        self.serve("openai", call("done", summary="x"))
        code = os.path.join(os.path.dirname(os.path.dirname(self.task(tid)["path"])), "code")
        os.makedirs(code, exist_ok=True)
        with open(os.path.join(code, f"{tid}.jsonl"), "w") as f:
            f.write(json.dumps({"kind": "start", "task": tid}) + "\n")
        r = self.code("--task", tid.lower(), "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(f"--resume {tid}", r.stderr, "the id is matched whatever its case")

    def test_it_refuses_a_task_another_run_is_working(self):
        import fcntl
        tid = self.brief()
        self.serve("openai", call("done", summary="x"))
        code = os.path.join(os.path.dirname(os.path.dirname(self.task(tid)["path"])), "code")
        os.makedirs(code, exist_ok=True)
        with open(os.path.join(code, f"{tid}.lock"), "w") as held:
            fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)  # as a running fm code holds it
            r = self.code("--task", tid, "--model", "fake", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("another fm code run", r.stderr)


class Failures(CodeCase):  # T-1754 (T-1334, T-1355)
    def test_every_failure_ends_with_one_next_line(self):
        last = lambda r: r.stderr.strip().splitlines()[-1]  # noqa: E731
        self.assertEqual(last(self.code("fix it", "--model", "nope", check=False)), "Next: fm code models")
        self.assertEqual(last(self.code(check=False)), 'Next: fm code "<what to do>"')
        self.serve("openai", plan(), call("read", path="calc.py"))  # the third call runs past the script: a 400
        r = self.code("fix add", "--model", "fake", "--json", check=False)
        self.assertEqual(last(r), "Next: fm code --resume T-0001")
        end = [json.loads(line) for line in r.stdout.splitlines()][-1]
        self.assertEqual((end["event"], end["next"]), ("error", "fm code --resume T-0001"))
        self.serve("openai", plan(), *[call("done", summary="nothing") for _ in range(4)])
        r = self.code("fix add", "--model", "fake", "--json", check=False)
        self.assertEqual(last(r), "Next: fm task show T-0002")
        self.assertEqual([json.loads(line) for line in r.stdout.splitlines()][-1]["next"], "fm task show T-0002")

    def test_the_start_event_names_the_foreman_running_it(self):
        self.serve("openai", plan(), *FIX)
        start = json.loads(self.code("fix add", "--model", "fake", "--json").stdout.splitlines()[0])
        with open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")) as f:
            version = json.load(f)["version"]
        self.assertEqual(start["foreman"], {"root": PLUGIN, "version": version})


def cmdline(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return f.read()
    except OSError:
        return b""


def alive(pid):
    try:
        with open(f"/proc/{pid}/stat") as f:
            return f.read().rsplit(")", 1)[1].split()[0] not in "ZX"
    except OSError:
        return False


class Survivors(CodeCase):  # T-1754 (T-1337)
    def test_a_runner_a_hard_kill_left_is_stopped_by_the_next_start(self):
        self.serve("openai", plan(), call("run", cmd="sleep 120"))
        reg = os.path.join(self.home, "state", "code-procs")
        p = subprocess.Popen([sys.executable, FM, "code", "fix add", "--model", "fake"], cwd=self.repo, env=self.env(),
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(1200):  # the run tool's runner, not the baseline check that runs before it
                names = [n for n in os.listdir(reg) if n.isdigit()] if os.path.isdir(reg) else []
                names = [n for n in names if b"sleep" in cmdline(n)]
                if names:
                    break
                time.sleep(0.05)
            self.assertTrue(names, "the runner was never registered")
            pid = int(names[0])
        finally:
            p.kill()
            p.wait(30)
        self.assertTrue(alive(pid), "the hard kill left the runner going")
        r = self.code("fix it", "--model", "nope", check=False)
        self.assertIn(f"stopped 1 runner(s) a killed fm code left running (pid {pid})", r.stdout + r.stderr)
        for _ in range(100):
            if not alive(pid):
                break
            time.sleep(0.05)
        self.assertFalse(alive(pid))
        self.assertEqual(os.listdir(reg), [])

    def test_a_live_runs_runner_and_a_reused_pid_are_left_alone(self):
        import fmcode
        import fmideas
        live = subprocess.Popen(["sleep", "60"], start_new_session=True)
        other = subprocess.Popen(["sleep", "60"], start_new_session=True)
        try:
            me = os.getpid()
            fmcode._register(live.pid)  # its owner (this test) is alive
            os.makedirs(os.path.join(self.home, "state", "code-procs"), exist_ok=True)
            with open(os.path.join(self.home, "state", "code-procs", str(other.pid)), "w") as f:
                f.write(f"1 {me} 1")  # an owner and runner that aren't the processes these pids now are
            for garbled in ("0", "1"):  # killpg(0) would be this test's own group
                with open(os.path.join(self.home, "state", "code-procs", garbled), "w") as f:
                    f.write("0 999999999 0")
            self.assertEqual(fmcode.stop_survivors(), [])
            self.assertTrue(alive(live.pid) and alive(other.pid))
            self.assertEqual(os.listdir(os.path.join(self.home, "state", "code-procs")), [str(live.pid)])
            self.assertEqual(fmideas._starttime(me), open(os.path.join(  # noqa: SIM115
                self.home, "state", "code-procs", str(live.pid))).read().split()[2])
        finally:
            for x in (live, other):
                x.kill()
                x.wait()


if __name__ == "__main__":
    import unittest
    unittest.main()
