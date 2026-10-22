"""T-1553 and its siblings: tools that test the guard against what the shell really does."""
import os
import shutil
import sys
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "lib")):
    if p not in sys.path:
        sys.path.insert(0, p)

import fmguard  # noqa: E402
import fmoracle  # noqa: E402
import fmreplay  # noqa: E402

SANDBOX = fmoracle.sandbox() is not None


@unittest.skipUnless(SANDBOX, "no bwrap: the oracle only runs commands inside a sandbox")
class Oracle(unittest.TestCase):
    """T-1553: run a line in a throwaway sandbox whose PATH holds nothing, so every program the shell would start is
    recorded with its real argv instead of run; each recorded command, judged alone, must pass where the line did."""

    def test_the_shell_runs_what_the_line_says(self):
        ran = fmoracle.ran("A=hi; echo $A | tr a-z A-Z; X=$(printf ls); $X -la")
        self.assertIn(["tr", "a-z", "A-Z"], ran)
        self.assertIn(["ls", "-la"], ran, "a computed command name is recorded as the shell expanded it")

    def test_nothing_real_runs(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            ran = fmoracle.ran("rm -rf ~; echo done > out.txt", d)
            self.assertEqual(ran[0], ["rm", "-rf", os.path.expanduser("~")], "recorded with the real ~, not run")
            self.assertFalse(os.path.exists(os.path.join(d, "out.txt")), "the line's folder is read-only")
            home_probe = os.path.join(os.path.expanduser("~"), "fm-oracle-probe-T1553")
            fmoracle.ran(f"/usr/bin/touch {d}/abs.txt {home_probe} /etc/fm-oracle-probe-T1553", d)
            for p in (os.path.join(d, "abs.txt"), home_probe, "/etc/fm-oracle-probe-T1553"):
                self.assertFalse(os.path.exists(p), f"a program run by its absolute path wrote {p}")

    def test_a_sandbox_that_fails_to_start_is_unable_not_agreement(self):
        with mock.patch.object(fmoracle, "sandbox", return_value="/bin/false"):
            self.assertIsNone(fmoracle.ran("ls"))
            bad = fmoracle.disagreements([("ls", "")])
        self.assertEqual([d["verdict"].split(":")[0] for d in bad], ["unable"])

    def test_both_branches_of_a_status_test_are_seen(self):
        self.assertIn(["rm", "-rf", "build"], fmoracle.ran("grep -q x f || rm -rf build"))
        self.assertIn(["touch", "y"], fmoracle.ran("if grep -q x f; then echo hi; else touch y; fi"))

    def test_the_line_cannot_switch_the_recorder_off(self):
        for off in ("command_not_found_handle() { :; }", "unset -f command_not_found_handle"):
            self.assertIn(["rm", "-rf", "build"], fmoracle.ran(f"{off}; rm -rf build"), off)

    def test_a_folder_above_home_or_tmp_does_not_uncover_them(self):
        import tempfile
        fd, marker = tempfile.mkstemp(dir="/tmp", prefix="fm-oracle-probe-")
        os.close(fd)
        try:
            self.assertEqual(fmoracle.ran("[ -e /proc/self ] && seen", "/"), [["seen"]], "the probe itself works")
            for where in ("/", "/tmp"):
                self.assertEqual(fmoracle.ran(f"[ -e {marker} ] && seen", where), [], where)
        finally:
            os.unlink(marker)

    def test_limits_and_tampered_records(self):
        ran = fmoracle.ran('probe "$(ulimit -v)" "$(ulimit -f)"; mkdir -p "$ORACLE_LOG/zz"; : > "$ORACLE_LOG/junk"; ls')
        self.assertEqual(ran[0][0], "probe")
        self.assertNotIn("unlimited", ran[0][1:], "memory and file size are capped")
        self.assertIn(["ls"], ran, "a stray file in the record folder is skipped, not a crash")

    def test_each_command_is_judged_in_the_folder_the_line_moved_to(self):
        home = os.path.expanduser("~")
        got = fmoracle.ran_in('cd ~/projects/x && git status; cd sub; ls; (cd /srv && make); cd ""; cd ../..; id', home)
        self.assertEqual(got, [(f"{home}/projects/x", ["git", "status"]), (f"{home}/projects/x/sub", ["ls"]),
                               ("/srv", ["make"]), (f"{home}/projects", ["id"])])
        tmp = fmoracle.ran_in('d=$(mktemp -d) && cd "$d" && git init -q', home)
        self.assertTrue(tmp[-1][0].startswith("/tmp/"), "mktemp ran (in the sandbox), so cd reached its folder")
        self.assertEqual(tmp[0][1][0], "mktemp", "and it was recorded")
        seen = []
        import types
        spy = types.SimpleNamespace(check=lambda tool, ti, ctx: seen.append((ti["command"], ctx.cwd)))
        with mock.patch.object(fmoracle, "_guard", return_value=spy):
            fmoracle.disagreements([("cd /srv && make", "")])
        self.assertIn(("make", "/srv"), seen)

    def test_a_guard_that_raises_is_unable(self):
        boom = mock.Mock()
        boom.check = mock.Mock(side_effect=RuntimeError("parser broke"))
        bad = fmoracle.disagreements([("ls", "")], guard=boom)
        self.assertEqual([d["verdict"].split(":")[0] for d in bad], ["unable"])

    def test_a_guard_that_misreads_a_line_is_caught(self):
        naive = mock.Mock()  # a guard that reads only the first word: the oracle sees what really runs
        naive.check = lambda tool, ti, ctx: None if ti["command"].startswith("true") else fmguard.check(tool, ti, ctx)
        bad = fmoracle.disagreements([("true; rm -rf ~", "")], guard=naive)
        self.assertEqual(len(bad), 1)
        self.assertEqual(bad[0]["ran"][:2], ["rm", "-rf"])

    def test_the_allow_corpus_agrees(self):
        with mock.patch.dict(os.environ):
            os.environ.pop("FOREMAN_GUARD_CASES", None)
            cases, _ = fmreplay.load_cases()
        labelled = [(k["cmd"], k.get("cwd") or "") for k in cases]  # the refused ones run nothing: skipped inside
        self.assertGreater(len(labelled), 100)
        self.assertEqual(fmoracle.disagreements(labelled), [], "nothing misread and nothing unable")

    def test_fm_replay_oracle_reports_a_misread_line(self):
        import contextlib
        import io
        import json
        import types
        args = types.SimpleNamespace(oracle=True, cases=False, candidate=None, cwd=None, cmd=None, json=True)
        planted = [{"id": "x", "cmd": "true; rm -rf ~", "cwd": "", "should": "allow"}]
        naive = lambda tool, ti, ctx: None if ti["command"].startswith("true") else fmguard.check(tool, ti, ctx)
        buf = io.StringIO()
        with mock.patch.object(fmreplay, "load_cases", return_value=(planted, 0)), \
                mock.patch.object(fmoracle, "_guard", return_value=types.SimpleNamespace(check=naive)), \
                contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as e:
            fmreplay.cmd_replay(args)
        self.assertEqual(e.exception.code, 1)
        res = json.loads(buf.getvalue())
        self.assertEqual((res["cases"], len(res["disagreements"])), (1, 1))
        self.assertEqual(res["disagreements"][0]["ran"][:2], ["rm", "-rf"])


    def test_fm_replay_oracle_takes_one_command(self):
        import contextlib
        import io
        import json
        import types
        args = types.SimpleNamespace(oracle=True, cases=False, candidate=None, cwd=None, cmd="true; rm -rf ~", json=True)
        naive = lambda tool, ti, ctx: None if ti["command"].startswith("true") else fmguard.check(tool, ti, ctx)
        buf = io.StringIO()
        with mock.patch.object(fmoracle, "_guard", return_value=types.SimpleNamespace(check=naive)), \
                contextlib.redirect_stdout(buf), self.assertRaises(SystemExit):
            fmreplay.cmd_replay(args)
        res = json.loads(buf.getvalue())
        self.assertEqual((res["cases"], res["disagreements"][0]["ran"][:2]), (1, ["rm", "-rf"]))


class NoSandbox(unittest.TestCase):
    def test_without_bwrap_nothing_runs_and_replay_says_why(self):
        import contextlib
        import io
        import types
        args = types.SimpleNamespace(oracle=True, cases=False, candidate=None, cwd=None, cmd=None, json=False)
        buf = io.StringIO()
        with mock.patch.object(shutil, "which", return_value=None), contextlib.redirect_stdout(buf):
            self.assertIsNone(fmoracle.ran("rm -rf ~"))
            fmreplay.cmd_replay(args)
        self.assertIn("bwrap", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
