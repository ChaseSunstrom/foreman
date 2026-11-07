"""T-3597: chat calls to the local Ollama take turns on its GPU when their models can't share it (they were seen
together in /api/ps, or they take turns); T-3598: /api/tags and the /models probe of the box's servers are read once a
minute per process; T-3599: a model Ollama can't load (unknown model architecture) is asked once, then skipped. A fake
Ollama only; no test reaches a live server."""
import http.server
import json
import os
import subprocess
import threading
import time
from unittest import mock

import test_models as tm
from sampo import models as m

LFM = "lfm3:1.7b"
UNKNOWN = {"error": "llama-server process has terminated: exit status 1: error loading model: unknown model "
                    "architecture: 'lfm3'"}


class Ollama:
    """A fake Ollama: /api/tags, /v1/models, /api/show, /api/ps (`loaded`, wholly in VRAM) and chat. A chat for a model
    in `gates` waits for that event; .log holds (event, model, time) for every chat start and end."""

    def __init__(self, loaded=()):
        self.loaded, self.gates, self.log, self.hits = list(loaded), {}, [], {}
        o = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def reply(self, code, body):
                data = json.dumps(body).encode()
                self.send_response(code)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                o.hits[self.path] = o.hits.get(self.path, 0) + 1
                if self.path == "/api/tags":
                    return self.reply(200, {"models": [{"name": "a:1b"}, {"name": "b:1b"}]})
                if self.path == "/v1/models":
                    return self.reply(200, {"data": [{"id": "a:1b"}, {"id": "b:1b"}]})
                if self.path == "/api/ps":
                    return self.reply(200, {"models": [{"name": n, "model": n, "size": 10, "size_vram": 10}
                                                       for n in o.loaded]})
                self.reply(404, {})

            def do_POST(self):
                o.hits[self.path] = o.hits.get(self.path, 0) + 1
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                if self.path == "/api/show":
                    return self.reply(200, {"parameters": "num_ctx 8192"})
                model = body.get("model")
                if model == LFM:
                    return self.reply(500, UNKNOWN)
                o.log.append(("start", model, time.monotonic()))
                gate = o.gates.get(model)
                if gate:
                    gate.wait(10)
                o.log.append(("end", model, time.monotonic()))
                self.reply(200, tm.oa_reply("ok"))

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}/v1"
        threading.Thread(target=self.srv.serve_forever, args=(0.02,), daemon=True).start()

    def started(self, model):
        return any(e == "start" and x == model for e, x, _ in self.log)

    def close(self):
        for g in self.gates.values():
            g.set()
        self.srv.shutdown()
        self.srv.server_close()


class Case(tm.Base):
    def setUp(self):
        super().setUp()
        os.makedirs(m.state_dir(), exist_ok=True)
        self.o = Ollama()
        self.addCleanup(self.o.close)
        m.LOCAL = [("ollama", self.o.url)]  # this fake is the box's Ollama
        for k, v in (("GPU_POLL", 0.02), ("GPU_HOLD", 0.0), ("GPU_TURN", 60.0)):
            p = mock.patch.object(m, k, v)
            p.start()
            self.addCleanup(p.stop)

    def prof(self, model):
        return {"name": model, "kind": "openai", "base_url": self.o.url, "model": model, "key_env": None,
                "context": 8192, "tools": True}

    def ask(self, model, out):
        def run():
            try:
                out[model] = m.complete(self.prof(model), [{"role": "user", "content": "hi"}], max_tokens=5)["text"]
            except m.ModelError as e:
                out[model] = e
        t = threading.Thread(target=run)
        t.start()
        return t

    def until(self, cond, s=5.0):
        end = time.monotonic() + s
        while not cond() and time.monotonic() < end:
            time.sleep(0.01)
        return cond()

    def ledger(self):
        with open(m._gpu_file(), encoding="utf-8") as f:
            return json.load(f)


class Turns(Case):
    def test_a_second_model_waits_until_the_first_models_call_ends(self):
        self.o.gates["a:1b"], out = threading.Event(), {}
        ta = self.ask("a:1b", out)
        self.assertTrue(self.until(lambda: self.o.started("a:1b")))
        tb = self.ask("b:1b", out)
        time.sleep(0.4)
        self.assertFalse(self.o.started("b:1b"), "b:1b reached Ollama while a:1b was mid-call: it evicts a:1b")
        self.o.gates["a:1b"].set()
        ta.join(5)
        tb.join(5)
        self.assertEqual(out, {"a:1b": "ok", "b:1b": "ok"})
        a_end = next(t for e, x, t in self.o.log if e == "end" and x == "a:1b")
        b_start = next(t for e, x, t in self.o.log if e == "start" and x == "b:1b")
        self.assertLess(a_end, b_start)
        self.assertEqual(self.ledger()["calls"], {})  # every call gave its turn back

    def test_models_seen_together_in_ps_share_the_gpu(self):
        self.o.loaded = ["a:1b", "b:1b"]
        self.o.gates["a:1b"], out = threading.Event(), {}
        ta = self.ask("a:1b", out)
        self.assertTrue(self.until(lambda: self.o.started("a:1b")))
        tb = self.ask("b:1b", out)
        self.assertTrue(self.until(lambda: self.o.started("b:1b")), "b:1b fits beside a:1b, yet it waited")
        self.o.gates["a:1b"].set()
        ta.join(5)
        tb.join(5)
        self.assertEqual(out, {"a:1b": "ok", "b:1b": "ok"})

    def test_a_dead_process_holds_no_turn(self):
        dead = subprocess.Popen(["true"])
        dead.wait()
        with open(m._gpu_file(), "w", encoding="utf-8") as f:
            json.dump({"calls": {"x": {"model": "a:1b", "pid": dead.pid, "since": time.time()}}}, f)
        out = {}
        self.ask("b:1b", out).join(5)
        self.assertEqual(out, {"b:1b": "ok"})

    def test_hold_and_turn_rules(self):
        now, me, pid = 1000.0, "me", 42

        def st(**kw):
            return {**{k: {} for k in m.LEDGER}, **kw}

        def may(s, model="b", who=me):
            return m._gpu_may(s, who, model, now, pid)
        held = {"a": {"t": now - 5, "pid": 7}}
        a_mid = {"x": {"model": "a", "pid": 1}}
        with mock.patch.object(m, "GPU_HOLD", 20.0), mock.patch.object(m, "GPU_TURN", 120.0):
            self.assertTrue(may(st()))
            self.assertTrue(may(st(calls={"x": {"model": "b", "pid": 1}})))  # same model: shares
            self.assertFalse(may(st(calls=a_mid)))
            self.assertFalse(may(st(last=held)))  # another process's a still holds it
            self.assertTrue(may(st(last={"a": {"t": now - 25, "pid": 7}})))  # a's hold ran out
            self.assertTrue(may(st(last={"a": {"t": now - 5, "pid": pid}})))  # its own hold never stops a process
            waited = {me: {"model": "b", "pid": 1, "since": now - 121}}
            self.assertTrue(may(st(last=held, wait=waited)))  # b waited a turn
            self.assertFalse(may(st(last=held, wait=waited), "a", "new"))  # so a's next call waits
            self.assertFalse(may(st(calls=a_mid, wait=waited)))  # until a drains
            older = {"o": {"model": "a", "pid": 1, "since": now - 200}, **waited}
            self.assertFalse(may(st(wait=older)))  # the longest-waiting model goes first
            self.assertTrue(may(st(wait=older), "a", "o"))
            self.assertTrue(may(st(calls=a_mid, fit={"a\nb": now - 60})))
            self.assertFalse(may(st(calls=a_mid, fit={"a\nb": now - 90000})))  # a fit seen a day ago is not trusted
            self.assertTrue(may(st(calls=a_mid, size={"a": 3, "b": 4}, gpu={"cap": 10})))  # 7 <= 0.8 x 10: fits
            self.assertFalse(may(st(calls=a_mid, size={"a": 3, "b": 6}, gpu={"cap": 10})))
            self.assertFalse(may(st(calls=a_mid, size={"a": 3}, gpu={"cap": 10})))  # b's size unknown: turns

    def test_an_untagged_model_matches_its_latest_tag_in_ps(self):
        self.o.loaded = ["a:latest", "b:1b"]
        self.o.gates["a"], out = threading.Event(), {}
        ta = self.ask("a", out)
        self.assertTrue(self.until(lambda: self.o.started("a")))
        tb = self.ask("b:1b", out)
        self.assertTrue(self.until(lambda: self.o.started("b:1b")), "a is a:latest in /api/ps; the pair fits")
        self.o.gates["a"].set()
        ta.join(5)
        tb.join(5)
        self.assertEqual(out, {"a": "ok", "b:1b": "ok"})

    def test_one_process_switches_its_own_models_without_waiting_and_learns_their_sizes(self):
        self.o.loaded = ["a:1b"]
        out = {}
        with mock.patch.object(m, "GPU_HOLD", 30.0):
            t = time.monotonic()
            for x in ("a:1b", "b:1b", "a:1b"):
                self.ask(x, out).join(5)
            self.assertLess(time.monotonic() - t, 5)
        self.assertEqual(out, {"a:1b": "ok", "b:1b": "ok"})
        self.assertEqual((self.ledger()["size"], self.ledger()["gpu"]), ({"a:1b": 10}, {"cap": 10}))

    def test_a_wait_ends_with_its_entry_gone_and_the_callers_timeout_caps_it(self):
        with open(m._gpu_file(), "w", encoding="utf-8") as f:
            json.dump({"calls": {"x": {"model": "a:1b", "pid": os.getpid(), "since": time.time()}}}, f)
        url = self.o.url + "/chat/completions"
        with mock.patch.object(m.time, "sleep", side_effect=KeyboardInterrupt), self.assertRaises(KeyboardInterrupt):
            m._gpu_take(url, "b:1b", 60)
        self.assertEqual(self.ledger()["wait"], {})
        t = time.monotonic()
        me, _ = m._gpu_take(url, "b:1b", 0.2)  # a:1b never ends: the caller's timeout sends b:1b anyway
        self.assertLess(time.monotonic() - t, 5)
        m._gpu_give(me, "b:1b", url)
        self.assertEqual((list(self.ledger()["calls"]), self.ledger()["wait"]), (["x"], {}))

    def test_other_servers_and_paths_take_no_turns(self):
        self.assertTrue(m._turn_url(self.o.url + "/chat/completions"))
        self.assertTrue(m._turn_url(self.o.url[:-3] + "/api/chat"))
        self.assertFalse(m._turn_url(self.o.url + "/embeddings"))
        self.assertFalse(m._turn_url("http://127.0.0.1:1/v1/chat/completions"))
        self.assertFalse(m._turn_url("https://api.example.com/v1/chat/completions"))


class Unloadable(Case):
    def test_an_unknown_architecture_is_asked_once_then_skipped_box_wide(self):
        out = {}
        self.ask(LFM, out).join(5)
        self.assertIsInstance(out[LFM], m.ModelError)
        self.assertIn("unknown model architecture", str(out[LFM]))
        self.assertIn("skipped", str(out[LFM]))
        self.assertEqual(self.o.hits.get("/v1/chat/completions"), 1)  # a load failure is not retried: each is a runner start
        self.assertGreater(self.ledger()["bad"][LFM]["until"], time.time() + 3600)  # every process reads it
        self.ask(LFM, out).join(5)
        self.assertIsInstance(out[LFM], m.ModelError)
        self.assertIn("skipped until", str(out[LFM]))
        self.assertIn(m._gpu_file(), str(out[LFM]))  # where to clear it
        self.assertEqual(self.o.hits.get("/v1/chat/completions"), 1)
        self.ask("a:1b", out).join(5)
        self.assertEqual(out["a:1b"], "ok")  # other models still answer


class Polls(Case):
    def test_tags_and_the_models_probe_are_read_once_a_minute(self):
        for _ in range(3):
            m.systemone_profiles(self.o.url[:-3])
            m.embedding_profiles(self.o.url[:-3])
            self.assertEqual(next(m._local())["model"], "a:1b")
        self.assertEqual((self.o.hits.get("/api/tags"), self.o.hits.get("/v1/models"), self.o.hits.get("/api/show")),
                         (1, 1, 1))
        with mock.patch.object(m, "TAGS_S", 0.0):
            m.systemone_profiles(self.o.url[:-3])
        self.assertEqual(self.o.hits.get("/api/tags"), 2)

    def test_another_servers_tags_are_not_cached(self):
        f = Ollama()
        self.addCleanup(f.close)
        m.systemone_profiles(f.url[:-3])
        m.systemone_profiles(f.url[:-3])
        self.assertEqual(f.hits.get("/api/tags"), 2)

    def test_systemone_profiles_never_reach_the_box_under_no_local_models(self):
        with mock.patch.dict(os.environ, {"FOREMAN_NO_LOCAL_MODELS": "1"}), \
                mock.patch.object(m, "_tags", side_effect=AssertionError("probed")):
            self.assertEqual(m.systemone_profiles(), [])


if __name__ == "__main__":
    import unittest
    unittest.main()
