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
        self.states, self.crits, self.busy, srv = [], [], 0, self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.path.endswith("/systemone") and srv.busy > 0:
                    srv.busy -= 1
                    self.send_response(529)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                if self.path.endswith("/systemone"):
                    srv.states.append(body["state"])
                    srv.crits.append(next(iter(body["questions"].values()))["criteria"])
                    crit = list(srv.crits[-1])
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
            for base in ("majority", "orchestrator"):  # T-2894: two honest baselines, labelled
                self.assertEqual(by[(base, use)]["arm"], "decision")
            self.assertIn("orchestrator's own", by[("orchestrator", use)]["note"])
            self.assertNotIn(("without", use), by)
        train = [self.truth[t][0] for t in self.truth if t not in self.held]
        top = max(sorted(set(train)), key=train.count)
        self.assertEqual(by[("majority", "intake-type")]["accuracy"],
                         round(sum(self.truth[t][0] == top for t in self.held) / len(self.held), 3))
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
        inputs = {louhi._raw(c.find_brief(self.p, t)) for t in self.held}  # T-2894: the briefs' raw requests, no shadow row
        self.assertTrue(self.srv.states and set(self.srv.states) <= inputs)
        self.assertFalse([s for s in self.srv.states if "FEATURE" in s or "FIX" in s.split()])
        # every option carries its description, not its own label
        crits = [x for x in self.srv.crits if "FIX" in x]
        self.assertTrue(crits)
        for crit in self.srv.crits:
            self.assertTrue(all(v != k and len(v) > 12 for k, v in crit.items()), crit)

    def test_retrieval_rows_vote_from_the_nearest_train_requests_and_abstain_when_split(self):
        self.run_bench()
        by = {(r["backend"], r["use"]): r for r in self.rows()}
        for name in ("bm25", "retrieval:nomic"):
            r = by[(name, "intake-type")]
            self.assertEqual((r["arm"], r["n"]), ("retrieval", len(self.held)))
            self.assertEqual(r["answered"] + r["abstained"], r["n"])
            self.assertEqual(r["coverage"], round(r["answered"] / r["n"], 3))
            self.assertLessEqual(r["accuracy_all"], r["coverage"])
            if name == "bm25":  # the two kinds of request share no words (the fake embedder's letter counts blur them)
                self.assertEqual((r["accuracy"], r["accuracy_all"]), (1.0, r["coverage"]))
            self.assertIn((name, "intake-tier"), by)
        self.assertEqual(louhi._vote(["FIX"] * 4 + ["FEATURE"] * 3), "FIX")
        self.assertIsNone(louhi._vote(["FIX"] * 3 + ["FEATURE"] * 3))  # split: abstain
        self.run_bench()  # a second run embeds nothing new: the vectors are cached by model and text hash
        with open(os.path.join(self.p.dir, louhi.RETRIEVAL_VECTORS)) as f:
            ids = [(json.loads(x)["id"]) for x in f]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(os.path.exists(os.path.join(self.p.root, louhi.RETRIEVAL_VECTORS)), "the cache stays out of the repo")

    def test_a_busy_529_is_retried_then_counted(self):
        self.srv.busy = 4  # models._post retries 3 times; the bench retries after it
        louhi.BUSY_WAIT, was = 0, models._sleep
        models._sleep = lambda s: None
        self.addCleanup(setattr, louhi, "BUSY_WAIT", 2)
        self.addCleanup(setattr, models, "_sleep", was)
        self.run_bench()
        r = {(x["backend"], x["use"]): x for x in self.rows()}[("kev", "intake-type")]
        self.assertEqual((r["n"], r["errors"]), (len(self.held), 0))

    def test_the_generation_arm_writes_yield_and_pass_rate_one_endpoint_at_a_time(self):
        a, b = "http://127.0.0.1:1/v1", "http://127.0.0.1:2/v1"
        mk = lambda n, u: {"name": n, "kind": "openai", "base_url": u, "model": n, "key_env": None, "context": 8192}  # noqa: E731
        profs = [mk("b1", b), mk("a1", a), mk("b2", b), mk("a2", a)]
        calls = []

        def grow(prof, k):
            calls.append(("grow", prof["name"], k))
            return {"added": k, "kept": k // 2, "seconds": 30.0, "fallback": 0}

        def funnel(prof, sample):
            calls.append(("funnel", prof["name"], sample))
            return {"kill": {"in": 8, "kept": 6}, "tier": {"in": sample, "kept": 2}}

        def smith(prof):
            calls.append(("smith", prof["name"]))
            return {"closed": 3, "seeds": 4}

        louhi.bench_models(self.p, decision=[], embedders=[], generators=profs, k=16, grow_fn=grow, funnel_fn=funnel,
                           smith_fn=smith)
        order = [x[1] for x in calls]
        self.assertEqual(order, ["a1"] * 3 + ["a2"] * 3 + ["b1"] * 3 + ["b2"] * 3)  # an endpoint's models never alternate
        rows = {(x["backend"], x["use"]): x for x in self.rows() if x["arm"] == "generation"}
        y = rows[("a1", "moons-yield")]
        self.assertEqual((y["k"], y["added"], y["admitted"], y["kill_kept"], y["tier_in"], y["tier_kept"], y["moons_per_min"]),
                         (16, 16, 8, 6, 8, 2, 32.0))  # 16 moons in 30 s
        self.assertIn("sample", y["note"])  # the tier stage takes a sample and says so
        s = rows[("b2", "smith-seeds")]
        self.assertEqual((s["pass_rate"], s["n"]), (0.75, 4))
        self.assertIn("b2", self.fm("exam", "models", "show").stdout)

    def test_no_endpoint_is_named_in_the_code(self):
        src = os.path.join(os.path.dirname(louhi.__file__))
        for f in ("louhi.py", "models.py"):
            with open(os.path.join(src, f)) as fh:
                self.assertNotIn("<private>", fh.read(), f)
        self.assertFalse(hasattr(louhi, "SERVING"))
        profs = [{"base_url": "http://x/v1", "model": "first"}, {"base_url": "http://x/v1", "model": "second"}]
        self.assertEqual(louhi._serving(profs), {"http://x/v1": "first"})

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

    def test_a_failing_backend_counts_errors_and_a_second_run_appends_a_new_run(self):
        dead = {"name": "gone", "kind": "systemone", "base_url": "http://127.0.0.1:1/v1", "model": "gone", "key_env": None}
        louhi.bench_models(self.p, decision=[dead], embedders=[])
        r = {(x["backend"], x["use"]): x for x in self.rows()}[("gone", "intake-type")]
        self.assertEqual((r["n"], r["errors"], r["accuracy"]), (0, len(self.held), None))
        self.run_bench()
        self.assertEqual(len({x["run"] for x in self.rows()}), 2)
        self.assertNotIn("gone", self.fm("exam", "models", "show").stdout)  # show prints the latest run only
