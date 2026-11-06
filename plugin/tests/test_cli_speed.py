"""T-3252: the tests' fm calls go through a fork server: one process imports Sampo once and each call is a fork of it,
which must behave exactly like a fresh `python3 fm ...` (argv, cwd, env, stdin, exit code, output) and cost far less."""
import ast
import os
import statistics
import subprocess
import sys
import time
import unittest

from helpers import FM, ForemanTestCase

import forkcli

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "lib")


def base(**kw):
    """A small env a forked call can serve: PATH plus the locale and interpreter settings the server started with
    (without them forkcli runs the call fresh, and the comparison would prove nothing)."""
    return {**{k: v for k, v in os.environ.items() if k.startswith(forkcli.START_ENV)}, "PATH": os.environ["PATH"], **kw}


ECHO = r'''
import os, sys
data = sys.stdin.read()
print("argv", sys.argv[1:])
print("cwd", os.getcwd())
print("env", os.environ.get("PROBE"), "HOME" in os.environ)
print("stdin", repr(data))
sys.stderr.write("to stderr\n")
if sys.argv[1:2] == ["sleep"]:
    import time; time.sleep(30)
if sys.argv[1:2] == ["crash"]:
    raise RuntimeError("boom")
if sys.argv[1:2] == ["neg"]:
    sys.exit(-1)
if sys.argv[1:2] == ["tmp"]:
    import tempfile; print("tmp", tempfile.gettempdir())
if sys.argv[1:2] == ["path"]:
    print("tests on path", any(p.rstrip("/").endswith("plugin/tests") for p in sys.path))
sys.exit(int(sys.argv[1]) if sys.argv[1:2] and sys.argv[1].isdigit() else 0)
'''


class ForkServer(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.script = os.path.join(self.tmp, "echo.py")
        with open(self.script, "w") as f:
            f.write(ECHO)
        self.addCleanup(forkcli.stop)

    def both(self, args, env, cwd, input=None):
        env = base(**env)
        fresh = subprocess.run([sys.executable, self.script, *args], cwd=cwd, env=env, input=input,
                               capture_output=True, text=True, timeout=30)
        forked = forkcli.run(self.script, args, cwd=cwd, env=env, input=input, timeout=30)
        self.assertIn(os.getpid(), forkcli._SERVER, "the call went through the server")
        return fresh, forked

    def test_a_changed_locale_runs_fresh(self):
        forkcli.run(self.script, ["0"], cwd=self.tmp, env=base(LC_ALL="C", TZ="Pacific/Apia"), timeout=30)
        self.assertNotIn(os.getpid(), forkcli._SERVER, "a call with another locale or zone never reaches the server")

    def test_a_forked_call_sees_what_a_fresh_one_does(self):
        cwd = os.path.join(self.tmp, "here")
        os.makedirs(cwd)
        for args, env, input in ((["7", "x"], {"PROBE": "one", "PATH": os.environ["PATH"]}, "in put\n"),
                                 (["0"], {"PROBE": "two", "HOME": self.tmp, "PATH": os.environ["PATH"]}, None),
                                 (["crash"], {"PATH": os.environ["PATH"]}, None)):
            fresh, forked = self.both(args, env, cwd, input)
            self.assertEqual(forked.returncode, fresh.returncode, forked.stderr)
            self.assertEqual(forked.stdout, fresh.stdout)
            self.assertEqual(forked.stderr.splitlines()[:1], fresh.stderr.splitlines()[:1])
            if args == ["crash"]:
                self.assertIn("RuntimeError: boom", forked.stderr)

    def test_exit_codes_temp_dir_and_path_match_a_fresh_process(self):
        # review (T-3297): sys.exit(-1) is 255 fresh; a call's own TMPDIR wins; the tests folder isn't on fm's path
        other = os.path.join(self.tmp, "othertmp")
        os.makedirs(other)
        for args, env in ((["neg"], {"PATH": os.environ["PATH"]}),
                          (["tmp"], {"PATH": os.environ["PATH"], "TMPDIR": other}),
                          (["path"], {"PATH": os.environ["PATH"]})):
            fresh, forked = self.both(args, env, self.tmp)
            self.assertEqual((forked.returncode, forked.stdout), (fresh.returncode, fresh.stdout), args)

    def test_the_server_leaves_no_folder_behind(self):
        forkcli.run(self.script, ["0"], cwd=self.tmp, env=base(), timeout=30)
        path = forkcli._SERVER[os.getpid()][0]
        forkcli.stop()
        self.assertFalse(os.path.exists(os.path.dirname(path)))

    def test_a_slow_call_times_out_and_is_killed(self):
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            forkcli.run(self.script, ["sleep"], cwd=self.tmp, env=base(), timeout=1)
        self.assertLess(time.monotonic() - start, 10)

    def test_fm_calls_match_and_cost_a_fraction(self):
        env = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1")
        subprocess.run([sys.executable, FM, "init"], cwd=self.repo, env=env, capture_output=True, check=True)
        new = ["task", "new", "Speed", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s"]
        a = forkcli.run(FM, new, cwd=self.repo, env=env, timeout=60)
        self.assertEqual(a.returncode, 0, a.stderr)
        fresh = subprocess.run([sys.executable, FM, "task", "show", "T-0001"], cwd=self.repo, env=env,
                               capture_output=True, text=True)
        forked = forkcli.run(FM, ["task", "show", "T-0001"], cwd=self.repo, env=env, timeout=60)
        self.assertEqual((forked.returncode, forked.stdout), (fresh.returncode, fresh.stdout))
        bad = forkcli.run(FM, ["no-such-verb"], cwd=self.repo, env=env, timeout=60)
        self.assertEqual(bad.returncode, 2)

        def median(call):
            times = []
            for _ in range(9):
                t = time.perf_counter()
                call()
                times.append(time.perf_counter() - t)
            return statistics.median(times)

        slow = median(lambda: subprocess.run([sys.executable, FM, "task", "show", "T-0001"], cwd=self.repo, env=env,
                                             capture_output=True))
        fast = median(lambda: forkcli.run(FM, ["task", "show", "T-0001"], cwd=self.repo, env=env, timeout=60))
        # measured 2.4x both quiet (23 vs 55 ms) and at load 60 (85 vs 205 ms): the bar is a 40% cut
        self.assertLess(fast, slow * 0.6, f"forked {fast * 1000:.0f} ms, fresh {slow * 1000:.0f} ms")


class ImportAudit(unittest.TestCase):
    """What the server imports ahead must read nothing from the environment at import, or every fork inherits the
    server's value: a module-level statement may not call os.environ, getenv, expanduser or Path.home."""

    def test_the_preloaded_modules_read_no_environment_at_import(self):
        bad = []
        for mod in (m for m in forkcli.PRELOAD if m.startswith("sampo.")):  # the stdlib ones read nothing at import
            path = os.path.join(LIB, *mod.split(".")) + ".py"
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                src = ast.unparse(node)
                if src in {f"{n}(os.environ)" for n in forkcli.REAPPLY}:  # done again in each forked call
                    continue
                if any(k in src for k in ("os.environ", "getenv(", "expanduser(", "Path.home(", "getcwd(")):
                    bad.append(f"{mod}:{node.lineno}: {src[:100]}")
        self.assertEqual(bad, [])

    def test_a_forked_call_maps_sampo_names_as_a_fresh_one_does(self):
        env = base(SAMPO_PROBE_X="1", FOREMAN_HOME="/nowhere")
        code = ("import os, sys; sys.path.insert(0, %r); import sampo.core; "
                "print(os.environ.get('FOREMAN_PROBE_X'), 'SAMPO_PROBE_X' in os.environ)") % LIB
        fresh = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
        probe = os.path.join(forkcli.tempfile.mkdtemp(), "probe.py")
        with open(probe, "w") as f:
            f.write("import os; print(os.environ.get('FOREMAN_PROBE_X'), 'SAMPO_PROBE_X' in os.environ)\n")
        forked = forkcli.run(probe, [], env=env, timeout=30)
        forkcli.stop()
        self.assertEqual(forked.stdout, fresh.stdout)
        self.assertEqual(fresh.stdout.strip(), "1 False")


if __name__ == "__main__":
    unittest.main()
