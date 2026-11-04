"""T-2868: Moonscale part 1 — the candidate store, the write-time admit rules, the grid read thin-first, and grow routed
local-first then Haiku, budget-capped and resumable. T-2869: part 2 — the funnel (exact, embed or shingle dedupe, kill
check, tier screen and merge, novelty), families, promotion through the cold read, the export and check. Every model
call and embedding here is mocked."""
# map-links: plugin/lib/sampo/moonscale.py plugin/lib/sampo/rune.py plugin/lib/sampo/models.py plugin/lib/sampo/moons.py
import json
import os
import re
from unittest import mock

from helpers import ForemanTestCase
from test_genesis import GEN0_CAPS


def good(**kw):
    row = {"title": "Catch a flaky test before it reaches anyone",
           "today": "Today you can't tell a flaky test from a real failure until it has cost you a morning.",
           "with_this": "With this, you can ship a release knowing which red tests in your code are noise.",
           "what": "It reruns each new failure under changed timing and flags the ones that flip.",
           "kill": "Run it on 20 known flaky tests in one repo for a day; if it flags fewer than 15, it is dead.",
           "prior_art": "flaky-test dashboards", "tier": "high"}
    row.update(kw)
    return row


def reply(n, bad=0):
    """A model's batch: n moons as JSON lines inside a fence, the last `bad` of them internal-only."""
    lines = [json.dumps(good(title=f"Moon number {i}")) for i in range(n - bad)]
    lines += [json.dumps(good(title=f"Bad moon {i}", with_this="With this, you can keep the ledger and the guard in step."))
              for i in range(bad)]
    return "Here they are:\n```json\n" + "\n".join(lines) + "\n```\n"


class _Moons(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        from sampo import core as c
        from sampo import moonscale
        self.c, self.ms = c, moonscale
        self.p = c.find_project(self.repo)


class Admit(_Moons):
    def test_a_moon_with_the_line_and_a_falsifiable_kill_test_is_kept(self):
        self.assertEqual(self.ms.admit(good()), (True, ""))
        self.assertTrue(self.ms.admit(good(today="Today you can’t see it coming."))[0], "a curly apostrophe is the line")

    def test_each_rejection_names_its_reason(self):
        cases = {
            "line": good(today="You can't tell a flaky test from a real one."),
            "line ": good(with_this="Ship faster with your code."),
            "payoff": good(with_this="With this, you can keep the ledger, the guard and every lane in step."),
            "kill test": good(kill=""),
            "kill test ": good(kill="Try it on a project and see how it feels."),
            "code": good(today="Today you can't trust the parse_rows helper in loader.py."),
            "code ": good(with_this="With this, you can run your tests with --fast in your project."),
        }
        for want, row in cases.items():
            with self.subTest(want):
                ok, why = self.ms.admit(row)
                self.assertFalse(ok)
                self.assertTrue(why.startswith(want.strip() + ":"), why)

    def test_a_payoff_on_the_users_things_passes_even_with_an_internal_word(self):
        ok, why = self.ms.admit(good(with_this="With this, you can let a guard stop a bad deploy before your users see it."))
        self.assertTrue(ok, why)

    def test_product_names_and_plain_slashes_are_not_code(self):
        ok, why = self.ms.admit(good(today="Today you can't upgrade a Node.js app or a macOS build 24/7 without a pager."))
        self.assertTrue(ok, why)


class Store(_Moons):
    def cell(self, kind="bugs", scale="file", surface="terminal", mechanism="biology", problem="slow tests",
             source="pain"):
        return {"problem": problem, "source": source, "kind": kind, "mechanism": mechanism, "scale": scale,
                "surface": surface}

    def test_add_stores_every_row_and_the_funnel_keeps_each_fate(self):
        out = self.ms.add(self.p, [good(), good(kill="")], self.cell(), "haiku", 1)
        self.assertEqual([(i, v) for i, v, _ in out], [("C-000001", "kept"), ("C-000002", "rejected")])
        rows = self.ms.rows(self.p)
        self.assertEqual([r["id"] for r in rows], ["C-000001", "C-000002"])
        self.assertEqual((rows[0]["model"], rows[0]["batch"], rows[0]["cell"]["kind"]), ("haiku", 1, "bugs"))
        fate = self.ms.fate(self.p)
        self.assertEqual(fate["C-000001"]["verdict"], "kept")
        self.assertEqual((fate["C-000002"]["verdict"], fate["C-000002"]["stage"]), ("rejected", "write"))
        self.assertTrue(fate["C-000002"]["reason"].startswith("kill test:"))
        self.assertEqual(self.ms.add(self.p, [good()], self.cell(), "haiku", 2)[0][0], "C-000003")
        cov = self.ms.coverage(self.p)
        self.assertEqual((cov["total"], cov["kept"], cov["rejected"]), (3, 2, 1))
        self.assertEqual(cov["reasons"], {"kill test": 1})
        self.assertEqual(cov["cells"]["bugs/file/terminal"], 3)
        self.assertEqual((cov["mechanisms"]["biology"], cov["sources"]["pain"]), (3, 3))

    def test_pick_takes_the_thinnest_cells_problems_and_mechanisms_first(self):
        ms = self.ms
        probs = [{"text": "slow tests", "source": "pain"}, {"text": "late reviews", "source": "steer"}]
        with mock.patch.object(ms, "KINDS", ("bugs", "docs")), mock.patch.object(ms, "SCALES", ("file",)), \
                mock.patch.object(ms, "SURFACES", ("terminal",)), mock.patch.object(ms, "MECHANISMS", ("biology", "law")), \
                mock.patch.object(ms, "problems", return_value=probs):
            ms.add(self.p, [good()], self.cell(), "haiku", 1)
            got = ms.pick(self.p, 1, 0)[0]
            self.assertEqual((got["kind"], got["mechanism"], got["problem"], got["source"]),
                             ("docs", "law", "late reviews", "steer"))
            ms.add(self.p, [good(), good()], self.cell(kind="docs", mechanism="law", problem="late reviews"), "haiku", 2)
            self.assertEqual(ms.pick(self.p, 1, 0)[0]["kind"], "bugs")
            two = ms.pick(self.p, 2, 0)
            self.assertEqual([x["kind"] for x in two], ["bugs", "docs"])
            self.assertEqual(two[0]["mechanism"], "biology", "law holds 2 rows, biology 1")
        self.assertEqual(ms.pick(self.p, 6, 7), ms.pick(self.p, 6, 7), "a seed's draw is the same draw")
        self.assertEqual(len({(x["kind"], x["scale"], x["surface"]) for x in ms.pick(self.p, 40, 3)}), 40)
        untouched = set(ms.MECHANISMS) - {"biology", "law"}
        self.assertEqual({x["mechanism"] for x in ms.pick(self.p, len(untouched), 3)}, untouched,
                         "picks in one call spread over the mechanisms no row has used")

    def test_problems_come_from_the_records_and_the_constant_pains(self):
        with open(os.path.join(self.repo, "pyproject.toml"), "w") as f:
            f.write("[project]\nname = 'x'\n")
        with mock.patch.object(self.c, "steer_rules", return_value=[("2026-11-01", "make every reply shorter")]):
            probs = self.ms.problems(self.p)
        srcs = {x["source"] for x in probs}
        self.assertLessEqual({"pain", "steer", "project"}, srcs)
        self.assertGreaterEqual(sum(x["source"] == "pain" for x in probs), 25)
        proj = [x["text"] for x in probs if x["source"] == "project"]
        self.assertTrue(any(os.path.basename(self.repo) in t and "Python" in t for t in proj), proj)
        self.fm("sensitive", "on")
        self.assertFalse([x for x in self.ms.problems(self.p) if x["source"] == "project"
                          and os.path.basename(self.repo) in x["text"]], "a sensitive project's name stays home")


class Route(_Moons):
    PROFILE = {"name": "jarvis", "kind": "openai", "base_url": "https://127.0.0.1:9/v1", "model": "m",
               "key_env": "MOONS_TEST_KEY", "context": 8192, "tools": False}

    def ask(self, env, up=True):
        from sampo import ideas, models
        with mock.patch.dict(os.environ, {"MOONS_LOCAL": "jarvis", **env}), \
                mock.patch.object(models, "resolve", return_value=dict(self.PROFILE)), \
                mock.patch.object(self.ms, "_up", return_value=up), \
                mock.patch.object(models, "complete", return_value={"text": "local text"}) as comp, \
                mock.patch.object(ideas, "run_child", return_value="haiku text") as child:
            out = self.ms._ask(self.p, "sys", "prompt")
        return out, comp, child

    def test_the_local_model_answers_first(self):
        out, comp, child = self.ask({"MOONS_TEST_KEY": "k"})
        self.assertEqual(out, ("local text", "jarvis"))
        self.assertEqual(comp.call_args[0][0]["name"], "jarvis")
        child.assert_not_called()

    def test_haiku_when_the_key_is_unset_or_the_server_is_down(self):
        os.environ.pop("MOONS_TEST_KEY", None)
        for env, up in (({}, True), ({"MOONS_TEST_KEY": "k"}, False)):
            with self.subTest(env=env, up=up):
                out, comp, child = self.ask(env, up)
                self.assertEqual(out, ("haiku text", "haiku"))
                comp.assert_not_called()
                self.assertEqual((child.call_args[0][0], child.call_args[0][3]), ("moons-grow", "haiku"))

    def test_haiku_when_the_local_model_errs(self):
        from sampo import ideas, models
        with mock.patch.dict(os.environ, {"MOONS_TEST_KEY": "k", "MOONS_LOCAL": "jarvis"}), \
                mock.patch.object(models, "resolve", return_value=dict(self.PROFILE)), \
                mock.patch.object(self.ms, "_up", return_value=True), \
                mock.patch.object(models, "complete", side_effect=models.ModelError("down")), \
                mock.patch.object(ideas, "run_child", return_value="haiku text"):
            self.assertEqual(self.ms._ask(self.p, "sys", "prompt"), ("haiku text", "haiku"))

    def test_local_only_never_reaches_haiku_when_no_local_model_answers_or_it_errs(self):  # T-2916
        from sampo import ideas, models
        with mock.patch.object(self.ms, "_LOCAL_ONLY", True), mock.patch.object(ideas, "run_child") as child:
            with mock.patch.dict(os.environ, {"MOONS_LOCAL": ""}):
                with self.assertRaises(self.ms.LocalOnly) as e:
                    self.ms._ask(self.p, "sys", "prompt")
                self.assertIn("local-only", str(e.exception))
            with mock.patch.dict(os.environ, {"MOONS_TEST_KEY": "k", "MOONS_LOCAL": "jarvis"}), \
                    mock.patch.object(models, "resolve", return_value=dict(self.PROFILE)), \
                    mock.patch.object(self.ms, "_up", return_value=True), \
                    mock.patch.object(models, "complete", side_effect=models.ModelError("down")):
                with self.assertRaises(self.ms.LocalOnly):
                    self.ms._ask(self.p, "sys", "prompt")
            with self.assertRaises(self.ms.LocalOnly):  # audit: cheap=False (promote's strongest model) is paid too
                self.ms._ask(self.p, "sys", "prompt", cheap=False)
        child.assert_not_called()

    def test_grow_and_funnel_local_only_stop_with_the_reason_and_spend_nothing(self):  # T-2916
        from sampo import ideas
        with mock.patch.dict(os.environ, {"MOONS_LOCAL": ""}), mock.patch.object(ideas, "run_child") as child:
            r = self.ms.grow(self.p, 100, local_only=True)
            self.assertEqual((r["stopped"], r["calls"]), ("local", 1))
            self.assertIn("local-only", r["error"])
            cell = {"problem": "slow tests", "source": "pain", "kind": "bugs", "mechanism": "biology",
                    "scale": "file", "surface": "terminal"}
            self.ms.add(self.p, [good()], cell, "haiku", 1)
            with mock.patch.object(self.ms, "_embedder", return_value=None):  # the shingle fallback: no model
                r = self.ms.funnel(self.p, local_only=True)
            self.assertEqual(r["stopped"], "local")
            self.assertEqual((r["calls"], r["paid"]), (1, 0))
            self.assertIn("local-only", r["error"])
        child.assert_not_called()
        self.assertIn("(local-only", self.ms.funnel_line(r))

    def test_night_ready_wants_an_answering_local_model_a_plain_project_and_room_under_the_target(self):  # T-2916
        up = mock.patch.object(self.ms, "_local", return_value=dict(self.PROFILE))
        down = mock.patch.object(self.ms, "_local", return_value=None)
        with up:
            self.assertTrue(self.ms.night_ready(self.p))
            with mock.patch.object(self.ms, "TARGET", 0):
                self.assertFalse(self.ms.night_ready(self.p), "the target is met")
                self.ms.add(self.p, [good()], {"problem": "x", "source": "pain", "kind": "bugs", "mechanism": "law",
                                               "scale": "file", "surface": "terminal"}, "haiku", 1)
                self.assertEqual(self.ms.night_ready(self.p), {"funnel"}, "at the target, unjudged rows still funnel")
            self.assertEqual(self.ms.night_ready(self.p), {"grow", "funnel"})
            self.fm("sensitive", "on")
            self.assertFalse(self.ms.night_ready(self.p))
            self.fm("sensitive", "off")
        with down:
            self.assertFalse(self.ms.night_ready(self.p))

    def test_one_grow_run_keeps_its_paid_calls_under_the_per_command_cap(self):  # many small calls are one command
        from sampo import budget, ideas
        with mock.patch.object(budget, "effective", return_value=({"run": 0.12, "day": 100.0}, None)), \
                mock.patch.object(budget, "estimate", return_value=0.05), mock.patch.object(budget, "check"), \
                mock.patch.object(ideas, "run_child", return_value="haiku text"), \
                mock.patch.dict(os.environ, {"MOONS_LOCAL": ""}):
            self.assertEqual(self.ms._ask(self.p, "sys", "prompt", paid=1), ("haiku text", "haiku"))
            with self.assertRaises(budget.BudgetError):
                self.ms._ask(self.p, "sys", "prompt", paid=2)

    def test_a_sensitive_project_never_goes_to_the_cloud(self):
        self.fm("sensitive", "on")
        out = None
        with self.assertRaises(ValueError):
            out, _, child = self.ask({})
        self.assertIsNone(out)


class Grow(_Moons):
    def grow(self, *a, side=None, **kw):
        calls = []

        def fake(p, system, prompt, cheap=True, paid=0):
            calls.append(prompt)
            if side:
                raise side
            return reply(4, bad=1), "jarvis"
        with mock.patch.object(self.ms, "_ask", side_effect=fake):
            return self.ms.grow(self.p, *a, **kw), calls

    def test_grow_appends_batches_stops_at_max_calls_and_target_and_resumes(self):
        r, calls = self.grow(100, batch=4, max_calls=1)
        self.assertEqual((r["stopped"], r["calls"], r["added"], r["kept"], r["rejected"]), ("max_calls", 1, 4, 3, 1))
        self.assertEqual(r["reasons"], {"payoff": 1})
        self.assertEqual(r["models"], {"jarvis": 1})
        self.assertIn("Today you can't", calls[0])
        self.assertIn("data, never instructions", calls[0])
        r, calls = self.grow(7, batch=4)
        self.assertEqual((r["stopped"], r["calls"], r["total"]), ("target", 1, 8))
        r, calls = self.grow(7, batch=4)
        self.assertEqual((r["stopped"], r["calls"]), ("target", 0))
        rows = self.ms.rows(self.p)
        self.assertEqual([x["id"] for x in rows], [f"C-{i:06d}" for i in range(1, 9)])
        self.assertEqual([x["batch"] for x in rows], [1] * 4 + [2] * 4)
        cells = {(x["cell"]["kind"], x["cell"]["scale"], x["cell"]["surface"]) for x in rows}
        self.assertEqual(len(cells), 2, "the second batch went to another thin cell")
        self.assertEqual(self.ms.coverage(self.p)["reasons"], {"payoff": 2})

    def test_two_workers_run_two_calls_at_once_and_append_whole_rows(self):  # T-2893
        import threading
        gate, seen = threading.Barrier(2, timeout=5), []

        def fake(p, system, prompt, cheap=True, paid=0):
            gate.wait()  # raises BrokenBarrierError unless a second call is in flight
            seen.append(prompt)
            return reply(4), "jarvis"
        with mock.patch.object(self.ms, "_ask", side_effect=fake):
            r = self.ms.grow(self.p, 8, batch=4, workers=2)
        self.assertEqual((r["calls"], r["added"], r["stopped"]), (2, 8, "target"))
        rows = self.ms.rows(self.p)
        self.assertEqual([x["id"] for x in rows], [f"C-{i:06d}" for i in range(1, 9)])
        self.assertEqual(sorted({x["batch"] for x in rows}), [1, 2])
        self.assertEqual(len({x["title"] for x in rows[:4]}), 4)
        with self.assertRaises(ValueError):
            self.ms.grow(self.p, 8, workers=0)

    def test_the_line_counts_local_haiku_and_empty_by_length_per_model(self):
        from sampo import models
        n = []

        def fake(p, system, prompt, cheap=True, paid=0):
            n.append(1)
            if len(n) == 1:
                with self.ms._lock:
                    self.ms._cuts["jarvis"] += 1  # what _ask books when the local reply was cut empty
                return reply(2), "haiku"
            return reply(2), "jarvis"
        with mock.patch.object(self.ms, "_ask", side_effect=fake):
            r = self.ms.grow(self.p, 100, batch=2, max_calls=2)
        self.assertEqual((r["models"], r["cut"]), ({"haiku": 1, "jarvis": 1}, {"jarvis": 1}))
        self.assertIn("haiku 1, jarvis 1; empty by length (reasoning ate the budget): jarvis 1", self.ms.grow_line(r))
        prof = {"name": "jarvis", "kind": "openai", "base_url": "https://127.0.0.1:9/v1", "model": "m",
                "key_env": None, "context": 8192, "tools": False}
        err = models.ModelError("jarvis: reasoning used the whole budget: no text")
        with mock.patch.object(self.ms, "_local", return_value=prof), mock.patch.object(models, "complete", side_effect=err), \
                mock.patch.object(self.ms.ideas, "run_child", return_value="h"):
            self.ms._cuts.clear()
            self.assertEqual(self.ms._ask(self.p, "s", "p"), ("h", "haiku"))
        self.assertEqual(dict(self.ms._cuts), {"jarvis": 1})

    def test_think_and_max_out_reach_the_local_call(self):
        from sampo import models
        prof = {"name": "jarvis", "kind": "openai", "base_url": "https://127.0.0.1:9/v1", "model": "m",
                "key_env": None, "context": 8192, "tools": False, "max_out": 1500}
        with mock.patch.object(self.ms, "_local", return_value=prof), \
                mock.patch.object(models, "complete", return_value={"text": "t"}) as comp:
            self.ms._ask(self.p, "s", "p")
            self.assertEqual((comp.call_args.kwargs["max_tokens"], comp.call_args.kwargs["think"]), (1500, None))
            self.ms._THINK = False
            try:
                self.ms._ask(self.p, "s", "p")
            finally:
                self.ms._THINK = None
            self.assertIs(comp.call_args.kwargs["think"], False)
            self.ms._THINK = True
            try:
                self.assertEqual(self.ms._ask(self.p, "s", "p"), ("t", "jarvis+think"))
            finally:
                self.ms._THINK = None
        cell = {"problem": "slow tests", "source": "pain", "kind": "bugs", "mechanism": "biology", "scale": "file",
                "surface": "terminal"}
        self.ms.add(self.p, [good(), good(kill="")], cell, "jarvis+think", 1)
        self.ms.add(self.p, [good()], cell, "jarvis+nothink", 2)
        by = self.ms.coverage(self.p)["by_model"]
        self.assertEqual(by, {"jarvis+think": {"rows": 2, "kept": 1}, "jarvis+nothink": {"rows": 1, "kept": 1}})
        self.assertIn("Kept by model: jarvis+nothink 1 of 1, jarvis+think 1 of 2", self.ms.coverage_lines(self.ms.coverage(self.p)))

    def test_the_default_local_profile_is_the_first_own_or_loopback_generative_one(self):
        from sampo import models

        def prof(name, base, model, **kw):
            return {"name": name, "kind": "openai", "base_url": base, "model": model, "key_env": None, "context": 8192,
                    "tools": False, **kw}
        conf = {"cloud": prof("cloud", "https://api.example.com/v1", "big"),
                "embed": prof("embed", "http://127.0.0.1:11434/v1", "nomic", own=True),
                "decide": prof("decide", "http://127.0.0.1:11434/v1", "jev", own=True),
                "mine": prof("mine", "https://gpu.example.com/v1", "qwen", own=True),
                "loop": prof("loop", "http://127.0.0.1:8080/v1", "small")}
        env = {k: v for k, v in os.environ.items() if k != "MOONS_LOCAL"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(models, "configured", return_value=(None, conf)), \
                mock.patch.object(models, "_local", side_effect=lambda *a: iter([prof("ollama", "http://127.0.0.1:11434/v1", "gen")])), \
                mock.patch.object(models, "embedding_profiles", return_value=[prof("nomic", "", "nomic")]), \
                mock.patch.object(models, "systemone_profiles", return_value=[prof("jev", "", "jev")]), \
                mock.patch.object(self.ms, "_up", return_value=True):
            self.assertEqual(self.ms._local(False)["name"], "mine")
            self.assertEqual(self.ms._local(True)["name"], "loop", "a sensitive project's is loopback only")
        with mock.patch.dict(os.environ, {"MOONS_LOCAL": ""}), mock.patch.object(models, "configured", return_value=(None, conf)):
            self.assertIsNone(self.ms._local(False), "an empty MOONS_LOCAL turns the local model off")

    def test_grow_tells_each_call_how_many_paid_calls_came_before(self):
        seen = []

        def fake(p, system, prompt, cheap=True, paid=0):
            seen.append(paid)
            return reply(2), ("haiku" if len(seen) < 3 else "jarvis")
        with mock.patch.object(self.ms, "_ask", side_effect=fake):
            self.ms.grow(self.p, 100, batch=2, max_calls=4)
        self.assertEqual(seen, [0, 1, 2, 2], "a local answer costs nothing")

    def test_moons_inside_a_wrapper_object_are_found(self):
        self.assertEqual(len(self.ms._objects(json.dumps({"moons": [good(), good()]}), 8)), 2)
        self.assertEqual(len(self.ms._objects("[" + json.dumps(good()) + ", {\"note\": 1}]", 8)), 1)

    def test_a_batch_takes_no_more_than_it_asked_for(self):
        with mock.patch.object(self.ms, "_ask", return_value=(reply(30), "haiku")):
            r = self.ms.grow(self.p, 100, batch=3, max_calls=1)
        self.assertEqual(r["added"], 3)

    def test_grow_stops_cleanly_on_the_budget_and_after_three_failures(self):
        from sampo import budget
        r, calls = self.grow(50, side=budget.BudgetError("budget: over the cap"))
        self.assertEqual((r["stopped"], r["added"], len(calls)), ("budget", 0, 1))
        self.assertIn("over the cap", r["error"])
        r, calls = self.grow(50, side=ValueError("nothing came back"))
        self.assertEqual((r["stopped"], len(calls)), ("failed", 3))
        with mock.patch.object(self.ms, "_ask", return_value=("no json here", "haiku")):
            self.assertEqual(self.ms.grow(self.p, 50)["stopped"], "failed")
        self.assertEqual(self.ms.rows(self.p), [])

    def test_bad_arguments_are_refused(self):
        for kw in ({"target": -1}, {"target": 5, "batch": 0}, {"target": 5, "batch": 500}, {"target": 5, "max_calls": -2}):
            with self.subTest(kw), self.assertRaises(ValueError):
                self.ms.grow(self.p, **kw)


class Cli(_Moons):
    def test_coverage_and_grow_verbs(self):
        cov = self.fm_json("moons", "coverage")
        self.assertEqual((cov["total"], len(cov["thinnest"])), (0, 10))
        text = self.fm("moons", "coverage").stdout
        self.assertIn("0 candidates", text)
        r = self.fm_json("moons", "grow", "--target", "0")
        self.assertEqual((r["stopped"], r["calls"]), ("target", 0))
        bad = self.fm("moons", "grow", "--batch", "0", check=False)
        self.assertNotEqual(bad.returncode, 0)

    def test_funnel_families_and_promote_verbs(self):
        r = self.fm_json("moons", "funnel")
        self.assertEqual((r["calls"], r["stopped"]), (0, "done"))
        self.assertEqual(self.fm_json("moons", "families")["families"], [])
        self.assertEqual(self.fm_json("moons", "promote", "--max", "0")["blocks"], [])
        self.assertIn("Moons funnel", self.fm("moons", "funnel", "--stage", "kill").stdout)
        self.assertNotEqual(self.fm("moons", "funnel", "--stage", "bogus", check=False).returncode, 0)


# T-2869 ------------------------------------------------------------------------------------------------------------

def moon(title, today, with_this, **kw):
    return good(title=title, today="Today you can't " + today, with_this="With this, you can " + with_this, **kw)


FLAKY = good()
DEPLOY = moon("Roll back a bad deploy before users notice", "undo a Friday deploy without waking the whole team.",
              "pull a broken release out of production in seconds.")
REVIEW = moon("Answer a waiting review within the hour", "get a pull request reviewed without nagging people for days.",
              "merge your code the same day it is ready.")
SECRET = moon("Stop a secret before it is pushed", "see a secret slip into a repo until a scanner emails you.",
              "keep every key out of your code before it leaves your machine.")
NUDGE = moon("Nudge whoever owes you a pull request", "tell who is sitting on your pull request.",
             "get your code merged without chasing anyone.")
FLAKY_SAME = good(title="Catch a FLAKY test, before it reaches anyone!")         # the exact key matches FLAKY's
FLAKY_NEAR = good(title="Catch a flaky test before it reaches anybody")         # one word: a shingle dup
FLAKY_ALSO = moon("Tell flaky tests from real failures", "trust a red build on a busy morning.",
                  "stop rerunning your tests until they pass.")                 # other words, the same idea: embed dup
# the fake embedding: the first keyword the text holds picks its vector (cosine: nudge~review 0.90, mutate~flaky 0.80)
VEC = (("nudge", (0, 0, 0.9, 0.436)), ("mutate", (0.8, 0.6, 0, 0)), ("leak", (0, 0, 0.6, 0.8)), ("flaky", (1, 0, 0, 0)),
       ("deploy", (0, 1, 0, 0)), ("review", (0, 0, 1, 0)), ("secret", (0, 0, 0, 1)))
PROFILE = {"name": "jarvis", "kind": "openai", "base_url": "https://127.0.0.1:9/v1", "model": "m",
           "key_env": "MOONS_TEST_KEY", "context": 8192, "tools": False}


class Judge:
    """A fake _ask for the funnel's judges, routed on the system prompt; answers by title, a default otherwise."""

    def __init__(self, ms, kill=None, tier=None, done=None, side=None):
        from sampo import moons
        self.route = {ms.KILL_SYSTEM: ("kill", kill or {}, "yes | one person, one day, a clear bar"),
                      moons.RATE_SYSTEM: ("tier", tier or {}, "high | wild 3 | a new capability"),
                      ms.NOVEL_SYSTEM: ("novelty", done or {}, "no | nothing does this")}
        self.calls, self.side = [], side

    def __call__(self, p, system, prompt, cheap=True, paid=0, **kw):
        stage, said, default = self.route[system]
        self.calls.append(stage)
        if self.side:
            raise self.side
        out = [f"{n}: {said.get(t, default)}" for n, t in re.findall(r"<moon n=(\d+)>\s*Title: (.*)", prompt)]
        return "\n".join(x for x in out if not x.endswith(": skip")), "jarvis"


class _Funnel(_Moons):
    def setUp(self):
        super().setUp()
        self.embeds = []

    def seed(self, *objs):
        cell = {"problem": "slow tests", "source": "pain", "kind": "bugs", "mechanism": "biology", "scale": "file",
                "surface": "terminal"}
        return [i for i, _, _ in self.ms.add(self.p, list(objs), cell, "haiku", 1)]

    def embed(self, profile, texts, timeout=120):
        self.embeds.append(list(texts))
        return [list(next((v for k, v in VEC if k in t.lower()), (0.5, 0.5, 0.5, 0.5))) for t in texts]

    def go(self, judge=None, local=True, **kw):
        from sampo import models
        judge = judge or Judge(self.ms)
        with mock.patch.object(self.ms, "_ask", side_effect=judge), \
                mock.patch.object(self.ms, "_embedder", return_value=dict(PROFILE) if local else None), \
                mock.patch.object(models, "embed", side_effect=self.embed):
            return self.ms.funnel(self.p, **kw), judge

    def test_the_embed_stage_has_its_own_profile_the_best_ranked_embedding_model(self):  # T-2893
        import http.server
        import threading
        from sampo import models
        seen = []

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _a(self):
                n = int(self.headers.get("Content-Length") or 0)
                seen.append((self.path, json.loads(self.rfile.read(n)) if n else None))
                if self.path == "/api/tags":
                    out = {"models": [{"name": "weak-embed", "capabilities": ["embedding"]},
                                      {"name": "bge-m3:567m", "capabilities": ["embedding"]},
                                      {"name": "gen", "capabilities": ["completion"]}]}
                elif self.path == "/v1/models":
                    out = {"data": [{"id": "bge-m3:567m"}]}
                else:
                    out = {"data": [{"index": 0, "embedding": [1.0, 0.0]}]}
                data = json.dumps(out).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            do_GET = do_POST = _a
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, args=(0.02,), daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        url, real = f"http://127.0.0.1:{srv.server_address[1]}", models.embedding_profiles
        bench = os.path.join(self.p.root, "research", "models")
        os.makedirs(bench)
        with open(os.path.join(bench, "bench.jsonl"), "w") as f:
            for name, rec in (("weak-embed", 0.5), ("bge-m3:567m", 0.9)):
                f.write(json.dumps({"arm": "embedding", "use": "title-to-brief", "backend": name, "recall_at_1": rec}) + "\n")
        env = {k: v for k, v in os.environ.items() if k != "MOONS_EMBED"}
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch.object(models, "embedding_profiles", side_effect=lambda *a: real(url)), \
                mock.patch.object(models, "_local", side_effect=lambda *a: iter(())):
            prof = self.ms._embedder(self.p)
            self.assertEqual(prof["model"], "bge-m3:567m", "the model the bench ranks best")
            self.assertEqual(models.embed(prof, ["a"]), [[1.0, 0.0]])
            self.assertEqual(seen[-1], ("/v1/embeddings", {"model": "bge-m3:567m", "input": ["a"]}))
            self.fm("sensitive", "on")
            self.assertEqual(self.ms._embedder(self.p)["model"], "bge-m3:567m", "loopback is fine for a sensitive project")
        with mock.patch.dict(os.environ, {"MOONS_EMBED": ""}):
            self.assertIsNone(self.ms._embedder(self.p), "an empty MOONS_EMBED turns it off")

    def fates(self):
        return {k: (e["stage"], e["verdict"]) for k, e in self.ms.fate(self.p).items()}

    def events(self):
        with open(os.path.join(self.ms._dir(self.p), self.ms.FUNNEL)) as f:
            return f.read().splitlines()


class Embed(_Moons):
    def test_embed_posts_the_openai_shape_and_orders_by_index(self):
        from sampo import models
        prof = dict(PROFILE, embed_model="e5")
        with mock.patch.dict(os.environ, {"MOONS_TEST_KEY": "k"}), mock.patch.object(models, "_post", return_value={
                "data": [{"index": 1, "embedding": [0, 1.5]}, {"index": 0, "embedding": [1, 0]}]}) as post:
            self.assertEqual(models.embed(prof, ["a", "b"]), [[1, 0], [0, 1.5]])
        url, body, headers = post.call_args[0][:3]
        self.assertEqual((url, body, headers), ("https://127.0.0.1:9/v1/embeddings", {"model": "e5", "input": ["a", "b"]},
                                                {"Authorization": "Bearer k"}))
        with mock.patch.dict(os.environ, {"MOONS_TEST_KEY": "k"}), \
                mock.patch.object(models, "_post", return_value={"data": [{"embedding": [1]}]}) as post:
            models.embed(dict(PROFILE), ["a"])
        self.assertEqual(post.call_args[0][1]["model"], "m", "no embed_model: the profile's model")

    def test_a_bad_reply_or_profile_is_a_model_error(self):
        from sampo import models
        for reply in ({"data": []}, {"data": [{"embedding": ["x"]}]}, {"data": [{"embedding": [True]}]}, {"nope": 1},
                      {"data": [{"embedding": []}]}):
            with self.subTest(reply), mock.patch.dict(os.environ, {"MOONS_TEST_KEY": "k"}), \
                    mock.patch.object(models, "_post", return_value=reply), self.assertRaises(models.ModelError):
                models.embed(dict(PROFILE), ["a"])
        os.environ.pop("MOONS_TEST_KEY", None)
        with self.assertRaises(models.ModelError):
            models.embed(dict(PROFILE), ["a"])  # the key unset
        with self.assertRaises(models.ModelError):
            models.embed(dict(PROFILE, kind="anthropic", key_env=None), ["a"])
        self.assertEqual(models._profile("x", {"model": "m", "embed_model": "e"}, "w")["embed_model"], "e")
        self.assertNotIn("embed_model", models._profile("x", {"model": "m"}, "w"))
        with self.assertRaises(models.ModelError):
            models._profile("x", {"model": "m", "embed_model": 3}, "w")


class Funnel(_Funnel):
    def test_kill_batches_run_at_once_up_to_the_local_slots(self):  # T-2953: 3 min a batch, one at a time
        import threading
        import time
        ids = self.seed(*[moon(f"Moon {i} for case {chr(97 + i % 26)}{i}", f"do thing {i}.", f"do thing {i} today.")
                          for i in range(2 * self.ms.JUDGE_BATCH + 1)])
        judge, live, peak, lock = Judge(self.ms), [0], [0], threading.Lock()

        def slow(*a, **kw):
            with lock:
                live[0] += 1
                peak[0] = max(peak[0], live[0])
            time.sleep(0.2)
            with lock:
                live[0] -= 1
            return judge(*a, **kw)
        rs = self.ms.rows(self.p)
        for stage, run in (("kill", self.ms._kill), ("tier", self.ms._tier)):  # T-2959: the tier stage too
            r = {"stages": {stage: {}}, "calls": 0, "models": {}, "stopped": "", "error": "", "paid": 0, "fails": 0}
            peak[0] = 0
            with mock.patch.object(self.ms, "_ask", side_effect=slow), \
                    mock.patch.object(self.ms, "_local", return_value={"name": "jarvis", "slots": 2}):
                run(self.p, r, rs, self.ms.fate(self.p), rs, None)
            self.assertEqual((stage, peak[0], r["calls"]), (stage, 2, 3))
            self.assertEqual({i: self.fates()[i][0] for i in ids}, {i: stage for i in ids})

    def test_each_candidate_gets_its_fate_and_reason_in_cost_order(self):
        ids = self.seed(FLAKY, DEPLOY, REVIEW, SECRET, NUDGE, FLAKY_SAME, FLAKY_ALSO, good(kill=""))
        judge = Judge(self.ms, kill={DEPLOY["title"]: "no | it needs live production traffic"},
                      tier={FLAKY["title"]: "extreme | wild 5 | new", SECRET["title"]: "low | wild 1 | a check",
                            NUDGE["title"]: "medium | wild 2 | a reminder"},
                      done={REVIEW["title"]: "yes | GitHub's review reminders"})
        r, _ = self.go(judge)
        self.assertEqual(judge.calls, ["kill", "tier", "novelty"], "cheapest first, one batch each")
        self.assertEqual((r["stopped"], r["calls"], r["method"]), ("done", 3, "embed"))
        f = self.ms.fate(self.p)
        self.assertEqual(self.fates(), {
            ids[0]: ("novelty", "kept"), ids[1]: ("kill", "rejected"), ids[2]: ("novelty", "rejected"),
            ids[3]: ("tier", "rejected"), ids[4]: ("tier", "merged"), ids[5]: ("exact", "dup"),
            ids[6]: ("embed", "dup"), ids[7]: ("write", "rejected")})
        self.assertEqual((f[ids[5]]["dup_of"], f[ids[5]]["reason"]), (ids[0], "exact"))
        self.assertEqual((f[ids[6]]["dup_of"], f[ids[6]]["reason"]), (ids[0], "embed"))
        self.assertEqual(f[ids[1]]["reason"], "kill: it needs live production traffic")
        self.assertEqual(f[ids[3]]["reason"], "tier: low or medium")
        self.assertEqual(f[ids[4]]["merged_into"], ids[2])
        self.assertEqual(f[ids[2]]["reason"], "novelty: already done: GitHub's review reminders")
        self.assertEqual((f[ids[0]]["tier"], f[ids[0]]["wild"]), ("extreme", 5))
        self.assertEqual(len(self.embeds), 1, "one embed call for the six rows that passed the exact check")
        self.assertEqual(len(self.embeds[0]), 6)
        with open(os.path.join(self.ms._dir(self.p), self.ms.VECTORS)) as fh:
            self.assertEqual(len(fh.read().splitlines()), 6)
        # export: the funnel's counts, and the one survivor's family
        x = self.ms.export(self.p)["funnel"]
        self.assertEqual((x["generated"], x["write"], x["dups"]), (8, {"kill test": 1}, {"exact": 1, "embed": 1,
                                                                                           "shingle": 0}))
        self.assertEqual((x["rejected"], x["merged"], x["kept"], x["pending"]),
                         ({"kill": 1, "tier": 1, "novelty": 1}, 1, 1, 0))
        fam = self.ms.export(self.p)
        self.assertEqual((fam["families_total"], fam["families"][0]["lead"], fam["families"][0]["tier"]),
                         (1, FLAKY["title"], "extreme"))
        # resumable: a second run judges nothing, embeds nothing and appends nothing
        before, n = self.events(), len(self.embeds)
        r, judge = self.go()
        self.assertEqual((r["calls"], judge.calls, len(self.embeds), self.events()), (0, [], n, before))
        # a new candidate: only its vector is fetched; the rest come from vectors.jsonl
        new = self.seed(moon("Mutate the tests that never fail", "know which of your tests would catch a real bug.",
                             "delete the tests that guard nothing in your code."))
        self.go(stage="exact")
        r, _ = self.go(stage="embed")
        self.assertEqual(self.embeds[-1], [self.ms._text(self.ms.rows(self.p)[-1])])
        self.assertEqual(self.fates()[new[0]], ("embed", "kept"))
        self.assertEqual(list(r["stages"]), ["embed"], "--stage runs that stage alone")

    def test_the_shingle_fallback_when_no_model_embeds(self):
        from sampo import models
        ids = self.seed(FLAKY, FLAKY_NEAR, FLAKY_ALSO, DEPLOY)
        r, _ = self.go(local=False, stage="exact")
        self.assertEqual(list(r["stages"]), ["exact"])
        r, _ = self.go(local=False, stage="embed")
        self.assertEqual(r["method"], "shingle")
        f = self.ms.fate(self.p)
        self.assertEqual((f[ids[1]]["verdict"], f[ids[1]]["reason"], f[ids[1]]["dup_of"]), ("dup", "shingle", ids[0]))
        self.assertEqual([f[i]["verdict"] for i in (ids[0], ids[2], ids[3])], ["kept"] * 3)
        self.assertEqual(f[ids[2]]["reason"], "shingle")
        self.assertEqual(self.embeds, [])
        with mock.patch.object(self.ms, "_local", return_value=dict(PROFILE)), \
                mock.patch.object(models, "embed", side_effect=models.ModelError("no /embeddings here")):
            self.assertEqual(self.ms._reps(self.p, self.ms.rows(self.p))[0], "shingle")

    def test_a_kill_test_that_needs_a_team_is_rejected_with_why_and_a_missed_answer_waits(self):
        ids = self.seed(FLAKY, DEPLOY, REVIEW)
        judge = Judge(self.ms, kill={DEPLOY["title"]: "no | it needs ten engineers for a month",
                                     REVIEW["title"]: "skip"})
        self.go(judge, stage="exact")
        self.go(judge, stage="embed")
        r, _ = self.go(judge, stage="kill")
        self.assertEqual(self.fates(), {ids[0]: ("kill", "kept"), ids[1]: ("kill", "rejected"),
                                        ids[2]: ("embed", "kept")})
        self.assertEqual(self.ms.fate(self.p)[ids[1]]["reason"], "kill: it needs ten engineers for a month")
        r, judge = self.go(stage="kill")
        self.assertEqual((judge.calls, self.fates()[ids[2]]), (["kill"], ("kill", "kept")))

    def test_the_novelty_stage_rejects_a_near_catalogue_title_unasked(self):
        ids = self.seed(FLAKY, DEPLOY)
        os.makedirs(self.ms.rune.home(self.p), exist_ok=True)
        with open(os.path.join(self.ms.rune.home(self.p), "moonshot.md"), "w") as f:
            f.write("# Moonshot catalogue\n\n### M-01 · Catch flaky tests early\n- Tier: high\n")
        r, judge = self.go()
        f = self.ms.fate(self.p)
        self.assertEqual((f[ids[0]]["stage"], f[ids[0]]["verdict"]), ("novelty", "rejected"))
        self.assertTrue(f[ids[0]]["reason"].startswith("novelty: near M-01"), f[ids[0]]["reason"])
        self.assertEqual(self.fates()[ids[1]], ("novelty", "kept"))

    def test_max_calls_and_the_budget_stop_a_run_that_resumes(self):
        from sampo import budget
        ids = self.seed(FLAKY, DEPLOY)
        r, judge = self.go(max_calls=1)
        self.assertEqual((r["stopped"], judge.calls), ("max_calls", ["kill"]))
        self.assertEqual(self.fates()[ids[0]], ("kill", "kept"))
        r, judge = self.go(Judge(self.ms, side=budget.BudgetError("budget: over the cap")))
        self.assertEqual((r["stopped"], r["calls"]), ("budget", 1))
        self.assertIn("over the cap", r["error"])
        self.assertEqual(self.fates()[ids[0]], ("kill", "kept"))
        r, judge = self.go(Judge(self.ms, side=ValueError("down")))
        self.assertEqual((r["stopped"], len(judge.calls)), ("failed", 3))
        r, judge = self.go()
        self.assertEqual((r["stopped"], judge.calls), ("done", ["tier", "novelty"]))
        self.assertEqual(self.fates()[ids[1]], ("novelty", "kept"))
        with self.assertRaises(ValueError):
            self.ms.funnel(self.p, stage="bogus")


class Families(_Funnel):
    def survive(self, *rows):
        """Each (moon, tier, wild) stored and marked kept at novelty, as the funnel would."""
        ids = self.seed(*(m for m, _, _ in rows))
        lines = [json.dumps({"id": i, "at": "2026-11-03T00:00:00Z", "stage": "novelty", "verdict": "kept",
                             "reason": "", "model": "jarvis", "tier": t, "wild": w}) for i, (_, t, w) in zip(ids, rows)]
        self.c.append_line(os.path.join(self.ms._dir(self.p), self.ms.FUNNEL), "\n".join(lines))
        return ids

    def build(self, local=True):
        from sampo import models
        with mock.patch.object(self.ms, "_local", return_value=dict(PROFILE) if local else None), \
                mock.patch.object(models, "embed", side_effect=self.embed):
            return self.ms.families(self.p)

    MUTATE = moon("Mutate the tests that never fail", "know which of your tests would catch a real bug.",
                  "delete the tests that guard nothing in your code.")
    LEAK = moon("Trace where a leak started", "find which commit let a key out of your repo.",
                "rotate only the keys that were exposed in your code.")

    def test_families_are_stable_and_led_by_tier_then_wild_then_the_earliest(self):
        ids = self.survive((FLAKY, "high", 3), (DEPLOY, "extreme", 4), (self.MUTATE, "high", 5), (SECRET, "xhigh", 2),
                           (self.LEAK, "xhigh", 2))
        r = self.build()
        got = [(f["id"], f["lead"], f["variants"], f["size"]) for f in r["families"]]
        self.assertEqual(got, [("F-000002", ids[1], [], 1), ("F-000004", ids[3], [ids[4]], 2),
                               ("F-000003", ids[2], [ids[0]], 2)])
        self.assertEqual(r["families"][0]["kinds"], ["bugs"])
        self.assertEqual(r["families"][0]["mechanisms"], ["biology"])
        path = os.path.join(self.ms._dir(self.p), self.ms.FAMILIES)
        with open(path) as f:
            first = f.read()
        self.assertEqual(self.build()["families"], r["families"])
        self.assertEqual(self.build(local=False)["families"], r["families"], "the server down: the cached vectors")
        with open(path) as f:
            self.assertEqual(f.read(), first, "a rerun writes the same file")
        self.assertEqual(self.ms.scale_problems(self.p), [])


class Promote(_Funnel):
    def setUp(self):
        super().setUp()
        from sampo import rune
        self.rune = rune
        rune.init(self.p, GEN0_CAPS.encode())
        self.doc = os.path.join(rune.home(self.p), "moonshot.md")
        with open(self.doc, "w") as f:
            f.write("# Moonshot catalogue\n\n### M-01 · Market for lane time\n- Tier: high\n\n"
                    "### M-02 · Grow a test garden\n- Tier: xhigh\n")

    def test_leads_land_in_moonshot_md_through_the_cold_read_once(self):
        from sampo import ideas
        ids = Families.survive(self, (FLAKY, "high", 3), (DEPLOY, "extreme", 4), (Families.MUTATE, "massive", 5),
                               (SECRET, "xhigh", 2))
        self.build_families()
        seen = []

        def child(feature, system, prompt, model, timeout, project=None, **kw):
            seen.append((feature, model))
            if feature == "genesis-read":
                return "CLEAN"
            if feature == "moonshot-rate":
                return "\n".join(f"{i}: massive | wild 5 | bold" for i in range(1, 30))
            return ("Kill: Run it on 10 repos for one day; if it catches fewer than 3 real bugs, it is dead.\n"
                    "Better by: no tool mutates and deletes tests on its own\nNovelty: 5\nNeeds: none\n")
        with mock.patch.object(self.rune, "REVIEW_MODELS", ("haiku", "opus-x")), \
                mock.patch.object(ideas, "run_child", side_effect=child), \
                mock.patch.object(self.rune, "put", wraps=self.rune.put) as put:
            r = self.ms.promote(self.p)
            self.assertEqual(r["blocks"], ["M-03", "M-04"], r)
            self.assertEqual(put.call_args[0][1], "moonshot.md")
            self.assertIn(("moons-promote", "opus-x"), seen, "the strongest model designs the kill test")
            self.assertIn("genesis-read", [f for f, _ in seen], "the cold read passed it")
            again = self.ms.promote(self.p)
        self.assertEqual(again["blocks"], [], "a promoted family isn't promoted twice")
        with open(self.doc) as f:
            doc = f.read()
        block = doc[doc.index("### M-03"):doc.index("### M-04")]
        for want in (f"### M-03 · {Families.MUTATE['title']}", "- Tier: massive", "- Domain: bugs", "- Lens: biology",
                     "- What: Today you can't", "- Prior art: flaky-test dashboards", "- Better by: no tool mutates",
                     "- Novelty: 5", "- Needs: none", "- Unblocks: none", "- Kill: Run it on 10 repos", "- Stage: idea",
                     "- Family: F-000003 (1 variant)"):
            self.assertIn(want, block)
        self.assertIn(f"### M-04 · {DEPLOY['title']}", doc)
        self.assertNotIn(SECRET["title"], doc, "an xhigh lead isn't promoted")
        from sampo import moons
        rated = {x["id"]: x["reviewer"] for x in moons.rows(self.p)}
        self.assertEqual(rated["M-03"], "massive", "moons.rate gave the cold tier")
        self.assertFalse([x for x in moons.check(self.p) if "family" in x.lower()])
        out = os.path.join(self.tmp, "site")
        self.rune.export(self.p, out)
        with open(os.path.join(out, "genesis.json")) as f:
            sc = json.load(f)["moons_scale"]
        self.assertEqual(sc["funnel"]["generated"], 4)
        lead = next(x for x in sc["families"] if x["id"] == "F-000003")
        self.assertEqual((lead["cold"], lead["stage"], lead["size"]), ("massive", "idea", 2))

    def build_families(self):
        return Families.build(self)

    def test_check_names_a_family_line_with_no_family_unknown_ids_and_stale_families(self):
        Families.survive(self, (FLAKY, "high", 3))
        bad = self.ms.scale_problems(self.p)
        self.assertTrue(any("families.json" in x for x in bad), bad)
        self.build_families()
        self.assertEqual(self.ms.scale_problems(self.p), [])
        with open(self.doc, "a") as f:
            f.write("\n### M-03 · Ghost\n- Tier: massive\n- Family: F-999999 (2 variants)\n")
        self.c.append_line(os.path.join(self.ms._dir(self.p), self.ms.FUNNEL),
                           json.dumps({"id": "C-999999", "stage": "kill", "verdict": "kept"}))
        bad = self.ms.scale_problems(self.p)
        self.assertTrue(any("F-999999" in x for x in bad), bad)
        self.assertTrue(any("C-999999" in x for x in bad), bad)
        from sampo import moons
        self.assertTrue(any("F-999999" in x for x in moons.check(self.p)))


class PromoteDomain(_Moons):
    def test_a_lead_domain_reads_as_plain_words(self):
        # T-2940: promote wrote 'refactors, at ecosystem scale, in the phone' and the cold read refused the catalogue
        from sampo import moonscale as ms
        self.assertEqual(ms._domain({"kind": "refactors", "scale": "ecosystem", "surface": "phone"}),
                         "refactors across the open-source ecosystem, from a phone")
        for s in ms.SCALES:
            for u in ms.SURFACES:
                d = ms._domain({"kind": "bugs", "scale": s, "surface": u})
                self.assertNotRegex(d, r" scale,|in the phone|in the CI|in the chat")
                self.assertTrue(d.startswith("bugs "), d)
