"""T-1211: fmmodels, the stdlib model client for fm code. Every request goes to an in-process fake server; no test
reaches the real network."""
import http.server
import json
import os
import tempfile
import threading
import unittest

import helpers  # noqa: F401  (puts plugin/lib on sys.path)
import fmmodels as m

KEYS = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY", "FM_TEST_KEY")
SECRET = "sk-test-SECRET-123"


class Fake:
    """A one-port HTTP server answering from a script: each request pops (status, body, headers); the last one repeats.
    Records (method, path, headers, json body) of every request."""

    def __init__(self, script):
        self.script, self.seen = list(script), []
        fake = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _answer(self):
                n = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(n) if n else b""
                fake.seen.append((self.command, self.path, dict(self.headers), json.loads(raw) if raw else None))
                status, body, hdrs = fake.script.pop(0) if len(fake.script) > 1 else fake.script[0]
                data = (body if isinstance(body, str) else json.dumps(body)).encode()
                self.send_response(status)
                for k, v in (hdrs or {}).items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            do_GET = do_POST = _answer

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}/v1"
        threading.Thread(target=self.srv.serve_forever, args=(0.02,), daemon=True).start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def oa_reply(text="hi", tool_calls=None, finish="stop"):
    msg = {"role": "assistant", "content": text}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return {"choices": [{"message": msg, "finish_reason": finish}],
            "usage": {"prompt_tokens": 7, "completion_tokens": 3}}


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._env = {k: os.environ.get(k) for k in KEYS + ("FOREMAN_HOME",)}
        for k in KEYS:
            os.environ.pop(k, None)
        os.environ["FOREMAN_HOME"] = self._tmp.name
        self.slept = []
        self._sleep, m._sleep = m._sleep, self.slept.append
        self._local, m.LOCAL = m.LOCAL, []
        self.fakes = []

    def tearDown(self):
        m._sleep, m.LOCAL = self._sleep, self._local
        for f in self.fakes:
            f.close()
        for k, v in self._env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self._tmp.cleanup()

    def fake(self, *script):
        f = Fake(script)
        self.fakes.append(f)
        return f

    def profile(self, fake, kind="openai", key=True):
        if key:
            os.environ["FM_TEST_KEY"] = SECRET
        return {"name": "t", "kind": kind, "base_url": fake.url, "model": "m1",
                "key_env": "FM_TEST_KEY" if key else None, "context": 8192, "tools": True}


TOOL = {"type": "function", "function": {"name": "read", "description": "read a file",
                                         "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}}}


class OpenAIShape(Base):
    def test_plain_text(self):
        f = self.fake((200, oa_reply("hello"), None))
        r = m.complete(self.profile(f), [{"role": "user", "content": "hi"}], max_tokens=50)
        self.assertEqual(r["text"], "hello")
        self.assertEqual(r["tool_calls"], [])
        self.assertEqual(r["usage"], {"in": 7, "out": 3})
        self.assertEqual(r["stop"], "stop")
        method, path, hdrs, body = f.seen[0]
        self.assertEqual((method, path), ("POST", "/v1/chat/completions"))
        self.assertEqual(hdrs["Authorization"], f"Bearer {SECRET}")
        self.assertEqual(body["model"], "m1")
        self.assertEqual(body["max_tokens"], 50)
        self.assertNotIn("tools", body)

    def test_native_tool_call(self):
        call = {"id": "c1", "type": "function", "function": {"name": "read", "arguments": '{"path": "a.py"}'}}
        f = self.fake((200, oa_reply(None, [call], "tool_calls"), None))
        r = m.complete(self.profile(f), [{"role": "user", "content": "read a.py"}], tools=[TOOL])
        self.assertEqual(r["tool_calls"], [{"id": "c1", "name": "read", "args": {"path": "a.py"}}])
        self.assertEqual(r["text"], "")
        self.assertEqual(f.seen[0][3]["tools"], [TOOL])

    def test_complete_s_own_tool_calls_go_back_in_wire_shape(self):
        f = self.fake((200, oa_reply("done"), None))
        msgs = [{"role": "user", "content": "x"},
                {"role": "assistant", "content": None, "tool_calls": [{"id": "c1", "name": "read", "args": {"p": 1}}]},
                {"role": "tool", "tool_call_id": "c1", "content": "data"}]
        m.complete(self.profile(f), msgs)
        sent = f.seen[0][3]["messages"][1]["tool_calls"][0]
        self.assertEqual(sent["function"]["name"], "read")
        self.assertEqual(json.loads(sent["function"]["arguments"]), {"p": 1})
        self.assertEqual(sent["type"], "function")

    def test_429_then_success_honours_retry_after(self):
        f = self.fake((429, {"error": "slow down"}, {"Retry-After": "3"}), (200, oa_reply("ok"), None))
        r = m.complete(self.profile(f), [{"role": "user", "content": "hi"}])
        self.assertEqual(r["text"], "ok")
        self.assertEqual(self.slept, [3.0])
        self.assertEqual(len(f.seen), 2)

    def test_retry_after_is_capped(self):
        f = self.fake((429, "", {"Retry-After": "9999"}), (200, oa_reply("ok"), None))
        m.complete(self.profile(f), [{"role": "user", "content": "hi"}])
        self.assertEqual(self.slept, [20.0])

    def test_odd_retry_after_falls_back(self):
        f = self.fake((503, "", {"Retry-After": "nan"}), (503, "", {"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}),
                      (200, oa_reply("ok"), None))
        m.complete(self.profile(f), [{"role": "user", "content": "hi"}])
        self.assertEqual(self.slept, [1.0, 2.0])

    def test_500_three_times_raises_without_the_key(self):
        f = self.fake((500, f"boom, you sent {SECRET}", None))
        with self.assertRaises(m.ModelError) as cm:
            m.complete(self.profile(f), [{"role": "user", "content": "hi"}])
        self.assertEqual(len(f.seen), 3)
        self.assertEqual(cm.exception.status, 500)
        self.assertIn("500", str(cm.exception))
        self.assertIn("boom", str(cm.exception))
        self.assertNotIn(SECRET, str(cm.exception))
        self.assertEqual(len(self.slept), 2)

    def test_400_is_not_retried(self):
        f = self.fake((400, "bad request", None))
        with self.assertRaises(m.ModelError):
            m.complete(self.profile(f), [{"role": "user", "content": "hi"}])
        self.assertEqual(len(f.seen), 1)

    def test_missing_key_env_raises(self):
        f = self.fake((200, oa_reply(), None))
        p = self.profile(f)
        os.environ.pop("FM_TEST_KEY")
        with self.assertRaises(m.ModelError) as cm:
            m.complete(p, [{"role": "user", "content": "hi"}])
        self.assertIn("FM_TEST_KEY", str(cm.exception))
        self.assertEqual(f.seen, [])

    def test_keyless_local_profile_sends_no_auth(self):
        f = self.fake((200, oa_reply(), None))
        m.complete(self.profile(f, key=False), [{"role": "user", "content": "hi"}])
        self.assertNotIn("Authorization", f.seen[0][2])

    def test_redirect_is_not_followed(self):
        f = self.fake((302, "", {"Location": "http://127.0.0.1:9/steal"}))
        with self.assertRaises(m.ModelError):
            m.complete(self.profile(f), [{"role": "user", "content": "hi"}])
        self.assertEqual(len(f.seen), 1)

    def test_non_json_reply_raises(self):
        f = self.fake((200, "<html>proxy</html>", None))
        with self.assertRaises(m.ModelError):
            m.complete(self.profile(f), [{"role": "user", "content": "hi"}])

    def test_non_http_base_url_refused(self):
        p = {"name": "x", "kind": "openai", "base_url": "file:///etc", "model": "m", "key_env": None}
        with self.assertRaises(m.ModelError):
            m.complete(p, [{"role": "user", "content": "hi"}])


class AnthropicShape(Base):
    def reply(self, content, stop="end_turn"):
        return {"content": content, "stop_reason": stop, "usage": {"input_tokens": 11, "output_tokens": 4}}

    def test_plain_text(self):
        f = self.fake((200, self.reply([{"type": "text", "text": "hel"}, {"type": "text", "text": "lo"}]), None))
        r = m.complete(self.profile(f, "anthropic"), [{"role": "system", "content": "be brief"},
                                                       {"role": "user", "content": "hi"}])
        self.assertEqual(r, {"text": "hello", "tool_calls": [], "usage": {"in": 11, "out": 4}, "stop": "end_turn"})
        method, path, hdrs, body = f.seen[0]
        self.assertEqual(path, "/v1/messages")
        hdrs = {k.lower(): v for k, v in hdrs.items()}
        self.assertEqual(hdrs["x-api-key"], SECRET)
        self.assertIn("anthropic-version", hdrs)
        self.assertNotIn("authorization", hdrs)
        self.assertEqual(body["system"], "be brief")
        self.assertEqual(body["messages"], [{"role": "user", "content": [{"type": "text", "text": "hi"}]}])

    def test_native_tool_call(self):
        f = self.fake((200, self.reply([{"type": "text", "text": "reading"},
                                        {"type": "tool_use", "id": "tu1", "name": "read", "input": {"path": "a"}}],
                                       "tool_use"), None))
        r = m.complete(self.profile(f, "anthropic"), [{"role": "user", "content": "go"}], tools=[TOOL])
        self.assertEqual(r["tool_calls"], [{"id": "tu1", "name": "read", "args": {"path": "a"}}])
        self.assertEqual(r["text"], "reading")
        self.assertEqual(r["stop"], "tool_use")
        self.assertEqual(f.seen[0][3]["tools"], [{"name": "read", "description": "read a file",
                                                  "input_schema": TOOL["function"]["parameters"]}])

    def test_message_conversion(self):
        msgs = [{"role": "system", "content": "s1"}, {"role": "system", "content": "s2"},
                {"role": "user", "content": "q"},
                {"role": "assistant", "content": "let me look", "tool_calls": [
                    {"id": "a", "type": "function", "function": {"name": "read", "arguments": '{"path": "x"}'}},
                    {"id": "b", "name": "ls", "args": {}}]},
                {"role": "tool", "tool_call_id": "a", "content": "X"},
                {"role": "tool", "tool_call_id": "b", "content": "Y"},
                {"role": "user", "content": "and?"}]
        system, out = m.to_anthropic(msgs)
        self.assertEqual(system, "s1\n\ns2")
        self.assertEqual(out, [
            {"role": "user", "content": [{"type": "text", "text": "q"}]},
            {"role": "assistant", "content": [{"type": "text", "text": "let me look"},
                                              {"type": "tool_use", "id": "a", "name": "read", "input": {"path": "x"}},
                                              {"type": "tool_use", "id": "b", "name": "ls", "input": {}}]},
            {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "a", "content": "X"},
                                         {"type": "tool_result", "tool_use_id": "b", "content": "Y"},
                                         {"type": "text", "text": "and?"}]}])

    def test_tool_conversion_accepts_bare_specs(self):
        bare = TOOL["function"]
        self.assertEqual(m.to_anthropic_tools([TOOL, bare]),
                         [{"name": "read", "description": "read a file", "input_schema": bare["parameters"]}] * 2)

    def test_500_three_times_raises_without_the_key(self):
        f = self.fake((503, {"error": {"message": f"overloaded {SECRET}"}}, None))
        with self.assertRaises(m.ModelError) as cm:
            m.complete(self.profile(f, "anthropic"), [{"role": "user", "content": "hi"}])
        self.assertEqual(len(f.seen), 3)
        self.assertNotIn(SECRET, str(cm.exception))


class ExtractJson(unittest.TestCase):
    def test_fenced(self):
        self.assertEqual(m.extract_json('Sure:\n```json\n{"a": 1}\n```\nthanks'), {"a": 1})

    def test_bare(self):
        self.assertEqual(m.extract_json('the answer is {"a": [1, 2]} ok'), {"a": [1, 2]})

    def test_nested_and_braces_in_strings(self):
        self.assertEqual(m.extract_json('x {"a": {"b": "}{"}, "c": 2} y {"d": 3}'), {"a": {"b": "}{"}, "c": 2})

    def test_broken(self):
        self.assertIsNone(m.extract_json('{"a": 1, '))
        self.assertIsNone(m.extract_json("no json here"))
        self.assertIsNone(m.extract_json(""))
        self.assertIsNone(m.extract_json(None))

    def test_skips_a_broken_one_for_a_later_good_one(self):
        self.assertEqual(m.extract_json('{oops} then {"ok": true}'), {"ok": True})

    def test_hostile_input_is_bounded(self):
        self.assertIsNone(m.extract_json('{"a":' * 50000))
        self.assertIsNone(m.extract_json("[" * 50000))


class Profiles(Base):
    def write_models(self, data):
        with open(os.path.join(self._tmp.name, "models.json"), "w") as f:
            json.dump(data, f)

    def test_named_profile_from_models_json(self):
        self.write_models({"profiles": {"mine": {"kind": "anthropic", "base_url": "http://h/v1", "model": "c",
                                                 "key_env": "FM_TEST_KEY"}}})
        p = m.resolve("mine")
        self.assertEqual(p["name"], "mine")
        self.assertEqual(p["kind"], "anthropic")
        self.assertEqual(p["model"], "c")
        self.assertEqual(set(p), {"name", "kind", "base_url", "model", "key_env", "context", "tools"})

    def test_models_json_default_beats_local_and_keys(self):
        local = self.fake((200, {"data": [{"id": "llama"}]}, None))
        m.LOCAL = [("ollama", local.url)]
        os.environ["OPENAI_API_KEY"] = "k"
        self.write_models({"default": "mine", "profiles": {"mine": {"base_url": "http://h/v1", "model": "x"}}})
        self.assertEqual(m.resolve()["name"], "mine")

    def test_local_beats_keyed_cloud(self):
        local = self.fake((200, {"data": [{"id": "qwen"}, {"id": "other"}]}, None))
        m.LOCAL = [("dead", "http://127.0.0.1:9/v1"), ("lmstudio", local.url)]
        os.environ["OPENAI_API_KEY"] = "k"
        p = m.resolve()
        self.assertEqual((p["name"], p["model"], p["base_url"], p["key_env"]), ("lmstudio", "qwen", local.url, None))
        self.assertEqual(local.seen[0][:2], ("GET", "/v1/models"))

    def test_first_keyed_cloud_without_local(self):
        os.environ["GROQ_API_KEY"] = "k"
        os.environ["GEMINI_API_KEY"] = "k"
        p = m.resolve()
        self.assertEqual((p["name"], p["key_env"]), ("groq", "GROQ_API_KEY"))
        os.environ["ANTHROPIC_API_KEY"] = "k"
        p = m.resolve()
        self.assertEqual((p["name"], p["kind"]), ("anthropic", "anthropic"))

    def test_gemini_goes_through_its_openai_endpoint(self):
        os.environ["GEMINI_API_KEY"] = "k"
        p = m.resolve("gemini")
        self.assertEqual(p["kind"], "openai")
        self.assertIn("generativelanguage.googleapis.com", p["base_url"])
        self.assertTrue(p["base_url"].endswith("/openai"))

    def test_nothing_available_raises(self):
        with self.assertRaises(m.ModelError):
            m.resolve()

    def test_unknown_name_raises(self):
        with self.assertRaises(m.ModelError):
            m.resolve("nope")

    def test_broken_models_json_raises_naming_it(self):
        with open(os.path.join(self._tmp.name, "models.json"), "w") as f:
            f.write("{nope")
        with self.assertRaises(m.ModelError) as cm:
            m.resolve()
        self.assertIn("models.json", str(cm.exception))

    def test_local_server_with_no_models_is_skipped(self):
        empty = self.fake((200, {"data": []}, None))
        odd = self.fake((200, {"data": 5}, None))
        m.LOCAL = [("ollama", empty.url), ("vllm", odd.url)]
        os.environ["OPENAI_API_KEY"] = "k"
        self.assertEqual(m.resolve()["name"], "openai")

    def test_profiles_lists_configured_keyed_and_local(self):
        local = self.fake((200, {"data": [{"id": "llama"}]}, None))
        m.LOCAL = [("ollama", local.url)]
        os.environ["OPENAI_API_KEY"] = "k"
        self.write_models({"profiles": {"mine": {"base_url": "http://h/v1", "model": "x"}}})
        self.assertEqual([p["name"] for p in m.profiles()], ["mine", "ollama", "openai"])


if __name__ == "__main__":
    unittest.main()
