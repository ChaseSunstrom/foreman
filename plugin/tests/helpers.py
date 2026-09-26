"""Shared test helpers: isolated FOREMAN_HOME, scratch git repos, running the CLI."""
import json
import os
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
        self._env = {k: os.environ.get(k) for k in ("FOREMAN_HOME", "FOREMAN_SESSION_ID", "FOREMAN_PROJECT")}
        os.environ["FOREMAN_HOME"] = self.home
        os.environ.pop("FOREMAN_SESSION_ID", None)
        os.environ.pop("FOREMAN_PROJECT", None)
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
        e.update(env or {})
        p = subprocess.run([sys.executable, FM, *args], cwd=cwd or self.repo, env=e,
                           capture_output=True, text=True, input=input, timeout=30)
        if check and p.returncode != 0:
            raise AssertionError(f"fm {' '.join(args)} exited {p.returncode}\nstdout:{p.stdout}\nstderr:{p.stderr}")
        return p

    def fm_json(self, *args, **kw):
        return json.loads(self.fm(*args, "--json", **kw).stdout)

    def hook(self, event, payload, env=None, timeout=10):
        e = dict(os.environ, FOREMAN_HOME=self.home)
        e.update(env or {})
        payload = dict({"session_id": "sess-1", "cwd": self.repo, "hook_event_name": event}, **payload)
        return subprocess.run([sys.executable, HOOK, event], input=json.dumps(payload), env=e,
                              capture_output=True, text=True, timeout=timeout, cwd=payload["cwd"])
