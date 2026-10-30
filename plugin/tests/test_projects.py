"""fm projects --json and --follow (T-0322): the device-wide read surface the desktop app drives, locally or over ssh."""
import json
import os
import select
import subprocess
import sys
import time

from helpers import FM, ForemanTestCase, git_repo


class Projects(ForemanTestCase):
    def test_every_project_with_its_summary(self):
        self.fm("init")
        self.fm("task", "new", "Login times out", "--type", "FIX", "--tier", "S", "--ac", "logs in :: true",
                "--step", "red test", "--step", "fix", "--focus")
        self.fm("capture", "Merge the date helpers")
        other = git_repo(self.tmp, "other")
        self.fm("init", cwd=other)
        rows = {r["root"]: r for r in json.loads(self.fm("projects", "--json").stdout)["projects"]}
        self.assertEqual(set(rows), {os.path.realpath(self.repo), os.path.realpath(other)})
        mine = rows[os.path.realpath(self.repo)]
        self.assertEqual((mine["active"]["id"], mine["active"]["stage"], mine["active"]["steps_total"]),
                         ("T-0001", "executing", 2))
        self.assertEqual((mine["inbox"], mine["queue"], mine["drive"], mine["autonomy"]), (1, 0, True, "standard"))
        self.assertIsNone(rows[os.path.realpath(other)]["active"])
        self.assertIn(os.path.basename(other), self.fm("projects").stdout)  # plain text too
        self.fm("capture", "Write the onboarding guide", cwd=other)  # T-0890: one ranked list of what's next
        ranked = self.fm("projects", "--next").stdout.splitlines()
        self.assertEqual(len(ranked), 2, ranked)
        self.assertIn("T-0001 Login times out", ranked[0])  # an active task outranks an inbox-only project
        self.assertIn("Write the onboarding guide", ranked[1])


class Usage(ForemanTestCase):
    def test_projects_carry_the_devices_usage_pace(self):  # T-0346: the desktop app's sidebar meter
        self.fm("init")
        self.assertEqual(json.loads(self.fm("projects", "--json").stdout)["usage"], {})
        folder = os.path.join(self.home, "state", "sessions")
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "s.json"), "w") as f:
            json.dump({"rate_limits": {"five_hour": {"used_percentage": 42, "resets_at": time.time() + 3600},
                                       "seven_day": {"used_percentage": 31, "resets_at": time.time() + 3 * 86400}}}, f)
        u = json.loads(self.fm("projects", "--json").stdout)["usage"]
        self.assertEqual((u["five_hour"], u["seven_day"]), (42, 31))
        self.assertAlmostEqual(u["week_gone"], 4 / 7, places=2)


class Follow(ForemanTestCase):
    def read_line(self, proc, timeout=10):
        ready, _, _ = select.select([proc.stdout], [], [], timeout)
        self.assertTrue(ready, "no line within the timeout")
        return json.loads(proc.stdout.readline())

    def follow(self, *args):
        proc = subprocess.Popen([sys.executable, FM, *args, "--json", "--follow", "--interval", "0.1"], cwd=self.repo,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                env=dict(os.environ, FOREMAN_HOME=self.home))
        self.addCleanup(lambda: (proc.kill(), proc.wait(), proc.stdout.close(), proc.stderr.close()))
        return proc

    def test_a_view_line_each_time_the_project_changes(self):
        self.fm("init")
        proc = self.follow("ui")
        self.assertEqual(self.read_line(proc)["inbox_total"], 0)
        time.sleep(0.05)
        self.fm("capture", "Merge the date helpers")
        deadline = time.monotonic() + 10  # capture writes more than once, so a line can land between its writes
        while self.read_line(proc, max(0.1, deadline - time.monotonic()))["inbox_total"] != 1:
            pass

    def test_a_change_while_the_view_is_built_is_not_missed(self):  # T-1882: the snapshot comes before the build
        import contextlib
        import fmwatch
        path = os.path.join(self.home, "src")
        with open(path, "w") as f:
            f.write("0")
        os.utime(path, (time.time() - 10, time.time() - 10))  # an old mtime, so the write below always moves it

        def build():
            with open(path) as f:
                n = f.read()
            if n == "0":  # a capture lands right after the view read the state
                with open(path, "w") as f:
                    f.write("1")
            return {"n": n}

        class Out(list):
            def write(self, s):
                self.append(s)
                if '"1"' in s:
                    raise BrokenPipeError  # the reader saw the change: stop

            def flush(self):
                pass

        out, t = Out(), time.time()
        with contextlib.redirect_stdout(out):
            fmwatch._follow(build, lambda v: [path], 0.01, refresh=3)
        self.assertLess(time.time() - t, 1.5, out)  # the change came through, not held until the refresh

    def test_projects_follow_sees_a_new_project(self):
        self.fm("init")
        proc = self.follow("projects")
        self.assertEqual(len(self.read_line(proc)["projects"]), 1)
        self.fm("init", cwd=git_repo(self.tmp, "other"))
        self.assertEqual(len(self.read_line(proc)["projects"]), 2)
