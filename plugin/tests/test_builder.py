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
