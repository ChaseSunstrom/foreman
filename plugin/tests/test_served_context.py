"""T-2935: a local Ollama serves 4096 tokens unless a num_ctx variant is used, whatever models.json says. served_context
reads what the server really serves (api/ps while loaded, else api/show); fm code corrects the profile to it and stops
before the first model call when the plan prompt cannot fit. Fake servers only."""
import http.server
import json
import os
import threading
import unittest

import helpers  # noqa: F401  (puts plugin/lib on sys.path)
from sampo import models as m
from test_code import CodeCase
from test_code_truncation import LONG


class Ollama:
    """A fake Ollama: GET /api/ps lists `loaded`, POST /api/show answers `show`; chat requests are recorded in .chat."""

    def __init__(self, loaded=(), show=None, ps=True):
        self.loaded, self.show, self.chat = list(loaded), show or {}, []
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
                self.reply(200, {"models": o.loaded}) if ps and self.path == "/api/ps" else self.reply(404, {})

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                if self.path == "/api/show":
                    return self.reply(200, o.show)
                o.chat.append(raw)
                self.reply(400, {"error": "no chat expected"})

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.root = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, args=(0.02,), daemon=True).start()

    def profile(self, **kw):
        return dict({"name": "gpu", "kind": "openai", "base_url": self.root + "/v1", "model": "q:4b", "context": 32768}, **kw)

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


class ServedContext(unittest.TestCase):
    def serve(self, **kw):
        o = Ollama(**kw)
        self.addCleanup(o.close)
        return o

    def test_a_loaded_model_reports_its_ps_context(self):
        o = self.serve(loaded=[{"name": "q:4b", "context_length": 4096}], show={"parameters": "num_ctx 8192"})
        self.assertEqual(m.served_context(o.profile()), 4096)

    def test_an_unloaded_model_falls_back_to_show_then_the_ollama_default(self):
        o = self.serve(show={"parameters": "num_ctx 8192"})
        self.assertEqual(m.served_context(o.profile()), 8192)
        o = self.serve(show={"parameters": ""})
        self.assertEqual(m.served_context(o.profile()), m.OLLAMA_CONTEXT)

    def test_a_non_ollama_or_non_loopback_profile_is_none(self):
        o = self.serve(ps=False)
        self.assertIsNone(m.served_context(o.profile()))
        self.assertIsNone(m.served_context(o.profile(base_url="https://api.example.com/v1")))
        self.assertIsNone(m.served_context(o.profile(kind="anthropic")))


class Smith(CodeCase):
    def run_code(self, o):
        path = os.path.join(self.home, "models.json")
        with open(path, "w") as f:
            json.dump({"profiles": {"gpu": {"kind": "openai", "base_url": o.root + "/v1", "model": "q:4b",
                                            "context": 32768, "tools": True}}}, f)
        return self.code(LONG, "--model", "gpu", "--dry-plan", check=False)

    def test_a_profile_above_the_served_context_is_corrected_and_a_long_prompt_stops_before_any_call(self):
        o = Ollama(loaded=[{"name": "q:4b", "context_length": 1024}])
        self.addCleanup(o.close)
        r = self.run_code(o)
        out = r.stdout + r.stderr
        self.assertEqual(r.returncode, 1, out)
        self.assertIn("profile says 32768", out)
        self.assertIn("serves 1024", out)
        self.assertIn("num_ctx", out)  # the variant to use
        self.assertEqual(o.chat, [])  # stopped before the first model call


if __name__ == "__main__":
    unittest.main()
