"""T-1212: fm code, the harness-run loop. A scripted fake model server (OpenAI or Anthropic wire shape) answers every
request in order; fm code runs as a real subprocess on a throwaway repo with a seeded bug. No real model, no network."""
import http.server
import json
import os
import subprocess
import sys
import threading

from helpers import FM, ForemanTestCase, read_json, read_text

PLAN = {"type": "FIX", "tier": "S", "title": "Make calc.add add",
        "criteria": [{"text": "calc.add adds", "verify": "python3 test_calc.py"}], "steps": ["fix calc.add"]}
HANG = object()


class Fake:
    """Answers each POST with the next scripted reply (a dict: text and/or calls) in the profile's wire shape; HANG
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
            return {"content": content, "stop_reason": "tool_use" if calls else "end_turn",
                    "usage": {"input_tokens": 5, "output_tokens": 2}}
        msg = {"role": "assistant", "content": step.get("text")}
        if calls:
            msg["tool_calls"] = [{"id": i, "type": "function", "function": {"name": n, "arguments": json.dumps(a)}}
                                 for i, n, a in calls]
        return {"choices": [{"message": msg, "finish_reason": "tool_calls" if calls else "stop"}],
                "usage": {"prompt_tokens": 5, "completion_tokens": 2}}

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
    def setUp(self):
        super().setUp()
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
        e = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1", HOME=self.fake_home, **(extra or {}))
        e.pop("CLAUDE_CODE_SESSION_ID", None)
        return e

    def code(self, *args, check=True, env=None):
        p = subprocess.run([sys.executable, FM, "code", *args], cwd=self.repo, env=self.env(env), capture_output=True,
                           text=True, timeout=60)
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


class Resume(CodeCase):
    def test_resume_after_a_killed_run_finishes_the_task(self):
        first = self.serve("openai", plan(), call("read", path="calc.py"), HANG)
        p = subprocess.Popen([sys.executable, FM, "code", "fix add", "--model", "fake"], cwd=self.repo, env=self.env(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertTrue(first.hung.wait(30), "fm code never reached the hanging request")
            p.kill()
        finally:
            p.communicate(timeout=30)
        self.assertEqual(self.task()["status"], "active")
        second = self.serve("openai", call("edit", file="calc.py", old="a - b", new="a + b"),
                            call("done", summary="fixed"))
        r = self.code("--resume", "--model", "fake")
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)
        self.assertIn("return a + b", self.calc())
        self.assertIn("return a - b", second.said(0))  # it picked up the conversation, read result and all
        self.assertEqual(len(second.seen), 2)  # no second plan, no second task
        self.assertNotEqual(self.fm("task", "show", "T-0002", check=False).returncode, 0)

    def test_resume_with_nothing_to_resume_says_so(self):
        r = self.code("--resume", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("nothing to resume", r.stderr)


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


if __name__ == "__main__":
    import unittest
    unittest.main()
