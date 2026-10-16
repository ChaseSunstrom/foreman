"""T-0134: a linked git worktree is a lane of its project: it shares the project's state, keeps its own active task
(focus there pauses only that lane's), does its git work in its own files, and neither side's next or queue offers a
task the other holds. fm lane new|list|rm manage them; rm never discards uncommitted work."""
import json
import os
import subprocess
import unittest

from helpers import ForemanTestCase, read_text

import fmcore as c

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # --focus prints its own lines after the JSON


class Lanes(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.lane = os.path.join(self.tmp, "lane")
        subprocess.run(["git", "-C", self.repo, "worktree", "add", "-q", "-b", "foreman/lane", self.lane], check=True)

    def git(self, *args, cwd=None):
        return subprocess.run(["git", "-C", cwd or self.repo, *args], capture_output=True, text=True).stdout

    def new(self, title, cwd, focus=True):
        args = ["task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--json"]
        return first(self.fm(*args, *(["--focus"] if focus else []), cwd=cwd).stdout)["id"]

    def test_a_worktree_is_a_lane_with_its_own_active_task(self):
        main = self.new("Main work", self.repo)
        lane = self.new("Lane work", self.lane)  # must not pause the main checkout's task
        st_main = json.loads(self.fm("state", "--json").stdout)
        st_lane = json.loads(self.fm("state", "--json", cwd=self.lane).stdout)
        self.assertEqual(st_main["active"]["id"], main)
        self.assertEqual(st_lane["active"]["id"], lane)
        self.assertNotIn(lane, [q["id"] for q in st_main["queue"]])
        self.assertNotIn(main, [q["id"] for q in st_lane["queue"]])
        self.assertIn(main, self.fm("next").stdout)
        self.assertIn(lane, self.fm("next", cwd=self.lane).stdout)
        p = self.fm("focus", lane, check=False)  # the lane holds it
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("lane", p.stderr)

    def test_the_edit_gate_in_a_lane_needs_that_lanes_task(self):
        self.new("Main work", self.repo)
        edit = {"tool_name": "Write", "tool_input": {"file_path": os.path.join(self.lane, "x.py"), "content": "x"},
                "cwd": self.lane}
        self.assertEqual(self.hook("PreToolUse", edit).returncode, 2, "the main checkout's task doesn't cover the lane")
        self.new("Lane work", self.lane)
        self.assertEqual(self.hook("PreToolUse", edit).returncode, 0)

    def test_finish_commit_in_a_lane_commits_on_its_branch(self):
        tid = self.new("Lane work", self.lane)
        with open(os.path.join(self.lane, "lane.py"), "w") as f:
            f.write("x = 1\n")
        self.fm("task", "finish", tid, "--run", "true", "--audit", "self check", "--commit", "Lane work", cwd=self.lane)
        self.assertIn("Lane work", self.git("log", "--format=%s", "foreman/lane"))
        self.assertNotIn("Lane work", self.git("log", "--format=%s", "main"))
        self.assertFalse(os.path.exists(os.path.join(self.repo, "lane.py")))

    def test_a_merged_lanes_task_is_measured_from_the_main_commit_before_the_merge(self):
        # T-0804: main-thread commits made while the lane ran were counted as the lane task's out-of-scope edits
        tid = self.new("Lane work", self.lane)
        for root, name in ((self.lane, "lane.py"), (self.repo, "main_work.py")):
            with open(os.path.join(root, name), "w") as f:
                f.write("x = 1\n")
            self.git("add", name, cwd=root)
            self.git("commit", "-qm", name, cwd=root)
        self.fm("lane", "merge", tid)
        meta = json.loads(self.fm("task", "show", tid, "--json").stdout)["meta"]
        changed = self.git("diff", "--name-only", meta["base"], "HEAD").split()
        self.assertEqual(changed, ["lane.py"])
        # T-0812: closed from the main checkout, it re-snapshotted its start from the merged files: its diff was empty
        self.fm("lane", "rm", tid)
        self.fm("focus", tid)
        meta = json.loads(self.fm("task", "show", tid, "--json").stdout)["meta"]
        self.assertEqual(self.git("diff", "--name-only", meta.get("base_tree") or meta["base"]).split(), ["lane.py"])

    def test_tidy_sweeps_stale_lanes(self):
        # T-0186: a closed task's lane and its branch stayed until someone ran fm lane rm
        home = {"HOME": self.tmp}  # tidy's global checks stay off the real ~/.claude
        done = self.new("Done in a lane", self.repo, focus=False)
        path = json.loads(self.fm("lane", "new", done, "--json").stdout)["path"]
        self.fm("focus", done, cwd=path)
        with open(os.path.join(path, "done.py"), "w") as f:
            f.write("x = 1\n")
        self.fm("task", "finish", done, "--run", "true", "--audit", "self check", "--commit", "Done work", cwd=path)
        dropped = self.new("Dropped with work left", self.repo, focus=False)
        kept = json.loads(self.fm("lane", "new", dropped, "--json").stdout)["path"]
        with open(os.path.join(kept, "wip.py"), "w") as f:
            f.write("y = 1\n")
        self.fm("task", "drop", dropped, "not needed")
        self.assertIn(f"stale_lane: {done}", self.fm("tidy", env=home).stdout)
        self.fm("tidy", "--apply", env=home)
        self.assertFalse(os.path.isdir(path))
        self.assertTrue(os.path.isdir(kept), "uncommitted work is never discarded")
        self.assertIn(f"foreman/{done}", self.git("branch", "--list", "foreman/T-*"), "not merged yet: kept")
        self.git("merge", "-q", f"foreman/{done}")
        self.assertIn(f"merged_lane_branch: foreman/{done}", self.fm("tidy", env=home).stdout)
        self.fm("tidy", "--apply", env=home)
        self.assertNotIn(f"foreman/{done}", self.git("branch", "--list", "foreman/T-*"))

    def test_rm_waits_for_an_open_conflict_unless_the_task_is_dropped(self):
        # T-1136: rm right after a conflicted merge took the builder record, so the lane couldn't be resumed
        tid = self.new("Conflicted", self.repo, focus=False)
        path = json.loads(self.fm("lane", "new", tid, "--json").stdout)["path"]
        with open(os.path.join(path, "work.py"), "w") as f:
            f.write("x = 1\n")
        self.git("add", "work.py", cwd=path)
        self.git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "work", cwd=path)
        audits = os.path.join(c.find_project(self.repo).dir, "audits")
        os.makedirs(audits, exist_ok=True)
        with open(os.path.join(audits, f"{tid}.conflict.md"), "w") as f:
            f.write("# Conflict\n")
        p = self.fm("lane", "rm", tid, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("conflict", p.stderr + p.stdout)
        self.assertTrue(os.path.isdir(path))
        self.fm("task", "drop", tid, "abandoned")
        self.fm("lane", "rm", tid)
        self.assertFalse(os.path.isdir(path))

    def test_fm_lane_new_list_and_rm(self):
        tid = self.new("Laned", self.repo, focus=False)
        data = json.loads(self.fm("lane", "new", tid, "--json").stdout)
        self.assertTrue(os.path.isdir(data["path"]))
        self.assertEqual(data["branch"], f"foreman/{tid}")
        self.assertIn(tid, self.fm("lane", "list").stdout)
        self.assertNotIn(tid, [q["id"] for q in json.loads(self.fm("state", "--json").stdout)["queue"]],
                         "the main checkout doesn't offer a task given to a lane")
        with open(os.path.join(data["path"], "wip.py"), "w") as f:
            f.write("x = 1\n")
        p = self.fm("lane", "rm", tid, check=False)
        self.assertNotEqual(p.returncode, 0, "uncommitted work is never discarded")
        self.assertTrue(os.path.isdir(data["path"]))
        os.remove(os.path.join(data["path"], "wip.py"))
        self.fm("lane", "rm", tid)
        self.assertFalse(os.path.isdir(data["path"]))
        self.assertIn(tid, [q["id"] for q in json.loads(self.fm("state", "--json").stdout)["queue"]], "back in the queue")

    def test_rm_unlocks_a_finished_agents_worktree_once_merged(self):
        # T-0725: Claude Code keeps a builder's worktree locked ("claude agent … (pid …)") after it finishes, so
        # fm lane rm failed on git's lock even with the branch merged
        tid = self.new("Laned", self.repo, focus=False)
        data = json.loads(self.fm("lane", "new", tid, "--json").stdout)
        with open(os.path.join(data["path"], "done.py"), "w") as f:
            f.write("x = 1\n")
        self.git("add", "done.py", cwd=data["path"])
        self.git("commit", "-qm", "done", cwd=data["path"])
        self.git("worktree", "lock", "--reason", "claude agent agent-x (pid 1 start 1)", data["path"])
        p = self.fm("lane", "rm", tid, check=False)
        self.assertNotEqual(p.returncode, 0, "not merged: the agent's lock holds")
        self.assertIn("merge", p.stderr)
        self.git("merge", "-q", "--no-ff", "-m", "merge", data["branch"])
        self.fm("lane", "rm", tid)
        self.assertFalse(os.path.isdir(data["path"]))

    def test_the_shared_status_files_keep_the_main_checkouts_view(self):
        # review: a lane's write overwrote status.json, so the main session's statusline showed the lane's task
        import fmcore as c
        main = self.new("Main work", self.repo)
        self.new("Lane work", self.lane)
        with open(os.path.join(c.find_project(self.repo).dir, "status.json")) as f:
            self.assertIn(main, f.read())

    def test_rm_keeps_ignored_files_and_frees_a_hand_deleted_lane(self):
        import shutil
        tid = self.new("Laned", self.repo, focus=False)
        path = json.loads(self.fm("lane", "new", tid, "--json").stdout)["path"]
        with open(os.path.join(path, ".gitignore"), "w") as f:
            f.write(".env\n.gitignore\n")
        with open(os.path.join(path, ".env"), "w") as f:
            f.write("KEY=x\n")
        p = self.fm("lane", "rm", tid, check=False)
        self.assertNotEqual(p.returncode, 0, "an ignored .env would go with the folder")
        self.assertIn(".env", p.stderr)
        shutil.rmtree(path)  # deleted by hand
        self.assertIn("missing", self.fm("lane", "list").stdout)
        out = self.fm("lane", "rm", tid).stdout
        self.assertNotIn("kept", out, "its branch is merged (no commits): it goes")
        self.fm("lane", "new", tid)  # and the lane can be made again

    def test_a_criterions_command_run_in_a_lane_is_that_lanes_evidence(self):
        main = self.new("Main work", self.repo)
        lane = self.new("Lane work", self.lane)
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": "true"}, "cwd": self.lane,
                                  "tool_response": {"stdout": "", "stderr": "", "exitCode": 0}})
        self.assertIn("`true`", self.fm("task", "show", lane).stdout.split("## Verification evidence")[1])
        self.assertNotIn("`true`", self.fm("task", "show", main).stdout.split("## Verification evidence")[1])

    def test_task_set_cant_start_a_task_around_focus(self):
        tid = self.new("Main work", self.repo, focus=False)
        p = self.fm("task", "set", tid, "status=active", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("fm focus", p.stderr)

    def test_the_brief_agent_line_names_effort_by_tier(self):
        # T-0779: S builders run at medium effort, M at high, beside the model
        for tier, effort in (("S", "medium"), ("M", "high")):
            extra = ["--interpretation", "x", "--approach", "x"] if tier != "S" else []
            tid = first(self.fm("task", "new", f"T{tier}", "--type", "FEATURE", "--tier", tier, "--ac", "ok :: true",
                                "--step", "s", *extra, "--json").stdout)["id"]
            agent = json.loads(self.fm("lane", "brief", tid, "--json").stdout)["agent"]
            self.assertIn(f'effort: "{effort}"', agent)

    def stopped_builder(self, proc=None, wip="wip.py"):
        """T-1028: a builder whose launching claude process is gone, with work left in its lane."""
        import fmbus
        tid = first(self.fm("task", "new", "Built", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true", "--step", "s",
                            "--interpretation", "x", "--approach", "x", "--json").stdout)["id"]
        path = json.loads(self.fm("lane", "new", tid, "--json").stdout)["path"]
        p = c.find_project(self.repo)
        b = c.find_brief(p, tid)
        b.meta["builder"] = c.now()
        b.meta["builder_proc"] = proc or f"{fmbus.host_id()}|999999999|1"
        c.save_brief(p, b)
        with open(os.path.join(path, wip), "w") as f:
            f.write("x = 1\n")
        return tid, path

    def test_a_builder_whose_claude_process_ended_is_flagged_with_the_resume_command(self):
        tid, _ = self.stopped_builder()
        self.assertIn(f"fm lane resume {tid}", self.fm("next").stdout)
        import fmbus
        self.assertFalse(fmbus.proc_alive(999999999, "1"))
        self.assertTrue(fmbus.proc_alive(os.getpid(), fmbus._proc(os.getpid())[1]))
        self.assertEqual(fmbus.proc_state("elsewhere|ns|1|1"), "unknown")

    def test_resume_keeps_the_work_frees_the_folder_and_briefs_from_the_branch(self):
        tid, path = self.stopped_builder()
        self.fm("lane", "resume", tid)
        self.assertFalse(os.path.isdir(path))
        self.assertIn("WIP", self.git("log", "--format=%s", f"foreman/{tid}"))
        self.assertIn("wip.py", self.git("show", "--name-only", "--format=", f"foreman/{tid}"))
        meta = json.loads(self.fm("task", "show", tid, "--json").stdout)["meta"]
        self.assertNotIn("lane", meta)
        self.assertNotIn("|999999999|", meta.get("builder_proc") or "", "the dead process is no longer the builder's")
        self.assertIn("builder", meta, "briefed again")
        brief = read_text(os.path.join(c.find_project(self.repo).dir, "audits", f"{tid}.builder.md"))
        self.assertIn(f"git merge foreman/{tid}", brief)
        self.assertNotIn(f"fm lane resume {tid}", self.fm("next").stdout, "its new process is recorded")

    def test_resume_refuses_a_live_builder_unless_forced_with_a_reason(self):
        import fmbus
        me = fmbus._proc(os.getpid())[1]
        tid, path = self.stopped_builder(proc=f"{fmbus.host_id()}|{os.getpid()}|{me}")
        self.assertNotIn(f"fm lane resume {tid}", self.fm("next").stdout)
        self.assertNotEqual(self.fm("lane", "resume", tid, check=False).returncode, 0)
        self.assertTrue(os.path.isdir(path), "a live builder keeps its worktree")
        self.fm("lane", "resume", tid, "--force", "it hung")
        self.assertFalse(os.path.isdir(path))
        self.assertIn("it hung", self.fm("task", "show", tid).stdout)

    def test_another_host_is_unknown_not_stopped(self):
        tid, path = self.stopped_builder(proc="elsewhere|ns|999999999|1")
        self.assertNotIn(f"fm lane resume {tid}", self.fm("next").stdout)
        self.assertNotEqual(self.fm("lane", "resume", tid, check=False).returncode, 0)
        self.assertTrue(os.path.isdir(path))

    def test_a_briefed_never_launched_task_is_not_flagged(self):
        import fmbus
        tid = first(self.fm("task", "new", "Idle", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true", "--step", "s",
                            "--interpretation", "x", "--approach", "x", "--json").stdout)["id"]
        p = c.find_project(self.repo)
        b = c.find_brief(p, tid)
        b.meta["builder"] = c.now()
        b.meta["builder_proc"] = f"{fmbus.host_id()}|999999999|1"
        c.save_brief(p, b)
        self.assertNotIn(f"fm lane resume {tid}", self.fm("next").stdout)

    def test_resume_on_a_detached_head_keeps_the_commit_on_a_branch(self):
        tid, path = self.stopped_builder()
        self.git("checkout", "-q", "--detach", cwd=path)
        self.git("branch", "-D", f"foreman/{tid}")
        self.fm("lane", "resume", tid)
        brief = read_text(os.path.join(c.find_project(self.repo).dir, "audits", f"{tid}.builder.md"))
        self.assertNotIn("git merge HEAD", brief)
        self.assertIn("wip.py", self.git("show", "--name-only", "--format=", f"foreman/{tid}"))

    def test_resume_refuses_to_delete_ignored_files(self):
        tid, path = self.stopped_builder()
        with open(os.path.join(path, ".gitignore"), "w") as f:
            f.write(".venv/\n")
        os.makedirs(os.path.join(path, ".venv"))
        with open(os.path.join(path, ".venv", "x"), "w") as f:
            f.write("1")
        p = self.fm("lane", "resume", tid, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn(".venv", p.stderr)
        self.assertTrue(os.path.isdir(path))
        self.fm("lane", "resume", tid, "--force", "venv is rebuilt")
        self.assertFalse(os.path.isdir(path))

    def test_resume_leaves_secrets_out_of_the_wip_commit_and_stops(self):
        tid, path = self.stopped_builder(wip=".env")
        p = self.fm("lane", "resume", tid, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn(".env", p.stderr)
        self.assertTrue(os.path.isdir(path), "nothing is removed")
        self.assertNotIn(".env", self.git("show", "--name-only", "--format=", f"foreman/{tid}"))


if __name__ == "__main__":
    unittest.main()


class BuilderGates(unittest.TestCase):
    def test_builders_run_affected_tests_and_leave_the_full_gates_to_the_merge(self):
        # T-0806: two lanes and the main thread ran three full gate runs at once (load 74): tests timed out, lanes
        # reported load as red gates, and the merge re-ran the full gates anyway
        import fmlanes
        agent = read_text(os.path.join(os.path.dirname(__file__), "..", "agents", "fm-builder.md"))
        for text in (fmlanes.CONTRACT, agent):
            self.assertIn("fm check --affected --evidence", text)
            self.assertIn("full gates run after the merge", text)
            self.assertNotRegex(text, r"`fm check --evidence")
        self.assertIn("without `cd DIR &&` chains", fmlanes.CONTRACT)  # T-0808

    def test_builders_review_their_own_change_as_an_adversary_before_reporting(self):
        # T-1147: reviewers found real defects in almost every builder branch
        import fmlanes
        agent = read_text(os.path.join(os.path.dirname(__file__), "..", "agents", "fm-builder.md"))
        for text in (fmlanes.CONTRACT, agent):
            for w in ("Self-review", "what input breaks it", "what outside text it trusts", "what is unbounded",
                      "what it writes and where", "a second run"):
                self.assertIn(w, text)


class BoardLanes(ForemanTestCase):
    """T-0961: the merge base is on disk before git merge runs (a merge that dies midway still measures the task from
    there) and a failed merge leaves the old one; one git runner (fmcore's) behind fmlanes, fmsecrets, fmmap, fmbench."""

    def git(self, root, *args):
        return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, check=True).stdout

    def lane(self, text):
        self.fm("init")
        self.fm("task", "new", "Lane work", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        path = json.loads(self.fm("lane", "new", "T-0001", "--json").stdout)["path"]
        with open(os.path.join(path, "shared.py"), "w") as f:
            f.write(text)
        self.git(path, "add", "shared.py")
        self.git(path, "commit", "-qm", "lane change")
        return path

    def base(self):
        import fmcore as c
        return c.load_briefs(c.find_project(self.repo))[0].meta.get("base")

    def test_the_base_is_saved_before_git_merge_runs(self):
        import fmcli
        import fmcore as c
        import fmlanes
        self.lane("x = 2\n")
        head, seen, real = self.git(self.repo, "rev-parse", "HEAD").strip(), [], fmlanes._git

        def spy(root, *args, **kw):
            if args[:2] == ("merge", "--no-ff"):
                seen.append(self.base())
            return real(root, *args, **kw)
        fmlanes._git = spy
        try:
            p = c.find_project(self.repo)
            fmlanes.merge(p, fmcli.need_brief(p, "T-0001"), self.repo, unverified="test")
        finally:
            fmlanes._git = real
        self.assertEqual(seen, [head], "on disk before git merge ran")
        self.assertEqual(self.base(), head)

    def test_a_failed_merge_leaves_no_stale_base(self):
        with open(os.path.join(self.repo, "shared.py"), "w") as f:
            f.write("x = 1\n")
        self.git(self.repo, "add", "shared.py")
        self.git(self.repo, "commit", "-qm", "base")
        self.lane("x = 2\n")
        before = self.base()
        with open(os.path.join(self.repo, "shared.py"), "w") as f:
            f.write("x = 3\n")
        self.git(self.repo, "commit", "-qam", "main change")
        r = self.fm("lane", "merge", "T-0001", "--unverified", "test", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.base(), before, "the pre-merge base is taken back with the aborted merge")

    def test_one_git_runner(self):
        import ast
        import fmcore as c
        lib = os.path.join(os.path.dirname(__file__), "..", "lib")
        defs = lambda m: {n.name for n in ast.walk(ast.parse(read_text(os.path.join(lib, m + ".py"))))
                          if isinstance(n, ast.FunctionDef)}
        for m in ("fmcore", "fmguard"):
            self.assertIn("_git", defs(m), m)
        for m in ("fmlanes", "fmsecrets", "fmmap", "fmbench"):
            self.assertNotIn("_git", defs(m), f"{m} runs git through fmcore._git")
        r = c._git(self.repo, "rev-parse", "--verify", "-q", "refs/heads/nope", proc=True)
        self.assertNotEqual(r.returncode, 0)
        r = c._git(os.path.join(self.tmp, "missing"), "status", proc=True)
        self.assertNotEqual(r.returncode, 0, "git that can't run is a failed process, not an exception")
        r = c._git(self.repo, "rev-parse", "HEAD", proc=True)
        self.assertEqual((r.returncode, len(r.stdout.strip())), (0, 40))


class SafeGitFailsClosed(unittest.TestCase):
    """T-0961 security review: when the filter-driver lookup fails, fmbench's git refuses instead of running unguarded."""

    def test_a_timed_out_config_lookup_refuses_the_command(self):
        import unittest.mock
        import fmbench
        real, calls = subprocess.run, []

        def run(cmd, *a, **k):  # the real runner, with git config timing out
            calls.append(cmd)
            if "config" in cmd:
                raise subprocess.TimeoutExpired(cmd, 1)
            return real(cmd, *a, **k)
        with unittest.mock.patch.object(subprocess, "run", side_effect=run):
            r = fmbench._safe_git("/nowhere", "checkout", "x")
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(any("checkout" in x for x in calls), calls)  # the guarded command never ran

    def test_the_runner_tells_a_timeout_from_a_no_match(self):
        import unittest.mock
        with unittest.mock.patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 1)):
            self.assertEqual(c._git("/x", "status", proc=True).returncode, 124)
        with unittest.mock.patch.object(subprocess, "run", side_effect=OSError("no git")):
            self.assertEqual(c._git("/x", "status", proc=True).returncode, 127)

    def test_a_secrets_audit_that_cant_list_files_says_so(self):
        import tempfile
        import unittest.mock
        import fmsecrets
        with tempfile.TemporaryDirectory() as t:
            subprocess.run(["git", "init", "-q", t], check=True)
            with unittest.mock.patch.object(fmsecrets.c, "_git", return_value=subprocess.CompletedProcess(
                    [], 124, "", "timed out")):
                found = fmsecrets._tree(t)
        self.assertTrue(found and "couldn't list" in found[0]["kind"], found)  # never a false "no credentials"
