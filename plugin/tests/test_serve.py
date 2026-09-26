"""fm serve / fm run with stub systemctl, journalctl and claude on PATH: no real services, sessions or network."""
import json
import os
import sys

from helpers import FM, ForemanTestCase, read_text

import fmcore as c
import fmserve


class ServeCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")  # HOME: systemd unit dir and ~/.claude.json live here
        self.bin = os.path.join(self.tmp, "bin")
        self.calls = os.path.join(self.tmp, "calls.log")
        os.makedirs(self.uhome)
        os.makedirs(self.bin)
        self.stub("systemctl", 'if [ "$2" = is-active ]; then echo active; fi\n')
        self.stub("journalctl", 'echo "Error: Workspace not trusted."\necho "session https://claude.ai/code/x?t=1"\n')
        self.stub("claude", "")
        self.stub("loginctl", 'if [ "$1" = show-user ]; then echo yes; fi\n')
        self.trust(self.repo)
        self.fm("init")
        self.slug = c.find_project(self.repo).slug
        self.unit = os.path.join(self.uhome, ".config", "systemd", "user", f"foreman-serve-{self.slug}.service")

    def stub(self, name, body):
        path = os.path.join(self.bin, name)
        with open(path, "w") as f:
            f.write(f'#!/usr/bin/env bash\necho "{name} $*" >> {self.calls}\n' + body)
        os.chmod(path, 0o755)

    def trust(self, path):
        with open(os.path.join(self.uhome, ".claude.json"), "w") as f:
            json.dump({"projects": {path: {"hasTrustDialogAccepted": True}}}, f)

    def env(self, **extra):
        return dict({"HOME": self.uhome, "XDG_CONFIG_HOME": os.path.join(self.uhome, ".config"),
                     "PATH": self.bin + os.pathsep + os.environ["PATH"]}, **extra)

    def serve(self, *args, check=True):
        return self.fm("serve", *args, check=check, env=self.env())

    def called(self):
        return read_text(self.calls) if os.path.exists(self.calls) else ""

    def meta(self):
        return c.read_meta(c.find_project(self.repo))


class Serve(ServeCase):
    def test_start_writes_and_enables_a_unit_and_sets_full_auto_drive(self):
        self.fm("autonomy", "standard")
        self.fm("drive", "off")
        self.serve()
        unit = read_text(self.unit)
        for needle in ("Managed by Foreman", f"WorkingDirectory={self.repo}", "Type=simple", "Restart=always",
                       "StartLimitBurst=", "env claude remote-control", "--spawn same-dir", "StandardOutput=null"):
            self.assertIn(needle, unit)
        self.assertNotIn("--permission-mode", unit, "the user's own default mode applies unless one is given")
        self.assertIn(f"systemctl --user enable --now foreman-serve-{self.slug}.service", self.called())
        self.assertNotIn("claude ", self.called(), "serve never runs claude itself (remote-control --help blocks)")
        m = self.meta()
        self.assertEqual((m["autonomy"], m["drive"]), ("full", True))
        self.assertEqual((m["serve"]["prev_autonomy"], m["serve"]["prev_drive"]), ("standard", False))

    def test_linger_is_enabled_so_the_unit_outlives_the_login(self):
        # without linger, systemd --user (and the unit) stops when the SSH session that ran fm serve ends
        self.serve()
        self.assertNotIn("enable-linger", self.called())
        self.stub("loginctl", 'if [ "$1" = show-user ]; then echo no; fi\n')
        out = self.serve().stdout
        self.assertIn("loginctl enable-linger", self.called())
        self.assertIn("linger is off", out)

    def test_stop_reverses_everything(self):
        self.fm("autonomy", "standard")
        self.serve()
        self.serve("stop")
        self.assertFalse(os.path.exists(self.unit))
        self.assertIn(f"systemctl --user disable --now foreman-serve-{self.slug}.service", self.called())
        m = self.meta()
        self.assertEqual((m["autonomy"], m["drive"]), ("standard", True))
        self.assertNotIn("serve", m)

    def test_untrusted_workspace_is_refused_with_the_reason(self):
        self.trust(os.path.join(self.tmp, "elsewhere"))
        p = self.serve(check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("trust", p.stderr)
        self.assertFalse(os.path.exists(self.unit))
        self.trust(self.tmp)  # Claude Code checks the repo root itself: a trusted parent folder doesn't count
        self.assertNotEqual(self.serve(check=False).returncode, 0)
        self.trust(self.repo)
        self.serve(os.path.join(self.repo, "."))

    def test_permission_mode_given_or_sensitive(self):
        self.serve("--permission-mode", "acceptEdits")
        self.assertIn("--permission-mode acceptEdits", read_text(self.unit))
        self.serve("stop")
        self.fm("sensitive", "on")
        self.serve()
        self.assertIn("--permission-mode default", read_text(self.unit), "sensitive repos approve from the phone")
        self.assertNotEqual(self.serve("--permission-mode", "yolo", check=False).returncode, 0)

    def test_status_names_the_unit_state_and_the_last_error_when_down(self):
        self.serve()
        out = self.serve("status").stdout
        for needle in (self.slug, "active", self.repo, "idle"):
            self.assertIn(needle, out)
        self.assertNotIn("Workspace not trusted", out)
        self.stub("systemctl", 'if [ "$2" = is-active ]; then echo failed; fi\n')
        out = self.serve("status").stdout
        self.assertIn("Workspace not trusted", out)
        self.assertNotIn("https://", out, "the session URL is never shown")
        self.assertIn("still full autonomy with drive on", out, "a dead unit leaves the project in serve mode")

    def test_control_characters_never_reach_the_unit_file(self):
        # a newline in the repo path or PATH would end its line and start a new unit directive
        bad = type("P", (), {"root": "/srv/app\nExecStartPre=/bin/evil", "slug": "app-1"})()
        with self.assertRaises(c.PolicyError):
            fmserve.unit_text(bad, None)
        p = c.find_project(self.repo)
        old = os.environ["PATH"]
        os.environ["PATH"] = old + ":/x\nExecStartPre=/bin/evil"
        try:
            text = fmserve.unit_text(p, None)
        finally:
            os.environ["PATH"] = old
        self.assertNotIn("\nExecStartPre", text)

    def test_units_of_another_foreman_install_are_left_alone(self):
        self.serve()
        other = self.unit.replace(self.slug, "elsewhere-123456")
        with open(self.unit) as f:
            text = f.read().replace(self.home, "/other/foreman")
        with open(other, "w") as f:
            f.write(text)
        self.fm("uninstall-user", env=self.env())
        self.assertFalse(os.path.exists(self.unit))
        self.assertTrue(os.path.exists(other))

    def test_refuses_while_fm_run_works_here(self):
        import fcntl
        with open(os.path.join(c.find_project(self.repo).dir, "run.lock"), "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            p = self.serve(check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("fm run", p.stderr)

    def test_uninstall_user_stops_serve_units(self):
        self.serve()
        self.fm("uninstall-user", env=self.env())
        self.assertFalse(os.path.exists(self.unit))
        self.assertIn("disable --now", self.called())


class Run(ServeCase):
    def setUp(self):
        super().setUp()
        # a stub session that finishes whatever task it is scoped to, the way a real one would through fm
        fm = f"{sys.executable} {FM}"
        self.finisher = (f't=$FOREMAN_DRIVE_TASK\necho "session for $t"\n{fm} focus $t >/dev/null\n'
                         f'{fm} task step $t done 1 --evidence x ok >/dev/null\n'
                         f'{fm} task ac $t check 1 --evidence x ok >/dev/null\n'
                         f'{fm} task audit $t self x ok >/dev/null\n{fm} task done $t\n')

    def task(self, title):
        return json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--ac", "works",
                                  "--step", "fix it", "--json").stdout)["id"]

    def run_fm(self, *args, check=True):
        return self.fm("run", *args, check=check, env=self.env())

    def test_each_task_runs_in_its_own_fresh_session(self):
        a, b = self.task("one"), self.task("two")
        self.stub("claude", self.finisher)
        out = self.run_fm().stdout
        p = c.find_project(self.repo)
        self.assertEqual([c.find_brief(p, t).status for t in (a, b)], ["done", "done"])
        sessions = [l for l in self.called().splitlines() if l.startswith("claude ")]
        self.assertEqual(len(sessions), 2)
        self.assertTrue(all(" -p " in s for s in sessions))
        self.assertIn(f"{a} done", out)
        self.assertIn(f"session for {a}", read_text(os.path.join(c.state_dir(), "logs", f"run-{self.slug}.log")))

    def test_a_timed_out_session_is_logged_with_its_errors(self):
        self.task("one")
        self.stub("claude", 'echo "stuck on the login" >&2\nsleep 5\n')
        p = self.run_fm("--timeout", "0.02", check=False)  # minutes
        self.assertEqual(p.returncode, 1)
        self.assertIn("limit", p.stderr)
        self.assertIn("stuck on the login", read_text(os.path.join(c.state_dir(), "logs", f"run-{self.slug}.log")))

    def test_a_session_without_progress_stops_the_run(self):
        self.task("one")
        p = self.run_fm(check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("no progress", p.stderr)
        self.assertEqual(len([l for l in self.called().splitlines() if l.startswith("claude ")]), 1)

    def limited_then(self, body):
        """A stub session that hits the usage limit on its first call, then runs body."""
        n = os.path.join(self.tmp, "sessions")
        return (f'echo x >> {n}\nif [ "$(wc -l < {n})" -eq 1 ]; then\n'
                f'echo "You\'ve hit your session limit · resets 3pm (Europe/Berlin)" >&2; exit 1\nfi\n' + body)

    def test_a_usage_limit_is_waited_out_and_the_task_retried(self):
        a = self.task("one")
        self.stub("claude", self.limited_then(self.finisher))
        out = self.run_fm("--wait", "0.0003").stdout  # hours: ~1 s budget
        self.assertEqual(c.find_brief(c.find_project(self.repo), a).status, "done")
        self.assertIn("usage limit", out)
        self.assertIn("usage limit", read_text(os.path.join(c.state_dir(), "logs", f"run-{self.slug}.log")))

    def test_a_usage_limit_past_the_wait_budget_stops_the_run(self):
        self.task("one")
        self.stub("claude", 'echo "You\'ve hit your weekly limit" >&2\nexit 1\n')
        p = self.run_fm("--wait", "0.0003", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("usage limit", p.stderr)
        self.assertEqual(len([l for l in self.called().splitlines() if l.startswith("claude ")]), 2)

    def test_wait_zero_and_other_failures_stop_at_once(self):
        self.task("one")
        self.stub("claude", self.limited_then(self.finisher))
        p = self.run_fm("--wait", "0", check=False)
        self.assertEqual((p.returncode, "usage limit" in p.stderr), (1, True))
        # a crash whose earlier output merely mentions a limit is a crash, not a limit (only the last line counts)
        self.stub("claude", 'echo "You\'ve reached your quota, the API said"\necho "Error: boom" >&2\nexit 1\n')
        p = self.run_fm("--wait", "1", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("claude exited 1", p.stderr)
        for bad in ("nan", "-1", "inf"):
            self.assertIn("--wait", self.run_fm("--wait", bad, check=False).stderr)

    def test_tasks_waiting_on_the_user_are_skipped(self):
        a, b = self.task("one"), self.task("two")
        self.fm_ask(a, "publish")
        self.stub("claude", self.finisher)
        out = self.run_fm().stdout
        self.assertIn(f"{a} waits on the user", out)
        self.assertEqual(c.find_brief(c.find_project(self.repo), b).status, "done")

    def test_refuses_while_serve_runs_here(self):
        self.task("one")
        self.fm("serve", env=self.env())
        p = self.run_fm(check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("fm serve", p.stderr)
