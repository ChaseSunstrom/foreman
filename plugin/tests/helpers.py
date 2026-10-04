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
atexit.register(shutil.rmtree, _LOCKOUT, True)


def read_text(path, encoding="utf-8", limit=-1):
    with open(path, encoding=encoding) as f:
        return f.read(limit)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


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
                                                     "FOREMAN_STATE", "XDG_STATE_HOME", "FOREMAN_NO_BACKGROUND")}
        os.environ["FOREMAN_HOME"] = self.home
        os.environ["FOREMAN_NO_BACKGROUND"] = "1"  # a detached child writing into a test's folder races its cleanup
        for k in ("FOREMAN_SESSION_ID", "FOREMAN_PROJECT", "FOREMAN_STATE"):
            os.environ.pop(k, None)
        os.environ["XDG_STATE_HOME"] = os.path.join(self.tmp, "xdg")  # a state fallback never reaches the real one
        self.repo = git_repo(self.tmp)

    def tearDown(self):
        for k, v in self._env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self._tmp.cleanup()

    def fm(self, *args, cwd=None, check=True, env=None, input=None):
        e = dict(os.environ, FOREMAN_HOME=self.home)
        e.pop("CLAUDE_CODE_SESSION_ID", None)  # tests may run inside a live Claude Code session
        e.update(env or {})
        p = subprocess.run([sys.executable, FM, *args], cwd=cwd or self.repo, env=e,
                           capture_output=True, text=True, input=input, timeout=30)
        if check and p.returncode != 0:
            raise AssertionError(f"fm {' '.join(args)} exited {p.returncode}\nstdout:{p.stdout}\nstderr:{p.stderr}")
        return p

    def fm_ask(self, tid, *cats, session="sess-1", why="needs it", env=None, check=True, pin=None):
        """fm ask the way a session runs it: PreToolUse sees the Bash command (trusted session id), then fm runs."""
        extra = ["--pin", pin] if pin else []
        cmd = f"fm ask {tid} {' '.join(cats + tuple(extra))} --why '{why}'"
        self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}, "session_id": session})
        return self.fm("ask", tid, *cats, *extra, "--why", why, env=env, check=check)

    def fm_json(self, *args, **kw):
        return json.loads(self.fm(*args, "--json", **kw).stdout)

    def hook(self, event, payload, env=None, timeout=10):
        e = dict(os.environ, FOREMAN_HOME=self.home)
        e.update(env or {})
        payload = dict({"session_id": "sess-1", "cwd": self.repo, "hook_event_name": event}, **payload)
        return subprocess.run([sys.executable, HOOK, event], input=json.dumps(payload), env=e,
                              capture_output=True, text=True, timeout=timeout, cwd=payload["cwd"])
