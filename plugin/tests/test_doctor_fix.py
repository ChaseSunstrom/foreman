"""fm doctor --fix (T-1184): applies only the findings that already have a safe repair (stale status views, empty
git objects, fallback state) and lists every finding it left for a person."""
import json
import os

from helpers import ForemanTestCase


class Fix(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        import fmcore as c
        import fmdoctor
        self.c, self.d, self.p = c, fmdoctor, c.find_project(self.repo)

    def findings(self):
        return [self.d.Result("views", "WARN", "stale"), self.d.check_integrity([self.repo], [self.p]),
                self.d.Result("hook latency", "WARN", "slow")]

    def test_fixes_the_view_and_lists_the_truncated_brief_as_left(self):
        tid = json.loads(self.fm("capture", "a thing", "--json").stdout)["id"]
        open(self.c.find_brief(self.p, tid).path, "w").close()  # a truncated brief: no safe repair
        with open(os.path.join(self.p.dir, "state.line"), "w") as f:
            f.write("torn")
        self.assertFalse(self.d.views_match(self.p))
        fixed, left = self.d.fix(self.findings())
        self.assertTrue(self.d.views_match(self.p))
        self.assertEqual([f.split(":")[0] for f in fixed], ["views"])
        self.assertEqual([f.split(":")[0] for f in left], ["integrity", "hook latency"])

    def test_nothing_unsafe_is_touched_when_all_pass(self):
        fixed, left = self.d.fix([self.d.Result("views", "PASS", "ok"), self.d.Result("briefs", "PASS", "ok")])
        self.assertEqual((fixed, left), ([], []))

    def test_cli_flag_exists(self):
        self.assertIn("--fix", self.fm("doctor", "--help").stdout)
