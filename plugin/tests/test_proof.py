"""fm proof: done tasks whose claims no run here proved (T-2273): typed evidence, inconclusive runs, UI edits unshot."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


class Proof(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def task(self, *files, evidence=(), type="FIX", lines=(), decision=None, base=None, log=()):
        """A done task; evidence: (flags..., cmd, result) tuples handed to fm task evidence; files: its edits; lines:
        (step, cmd, result) evidence lines written as fm's own runs (ran); base: the commit its change starts at."""
        tid = self.fm_json("task", "new", "Do a thing", "--type", type, "--tier", "S", "--ac", "ok :: true",
                           "--step", "s")["id"]
        for ev in evidence:
            self.fm("task", "evidence", tid, *ev)
        for f in files:
            path = os.path.join(self.repo, f)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if not os.path.exists(path):  # the classifiers read the file itself
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("FROM scratch\n" if f.endswith("Dockerfile") else "x\n")
            c.log_event(self.p, "touched", task=tid, data={"file": path})
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, tid)
            for step, cmd, result in lines:
                b.add_evidence(cmd, result, step=step, ran=True)
            for x in log:
                b.append_log(x)
            if decision:
                b.set_section("Decision", decision)
            if base:
                b.meta["base"] = base
            b.meta["status"] = "done"
            c.save_brief(self.p, b)
        return tid

    def needs(self, tid):
        return {x["kind"]: x for x in next(r for r in c.unproven(self.p) if r["id"] == tid)["needs"]}

    def listed(self):
        return {x["id"]: x["kinds"] for x in self.fm_json("proof")["tasks"]}

    def test_typed_inconclusive_and_unshot_ui_are_each_listed(self):
        typed = self.task(evidence=[("--step", "1", "pytest", "9 passed")])
        inc = self.task(evidence=[("--step", "1", "--run", "true", "--inconclusive")])
        ui = self.task("web/app.css", evidence=[("--step", "1", "--run", "true")])
        got = self.listed()
        self.assertEqual(got[typed], ["typed"])
        self.assertEqual(got[inc], ["inconclusive"])
        self.assertEqual(got[ui], ["ui-unshot"])

    def test_a_task_whose_every_check_ran_green_is_never_listed(self):
        ok = self.task("calc.py", evidence=[("--step", "1", "--run", "true")])
        shot = self.task("web/app.css", evidence=[("--step", "1", "--run", "true"),
                                                  ("--step", "1", "--run", "echo fm shot app.css")])
        self.assertNotIn(ok, self.listed())
        self.assertNotIn(shot, self.listed(), "a shot named in the evidence covers the UI change")

    def test_a_later_green_run_supersedes_a_typed_or_inconclusive_line(self):
        t = self.task(evidence=[("--step", "1", "pytest", "ok"), ("--step", "1", "--run", "true")])
        self.assertNotIn(t, self.listed())

    def test_a_warm_status_reads_the_cache_not_the_briefs_or_the_ledger(self):
        from unittest import mock
        t = self.task(evidence=[("--step", "1", "pytest", "ok")])
        tdir = os.path.join(self.p.dir, "tasks")
        src = next(f for f in os.listdir(tdir) if f.startswith(t))
        text = open(os.path.join(tdir, src), encoding="utf-8").read()
        for i in range(500):  # 500 more closed briefs
            n = 900 + i
            with open(os.path.join(tdir, f"T-{n}-x.md"), "w", encoding="utf-8") as f:
                f.write(text.replace(t, f"T-{n}"))
        self.assertIn("unproven: 501", self.fm("status").stdout)  # cold: fills the cache
        with mock.patch.object(c, "ledger_tail", side_effect=AssertionError("ledger read")), \
                mock.patch.object(c, "load_briefs", wraps=c.load_briefs) as lb:
            self.assertGreaterEqual(c.unproven_cached(self.p), 0)
            self.assertEqual(lb.call_count, 0, "a warm call never loads the closed briefs")
        t2 = self.task(evidence=[("--step", "1", "pytest", "ok")])  # a new closed brief changes the key
        self.assertIn(t2, [r["id"] for r in c.unproven(self.p)])
        self.assertEqual(self.fm_json("status", "--json")["unproven"], c.unproven_cached(self.p))

    def test_the_window_bounds_the_list_and_the_count_is_on_status_and_digest(self):
        t = self.task(evidence=[("--step", "1", "pytest", "ok")])
        self.assertEqual(self.fm_json("proof", "--days", "7")["count"], 1)
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, t)
            b.meta["updated"] = "2020-01-01T00:00:00Z"
            c.save_brief(self.p, b, touch=False)
        self.assertEqual(self.fm_json("proof", "--days", "7")["count"], 0)
        self.assertEqual(self.fm_json("proof", "--days", "100000")["count"], 1)
        self.assertEqual(self.fm("proof").stdout.count(t), 0)
        t2 = self.task(evidence=[("--step", "1", "pytest", "ok")])
        self.assertIn("unproven: 1 (fm proof)", self.fm("status").stdout)
        self.assertIn("unproven: 1 (fm proof)", self.fm("digest").stdout)
        self.assertEqual(self.fm_json("status", "--json")["unproven"], 1)
        self.assertIn(t2, self.fm("proof").stdout)
        self.assertEqual(json.loads(self.fm("proof", "--json").stdout)["count"], 1)

    # --- T-2391: the proof-kinds table, one row per domain
    GREEN, RED, RED1ST = "exit 0 · ok", "✗ exit 1 · boom", "red as expected (exit 1) · boom"

    def test_rollup_red_first_a_red_step_counts_only_when_the_same_command_ran_green_later(self):
        later = self.task(lines=[(1, "pytest -q t", self.RED1ST), (2, "pytest -q t", self.GREEN)])
        never = self.task(lines=[(1, "pytest -q t", self.RED)])
        before = self.task(lines=[(2, "pytest -q t", self.GREEN), (1, "pytest -q t", self.RED)])
        other = self.task(lines=[(1, "pytest -q a", self.RED), (2, "pytest -q b", self.GREEN)])
        got = self.listed()
        self.assertNotIn(later, got, "red then the same command green: proven")
        self.assertEqual(got[never], ["red"])
        self.assertEqual(got[before], ["red"], "a green run before the red one doesn't clear it")
        self.assertEqual(got[other], ["red"], "a different command's green run doesn't clear it")

    def test_rollup_red_first_a_bench_line_is_a_green_run(self):
        bench = "slow: 2.000s → 1.000s (5 runs each)"
        t = self.task(type="PERFORMANCE", lines=[(1, "slow", self.RED1ST), (1, "slow", bench)])
        self.assertNotIn(t, self.listed())

    def test_proof_kind_table_names_every_kind_with_its_upgrade_command(self):
        for kind in ("typed", "red", "inconclusive", "ui-unshot", "docs", "infra", "migration", "data", "perf-typed",
                     "perf-noise", "research-uncited", "hollow"):
            row = c.PROOF_KINDS[kind]
            self.assertTrue(row["need"] and row["upgrade"] and "{id}" in row["upgrade"], kind)
        t = self.task("data/users.csv")
        out = self.fm("proof").stdout
        self.assertIn(t, out)
        self.assertIn(f"fm task evidence {t} --run", out, "each row prints its upgrade command")

    def _doc_task(self, text):
        base = c._git(self.repo, "rev-parse", "HEAD").strip()
        os.makedirs(os.path.join(self.repo, "docs"), exist_ok=True)
        with open(os.path.join(self.repo, "docs", "guide.md"), "a", encoding="utf-8") as f:
            f.write(text)
        c._git(self.repo, "add", "-A")
        c._git(self.repo, "-c", "user.email=t@e.c", "-c", "user.name=t", "commit", "-qm", "docs")
        return self.task("docs/guide.md", evidence=[("--step", "1", "--run", "true")], base=base)

    def test_proof_kind_docs_needs_a_checkable_claim_in_the_lines_the_task_added(self):
        claim = self._doc_task("Run `fm proof --days 7` to see it.\n")
        prose = self._doc_task("This is only prose about nothing you could run.\n")
        got = self.listed()
        self.assertEqual(got[claim], ["docs"])
        self.assertNotIn(prose, got, "a prose-only edit never counts")
        self.assertIn("fm prove --docs", self.needs(claim)["docs"]["upgrade"])

    def test_proof_kind_docs_is_cleared_by_a_green_prove_docs_run(self):
        t = self._doc_task("Use `make test` first.\n")
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, t)
            b.add_evidence("fm prove --docs", self.GREEN, step=1, ran=True)
            c.save_brief(self.p, b)
        self.assertNotIn(t, self.listed())

    def test_proof_kind_infra_migration_and_data_are_read_from_the_files_touched(self):
        run = [("--step", "1", "--run", "true")]
        infra = self.task("Dockerfile", evidence=run)
        mig = self.task("db/migrations/001_init.sql", evidence=run)
        data = self.task("data/users.csv", evidence=run)
        code = self.task("calc.py", evidence=run)
        got = self.listed()
        self.assertEqual((got[infra], got[mig], got[data]), (["infra"], ["migration"], ["data"]))
        self.assertNotIn(code, got)
        self.assertIn("fm prove --infra", self.needs(infra)["infra"]["upgrade"])
        self.assertIn("fm prove --migration", self.needs(mig)["migration"]["upgrade"])
        cleared = self.task("Dockerfile", "data/users.csv", evidence=run,
                            lines=[(1, "fm prove --infra", self.GREEN), (1, "dbt test", self.GREEN)])
        self.assertNotIn(cleared, self.listed(), "the green run that clears a kind removes it")

    def test_proof_kind_perf_typed_is_a_performance_close_without_a_bench_run(self):
        plain = self.task(type="PERFORMANCE", evidence=[("--step", "1", "--run", "true")])
        bench = self.task(type="PERFORMANCE", lines=[(1, "slow", "slow: 2.000s → 1.000s (5 runs each)")])
        fix = self.task(evidence=[("--step", "1", "--run", "true")])
        got = self.listed()
        self.assertEqual(got[plain], ["perf-typed"])
        self.assertNotIn(bench, got)
        self.assertNotIn(fix, got, "only PERFORMANCE closes need a bench")
        self.assertIn("--bench", self.needs(plain)["perf-typed"]["upgrade"])

    def test_perf_noise_a_bench_inside_the_gates_noise_band_is_listed(self):
        noisy = self.task(type="PERFORMANCE", lines=[(1, "slow", "slow: 1.000s → 0.950s (5 runs each)")])
        real = self.task(type="PERFORMANCE", lines=[(1, "slow", "slow: 1.000s → 0.500s (5 runs each)")])
        slower = self.task(type="PERFORMANCE", lines=[(1, "slow", "slow: 1.000s → 1.800s (5 runs each)")])
        got = self.listed()
        self.assertEqual(got[noisy], ["perf-noise"])
        self.assertNotIn(real, got)
        self.assertNotIn(slower, got, "a change past the band either way is not noise")
        self.assertIn("--repeat", self.needs(noisy)["perf-noise"]["upgrade"])

    def test_proof_kind_research_uncited_names_no_saved_note_with_a_verified_claim(self):
        notes = os.path.join(self.p.dir, "research")
        os.makedirs(notes, exist_ok=True)
        with open(os.path.join(notes, "queues.md"), "w", encoding="utf-8") as f:
            f.write("# queues\n- ✓ claim one\n")
        with open(os.path.join(notes, "weak.md"), "w", encoding="utf-8") as f:
            f.write("# weak\n- ? claim\n")
        bare = self.task(type="RESEARCH", decision="Use a queue.")
        cited = self.task(type="RESEARCH", decision="Use a queue (research/queues.md).")
        weak = self.task(type="RESEARCH", decision="Use a queue (weak.md).")
        got = self.listed()
        self.assertEqual(got[bare], ["research-uncited"])
        self.assertEqual(got[weak], ["research-uncited"], "a note with no verified claim isn't a citation")
        self.assertNotIn(cited, got)
        self.assertIn("fm ask", self.needs(bare)["research-uncited"]["upgrade"])

    def test_proof_kind_hollow_is_a_criterion_the_newest_vacuous_run_found_passing_on_the_start_tree(self):
        run = [("--step", "1", "--run", "true")]
        hollow = self.task(evidence=run, log=["vacuous checks: ac 1"])
        fixed = self.task(evidence=run, log=["vacuous checks: ac 1", "vacuous checks: none"])
        got = self.listed()
        self.assertEqual(got[hollow], ["hollow"])
        self.assertNotIn(fixed, got)
        self.assertIn("--vacuous", self.needs(hollow)["hollow"]["upgrade"])

    def test_unproven_line_is_one_function_the_four_renderers_call(self):
        self.assertEqual(c.unproven_line(3), "unproven: 3 (fm proof)")
        self.assertEqual(c.unproven_line(3, {"docs": 2, "typed": 1}), "unproven: 3 (fm proof) · typed 1, docs 2")
        self.assertEqual(c.unproven_line(0), "")
        self.task(evidence=[("--step", "1", "pytest", "ok")])
        for verb in ("status", "digest"):  # one function's text, with the kind counts
            self.assertIn(c.unproven_line(1, {"typed": 1}), self.fm(verb).stdout, verb)
        import fmexam
        import fmgenesis
        for mod in (fmexam, fmgenesis):  # their renderers need a whole tower or exam run; the call is what's checked
            self.assertIn("c.unproven_line(", open(mod.__file__, encoding="utf-8").read(), mod.__name__)

    def test_unproven_line_fm_proof_json_carries_per_kind_counts(self):
        self.task(evidence=[("--step", "1", "pytest", "ok")])
        self.task("data/a.csv", evidence=[("--step", "1", "--run", "true")])
        self.task("data/b.csv", evidence=[("--step", "1", "pytest", "ok")])
        d = self.fm_json("proof")
        self.assertEqual(d["counts"], {"typed": 2, "data": 2})
        self.assertEqual(d["count"], 3)

    def test_proof_kind_finish_names_each_rollup_kind_the_closing_task_still_needs(self):
        self.fm("task", "new", "One", "--type", "FEATURE", "--tier", "S", "--ac", "ran :: true", "--step", "a",
                "--focus")
        c.log_event(self.p, "touched", task="T-0001", data={"file": os.path.join(self.repo, "data/users.csv")})
        out = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check").stdout
        block = out.split("Not verified", 1)[1]
        self.assertIn("data", block)
        self.assertIn("fm task evidence T-0001 --run", block)

    def test_proof_kind_next_names_the_newest_unproven_row_that_can_run_here(self):
        from unittest import mock
        old = self.task(evidence=[("--step", "1", "pytest", "ok")])
        wait = self.task("Dockerfile", evidence=[("--step", "1", "--run", "true")])
        with mock.patch.object(c.shutil, "which", return_value=None):
            rows = {r["id"]: r for r in self.fm_json("proof")["tasks"]}
            self.assertTrue(rows[wait]["needs"][0]["waiting"], "a missing tool is waiting, not a to-do")
            self.assertIn("waiting", self.fm("proof").stdout)
            nxt = c.next_for(self.p)[2]
        self.assertIn(old, nxt, "the newer row waits on an install, so the older runnable one is named")
        self.assertNotIn(wait, nxt)
        self.assertIn(f"fm task evidence {old} --run", nxt)

    def test_proof_kind_next_is_silent_with_a_queue_and_when_nothing_can_run(self):
        from unittest import mock
        wait = self.task("Dockerfile", evidence=[("--step", "1", "--run", "true")])
        with mock.patch.object(c.shutil, "which", return_value=None):
            self.assertNotIn(wait, c.next_for(self.p)[2])
        self.fm("task", "new", "Queued", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        with mock.patch.object(c.shutil, "which", return_value="/bin/true"):
            self.assertNotIn("fm prove", c.next_for(self.p)[2], "a queued task comes first")
