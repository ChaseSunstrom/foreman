"""T-0691 (Intelligence — planning and decomposition 1): replan on surprise or a false assumption, stress-test roles for
the second plan read, step order by risk, decomposition recipes, skeleton and spike steps, planned obligations, plans
bound to assumptions, and sizing against what tasks usually take."""
import json
import os
import time

from helpers import ForemanTestCase, read_text

import fmcore as c

REFS = os.path.join(c.PLUGIN_ROOT, "skills", "intake", "references")
STUB = r'''#!/usr/bin/env python3
import os, sys
sys.stdin.read()
with open(os.environ["ARGV_OUT"], "w") as f:
    f.write(" ".join(sys.argv))
print("## Objections\n- HIGH: the rollout has no canary — add one\nVerdict: revise — add the canary")
'''


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        with open(os.path.join(self.repo, "p.txt"), "w") as f:
            f.write("ok\n")

    def mid(self, title="Sync", *steps, tier="M", focus=True):
        self.fm("task", "new", title, "--type", "FEATURE", "--tier", tier, "--interpretation", "x", "--approach",
                "a vs b: a", "--ac", "syncs :: grep -q ok p.txt", *[a for s in steps or ["s"] for a in ("--step", s)],
                *(["--focus"] if focus else []))
        return c.load_briefs(self.p)[-1].id

    def next(self):
        return self.fm("next").stdout


class Replan(Base):
    def test_a_surprise_on_an_active_m_task_leads_fm_next_until_answered(self):
        tid = self.mid()
        self.fm("surprise", "expected one page → the API returned three")
        self.assertRegex(self.next(), rf"replan {tid}: surprise: expected one page")
        self.fm("task", "log", tid, "replan: loop over pages")
        self.assertNotIn("replan", self.next())
        self.assertIn("plan revision needed", c.find_brief(self.p, tid).section("Log"))

    def test_an_unanswered_replan_warns_at_close(self):
        import fmcli
        tid = self.mid()
        self.fm("surprise", "expected a → got b")
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, tid), [])
        self.assertTrue(any("replan never answered" in w for w in warns), warns)

    def test_an_s_task_gets_no_replan(self):
        self.fm("task", "new", "Tiny", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.fm("surprise", "expected a → got b")
        self.assertNotIn("replan", self.next())


class Bind(Base):
    def test_a_false_assumption_names_the_steps_that_cite_it(self):
        tid = self.mid("Sync", "Read the config", "Fetch every page (A1)")
        self.fm("task", "assume", tid, "add", "the API paginates")
        self.fm("task", "assume", tid, "verify", "1", "--run", "false", check=False)
        out = self.next()
        self.assertRegex(out, rf"replan {tid}: assumption 1 is false.*step 2 cites it")


class Roles(Base):
    def test_second_plan_takes_a_stress_test_role(self):
        bindir, argv = os.path.join(self.tmp, "bin"), os.path.join(self.tmp, "argv.txt")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        tid = self.mid(focus=False)
        env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "ARGV_OUT": argv}
        self.fm("second", "plan", tid, "--role", "pre-mortem", "--force", env=env)
        self.assertIn("six weeks", read_text(argv))
        self.assertIn("no canary", c.find_brief(self.p, tid).section("Plan review: pre-mortem"))
        self.assertNotEqual(self.fm("second", "plan", tid, "--role", "oracle", check=False, env=env).returncode, 0)


class Order(Base):
    def test_focus_flags_an_unknown_explored_after_a_step_hard_to_undo(self):
        self.mid("Schema", "Deploy the new schema", "Spike: measure the query latency", focus=False)
        self.assertIn("unknowns first", self.fm("focus", "T-0001").stdout)

    def test_the_right_order_is_quiet(self):
        self.mid("Schema", "Spike: measure the query latency", "Add a dropdown", "Prototype the filter",
                 "Deploy the new schema", focus=False)
        self.assertNotIn("unknowns first", self.fm("focus", "T-0001").stdout)


class Recipes(Base):
    def test_decomposition_recipes_exist_and_planning_links_them(self):
        text = read_text(os.path.join(REFS, "decomposition.md")).lower()
        for word in ("expand", "contract", "walking skeleton", "test ladder", "one observable"):
            self.assertIn(word, text)
        self.assertIn("decomposition.md", read_text(os.path.join(REFS, "planning.md")))


class Skeleton(Base):
    def test_planning_has_the_walking_skeleton_and_spike_step_rules(self):
        text = read_text(os.path.join(REFS, "planning.md"))
        self.assertRegex(text.lower(), r"feature l.*walking skeleton")
        self.assertIn("Spike:", text)


class Obligations(Base):
    def test_rubric_names_obligations_and_an_l_close_without_rollback_warns(self):
        text = read_text(os.path.join(REFS, "planning.md")).lower()
        for word in ("contain", "cure", "inoculate", "cleanup"):
            self.assertIn(word, text)
        import fmcli
        tid = self.mid("Big", tier="L", focus=False)
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, tid), [])
        self.assertTrue(any("Risks and rollback" in w for w in warns), warns)


class Estimate(Base):
    def test_fm_next_suggests_a_reframe_past_twice_the_usual_and_digest_shows_scope_growth(self):
        tid = self.mid("Slow", tier="S")
        old = lambda m: c.iso(time.time() - m * 60)
        rows = []
        for i in range(3):
            t = f"T-01{i:02d}"
            rows += [{"ts": old(90), "task": t, "event": "task_new", "data": {"type": "FEATURE", "tier": "S"}},
                     {"ts": old(90), "task": t, "event": "focus", "data": {}},
                     {"ts": old(89), "task": t, "event": "task_done", "data": {"planned": 2, "changed": 4}}]
        rows.append({"ts": old(30), "task": tid, "event": "focus", "data": {}})
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
        self.assertRegex(self.next(), r"on it \d+ min, over twice the usual 1 min for a FEATURE S: re-frame")
        self.assertNotIn("usually takes", self.next())
        self.assertRegex(self.fm("digest").stdout, r"Planned vs changed files: .*×2\.0")
