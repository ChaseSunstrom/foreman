"""T-0134: a linked git worktree is a lane of its project: it shares the project's state, keeps its own active task
(focus there pauses only that lane's), does its git work in its own files, and neither side's next or queue offers a
task the other holds. fm lane new|list|rm manage them; rm never discards uncommitted work."""
import json
import os
import subprocess
import unittest

from helpers import ForemanTestCase

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


if __name__ == "__main__":
    unittest.main()
