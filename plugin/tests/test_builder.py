"""Builder lanes (T-0234): an S/M task worked by a foreman:fm-builder subagent in its own git worktree (Agent isolation
"worktree"); the main thread reviews, merges, re-verifies and closes. At most two builders at once."""
import json
import os
import re
import subprocess

from helpers import PLUGIN, ForemanTestCase, read_text


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, check=True).stdout.strip()


class _Tasks(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def task(self, title, tier="S"):
        extra = ["--interpretation", "x", "--approach", "x"] if tier != "S" else []
        return json.loads(self.fm("task", "new", title, "--type", "FEATURE", "--tier", tier, "--ac",
                                  f"{title} works :: python3 -c 'print(1)'", "--step", "build it", *extra,
                                  "--json").stdout)["id"]


class Agent(ForemanTestCase):
    def test_the_builder_agent_has_a_worktree_only_contract(self):
        text = read_text(os.path.join(PLUGIN, "agents", "fm-builder.md"))
        head = text.split("---")[1]
        tools = re.search(r"(?m)^tools:\s*(.+)$", head).group(1)
        for tool in ("Edit", "Write", "Bash", "Read"):
            self.assertIn(tool, tools)
        self.assertNotIn("Agent", tools)  # it never launches agents of its own
        for rule in ("fm focus", "worktree", "never push", "never merge", "fm task evidence", "git commit"):
            self.assertIn(rule, text.lower() if rule.islower() else text)


class Brief(_Tasks):
    def test_a_self_contained_brief_and_the_agent_call(self):
        tid = self.task("Parse dates")
        res = json.loads(self.fm("lane", "brief", tid, "--json").stdout)
        brief = read_text(res["path"])
        for part in ("Parse dates works", "python3 -c 'print(1)'", "build it", f"fm focus {tid}", "never push"):
            self.assertIn(part.lower(), brief.lower())
        self.assertIn('isolation: "worktree"', res["agent"])
        self.assertIn("foreman:fm-builder", res["agent"])
        self.assertIn("builder", self.fm("task", "show", tid).stdout)

    def test_the_brief_names_its_base_and_the_isolation_rule(self):
        # T-0379 (JARVIS 2026-10-09): Claude Code makes the worktree from the default branch, so a builder can start on
        # stale code; and its isolation refuses make/gradle/"too complex" commands, which builders retried again and again
        tid = self.task("Based")
        brief = read_text(json.loads(self.fm("lane", "brief", tid, "--json").stdout)["path"])
        head = git(self.repo, "rev-parse", "HEAD").strip()
        self.assertIn(head, brief)
        self.assertIn("merge --ff-only", brief)
        self.assertIn("isolated in the worktree", brief)
        self.assertIn("main thread", brief)

    def test_the_brief_says_edit_with_the_edit_tool(self):
        # T-0399 (JARVIS 2026-10-09): builders edited files with `python3 - <<'E' … s.replace(…)` and `cat > f <<EOF`;
        # Claude Code's isolation refused each as "too complex", five in ten minutes
        tid = self.task("Edits")
        brief = read_text(json.loads(self.fm("lane", "brief", tid, "--json").stdout)["path"])
        self.assertIn("Edit and Write tools", brief)
        self.assertIn("too complex", brief)

    def test_builder_model_follows_the_tier(self):
        # T-0373: "not everything needs to be opus if opus orchestrates": an S task's builder runs on Sonnet, an M
        # task's on the main model; the main thread still reviews, merges and re-verifies
        small, mid = self.task("Small one"), self.task("Mid one", tier="M")
        self.assertIn('model: "sonnet"', json.loads(self.fm("lane", "brief", small, "--json").stdout)["agent"])
        self.assertNotIn("model:", json.loads(self.fm("lane", "brief", mid, "--json").stdout)["agent"])

    def test_l_tasks_held_tasks_and_a_third_builder_are_refused(self):
        big = self.task("Rewrite the engine", tier="L")
        self.assertNotEqual(self.fm("lane", "brief", big, check=False).returncode, 0)
        busy = self.task("Busy")
        self.fm("focus", busy)
        self.assertNotEqual(self.fm("lane", "brief", busy, check=False).returncode, 0)  # the main thread has it
        one, two, three = self.task("One"), self.task("Two"), self.task("Three")
        self.fm("lane", "brief", one)
        self.fm("lane", "brief", two)
        p = self.fm("lane", "brief", three, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("two builders", p.stderr + p.stdout)
        self.fm("task", "drop", one, "not needed")  # a closed one frees its slot
        self.fm("lane", "brief", three)


class Flow(_Tasks):
    def test_focus_in_a_worktree_binds_and_main_takes_it_back_after_the_merge(self):
        tid = self.task("Add greet")
        self.fm("lane", "brief", tid)
        wt = os.path.join(self.tmp, "wt")
        git(self.repo, "worktree", "add", "-q", "-b", "builder/greet", wt)
        self.fm("focus", tid, cwd=wt)  # the builder's first command, in its own worktree
        self.assertEqual(self.meta(tid).get("lane"), os.path.realpath(wt))
        self.assertNotEqual(self.fm("focus", tid, check=False).returncode, 0)  # main sees it held by the worktree
        with open(os.path.join(wt, "greet.py"), "w") as f:
            f.write("def greet():\n    return 'hi'\n")
        git(wt, "add", "greet.py")
        git(wt, "commit", "-qm", f"greet ({tid})")
        git(self.repo, "merge", "-q", "--no-ff", "-m", "merge builder/greet", "builder/greet")
        self.fm("lane", "rm", tid)  # takes it back: the worktree goes, and its branch, now merged
        self.assertFalse(os.path.exists(wt))
        self.assertNotIn("builder/greet", git(self.repo, "branch", "--list", "builder/greet"))
        self.fm("focus", tid)  # back in the main checkout to re-verify and close
        self.assertIsNone(self.meta(tid).get("lane"))
        self.assertTrue(os.path.exists(os.path.join(self.repo, "greet.py")))

    def meta(self, tid):
        import fmcore as c
        return c.find_brief(c.find_project(self.repo), tid).meta


class Contract(_Tasks):
    """T-0234 review: the contract is enforced, not only written."""

    def lane(self, title):
        tid = self.task(title)
        self.fm("lane", "brief", tid)
        wt = os.path.join(self.tmp, "wt-" + tid)
        git(self.repo, "worktree", "add", "-q", "-b", f"builder/{tid}", wt)
        self.fm("focus", tid, cwd=wt)
        return tid, wt

    def test_a_builder_cant_close_its_task_or_hand_itself_back(self):
        tid, wt = self.lane("Close it")
        for args in (["task", "finish", tid, "--audit", "self: ok"], ["task", "done", tid],
                     ["task", "audit", tid, "intent", "x", "ok"], ["task", "drop", tid, "meh"], ["lane", "rm", tid]):
            p = self.fm(*args, cwd=wt, check=False)
            self.assertNotEqual(p.returncode, 0, args)

    def test_a_builder_writes_only_in_its_worktree(self):
        tid, wt = self.lane("Stay in")

        def verdict(tool, inp):
            out = self.hook("PreToolUse", {"tool_name": tool, "tool_input": inp, "cwd": wt}).stdout
            return "confine" if "blocked confine" in out else "ok"
        main_file = os.path.join(self.repo, "x.py")
        self.assertEqual(verdict("Write", {"file_path": main_file, "content": "x"}), "confine")
        self.assertEqual(verdict("Write", {"file_path": os.path.join(wt, "x.py"), "content": "x"}), "ok")
        self.assertEqual(verdict("Bash", {"command": f"echo x > {main_file}"}), "confine")
        said = self.hook("PreToolUse", {"tool_name": "Write", "tool_input": {"file_path": main_file, "content": "x"},
                                        "cwd": wt}).stdout
        self.assertIn("outside this builder's worktree", said)  # says why, and that no grant exists
        self.assertEqual(verdict("Bash", {"command": "echo x > /tmp/scratch.txt 2>/dev/null"}), "ok")
        main = self.hook("PreToolUse", {"tool_name": "Write", "tool_input": {"file_path": main_file, "content": "x"}})
        self.assertNotIn("blocked", main.stdout)  # the main thread isn't confined

    def test_lane_merge_and_cache_only_removal(self):
        # T-0377: on Foreman's own repo the guard refuses `git merge` (a tree write over core), so a reviewed branch
        # lands through fm, each file it changes judged as its task's write; and python caches don't hold a lane
        with open(os.path.join(self.repo, ".git", "info", "exclude"), "a") as f:
            f.write("__pycache__/\n")
        tid, wt = self.lane("Merge me")
        with open(os.path.join(wt, "new.py"), "w") as f:
            f.write("x = 1\n")
        git(wt, "add", "new.py")
        git(wt, "commit", "-qm", "builder work")
        os.makedirs(os.path.join(wt, "__pycache__"))
        open(os.path.join(wt, "__pycache__", "new.cpython-314.pyc"), "w").close()
        self.fm("lane", "merge", tid)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "new.py")))
        self.assertIn(f"Merge {tid}", git(self.repo, "log", "-1", "--format=%s"))
        self.fm("lane", "rm", tid)  # only caches were left: they go with the folder
        self.assertFalse(os.path.isdir(wt))
        sneaky, wt2 = self.lane("Sneaky")
        os.makedirs(os.path.join(wt2, "config"))
        with open(os.path.join(wt2, "config", "secrets.yaml"), "w") as f:
            f.write("k: v\n")
        git(wt2, "add", "config")
        git(wt2, "commit", "-qm", "writes a secret")
        p = self.fm("lane", "merge", sneaky, check=False)
        self.assertNotEqual(p.returncode, 0, "fm is no way around the guard")
        self.assertIn("credentials", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "config", "secrets.yaml")))

    def test_lane_merge_checks_both_sides_of_a_rename(self):
        # T-0382 (security review): git diff --name-only shows a rename by its new name only, so a lane that moves a
        # guarded file away (deleting it from main) must be judged by its old path too
        os.makedirs(os.path.join(self.repo, "config"))
        with open(os.path.join(self.repo, "config", "secrets.yaml"), "w") as f:
            f.write("k: v\n")
        git(self.repo, "add", "config")
        git(self.repo, "commit", "-qm", "a secret")
        tid, wt = self.lane("Mover")
        git(wt, "mv", "config/secrets.yaml", "notes.txt")
        git(wt, "commit", "-qm", "moves the secret")
        p = self.fm("lane", "merge", tid, check=False)
        self.assertNotEqual(p.returncode, 0, "a rename is a delete of the old path")
        self.assertIn("credentials", p.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "config", "secrets.yaml")))

    def test_lane_merge_over_unrelated_uncommitted_work(self):
        # T-0403 (JARVIS): the main thread was mid-T-0278 with uncommitted edits, so `fm lane merge T-0280` refused and
        # the lane couldn't land; git merges safely over edits the branch doesn't touch, with nothing staged
        with open(os.path.join(self.repo, "mine.txt"), "w") as f:
            f.write("committed\n")
        git(self.repo, "add", "mine.txt")
        git(self.repo, "commit", "-qm", "mine")
        tid, wt = self.lane("Lands beside my work")
        with open(os.path.join(wt, "theirs.py"), "w") as f:
            f.write("x = 1\n")
        git(wt, "add", "theirs.py")
        git(wt, "commit", "-qm", "builder work")
        with open(os.path.join(self.repo, "mine.txt"), "w") as f:
            f.write("in progress\n")  # the main thread's own uncommitted work
        self.fm("lane", "merge", tid)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "theirs.py")))
        with open(os.path.join(self.repo, "mine.txt")) as f:
            self.assertEqual(f.read(), "in progress\n", "uncommitted work survives the merge")
        self.fm("lane", "rm", tid)  # merged: its slot comes back (two builders at most)
        clash, wt2 = self.lane("Touches my file")
        with open(os.path.join(wt2, "mine.txt"), "w") as f:
            f.write("theirs\n")
        git(wt2, "commit", "-qam", "edits mine.txt")
        p = self.fm("lane", "merge", clash, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("mine.txt", p.stderr)
        git(self.repo, "add", "mine.txt")  # staged: a merge commit would record it
        other, wt3 = self.lane("Unrelated again")
        with open(os.path.join(wt3, "third.py"), "w") as f:
            f.write("y = 2\n")
        git(wt3, "add", "third.py")
        git(wt3, "commit", "-qm", "third")
        p = self.fm("lane", "merge", other, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("staged", p.stderr)

    def test_rm_deletes_only_the_lanes_own_branch(self):
        tid, wt = self.lane("Branches")
        git(self.repo, "branch", "release")  # merged into main
        git(wt, "switch", "-q", "release")  # the lane wandered off its branch
        self.fm("lane", "rm", tid)
        self.assertIn("release", git(self.repo, "branch", "--list", "release"))  # never one it switched to
        self.assertEqual(git(self.repo, "branch", "--list", f"builder/{tid}"), "")  # its own, merged, goes
        self.assertNotIn("builder", self.fm("task", "show", tid, "--json").stdout.split('"meta"', 1)[1].split("}", 1)[0])

    def test_a_briefed_task_that_never_launched_frees_its_slot(self):
        one, two, three = self.task("One"), self.task("Two"), self.task("Three")
        self.fm("lane", "brief", one)
        self.fm("lane", "brief", two)
        self.assertNotEqual(self.fm("lane", "brief", three, check=False).returncode, 0)
        self.fm("lane", "rm", one)
        self.fm("lane", "brief", three)
