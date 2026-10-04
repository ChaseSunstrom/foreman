"""Handoff (T-0263): a reading order for a task's diff (T-0248), the proof in fm pr (T-0249) and AGENTS.md for other
harnesses (T-0246)."""
import json
import os

from helpers import ForemanTestCase


class _Task(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = json.loads(self.fm("task", "new", "Cache the session token", "--type", "FEATURE", "--tier", "S",
                                      "--ac", "it caches :: test -f flag", "--step", "write the cache",
                                      "--step", "use it", "--json").stdout)["id"]
        self.fm("focus", self.tid)

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)


class Tour(_Task):
    def test_imported_files_come_first_with_sizes(self):
        self.write("session.py", "from tokencache import get\n\ndef login():\n    return get()\n")
        self.write("tokencache.py", "CACHE = {}\n\ndef get():\n    return CACHE\n")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true")
        rows = json.loads(self.fm("tour", self.tid, "--json").stdout)["files"]
        self.assertEqual([r["path"] for r in rows], ["tokencache.py", "session.py"])
        self.assertEqual((rows[0]["add"], rows[0]["del"]), (4, 0))
        self.assertEqual(rows[1]["uses"], ["tokencache.py"])
        out = self.fm("tour", self.tid).stdout
        self.assertLess(out.index("tokencache.py"), out.index("session.py"))
        self.assertIn("+4", out)

    def test_a_rename_is_a_delete_and_an_add(self):
        self.write("tokencache.py", "CACHE = {}\n")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "git add -A && git commit -qm base")
        self.fm("task", "drop", self.tid, "restart from the commit")
        tid = json.loads(self.fm("task", "new", "Rename it", "--type", "CLEAN", "--tier", "S", "--ac", "x :: true",
                                 "--step", "x", "--json").stdout)["id"]
        self.fm("focus", tid)
        os.rename(os.path.join(self.repo, "tokencache.py"), os.path.join(self.repo, "token_store.py"))
        rows = {r["path"]: r for r in json.loads(self.fm("tour", tid, "--json").stdout)["files"]}
        self.assertEqual(set(rows), {"tokencache.py", "token_store.py"})
        self.assertTrue(rows["tokencache.py"]["deleted"])
        self.assertFalse(rows["token_store.py"]["deleted"])

    def test_nothing_changed(self):
        self.assertIn("no changes", self.fm("tour", self.tid).stdout)


class Proof(_Task):
    def test_pr_carries_red_green_lenses_assumptions_and_bench(self):
        self.fm("task", "assume", self.tid, "add", "the cache is per process")
        self.fm("task", "assume", self.tid, "verify", "1", "--evidence", "read session.py:1")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "test -f flag", check=False)
        self.write("flag", "")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "test -f flag")
        self.fm("task", "evidence", self.tid, "--step", "2", "--run", "true")
        self.fm("task", "finish", self.tid, "--audit", "self checklist", "--result", "no findings: cache keyed by user")
        import fmcore as c
        p = c.find_project(self.repo)
        os.makedirs(os.path.join(p.dir, "bench", "results"))
        with open(os.path.join(p.dir, "bench", "results", "night.json"), "w") as f:
            json.dump({"cases": [{"id": self.tid, "pass": True, "turns": 7, "cost_usd": 0.21}]}, f)
        with open(os.path.join(p.dir, "bench", "results", "broken.json"), "w") as f:
            json.dump({"cases": 5}, f)  # a hand-edited file never crashes fm pr
        out = self.fm("pr", self.tid).stdout
        self.assertIn("red→green: `test -f flag`", out)
        self.assertIn("self: no findings: cache keyed by user", out)
        self.assertIn("[verified: read session.py:1] the cache is per process", out)
        self.assertIn("bench: ✓ replayed in night (7 turns, $0.21)", out)


class Export(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("decide", "use sqlite for the cache", "--why", "one file, no server")
        self.path = os.path.join(self.repo, "AGENTS.md")

    def test_writes_the_sections_under_the_cap(self):
        self.fm("export", "agents")
        with open(self.path) as f:
            text = f.read()
        for head in ("## How work is done here", "## Project map", "## Decisions", "## Playbooks"):
            self.assertIn(head, text)
        self.assertIn("use sqlite for the cache", text)
        self.assertLessEqual(len(text.encode()), 32 * 1024)
        self.fm("export", "agents")  # its own file: rewritten

    def test_corrections_go_in_unless_the_project_is_sensitive(self):
        import fmcore as c
        p = c.find_project(self.repo)
        with c.lock(p.dir):
            c.log_event(p, "correction", data={"text": "never push without asking"})
        self.fm("export", "agents")
        with open(self.path) as f:
            text = f.read()
        self.assertIn("never push without asking", text)
        self.assertNotIn(c.PLUGIN_ROOT, text)  # playbooks by plugin-relative path, no home directory
        self.fm("sensitive", "on")
        self.fm("export", "agents")
        with open(self.path) as f:
            text = f.read()
        self.assertNotIn("never push without asking", text)
        self.assertNotIn("use sqlite for the cache", text)

    def test_a_symlink_is_refused(self):
        target = os.path.join(self.repo, "CLAUDE.md")
        with open(target, "w") as f:
            f.write("# notes\n")
        os.symlink(target, self.path)
        self.assertNotEqual(self.fm("export", "agents", check=False).returncode, 0)
        with open(target) as f:
            self.assertEqual(f.read(), "# notes\n")

    def test_a_hand_written_file_is_kept_without_force(self):
        with open(self.path, "w") as f:
            f.write("# our own agent notes\n")
        p = self.fm("export", "agents", check=False)
        self.assertNotEqual(p.returncode, 0)
        with open(self.path) as f:
            self.assertEqual(f.read(), "# our own agent notes\n")
        self.fm("export", "agents", "--force")
        with open(self.path) as f:
            self.assertIn("## Project map", f.read())
