"""T-0677: planning, briefs and queue — first versions: a deferral's revisit date, the usual minutes in fm next,
standing orders, tier drift at done, assumption re-checks, a build-vs-reuse line before an L feature is approved, and
MASTER.md naming every module."""
import os

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
