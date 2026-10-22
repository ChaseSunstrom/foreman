"""Shared test helpers: isolated FOREMAN_HOME, scratch git repos, running the CLI."""
import atexit
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(PLUGIN, "lib")
FM = os.path.join(PLUGIN, "bin", "fm")
HOOK = os.path.join(PLUGIN, "hooks", "hook")
RELAY = "import subprocess, sys; sys.exit(subprocess.run(sys.argv[1:4]).returncode)"
if LIB not in sys.path:
    sys.path.insert(0, LIB)

# T-0283: tests never reach the real claude. A stub dir a test puts first on PATH still wins; a stub that can't run (no
# shebang: ENOEXEC) makes the PATH lookup move on — to this lockout, not to the paid binary further along.
_LOCKOUT = tempfile.mkdtemp(prefix="fm-test-lockout-")
with open(os.path.join(_LOCKOUT, "claude"), "w") as _f:
    _f.write("#!/bin/sh\necho 'fm tests: the real claude is locked out (a stub on PATH is missing or could not run)' >&2"
             "\nexit 97\n")
os.chmod(os.path.join(_LOCKOUT, "claude"), 0o755)
os.environ["PATH"] = _LOCKOUT + os.pathsep + os.environ.get("PATH", "")
os.environ["FOREMAN_NATIVE_BIN"] = os.path.join(_LOCKOUT, "none")  # T-0992: nor fmcore's ~/.local/bin fallback
atexit.register(shutil.rmtree, _LOCKOUT, True)
# T-0744: every test sees a calm host unless it says otherwise; the machine's real load (a full run beside other work)
# turned lanes and ambient runs off and failed tests only then
os.environ.setdefault("FOREMAN_HOST", "load=0.1,cpus=8,mem_mb=8192")


def read_text(path, encoding="utf-8", limit=-1):
    with open(path, encoding=encoding) as f:
        return f.read(limit)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def headless_chrome():
    """A headless Chromium (T-1499, T-1610): FOREMAN_CHROME, one on PATH, or Playwright's download; None if absent."""
    import glob
    found = [os.environ.get("FOREMAN_CHROME")] + [shutil.which(n) for n in (
        "chrome-headless-shell", "chromium", "chromium-browser", "google-chrome")] + sorted(glob.glob(os.path.expanduser(
            "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell")))
    return next((p for p in found if p and os.access(p, os.X_OK)), None)


def stub_corpus_replay(repo, drifted=0, days=0, cases=3):
    """T-1401: the ledger record fm replay --cases leaves, without running the replay: red when drifted, days old."""
    import time
    from unittest import mock
    import fmcore as c
    p = c.find_project(repo, create=True)
    with mock.patch.object(c, "now", return_value=c.iso(time.time() - days * 86400)):
        c.log_event(p, "guard_corpus", data={"cases": cases, "drifted": drifted, "broken": 0})
    return p


def git_repo(parent, name="app"):
    root = os.path.join(parent, name)
    os.makedirs(root)
    subprocess.run(["git", "init", "-q", "-b", "main", root], check=True)
    subprocess.run(["git", "-C", root, "config", "user.email", "t@example.com"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.name", "t"], check=True)
    with open(os.path.join(root, "README.md"), "w") as f:
        f.write("# app\n")
    subprocess.run(["git", "-C", root, "add", "."], check=True)
    subprocess.run(["git", "-C", root, "commit", "-qm", "init"], check=True)
    return root


class ForemanTestCase(unittest.TestCase):
    """Each test gets its own FOREMAN_HOME and a scratch git repo."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = os.path.realpath(self._tmp.name)
        self.home = os.path.join(self.tmp, "fhome")
        os.makedirs(self.home)
        self._env = {k: os.environ.get(k) for k in ("FOREMAN_HOME", "FOREMAN_SESSION_ID", "FOREMAN_PROJECT",
                                                     "FOREMAN_STATE", "XDG_STATE_HOME", "FOREMAN_NO_BACKGROUND",
                                                     "FOREMAN_ONEOFF", "CLAUDE_CODE_ENTRYPOINT", "FOREMAN_DRIVE_TASK",
                                                     "FOREMAN_GUARD_CASES")}
        os.environ["FOREMAN_HOME"] = self.home
        os.environ["FOREMAN_NO_BACKGROUND"] = "1"  # a detached child writing into a test's folder races its cleanup
        # T-1004: a suite run from a one-off or headless session (the UI harness) sees what a working session sees
        for k in ("FOREMAN_SESSION_ID", "FOREMAN_PROJECT", "FOREMAN_STATE", "FOREMAN_ONEOFF", "CLAUDE_CODE_ENTRYPOINT",
                  "FOREMAN_DRIVE_TASK"):
            os.environ.pop(k, None)
        os.environ["XDG_STATE_HOME"] = os.path.join(self.tmp, "xdg")  # a state fallback never reaches the real one
        # T-1197: a temp repo has no plugin/, so fm guard wrong fell back to the real checkout's corpus
        os.environ["FOREMAN_GUARD_CASES"] = os.path.join(self.tmp, "guard_cases.jsonl")
        self.repo = git_repo(self.tmp)

    def tearDown(self):
        for k, v in self._env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self._tmp.cleanup()

    def fm(self, *args, cwd=None, check=True, env=None, input=None):
        # fm run never takes a real inhibitor lock; T-1379: fm doctor skips its hook bench (no test reads its timings)
        e = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1", FOREMAN_DOCTOR_BENCH="0")
        e.pop("CLAUDE_CODE_SESSION_ID", None)  # tests may run inside a live Claude Code session
        e.update(env or {})
        p = subprocess.run([sys.executable, FM, *args], cwd=cwd or self.repo, env=e,
                           capture_output=True, text=True, input=input, timeout=30)
        if check and p.returncode != 0:
            raise AssertionError(f"fm {' '.join(args)} exited {p.returncode}\nstdout:{p.stdout}\nstderr:{p.stderr}")
        return p

    def fm_ask(self, tid, *cats, session="sess-1", why="needs it", env=None, check=True, pin=None, flags=None):
        """fm ask the way a session runs it: PreToolUse sees the Bash command (trusted session id), then fm runs."""
        extra = ["--pin", pin] if pin else []
        cmd = f"fm ask {tid} {' '.join(cats + tuple(extra))} --why '{why}'"
        self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}, "session_id": session}, flags=flags)
        return self.fm("ask", tid, *cats, *extra, "--why", why, env=env, check=check)

    def fm_json(self, *args, **kw):
        return json.loads(self.fm(*args, "--json", **kw).stdout)

    def hook(self, event, payload, env=None, timeout=10, flags=None):
        e = dict(os.environ, FOREMAN_HOME=self.home)
        e.update(env or {})
        payload = dict({"session_id": "sess-1", "cwd": self.repo, "hook_event_name": event}, **payload)
        cmd = [sys.executable, HOOK, event]
        if flags is not None:  # T-1226: the hook asks which Claude Code runs it and how it was started; by default
            cmd = [self.claude_stand_in(), "-c", RELAY, *cmd, *flags]  # this test's process, else a new stand-in
        return subprocess.run(cmd, input=json.dumps(payload), env=e,
                              capture_output=True, text=True, timeout=timeout, cwd=payload["cwd"])

    def slow_start(self, delay=0.4):
        """T-1280: env for CI's slow interpreter start: every new Python process waits `delay` s (a sitecustomize)."""
        slow = os.path.join(self.tmp, "slow")
        os.makedirs(slow, exist_ok=True)
        with open(os.path.join(slow, "sitecustomize.py"), "w") as f:
            f.write(f"import time\ntime.sleep({delay})\n")
        return {"PYTHONPATH": slow}

    def claude_stand_in(self):
        """A process named claude (python under that name) that runs the command after its -c code."""
        path = os.path.join(self.tmp, "stand-in", "claude")
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            os.symlink(sys.executable, path)
        return path


# T-1361: misbehaving fake runner CLIs. One small sh script per failure mode; each ends by itself in seconds even if
# nothing stops it, so a test that goes wrong fails instead of hanging.
FAKE_MODES = {
    "ok": "echo done\n",
    "hang": "exec sleep {secs}\n",  # no output at all
    "silent": "echo starting\nexec sleep {secs}\n",  # talks, then goes quiet mid-stream
    "tty-prompt": "printf 'Overwrite settings? (y/n) '\nexec sleep {secs}\n",  # asks and waits; no TTY is there to answer
    "garbage-json": "echo '{{\"type\": \"result\", \"result\": '\necho 'not json at all {{{{'\nexit 0\n",
    "usage-limit": "echo 'Claude usage limit reached. Your limit will reset at 5pm.'\nexec sleep {secs}\n",
    "fork-exit": "sleep {secs} &\nexit 0\n",  # a child outlives the parent, still holding the pipe
}


def fake_cli(dir_, name, mode, secs=20):
    """Write an executable fake `name` in dir_ that misbehaves as `mode` (FAKE_MODES); returns its path."""
    os.makedirs(dir_, exist_ok=True)
    path = os.path.join(dir_, name)
    with open(path, "w") as f:
        f.write("#!/bin/sh\n" + FAKE_MODES[mode].format(secs=secs))
    os.chmod(path, 0o755)
    return path
