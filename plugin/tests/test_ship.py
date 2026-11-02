"""T-1943: fm ship lands the unpushed commits on the remote's main from a scratch worktree, behind the publish grant."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


def sh(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


class Ship(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", self.origin], check=True)
        sh(self.repo, "remote", "add", "origin", self.origin)
        sh(self.repo, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "checkout", "-q", "-b", "work")
        for name in ("a", "b"):
            with open(os.path.join(self.repo, f"{name}.txt"), "w") as f:
                f.write(name + "\n")
            sh(self.repo, "add", f"{name}.txt")
            sh(self.repo, "commit", "-qm", f"add {name}")
        self.tid = json.loads(self.fm("task", "new", "land", "--type", "FEATURE", "--tier", "S", "--json").stdout)["id"]
        self.fm("task", "step", self.tid, "add", "land it")
        self.fm("task", "ac", self.tid, "add", "landed", "--verify", "true")
        self.fm("focus", self.tid)

    def grant(self):
        p = c.find_project(self.repo)
        b = c.find_brief(p, self.tid)
        b.meta["allow"] = ["publish"]
        c.save_brief(p, b)

    def granted(self):
        return "publish" in (c.find_brief(c.find_project(self.repo), self.tid).meta.get("allow") or [])

    def main_log(self):
        return sh(self.origin, "log", "--format=%s", "main").split("\n")

    def ship(self, *a):
        return self.fm("ship", "--remote", "origin", *a, check=False)

    def test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check(self):
        # T-1978: the ship's suite had no marker (a full fm check ran beside it) and ran beside a live check here
        import threading
        self.grant()
        p = c.find_project(self.repo)
        seen = os.path.join(self.tmp, "seen.json")
        busy = subprocess.Popen(["sleep", "2"])
        threading.Thread(target=busy.wait, daemon=True).start()
        c.update_meta(p, gates_running={"task": None, "pid": busy.pid, "at": c.now(), "root": p.root})
        r = self.ship("--test", f"cp {os.path.join(p.dir, 'meta.json')} {seen}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("waiting for a running fm check", r.stdout + r.stderr)
        with open(seen) as f:
            self.assertEqual(json.load(f)["ship_testing"]["pid"] > 0, True)
        self.assertFalse(c.read_meta(p).get("ship_testing"), "cleared after the run")

    def test_the_default_fm_check_in_the_scratch_tree_never_waits_for_its_own_ship(self):
        # T-1978: the ship's marker names its scratch tree; the fm check it runs there must not wait 10 minutes on it
        self.grant()
        self.fm("check", "add", "true")
        r = self.ship()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("waiting for fm ship", r.stdout + r.stderr)
        self.assertIn("add b", self.main_log())

    def test_without_the_grant_nothing_is_pushed(self):
        r = self.ship("--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("publish", r.stdout + r.stderr)
        self.assertNotIn("add a", self.main_log())

    def test_ships_the_unpushed_commits_after_the_test_and_spends_the_grant(self):
        self.grant()
        status = sh(self.repo, "status", "--porcelain")
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add b", "add a"])
        tip = sh(self.origin, "rev-parse", "main").strip()
        self.assertIn(tip, r.stdout, "the pushed sha, for fm ci-watch --commit")
        self.assertEqual(sh(self.repo, "rev-parse", "refs/foreman/shipped-tip").strip(), tip,
                         "T-2527: fm ci-watch --last-ship reads the pushed main tip")
        self.assertIn("ci-watch", r.stdout)
        self.assertFalse(self.granted(), "the yes covers one push")
        self.assertEqual(sh(self.repo, "worktree", "list").count("\n"), 1, "the scratch worktree is gone")
        self.assertEqual(sh(self.repo, "status", "--porcelain"), status, "the working tree is untouched")
        r = self.ship("--test", "true")  # main has these changes now (by patch, not sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("nothing to ship", r.stdout)

    def test_chance_books_one_ship_bet_on_the_pushed_commit(self):  # T-2496
        self.grant()
        self.assertNotEqual(self.ship("--test", "true", "--chance", "150").returncode, 0)  # refused before any push
        self.assertTrue(self.granted())
        r = self.ship("--test", "true", "--chance", "85")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        tip = sh(self.origin, "rev-parse", "main").strip()
        rows = [json.loads(x) for x in open(os.path.join(c.find_project(self.repo).dir, "calibration.jsonl"))]
        self.assertEqual([(x["kind"], x["stated"], x["key"], x["task"]) for x in rows], [("ship", 85, tip[:12], self.tid)])
        self.assertIn("85%", r.stdout)

    def test_chance_far_from_the_ship_record_names_it_after_the_bet(self):  # T-2611
        with open(os.path.join(c.find_project(self.repo).dir, "calibration.jsonl"), "w") as f:
            for i in range(20):  # 20 earlier ship bets, all settled green by CI
                f.write(json.dumps({"ts": c.now(), "id": f"s{i}", "kind": "ship", "stated": 85, "base": None,
                                    "task": self.tid, "key": f"{i:012x}"}) + "\n")
                f.write(json.dumps({"ts": c.now(), "of": f"s{i}", "outcome": "held", "by": "seeded", "src": "ci"}) + "\n")
        self.grant()
        r = self.ship("--test", "true", "--chance", "80")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"Ship bet: 80%.*\nShip record: 20 of 20 ship bets held \(100%\); 80% sits 20 points under")

    def mover(self, rel):  # T-2511: a script the ship's test runs: someone else pushes a commit to main meanwhile
        script, other = os.path.join(self.tmp, f"move-{rel.replace('/', '-')}.sh"), os.path.join(self.tmp, "other")
        with open(script, "w") as f:
            f.write(f"set -e\nrm -rf {other}\ngit clone -q {self.origin} {other}\ncd {other}\n"
                    f"mkdir -p $(dirname {rel})\necho moved > {rel}\ngit add -A\n"
                    "git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm 'tower update'\n"
                    "git push -q origin HEAD:main\n")
        return script

    def ci_ignores(self, *globs):  # T-2572: main's workflow names what CI never tests
        other = os.path.join(self.tmp, "ci")
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        os.makedirs(os.path.join(other, ".github", "workflows"))
        with open(os.path.join(other, ".github", "workflows", "test.yml"), "w") as f:
            f.write("on:\n  push:\n    paths-ignore:  # data\n" + "".join(f"      - {g}\n" for g in globs) + "jobs: {}\n")
        sh(other, "add", "-A")
        sh(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "ci")
        sh(other, "push", "-q", "origin", "HEAD:main")

    def test_a_main_that_moved_only_in_other_files_is_re_picked_and_pushed(self):  # T-2511
        self.ci_ignores("site/genesis/genesis.json", "site/genesis/gen-*/**")
        self.grant()
        r = self.ship("--test", f"sh {self.mover('site/genesis/genesis.json')}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:3], ["add b", "add a", "tower update"])
        self.assertFalse(self.granted())

    def test_a_move_in_a_file_ci_tests_refuses_though_no_shipped_file_moved(self):  # T-2572
        self.ci_ignores("site/genesis/genesis.json")
        self.grant()
        r = self.ship("--test", f"sh {self.mover('lib/other.py')}")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("files CI tests", r.stdout + r.stderr)
        self.assertTrue(self.granted())

    def test_without_a_workflow_every_file_move_refuses(self):  # T-2572
        self.grant()
        r = self.ship("--test", f"sh {self.mover('site/genesis/genesis.json')}")
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue(self.granted())

    def test_ci_globs_follow_github_rules(self):  # T-2572
        import fmrelease
        g = fmrelease._glob_re
        self.assertTrue(g("site/genesis/gen-*/**").match("site/genesis/gen-2/a/b.md"))
        self.assertFalse(g("site/genesis/gen-*/**").match("site/x.md"))
        self.assertFalse(g("site/genesis/*.md").match("site/genesis/gen-2/x.md"))
        self.assertTrue(g("'site/genesis/*.md'").match("site/genesis/frame.md"))

    def test_a_main_that_moved_in_a_shipped_file_still_refuses(self):  # T-2511
        self.grant()
        r = self.ship("--test", f"sh {self.mover('a.txt')}")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("moved while testing", r.stdout + r.stderr)
        self.assertTrue(self.granted())

    def test_ship_on_a_named_tasks_grant(self):
        # T-2007: a finished task ships on its own grant: no separate ship task focused to hold one
        r = self.ship("--task", self.tid.lower(), "--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(f"{self.tid} has no publish grant", r.stdout + r.stderr)
        self.assertNotIn("add a", self.main_log())
        r = self.ship("--task", "T-9999", "--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no task T-9999", r.stdout + r.stderr)
        self.grant()
        other = json.loads(self.fm("task", "new", "other", "--type", "CLEAN", "--tier", "S", "--ac", "x :: true",
                                    "--step", "x", "--json").stdout)["id"]
        self.fm("checkpoint")
        self.fm("focus", other)  # the active task has no grant; the named one does
        r = self.ship("--task", self.tid, "--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add b", "add a"])
        self.assertFalse(self.granted(), "the named task's yes is spent")

    def test_check_says_whether_main_has_the_commits_without_the_grant(self):
        # T-1960: a ship task's verify was git log -n3 | grep, which a later ship pushes out of view
        first = sh(self.repo, "rev-parse", "HEAD~1").strip()
        r = self.ship("--check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("add a", r.stdout)
        self.grant()
        self.assertEqual(self.ship(first, "--test", "true").returncode, 0)
        self.assertTrue(self.granted() is False)
        self.assertEqual(self.ship("--check", first).returncode, 0)
        r = self.ship("--check")
        self.assertEqual(r.returncode, 1, "add b is still missing")
        self.assertIn("add b", r.stdout)
        self.assertNotRegex(r.stdout, r"\badd a\b", "a word: a hash ending in 'add' before 'add b' reads as 'add a'")

    def test_a_named_commit_ships_alone(self):
        self.grant()
        first = sh(self.repo, "rev-parse", "HEAD~1").strip()
        r = self.ship(first, "--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[0], "add a")
        self.assertNotIn("add b", self.main_log())

    def test_a_failed_test_pushes_nothing_and_keeps_the_grant(self):
        self.grant()
        r = self.ship("--test", "false")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())
        self.assertEqual(sh(self.repo, "worktree", "list").count("\n"), 1)

    def test_a_tree_changed_after_the_tests_ran_refuses_with_both_hashes(self):  # T-2642
        self.grant()
        r = self.ship("--test", "sh -c 'echo x > c.txt && git add c.txt && git -c user.name=t -c user.email=t@t commit -qm sneak'")
        out = r.stdout + r.stderr
        self.assertNotEqual(r.returncode, 0, out)
        self.assertIn("tree", out)
        self.assertRegex(out, r"[0-9a-f]{40}.*[0-9a-f]{40}")
        self.assertNotIn("add a", self.main_log())
        self.assertNotIn("sneak", self.main_log())
        self.assertTrue(self.granted())

    def affected_ship(self, template):
        # T-2323: a changed test file in the range, and a stubbed affected runner; the full suite writes a marker
        self.grant()
        with open(os.path.join(self.repo, "test_new.py"), "w") as f:
            f.write("x = 1\n")
        sh(self.repo, "add", "test_new.py")
        sh(self.repo, "commit", "-qm", "add test_new")
        self.fm("check", "affected", template)
        self.marker = os.path.join(self.tmp, "full-ran")
        return self.ship("--test", f"touch {self.marker}")

    def test_a_red_affected_run_stops_the_ship_before_the_full_suite_naming_the_class(self):
        r = self.affected_ship("echo {tests}; echo 'FAIL: test_x (test_new.Cls.test_x)'; exit 1")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("affected tests failed", r.stdout + r.stderr)
        self.assertIn("test_new.Cls", r.stdout + r.stderr)
        self.assertFalse(os.path.exists(self.marker), "the full suite never started")
        self.assertNotIn("add test_new", self.main_log())
        self.assertTrue(self.granted())

    def test_a_green_affected_run_goes_on_to_the_full_suite(self):
        r = self.affected_ship("echo {tests}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(self.marker))
        self.assertIn("add test_new", self.main_log())

    def test_a_red_test_captures_one_baseline_task_naming_the_failing_test(self):
        # T-2255: the ship's red run files what fm check would, once per failing set, and still pushes nothing
        self.grant()
        red = "sh -c 'echo \"FAIL: test_x (test_mod.Cls.test_x)\"; echo Ran 1 test; echo \"FAILED (failures=1)\"; exit 1'"
        r = self.ship("--test", red)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("FAIL: test_x", r.stdout)  # still streamed
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())
        p = c.find_project(self.repo)
        base = [b for b in c.load_briefs(p) if b.meta.get("baseline")]
        self.assertEqual(len(base), 1)
        self.assertEqual(base[0].meta.get("priority"), "urgent")
        self.assertIn("fails test_mod.Cls.test_x.", base[0].section("Raw request"))
        self.assertIn(base[0].id, r.stderr + r.stdout)
        self.ship("--test", red)
        self.assertEqual(len([b for b in c.load_briefs(p) if b.meta.get("baseline")]), 1)

    def base(self):
        return [b for b in c.load_briefs(c.find_project(self.repo)) if b.meta.get("baseline")]

    def test_a_background_process_holding_the_output_doesnt_hang_the_ship(self):
        import time
        self.grant()
        t = time.time()
        r = self.ship("--test", "sh -c 'sleep 30 & exit 1'")
        self.assertNotEqual(r.returncode, 0)
        self.assertLess(time.time() - t, 20)  # wall clock: a ship child must not wait out its background sleeper
        self.assertNotIn("add a", self.main_log())

    def test_a_failing_name_is_cleaned_and_cut_before_it_is_written(self):
        self.grant()
        out = os.path.join(self.tmp, "out.txt")  # a file, so the 10k name isn't also in the command
        with open(out, "w") as f:
            f.write("FAILED t.py::test_x_" + "y" * 10000 + "\x1b[31mz\n")
        red = f"sh -c 'cat {out}; exit 1'"
        r = self.ship("--test", red)
        self.assertTrue(self.base(), r.stdout[-300:] + r.stderr[-500:])
        text = self.base()[0].section("Raw request")
        self.assertNotIn("\x1b", text)
        self.assertLess(len(text), 1500)

    def test_an_environment_failure_captures_nothing(self):
        self.grant()
        red = "sh -c 'echo \"FAIL: test_x (m.C.test_x)\"; echo \"No space left on device\"; exit 1'"
        r = self.ship("--test", red)
        self.assertIn("the test failed in the scratch tree", r.stderr + r.stdout)
        self.assertFalse(self.base())

    def test_a_green_ship_records_the_footprint_and_a_red_one_does_not(self):  # T-2281
        self.grant()
        rec = os.path.join(c.find_project(self.repo).dir, "footprint.json")
        self.ship("--test", "false")
        self.assertFalse(os.path.exists(rec))
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        self.assertFalse(os.path.exists(rec))  # no plugin/rules/foreman.md in this repo: not Foreman's own
        os.makedirs(os.path.join(self.repo, "plugin", "rules"))
        with open(os.path.join(self.repo, "plugin", "rules", "foreman.md"), "w") as f:
            f.write("a rule\n")
        sh(self.repo, "add", "plugin")
        sh(self.repo, "commit", "-qm", "rules")
        self.grant()
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        with open(rec) as f:
            got = json.load(f)["metrics"]
        self.assertIn("rules chars", got)
        self.assertNotIn("SessionStart chars", got)  # no bench in this tree: not measured
        # T-2358: with the tree's own hook bench, the record carries injected chars and each hook's p95
        os.makedirs(os.path.join(self.repo, "plugin", "tests"))
        with open(os.path.join(self.repo, "plugin", "tests", "bench_hooks.py"), "w") as f:
            f.write("import json, sys\nassert '--inject' in sys.argv and '--json' in sys.argv\n"
                    "print(json.dumps({'bench': {'PreToolUse:Bash': {'p95': 40.0, 'cpu_p95': 30.0, 'load': 0.1}},"
                    " 'injected': {'SessionStart': 1234, 'UserPromptSubmit': 56}}))\n")
        sh(self.repo, "add", "plugin")
        sh(self.repo, "commit", "-qm", "bench")
        self.grant()
        r = self.fm("ship", "--remote", "origin", "--test", "true", check=False, env={"FOREMAN_DOCTOR_BENCH": "1"})
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(rec) as f:
            got = json.load(f)["metrics"]
        self.assertEqual((got.get("SessionStart chars"), got.get("PreToolUse:Bash p95 ms")), (1234, 40.0))

    def test_a_green_ship_names_an_open_baseline_task_it_turned_green(self):
        self.grant()
        flag = os.path.join(self.tmp, "ok")
        cmd = f"sh -c 'test -f {flag} || {{ echo \"FAIL: test_x (m.C.test_x)\"; exit 1; }}'"
        self.ship("--test", cmd)
        tid = self.base()[0].id
        open(flag, "w").close()
        r = self.ship("--test", cmd)
        self.assertEqual(r.returncode, 0)
        self.assertIn(f"baseline is green again: {tid}", r.stdout)

    def test_a_red_test_naming_no_failing_test_captures_nothing(self):
        self.ship("--test", "false")
        self.assertFalse([b for b in c.load_briefs(c.find_project(self.repo)) if b.meta.get("baseline")])

    def test_main_moving_during_the_test_in_no_shipped_file_is_re_picked(self):
        # T-2511: an empty commit lands on main mid-test; it touches no file the ship does, so the tested result
        # still holds on the new main (a move in a shipped file refuses: test_a_main_that_moved_in_a_shipped_file...)
        self.grant()
        other = os.path.join(self.tmp, "other")
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        sh(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "someone else")
        r = self.ship("--test", f"git -C {other} push -q origin HEAD:main")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("re-picked onto it", r.stdout)
        self.assertEqual(self.main_log()[:3], ["add b", "add a", "someone else"])
        self.assertFalse(self.granted())

    def test_main_moving_between_the_last_check_and_the_push_is_re_picked_without_a_retest(self):
        # T-2555: fm genesis live's tower publish landed between ship's last fetch and its push: "cannot lock ref"
        hook = os.path.join(self.origin, "hooks", "pre-receive")
        with open(hook, "w") as f:  # the first push moves main itself (an empty commit), as a racing writer would
            f.write('#!/bin/sh\n[ -f "$GIT_DIR/moved" ] && exit 0\ntouch "$GIT_DIR/moved"\n'
                    "unset GIT_QUARANTINE_PATH GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES\n"
                    "old=$(git rev-parse refs/heads/main)\n"
                    'new=$(echo "tower publish" | GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t '
                    'GIT_COMMITTER_EMAIL=t@t git commit-tree "$old^{tree}" -p "$old")\n'
                    'git update-ref refs/heads/main "$new"\n')
        os.chmod(hook, 0o755)
        self.grant()
        runs = os.path.join(self.tmp, "runs")
        r = self.ship("--test", f"sh -c 'echo x >> {runs}'")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:3], ["add b", "add a", "tower publish"])
        with open(runs) as f:
            self.assertEqual(f.read().count("x"), 1, "the move touched no shipped file: no second test run")
        self.assertFalse(self.granted())

    def test_a_rejected_push_keeps_the_grant(self):
        # review: the grant was spent before git push, so a rejected push cost the yes
        hook = os.path.join(self.origin, "hooks", "pre-receive")
        with open(hook, "w") as f:
            f.write("#!/bin/sh\necho no >&2\nexit 1\n")
        os.chmod(hook, 0o755)
        self.grant()
        r = self.ship("--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted(), "a push that failed gives the grant back")
        self.assertEqual(sh(self.repo, "worktree", "list").count("\n"), 1)

    def test_a_relative_remote_path_and_a_missing_test_program(self):
        self.grant()
        r = self.ship("--test", "no-such-program-1943")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertTrue(self.granted())
        sh(self.repo, "remote", "set-url", "origin", os.path.relpath(self.origin, self.repo))
        r = self.ship("--test", "true")  # fetched and pushed from the repo, not the scratch tree
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[0], "add b")

    def test_a_plain_ship_starts_after_the_shipped_ref(self):
        # T-1945: main held shipped commits under another patch (a merge), so git cherry listed them every time
        self.grant()
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        other = os.path.join(self.tmp, "other")
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        sh(other, "reset", "-q", "--hard", "HEAD~2")
        for name in ("a", "b"):
            with open(os.path.join(other, f"{name}.txt"), "w") as f:
                f.write(name + "\n")
        sh(other, "add", ".")
        sh(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "a and b squashed")
        sh(other, "push", "-qf", "origin", "HEAD:main")
        with open(os.path.join(self.repo, "c.txt"), "w") as f:
            f.write("c\n")
        sh(self.repo, "add", "c.txt")
        sh(self.repo, "commit", "-qm", "add c")
        self.grant()
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add c", "a and b squashed"])
        self.assertEqual(sh(self.repo, "rev-parse", "refs/foreman/shipped"), sh(self.repo, "rev-parse", "HEAD"))

    def test_a_merged_lane_whose_merge_settled_a_conflict_ships_through_the_merge(self):
        # T-2054: a builder lane's own commit didn't cherry-pick onto main alone; its merge on the branch had settled it
        self.grant()
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        shipped = sh(self.repo, "rev-parse", "HEAD").strip()
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("one\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "branch writes shared")
        sh(self.repo, "checkout", "-q", "-b", "lane", shipped)
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("two\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "lane writes shared")
        sh(self.repo, "checkout", "-q", "work")
        subprocess.run(["git", "-C", self.repo, "merge", "-q", "lane"], capture_output=True)
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("one\ntwo\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "Merge lane")
        self.grant()
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sh(self.origin, "show", "main:shared.txt"), "one\ntwo\n")
        self.assertEqual(self.main_log()[:2], ["Merge lane", "branch writes shared"])
        self.assertEqual(sh(self.repo, "rev-parse", "refs/foreman/shipped"), sh(self.repo, "rev-parse", "HEAD"))

    def _merged_lane_then_main_moves(self, name):
        # T-2212: the T-2054 setup, then someone pushes a commit to origin main touching `name` after the last ship
        self.grant()
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        shipped = sh(self.repo, "rev-parse", "HEAD").strip()
        for branch, text, msg in (("work", "one\n", "branch writes shared"), ("lane", "two\n", "lane writes shared")):
            if branch == "lane":
                sh(self.repo, "checkout", "-q", "-b", "lane", shipped)
            with open(os.path.join(self.repo, "shared.txt"), "w") as f:
                f.write(text)
            sh(self.repo, "add", "shared.txt")
            sh(self.repo, "commit", "-qm", msg)
        sh(self.repo, "checkout", "-q", "work")
        subprocess.run(["git", "-C", self.repo, "merge", "-q", "lane"], capture_output=True)
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("one\ntwo\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "Merge lane")
        other = os.path.join(self.tmp, "other")
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        os.makedirs(os.path.dirname(os.path.join(other, name)), exist_ok=True)
        with open(os.path.join(other, name), "w") as f:
            f.write("main moved\n")
        sh(other, "add", ".")
        sh(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "main moves")
        sh(other, "push", "-q", "origin", "HEAD:main")
        self.grant()

    def test_a_merged_lane_ships_when_main_moved_only_in_other_files(self):
        self._merged_lane_then_main_moves("site/genesis.json")
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sh(self.origin, "show", "main:shared.txt"), "one\ntwo\n")
        self.assertEqual(sh(self.origin, "show", "main:site/genesis.json"), "main moved\n")

    def test_a_merged_lane_is_refused_when_main_touched_the_branchs_files(self):
        self._merged_lane_then_main_moves("shared.txt")
        before = sh(self.origin, "rev-parse", "main")
        r = self.ship("--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(sh(self.origin, "rev-parse", "main"), before)

    def test_a_remembered_test_runs_when_test_is_left_out(self):
        # T-1950: the oldest runtime's suite was retyped on every ship
        mark = os.path.join(self.tmp, "ran")
        self.grant()
        self.assertEqual(self.ship("--test", f"touch {mark}").returncode, 0)
        os.remove(mark)
        with open(os.path.join(self.repo, "c.txt"), "w") as f:
            f.write("c\n")
        sh(self.repo, "add", "c.txt")
        sh(self.repo, "commit", "-qm", "add c")
        self.grant()
        r = self.ship()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(mark), "the remembered --test ran")
        self.assertIn(f"touch {mark}", r.stdout)

    def test_a_failed_ref_write_after_the_push_still_reports_the_ship(self):
        # T-1951: main got the commits, so a refs/foreman/shipped lock must not read as a failed ship
        lock = os.path.join(self.repo, ".git", "refs", "foreman", "shipped.lock")
        os.makedirs(os.path.dirname(lock))
        open(lock, "w").close()
        self.grant()
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add b", "add a"])
        self.assertIn("shipped 2 commits", r.stdout)
        self.assertIn("refs/foreman/shipped", r.stdout + r.stderr)

    def test_watch_watches_the_pushed_commit(self):
        # T-1946: ship, then CI on the pushed sha, in one background job
        import sys
        bin_dir = os.path.join(self.tmp, "bin")
        os.makedirs(bin_dir)
        with open(os.path.join(bin_dir, "gh"), "w") as f:
            f.write(f"#!{sys.executable}\nimport json, subprocess, sys\n"
                    "if sys.argv[1:3] != ['run', 'list']: sys.exit(3)\n"
                    f"sha = subprocess.run(['git', '-C', {self.origin!r}, 'rev-parse', 'main'], capture_output=True, text=True).stdout.strip()\n"
                    "print(json.dumps([{'databaseId': 1, 'status': 'completed', 'conclusion': 'success', 'headSha': sha, "
                    "'url': 'https://github.com/o/r/actions/runs/1'}]))\n")
        os.chmod(os.path.join(bin_dir, "gh"), 0o755)
        self.grant()
        r = self.fm("ship", "--remote", "origin", "--test", "true", "--watch",
                    env={"PATH": bin_dir + os.pathsep + os.environ["PATH"]}, check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        tip = sh(self.origin, "rev-parse", "main").strip()
        self.assertIn(f"watching {tip[:7]} on main", r.stdout)
        self.assertIn("CI green", r.stdout)

    def test_a_remote_or_commit_that_reads_as_an_option_is_refused(self):
        self.grant()
        for argv in (["--remote=--upload-pack=touch x"], ["--remote", "origin", "--", "--output=x"]):
            r = self.fm("ship", *argv, "--test", "true", check=False)
            self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())
