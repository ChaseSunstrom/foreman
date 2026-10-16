"""T-0677: planning, briefs and queue — first versions: a deferral's revisit date, the usual minutes in fm next,
standing orders, tier drift at done, assumption re-checks, a build-vs-reuse line before an L feature is approved, and
MASTER.md naming every module."""
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def new(self, title, type_="FEATURE", tier="S", *extra):
        return self.fm_json("task", "new", title, "--type", type_, "--tier", tier, "--ac", "ok :: true", "--step", "s",
                            *extra)["id"]

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)


class DeferRevisit(Base):
    def test_a_deferral_comes_back_at_its_revisit_date(self):
        old, later = self.new("Old idea"), self.new("Later idea")
        self.fm("task", "defer", old, "after the v2 launch", "--until", "2020-01-01")
        self.fm("task", "defer", later, "next quarter", "--until", "2999-01-01")
        out = self.fm("next").stdout
        self.assertIn(old, out)
        self.assertIn("revisit", out)
        self.assertNotIn(later, out)


class UsualMinutes(Base):
    def test_fm_next_says_how_long_this_kind_usually_takes(self):
        for i in range(3):
            t = self.new(f"Done {i}")
            self.fm("focus", t)
            self.fm("task", "finish", t, "--run", "true", "--audit", "self check")
        self.new("Next one")
        self.assertIn("usually", self.fm("next").stdout)


class StandingOrders(Base):
    def test_an_order_captures_when_due_and_once_per_period(self):
        self.fm("orders", "add", "--every", "1d", "Check the dependencies for updates")
        self.write("api.json", "{}\n")
        self.fm("orders", "add", "--on-change", "api.json", "Review the API change")
        first = self.fm_json("orders", "run")
        self.assertEqual(sorted(x["text"] for x in first["fired"]),
                         ["Check the dependencies for updates"], "a new watch only notes the file")
        self.assertEqual(self.fm_json("orders", "run")["fired"], [], "not again the same day")
        self.write("api.json", '{"v": 2}\n')
        self.assertEqual([x["text"] for x in self.fm_json("orders", "run")["fired"]], ["Review the API change"])
        titles = [b.title for b in c.load_briefs(self.p)]
        self.assertIn("Check the dependencies for updates", titles)
        self.assertIn("Review the API change", titles)
        self.assertIn("1d", self.fm("orders", "list").stdout)


class TierDrift(Base):
    def test_an_s_task_with_an_m_sized_diff_is_flagged_at_done(self):
        t = self.new("Small change")
        self.fm("focus", t)
        for i in range(6):
            self.write(f"f{i}.py", "x = 1\n" * 60)
        p = self.fm("task", "finish", t, "--run", "true", "--audit", "self check")
        self.assertIn("planned S", p.stderr + p.stdout)

    def test_a_touched_file_it_left_unchanged_adds_no_lines(self):
        # T-0812: a file missing from the diff was counted whole, as if new (T-0777: 226 lines read as 7,354)
        self.write("big.py", "x = 1\n" * 2000)
        subprocess.run(["git", "-C", self.repo, "add", "big.py"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "big"], check=True)
        t = self.new("Small change")
        self.fm("focus", t)
        c.log_event(self.p, "touched", task=t, data={"file": os.path.join(self.repo, "big.py")})
        self.write("small.py", "y = 2\n")
        p = self.fm("task", "finish", t, "--run", "true", "--audit", "self check")
        self.assertNotIn("planned S", p.stderr + p.stdout)


class AssumptionCheck(Base):
    def test_a_broken_assumption_is_found_by_the_sentinel(self):
        self.write("api.json", "{}\n")
        t = self.new("Use the API")
        self.fm("focus", t)
        self.fm("task", "assume", t, "add", "the API file exists", "--check", "test -f api.json")
        self.fm("task", "finish", t, "--run", "true", "--audit", "self check")
        self.assertIn("0 failing", self.fm("sentinel").stdout)
        os.remove(os.path.join(self.repo, "api.json"))
        r = self.fm("sentinel", check=False)
        self.assertEqual(r.returncode, 1, "a broken check fails the sentinel")
        self.assertIn("the API file exists", r.stdout)
        self.assertTrue([b for b in c.load_briefs(self.p) if "Assumption broke" in b.title])


class PlanRigour(Base):
    def test_an_l_feature_is_approved_only_with_a_build_vs_reuse_line(self):
        t = self.new("Big feature", "FEATURE", "L", "--interpretation", "x", "--approach", "x")
        r = self.fm("task", "set", t, "approved=true", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Build vs reuse", r.stderr)
        self.fm("task", "set", t, "--section", "Build vs reuse", "--text", "fm lane exists; reuse it for the worktrees")
        self.fm("task", "set", t, "approved=true")


class SelfDocsModules(Base):
    def test_master_names_every_module(self):
        import fmdoctor
        home = os.path.join(self.tmp, "fh")
        os.makedirs(os.path.join(home, "plugin", "lib"))
        for m in ("fmcore", "fmnew"):
            with open(os.path.join(home, "plugin", "lib", f"{m}.py"), "w") as f:
                f.write("")
        with open(os.path.join(home, "MASTER.md"), "w") as f:
            f.write("fmcore does things.\n")
        self.assertEqual(fmdoctor.missing_modules(home), ["fmnew"])


class CalibrationLedger(Base):
    """T-1061: closes that keep missing their plan slow the project to approval for M."""

    def close(self, miss):
        import fmoutcomes
        fmoutcomes.record_close(self.p, dict(outside=9 if miss else 0))

    def test_a_directory_scope_covers_its_subtree_and_the_start_scope_is_what_counts(self):
        import fmoutcomes
        t = self.new("Dir", "FEATURE", "S", "--scope", "src/")
        self.fm("task", "step", t, "add", "x")
        self.fm("focus", t)
        b = c.find_brief(self.p, t)
        self.assertEqual(b.meta["plan0_scope"], ["src/"])
        self.fm("task", "set", t, "scope=src/,lib/")  # widening later doesn't move the yardstick
        self.assertEqual(c.find_brief(self.p, t).meta["plan0_scope"], ["src/"])
        scope = type("B", (), {"meta": {"scope": b.meta["plan0_scope"]}})
        self.assertEqual(c.scope_drift(scope, ["src/a/b.py", "src/c.py", "lib/x.py"]), ["lib/x.py"])
        self.assertFalse(fmoutcomes.missed(dict(outside=2)))
        self.assertTrue(fmoutcomes.missed(dict(outside=3)))

    def test_predictions_are_bounded_and_fixed_once_work_starts(self):
        t = self.new("P")
        for bad in ("0", "10081", "x", "²"):
            self.assertNotEqual(self.fm("task", "set", t, f"predict_minutes={bad}", check=False).returncode, 0)
        self.assertNotEqual(self.fm("task", "set", t, "predict_attempts=21", check=False).returncode, 0)
        self.fm("task", "set", t, "predict_minutes=30")
        self.fm("focus", t)
        self.assertNotEqual(self.fm("task", "set", t, "predict_minutes=300", check=False).returncode, 0)

    def test_old_verdicts_are_ignored(self):
        import fmoutcomes
        for _ in range(5):
            self.close(1)
        self.assertTrue(fmoutcomes.misses(self.p))
        old = "2020-01-01T00:00:00Z"
        c.update_meta(self.p, plan_verdicts=[[old, True]] * 5)
        self.assertFalse(fmoutcomes.misses(self.p))

    def test_slow_blocks_fm_run_and_names_the_way_out(self):
        import fmserve
        m = self.new("M work", "FEATURE", "M")
        for _ in range(5):
            self.close(1)
        self.assertIsNone(fmserve._next_runnable(self.p, set(), set()))
        self.assertIn("fm task set", " ".join(c.plan_gaps(c.find_brief(self.p, m), "slow")))
        self.assertIn("slow", self.fm("autonomy").stdout)

    def test_misses_after_three_of_five_and_not_after_one(self):
        import fmoutcomes
        for miss in (1, 0, 1, 0, 1):
            self.close(miss)
        self.assertTrue(fmoutcomes.misses(self.p))
        for _ in range(3):
            self.close(0)
        self.assertFalse(fmoutcomes.misses(self.p))  # the last five hold 1 miss
        self.assertFalse(fmoutcomes.missed(dict(planned=1, changed=9)))  # a count of scope entries is no longer a signal

    def test_minutes_and_attempts_predictions_count(self):
        import fmoutcomes
        self.assertTrue(fmoutcomes.missed(dict(predict_minutes=10, minutes=25)))
        self.assertTrue(fmoutcomes.missed(dict(predict_attempts=1, attempts=2)))
        self.assertFalse(fmoutcomes.missed(dict(predict_minutes=10, minutes=15, predict_attempts=2, attempts=2)))

    def test_slow_gates_m_not_s_and_the_digest_says_so(self):
        m, s = self.new("M work", "FEATURE", "M"), self.new("S work")
        for _ in range(5):
            self.close(1)
        a = c.effective_autonomy(self.p)
        self.assertEqual(a, "slow")
        self.assertTrue(c.needs_approval(c.find_brief(self.p, m), a))
        self.assertFalse(c.needs_approval(c.find_brief(self.p, s), a))
        self.assertFalse(c.needs_approval(c.find_brief(self.p, m), "full"))
        self.assertIn("Plan calibration: 5 of the last 5", self.fm("digest").stdout)
        self.assertIn("slows to approval for M", self.fm("digest").stdout)
        for _ in range(3):
            self.close(0)
        self.assertEqual(c.effective_autonomy(self.p), "standard")
