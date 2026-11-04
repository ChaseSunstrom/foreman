"""T-2887: sampo louhi models, the decision arm (intake type and tier from held-out closed tasks, through systemone
backends) and the embedding arm (title to brief recall). Fake servers only; no live model."""
import http.server
import json
import os
import threading

from helpers import ForemanTestCase

from sampo import core as c
from sampo import louhi
from sampo import models

TASKS = [("the parser crashes on an empty file %d", "FIX", "S"), ("add a csv export to the report %d", "FEATURE", "M")]


class Server:
    """Answers /v1/systemone with `choice` at 0.9 (and records every state it saw) and /v1/embeddings with letter counts."""

    def __init__(self, choice="FIX"):
        self.states, srv = [], self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.path.endswith("/systemone"):
                    srv.states.append(body["state"])
                    crit = list(next(iter(body["questions"].values()))["criteria"])
                    pick = choice if choice in crit else crit[0]
                    out = {"answers": {"type": {"type": "choice", "choice": pick, "confidence": 0.9,
                                                "probabilities": {k: (0.9 if k == pick else 0.05) for k in crit}}}}
                else:
                    vec = lambda t: [float(t.lower().count(ch)) for ch in "abcdefghijklmnopqrstuvwxyz0123456789"]  # noqa: E731
                    xs = body["input"] if isinstance(body["input"], list) else [body["input"]]
                    out = {"data": [{"index": i, "embedding": vec(t)} for i, t in enumerate(xs)]}
                data = json.dumps(out).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}/v1"
        threading.Thread(target=self.srv.serve_forever, args=(0.02,), daemon=True).start()

    def profile(self, name, kind):
        return {"name": name, "kind": kind, "base_url": self.url, "model": name, "key_env": None, "context": 8192,
                "tools": False}

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


class LouhiModels(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.truth = {}
        for i in range(12):
            title, typ, tier = TASKS[i % 2]
            tid = json.loads(self.fm("capture", title % i, "--json").stdout)["id"]
            b = c.find_brief(self.p, tid)
            b.meta.update(type=typ, tier=tier, status="done")
            c.save_brief(self.p, b)
            self.truth[tid] = (typ, tier)
        self.held = sorted(t for t in self.truth if louhi.holdout(t))
        self.srv = Server("FIX")
        self.addCleanup(self.srv.close)

    def run_bench(self, **kw):
        return louhi.bench_models(self.p, decision=[self.srv.profile("kev", "systemone")],
                                  embedders=[self.srv.profile("nomic", "openai")], **kw)

    def rows(self):
        with open(os.path.join(self.p.root, louhi.BENCH)) as f:
            return [json.loads(x) for x in f]

    def test_run_writes_one_row_per_backend_and_use_from_held_out_tasks_only(self):
        self.assertTrue(self.held and len(self.held) < len(self.truth))
        res = self.run_bench()
        rows = self.rows()
        self.assertEqual(len(rows), len(res["rows"]))
        by = {(r["backend"], r["use"]): r for r in rows}
        for use in ("intake-type", "intake-tier"):
            r = by[("kev", use)]
            self.assertEqual((r["arm"], r["n"], r["errors"]), ("decision", len(self.held), 0))
            for k in ("accuracy", "brier", "p50_ms", "p95_ms", "run", "held"):
                self.assertIn(k, r)
            self.assertEqual(by[("without", use)]["arm"], "decision")  # the rules path, the baseline row
        typ = by[("kev", "intake-type")]
        want = sum(self.truth[t][0] == "FIX" for t in self.held) / len(self.held)
        self.assertAlmostEqual(typ["accuracy"], round(want, 3), places=3)
        self.assertAlmostEqual(typ["brier"], round(sum((0.9 - (self.truth[t][0] == "FIX")) ** 2 for t in self.held)
                                                   / len(self.held), 3), places=3)
        emb = by[("nomic", "title-to-brief")]
        self.assertEqual(emb["arm"], "embedding")
        self.assertEqual(emb["n"], len(self.held))
        self.assertTrue(0 <= emb["recall_at_1"] <= emb["recall_at_10"] <= 1)
        self.assertEqual(emb["recall_at_10"], 1.0)  # fewer than ten held-out briefs: the right one is always in the top ten
        # no held-out label reaches a prompt, and no train task is asked about
        with open(os.path.join(self.p.dir, "shadow.jsonl")) as f:
            inputs = {r["input"] for r in map(json.loads, f) if r.get("task") in self.held}
        self.assertTrue(set(self.srv.states) <= inputs)
        self.assertFalse([s for s in self.srv.states if "FEATURE" in s or "FIX" in s.split()])

    def test_cap_leaves_rows_out_and_show_says_how_many(self):
        self.run_bench(cap=1)
        r = {(x["backend"], x["use"]): x for x in self.rows()}[("kev", "intake-type")]
        self.assertEqual((r["n"], r["held"]), (1, len(self.held)))
        out = self.fm("exam", "models", "show").stdout
        self.assertIn("kev", out)
        self.assertIn(f"{len(self.held) - 1} held-out left out", out)

    def test_backends_run_grouped_by_endpoint_the_served_model_first(self):
        # a llama-swap endpoint takes ~3 minutes a switch and can't be asked what it holds: ordering, never alternation
        r, o = "https://jarvis.example/llm/v1", "http://127.0.0.1:11434/v1"
        mk = lambda base, model: ("decision", {"base_url": base, "model": model})  # noqa: E731
        jobs = [mk(r, "big-35b"), mk(o, "kev"), mk(r, "qwen3.8-27b"), mk(o, "d3"), mk(r, "big-35b")[0:1] + (
            {"base_url": r, "model": "aaa"},)]
        got = [(j[1]["base_url"], j[1]["model"]) for j in louhi._bench_order(jobs, {r: "qwen3.8-27b"})]
        self.assertEqual(got, [(o, "d3"), (o, "kev"), (r, "qwen3.8-27b"), (r, "aaa"), (r, "big-35b")])
        self.assertEqual(louhi.SERVING[r.replace("jarvis.example", "<host>")], "qwen3.8-27b")

    def test_a_failing_backend_counts_errors_and_a_second_run_appends_a_new_run(self):
        dead = {"name": "gone", "kind": "systemone", "base_url": "http://127.0.0.1:1/v1", "model": "gone", "key_env": None}
        louhi.bench_models(self.p, decision=[dead], embedders=[])
        r = {(x["backend"], x["use"]): x for x in self.rows()}[("gone", "intake-type")]
        self.assertEqual((r["n"], r["errors"], r["accuracy"]), (0, len(self.held), None))
        self.run_bench()
        self.assertEqual(len({x["run"] for x in self.rows()}), 2)
        self.assertNotIn("gone", self.fm("exam", "models", "show").stdout)  # show prints the latest run only
