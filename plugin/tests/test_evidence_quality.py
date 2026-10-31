"""Evidence quality (T-0261): a run that proves nothing never counts (T-0255), the brief's assumptions say whether they
were checked (T-0254), and where the model of the code was wrong is logged and comes back (T-0253)."""
import json

from helpers import ForemanTestCase


class _Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = json.loads(self.fm("task", "new", "Cache the session token", "--type", "FEATURE", "--tier", "M",
                                      "--ac", "it caches :: true", "--step", "do it",
                                      "--interpretation", "cache it", "--approach", "1) a 2) b 3) c Choice 1: a", "--json").stdout)["id"]


class Inconclusive(_Base):
    def test_an_inconclusive_run_never_counts(self):
        self.fm("focus", self.tid)
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true", "--inconclusive")
        brief = self.fm("task", "show", self.tid).stdout
        self.assertIn("[inconclusive]", brief)
        p = self.fm("task", "step", self.tid, "done", "1", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("inconclusive", p.stderr)
        p = self.fm("task", "done", self.tid, "--lesson", "none: test", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("no verification evidence", p.stderr)

    def test_next_asks_for_a_sharper_check(self):
        self.fm("focus", self.tid)
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true", "--inconclusive")
        self.assertIn("sharper check", self.fm("next").stdout)

    def test_a_failing_inconclusive_run_is_not_a_failed_run(self):
        self.fm("focus", self.tid)
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "false", "--inconclusive", check=False)
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true")
        self.fm("task", "step", self.tid, "done", "1")


class Assume(_Base):
    def test_add_and_verify_set_the_tags(self):
        self.fm("task", "assume", self.tid, "add", "the token lives in auth.py")
        self.fm("task", "assume", self.tid, "add", "the cache is per process")
        self.fm("task", "assume", self.tid, "verify", "1", "--run", "true")
        self.fm("task", "assume", self.tid, "verify", "2", "--run", "false", check=False)
        section = self.fm("task", "show", self.tid).stdout.split("## Assumptions", 1)[1].split("\n## ", 1)[0]
        self.assertRegex(section, r"- \[verified: `true` → exit 0[^\]]*\] the token lives in auth.py")
        self.assertIn("[false: `false` → ✗ exit 1", section)
        self.assertIn("the cache is per process", section)

    def test_a_typed_verification_is_kept(self):
        self.fm("task", "set", self.tid, "--section", "Assumptions (confidence)", "--text", "- tests exist (high)")
        self.fm("task", "assume", self.tid, "verify", "1", "--evidence", "read plugin/tests/run.py:6")
        self.assertIn("- [verified: read plugin/tests/run.py:6] tests exist (high)", self.fm("task", "show", self.tid).stdout)

    def test_done_warns_on_unverified_assumptions(self):
        self.fm("task", "assume", self.tid, "add", "the token lives in auth.py")
        self.fm("focus", self.tid)
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true")
        out = self.fm("task", "finish", self.tid, "--audit", "self", "--lens", "intent: ok", "--lens", "edge: ok",
                      "--docs", "none: test", "--lesson", "none: test", check=False)
        self.assertIn("unverified assumption", out.stdout + out.stderr)
        self.assertIn("the token lives in auth.py", out.stdout + out.stderr)

    def test_an_unknown_assumption_is_a_usage_error(self):
        p = self.fm("task", "assume", self.tid, "verify", "3", "--run", "true", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("no assumption 3", p.stderr)


class Surprise(_Base):
    def test_a_surprise_reaches_friction_and_recall(self):
        self.fm("focus", self.tid)
        self.fm("surprise", "the session token is cached per process → it is cached per request in middleware")
        self.assertIn("cached per request in middleware", self.fm("friction").stdout)
        out = self.fm("recall", "where is the session token cached").stdout
        self.assertIn("surprise", out)
        self.assertIn("cached per request in middleware", out)
        self.assertIn(self.tid, out)

    def test_an_unknown_task_is_refused(self):
        p = self.fm("surprise", "a → b", "--task", "T-9999", check=False)
        self.assertNotEqual(p.returncode, 0)

    def test_a_surprise_needs_text(self):
        p = self.fm("surprise", " ", check=False)
        self.assertNotEqual(p.returncode, 0)


class Bench(_Base):
    """T-2284: fm task evidence --bench times a command on the task's start tree and on this one."""

    def _commit(self, text):
        import os
        import subprocess
        with open(os.path.join(self.repo, "work.py"), "w") as f:
            f.write(text)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "w"], check=True)

    def _perf(self):
        return json.loads(self.fm("task", "new", "faster", "--type", "PERFORMANCE", "--tier", "S", "--ac", "fast :: true",
                                  "--step", "speed it up", "--json").stdout)["id"]

    def test_medians_before_and_after_are_recorded_and_finish_accepts_them(self):
        self._commit("import time\ntime.sleep(0.3)\n")
        tid = self._perf()
        self.fm("focus", tid)
        self._commit("pass\n")
        r = self.fm("task", "evidence", tid, "--step", "1", "--bench", "python3 work.py", "--repeat", "3")
        self.assertIn("(3 runs each)", r.stdout)
        shown = self.fm("task", "show", tid).stdout
        self.assertRegex(shown, r"python3 work.py: 0\.[3-9]\d*s → 0\.\d+s \(3 runs each\)")
        self.assertIn("(3 runs each)", shown.split("Measurements", 1)[1])
        self.fm("task", "finish", tid, "--audit", "read it")  # no --numbers: the bench is the numbers

    def test_a_failing_side_is_recorded_as_a_failure(self):
        self._commit("pass\n")
        tid = self._perf()
        self.fm("focus", tid)
        self._commit("raise SystemExit(3)\n")
        r = self.fm("task", "evidence", tid, "--bench", "python3 work.py", "--repeat", "2", check=False)
        self.assertEqual(r.returncode, 3)
        self.assertIn("failed on the current tree", r.stdout)

    def test_no_base_commit_is_refused(self):
        tid = self._perf()  # never focused: no start commit
        r = self.fm("task", "evidence", tid, "--bench", "true", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("start commit", r.stderr)

    def test_bench_does_not_mix_with_run_or_a_huge_repeat(self):
        tid = self._perf()
        for extra in (("--run", "true"), ("--repeat", "999")):
            r = self.fm("task", "evidence", tid, "--bench", "true", *extra, check=False)
            self.assertNotEqual(r.returncode, 0)
