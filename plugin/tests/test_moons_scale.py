"""T-2868: Moonscale part 1 — the candidate store, the write-time admit rules, the grid read thin-first, and grow routed
local-first then Haiku, budget-capped and resumable. Every model call here is mocked."""
# map-links: plugin/lib/sampo/moonscale.py plugin/lib/sampo/rune.py
import json
import os
from unittest import mock

from helpers import ForemanTestCase


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
        with mock.patch.dict(os.environ, env), mock.patch.object(models, "resolve", return_value=dict(self.PROFILE)), \
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
        with mock.patch.dict(os.environ, {"MOONS_TEST_KEY": "k"}), \
                mock.patch.object(models, "resolve", return_value=dict(self.PROFILE)), \
                mock.patch.object(self.ms, "_up", return_value=True), \
                mock.patch.object(models, "complete", side_effect=models.ModelError("down")), \
                mock.patch.object(ideas, "run_child", return_value="haiku text"):
            self.assertEqual(self.ms._ask(self.p, "sys", "prompt"), ("haiku text", "haiku"))

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
