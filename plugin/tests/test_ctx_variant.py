"""T-2938: a profile with ctx_variant true whose server serves less than its context gets a num_ctx variant (BASE-<n>k),
reused when api/tags lists it, else made with `ollama create` from a temp Modelfile. A fake server and a fake ollama
binary on PATH; no real ollama create."""
import http.server
import json
import os
import stat
import sys
import tempfile
import threading
import unittest
from unittest import mock

import helpers  # noqa: F401  (puts plugin/lib on sys.path)
from sampo import models as m
from test_code import CodeCase
from test_code_truncation import LONG

FAKE = """#!{py}
import os, sys
d = {d!r}
open(os.path.join(d, "calls"), "a").write(" ".join(sys.argv[1:]) + "\\n")
if os.path.exists(os.path.join(d, "fail")):
    sys.stderr.write("boom\\n")
    sys.exit(1)
name, mf = sys.argv[2], sys.argv[4]
open(os.path.join(d, name + ".mf"), "w").write(open(mf).read())
"""


class Fake:
    """A fake Ollama (tags, ps, show; a created variant is read from the fake binary's Modelfile copies) and a fake
    `ollama` script in .bin."""

    def __init__(self, tags=("q:4b",), with_binary=True):
        self.dir = tempfile.mkdtemp()
        self.bin = os.path.join(self.dir, "bin")
        os.mkdir(self.bin)
        self.tags, d = list(tags), self.dir
        if with_binary:
            path = os.path.join(self.bin, "ollama")
            with open(path, "w") as f:
                f.write(FAKE.format(py=sys.executable, d=d))
            os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)

        def made(name):
            try:
                with open(os.path.join(d, name + ".mf")) as f:
                    return f.read()
            except OSError:
                return None

        outer = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def reply(self, body):
                data = json.dumps(body).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                if self.path == "/api/tags":
                    extra = [f[:-3] for f in os.listdir(d) if f.endswith(".mf")]
                    return self.reply({"models": [{"name": n} for n in outer.tags + extra]})
                self.reply({"models": []})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)))
                mf = made(body.get("model"))
                self.reply({"parameters": mf.split("PARAMETER ")[1] if mf else ""})

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.root = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, args=(0.02,), daemon=True).start()

    def profile(self, **kw):
        return dict({"name": "gpu", "kind": "openai", "base_url": self.root + "/v1", "model": "q:4b", "context": 32768,
                     "ctx_variant": True}, **kw)

    def calls(self):
        try:
            with open(os.path.join(self.dir, "calls")) as f:
                return f.read().splitlines()
        except OSError:
            return []

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


class Variant(unittest.TestCase):
    def fake(self, **kw):
        f = Fake(**kw)
        self.addCleanup(f.close)
        patch = mock.patch.dict(os.environ, {"PATH": f.bin})
        patch.start()
        self.addCleanup(patch.stop)
        return f

    def test_a_missing_variant_is_created_from_a_temp_modelfile_and_the_profile_reports_it(self):
        f = self.fake()
        p, note = m.context_variant(f.profile())
        self.assertEqual(p["model"], "q-4b-32k")
        self.assertEqual(m.served_context(p), 32768)
        self.assertEqual(len(f.calls()), 1)
        self.assertTrue(f.calls()[0].startswith("create q-4b-32k -f "))
        with open(os.path.join(f.dir, "q-4b-32k.mf")) as mf:
            self.assertEqual(mf.read(), "FROM q:4b\nPARAMETER num_ctx 32768\n")
        self.assertIn("q-4b-32k", note)
        self.assertIn("unknown", note)  # T-2947: the base stated no num_ctx; the variant is made anyway

    def test_an_existing_variant_is_reused_and_ollama_is_not_run(self):
        f = self.fake()
        with open(os.path.join(f.dir, "q-4b-32k.mf"), "w") as mf:  # already made: listed by tags, serving 32768
            mf.write("FROM q:4b\nPARAMETER num_ctx 32768\n")
        p, note = m.context_variant(f.profile())
        self.assertEqual(p["model"], "q-4b-32k")
        self.assertEqual(f.calls(), [])
        self.assertIn("reusing", note)

    def test_nothing_is_created_without_the_opt_in_for_non_ollama_or_remote(self):
        f = self.fake()
        for prof in (f.profile(ctx_variant=False), f.profile(kind="anthropic"), f.profile(context=2048),
                     f.profile(base_url="https://api.example.com/v1")):
            self.assertEqual(m.context_variant(prof), (prof, None))
        self.assertEqual(f.calls(), [])

    def test_a_missing_binary_or_a_failed_create_stops_naming_the_manual_command(self):
        f = self.fake(with_binary=False)
        with self.assertRaises(m.ModelError) as e:
            m.context_variant(f.profile())
        self.assertIn("ollama create q-4b-32k", str(e.exception))
        f = self.fake()
        open(os.path.join(f.dir, "fail"), "w").close()
        with self.assertRaises(m.ModelError) as e:
            m.context_variant(f.profile())
        self.assertIn("ollama create q-4b-32k", str(e.exception))
        self.assertIn("boom", str(e.exception))

    def test_a_model_name_that_could_inject_a_modelfile_line_is_refused(self):
        f = self.fake()
        with self.assertRaises(m.ModelError):
            m.context_variant(f.profile(model="q:4b\nSYSTEM x"), 4096)  # served passed in: T-2947
        self.assertEqual(f.calls(), [])


class Smith(CodeCase):
    def test_smith_uses_the_variant_and_notes_it(self):
        f = Fake()
        self.addCleanup(f.close)
        with open(os.path.join(self.home, "models.json"), "w") as fh:
            json.dump({"profiles": {"gpu": {"kind": "openai", "base_url": f.root + "/v1", "model": "q:4b",
                                            "context": 32768, "ctx_variant": True}}}, fh)
        r = self.code(LONG, "--model", "gpu", "--dry-plan", check=False,
                      env={"PATH": f.bin + os.pathsep + os.environ["PATH"]})
        self.assertIn("q-4b-32k", r.stdout + r.stderr)
        self.assertEqual(len(f.calls()), 1)


if __name__ == "__main__":
    unittest.main()
