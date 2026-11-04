"""T-2998: sampo watch --web: a read-only, loopback-only server (settingsserve's token, cookie, Host check and CSP) with one
snapshot at /api/state and the same as a Server-Sent Events stream at /api/stream. A collector that fails leaves its field
empty; the snapshot names jobs, loaded models with VRAM, the GPU and the last minute's flows from calls already logged."""
import http.client
import json
import os
import threading
import time
import unittest.mock as mock

from helpers import ForemanTestCase

from sampo import core as c
from sampo import live

FIELDS = {"at", "project", "focus", "queue", "closed_today", "lanes", "jobs", "models", "gpu", "flows", "events", "stats"}


class Snapshot(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Show the live page", "--type", "FEATURE", "--tier", "S", "--ac", "it shows :: true",
                "--step", "build it", "--focus")
        self.p = c.find_project(self.repo)
        live._CACHE.clear()

    def test_every_field_of_the_contract_is_there_and_json(self):
        s = live.snapshot(self.p)
        self.assertEqual(set(s), FIELDS)
        json.dumps(s)
        self.assertEqual(s["project"]["slug"], self.p.slug)
        self.assertEqual(s["focus"]["step"], "0/1")
        self.assertEqual(s["focus"]["title"], "Show the live page")
        self.assertEqual([q["title"] for q in s["queue"]], ["Show the live page"])

    def test_a_failing_collector_leaves_its_field_empty_the_rest_stand(self):
        def boom(p):
            raise RuntimeError("down")
        with mock.patch.dict(live.COLLECTORS, {"gpu": boom, "models": boom, "jobs": boom, "flows": boom}):
            s = live.snapshot(self.p)
        self.assertEqual((s["gpu"], s["models"], s["jobs"], s["flows"]), (None, [], [], []))
        self.assertEqual(s["project"]["slug"], self.p.slug)

    def test_jobs_models_gpu_and_flows_from_fakes(self):
        procs = [(4242, "python3 plugin/bin/sampo moons funnel --stage kill"), (1, "bash")]
        ps = {"models": [{"name": "qwen3:14b", "size_vram": 9728 * 1048576, "size": 10000 * 1048576}]}
        smi = "NVIDIA RTX 4090, 11000, 24564, 37\n"
        with mock.patch.object(live, "_procs", return_value=procs), mock.patch.object(live, "_get_json", side_effect=[ps, None]), \
                mock.patch.object(live, "_smi", return_value=smi):
            c.log_event(self.p, "cards_grow", data={"calls": 3, "models": {"qwen3:14b": 3}})
            s = live.snapshot(self.p)
        self.assertEqual([(j["name"], j["kind"], j["pid"]) for j in s["jobs"]], [("moons funnel --stage kill", "funnel", 4242)])
        m = {x["name"]: x for x in s["models"]}["qwen3:14b"]
        self.assertEqual((m["family"], m["where"], m["loaded"], m["vram_mb"]), ("ollama", "gpu", True, 9728))
        self.assertEqual(s["gpu"], {"name": "NVIDIA RTX 4090", "used_mb": 11000, "total_mb": 24564, "util_pct": 37})
        self.assertEqual([(f["from"], f["to"], f["kind"]) for f in s["flows"]], [("card grow", "qwen3:14b", "write")])
        self.assertIn("cards_grow", [e["kind"] for e in s["events"]])

    def test_flows_older_than_a_minute_are_out_and_event_text_is_redacted(self):
        old = c.log_event(self.p, "cards_grow", data={"models": {"haiku": 1}})
        with mock.patch.object(c, "now", return_value="2026-01-01T00:00:00Z"):
            c.log_event(self.p, "cards_grow", data={"models": {"old-one": 1}, "note": "sk-ant-api03-" + "a" * 40})
        s = live.snapshot(self.p)
        self.assertEqual([f["to"] for f in s["flows"]], ["haiku"])
        self.assertNotIn("a" * 40, json.dumps(s))
        self.assertTrue(old)

    def test_logged_model_calls_become_lanterns_and_flows(self):  # T-3014 live: Jarvis and Smith never showed
        from sampo import models
        with mock.patch.object(models.sys, "argv", ["sampo", "exam", "run", "s5-019", "--model", "jarvis"]):
            models.note_call({"name": "jarvis", "model": "qwen3.8-27b", "base_url": "https://jarvis.example/llm/v1"})
        with mock.patch.object(models.sys, "argv", ["sampo", "playbooks", "small", "grow"]):
            models.note_call({"name": "gpu-qwen4", "model": "qwen3.5:4b", "base_url": "http://127.0.0.1:11434/v1"})
        with mock.patch.object(live, "_get_json", return_value=None):
            s = live.snapshot(self.p)
        self.assertEqual(sorted((f["from"], f["to"], f["kind"]) for f in s["flows"]),
                         [("exam run", "jarvis", "act"), ("playbooks small grow", "qwen3.5:4b", "write")])
        m = {x["name"]: x for x in s["models"]}
        self.assertEqual((m["jarvis"]["where"], m["jarvis"]["calls_5m"]), ("remote", 1))

    def test_a_child_under_a_temp_home_logs_to_the_inherited_file(self):  # T-3014: exam Smith runs
        from sampo import models
        path = os.path.join(self.tmp, "real-calls.jsonl")
        with mock.patch.dict(os.environ, {"SAMPO_CALLS": path}):
            models.note_call({"name": "jarvis", "model": "qwen3.8-27b", "base_url": "https://jarvis.example/v1"})
        with open(path) as f:
            self.assertEqual(json.loads(f.read())["to"], "jarvis")
        self.assertFalse(os.path.exists(os.path.join(c.state_dir(), models.CALLS)))

    def test_complete_and_embed_log_their_calls_even_when_the_call_fails(self):  # T-3014 review
        from sampo import models
        prof = {"name": "gpu-x", "kind": "openai", "base_url": "http://127.0.0.1:11434/v1", "model": "m:1", "key_env": None}
        with mock.patch.object(models, "_post", side_effect=models.ModelError("down")):
            for call in (lambda: models.complete(prof, [{"role": "user", "content": "hi"}]),
                         lambda: models.embed(prof, ["a"])):
                with self.assertRaises(models.ModelError):
                    call()
        with open(os.path.join(c.state_dir(), models.CALLS)) as f:
            rows = [json.loads(x) for x in f]
        self.assertEqual([(r["to"], r.get("kind")) for r in rows], [("m:1", None), ("m:1", "embed")])
        with mock.patch.object(live, "_get_json", return_value=None):
            self.assertIn("embed", [f["kind"] for f in live.snapshot(self.p)["flows"]])

    def test_the_cli_hands_its_call_log_to_children(self):  # T-3014 review: an exam's Smith under a temp home
        from sampo import cli
        with mock.patch.dict(os.environ), mock.patch.object(cli.sys, "argv", ["sampo", "--version"]):
            os.environ.pop("SAMPO_CALLS", None)
            with self.assertRaises(SystemExit):
                cli.main()
            self.assertEqual(os.environ.get("SAMPO_CALLS"), os.path.join(c.state_dir(), "calls.jsonl"))

    def test_the_call_log_rotates_past_its_cap(self):
        from sampo import models
        with mock.patch.object(models, "CALLS_CAP", 200):
            for _ in range(10):
                models.note_call({"name": "gpu-qwen4", "model": "qwen3.5:4b", "base_url": "http://127.0.0.1:11434/v1"})
        path = os.path.join(c.state_dir(), models.CALLS)
        self.assertLessEqual(os.path.getsize(path), 200 + 200)
        self.assertTrue(os.path.exists(path + ".1"))

    def test_events_read_in_words(self):  # T-3014 live: the ticker printed {"file": "/home/…", "tool": "Edit"}
        c.log_event(self.p, "touched", task="T-0001", data={"file": "/home/x/proj/plugin/tests/test_traces.py", "tool": "Edit"})
        c.log_event(self.p, "evidence", task="T-0001", data={"step": 3, "ac": None, "cmd": "python3 plugin/bin/sampo shot x"})
        text = {e["kind"]: e["text"] for e in live.snapshot(self.p)["events"]}
        self.assertEqual(text["touched"], "T-0001 Edit test_traces.py")
        self.assertEqual(text["evidence"], "T-0001 step 3 · python3 plugin/bin/sampo shot x")
        self.assertNotIn("{", text["touched"] + text["evidence"])

    def test_the_snapshot_is_cached_a_moment(self):
        with mock.patch.object(live, "_procs", return_value=[]) as g:
            live.snapshot(self.p)
            live.snapshot(self.p)
        self.assertEqual(g.call_count, 1)


class Serve(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Serve it", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        live._CACHE.clear()
        self.p = c.find_project(self.repo)
        self.server, self.token = live.make(self.p)
        self.port = self.server.server_address[1]
        self.stop = threading.Event()
        self.server.stop = self.stop
        self.thread = threading.Thread(target=live.serve, args=(self.server, self.stop), daemon=True)
        self.thread.start()
        self.cookie = None

    def tearDown(self):
        self.stop.set()
        self.thread.join(5)
        super().tearDown()

    def req(self, path="/", cookie=True, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        h = {"Host": f"127.0.0.1:{self.port}", **(headers or {})}
        if cookie and self.cookie:
            h["Cookie"] = self.cookie
        conn.request("GET", path, headers=h)
        r = conn.getresponse()
        out = r.status, r.read().decode(), dict(r.getheaders())
        conn.close()
        return out

    def login(self):
        st, _, h = self.req(f"/?t={self.token}", cookie=False)
        self.assertEqual(st, 303)
        self.cookie = h["Set-Cookie"].split(";")[0]

    def test_bound_to_loopback_only(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")

    def test_no_cookie_bad_host_and_the_token_works_once(self):
        for path in ("/", "/api/state", "/api/stream"):
            self.assertEqual(self.req(path, cookie=False)[0], 403)
        self.assertEqual(self.req("/", cookie=False, headers={"Host": "evil.example"})[0], 403)
        self.login()
        self.assertEqual(self.req(f"/?t={self.token}", cookie=False)[0], 403)  # spent
        self.assertEqual(self.req("/", headers={"Host": "evil.example"})[0], 403)  # a good cookie, a rebound host

    def test_state_is_json_with_the_contract_fields_and_a_csp(self):
        self.login()
        st, body, h = self.req("/api/state")
        self.assertEqual(st, 200)
        self.assertIn("application/json", h["Content-Type"])
        self.assertEqual(set(json.loads(body)), FIELDS)
        self.assertEqual(self.req("/api/nope")[0], 404)
        st, page, h = self.req("/")
        self.assertEqual(st, 200)
        self.assertIn("default-src 'none'", h["Content-Security-Policy"])
        self.assertNotIn("unsafe", h["Content-Security-Policy"])

    def test_a_collector_that_raises_is_not_a_500(self):
        self.login()

        def boom(p):
            raise OSError("no")
        with mock.patch.dict(live.COLLECTORS, {"jobs": boom, "stats": boom}):
            st, body, _ = self.req("/api/state")
        self.assertEqual(st, 200)
        self.assertEqual(json.loads(body)["jobs"], [])

    def test_static_files_come_from_the_folder_and_nothing_outside_it(self):
        self.login()
        d = os.path.join(self.tmp, "web")
        os.makedirs(d)
        with open(os.path.join(d, "live.css"), "w") as f:
            f.write("body{}")
        with mock.patch.object(live, "WEB", d):
            st, body, h = self.req("/static/live.css")
            self.assertEqual((st, body, h["Content-Type"].split(";")[0]), (200, "body{}", "text/css"))
            self.assertEqual(self.req("/static/..%2Flive.css")[0], 404)
            self.assertEqual(self.req("/static/../../x")[0], 404)
            self.assertEqual(self.req("/static/missing.js")[0], 404)

    def test_fonts_are_served_as_bytes(self):  # T-3014 live: every font fell back, _static 404'd anything not text
        self.login()
        d = os.path.join(self.tmp, "web")
        os.makedirs(d)
        raw = b"wOF2\x00\x01\xff\xfe" * 8
        with open(os.path.join(d, "A-normal.woff2"), "wb") as f:
            f.write(raw)
        with mock.patch.object(live, "WEB", d):
            conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
            conn.request("GET", "/static/A-normal.woff2", headers={"Host": f"127.0.0.1:{self.port}", "Cookie": self.cookie})
            r = conn.getresponse()
            self.assertEqual((r.status, r.getheader("Content-Type"), r.read()), (200, "font/woff2", raw))
            conn.close()
            self.assertEqual(self.req("/static/..%2FA-normal.woff2")[0], 404)

    def test_the_stream_sends_state_events(self):
        self.login()
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", "/api/stream", headers={"Host": f"127.0.0.1:{self.port}", "Cookie": self.cookie})
        r = conn.getresponse()
        self.assertEqual((r.status, r.getheader("Content-Type")), (200, "text/event-stream"))
        self.assertEqual(r.readline().decode().strip(), "event: state")
        data = r.readline().decode()
        self.assertTrue(data.startswith("data: "))
        self.assertEqual(set(json.loads(data[6:])), FIELDS)
        conn.close()

    def test_a_spent_token_is_replaced_and_the_url_file_follows(self):
        self.login()
        deadline = time.monotonic() + 5
        while self.server.token is None and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertIsNotNone(self.server.token)  # a fresh one, so `sampo watch --web --url` always prints a URL that works
        self.assertNotEqual(self.server.token, self.token)


class Url(ForemanTestCase):
    def test_url_reprints_what_the_server_wrote(self):
        self.fm("task", "new", "x", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        p = c.find_project(self.repo)
        self.assertNotEqual(self.fm("watch", "--web", "--url", check=False).returncode, 0)  # none running
        live.write_url(p, "http://127.0.0.1:1/?t=abc")
        out = self.fm("watch", "--web", "--url")
        self.assertEqual(out.stdout.strip(), "http://127.0.0.1:1/?t=abc")
        self.assertEqual(os.stat(os.path.join(p.dir, "live.url")).st_mode & 0o777, 0o600)
