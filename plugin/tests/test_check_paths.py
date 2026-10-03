"""T-0126: a gate can declare the paths it covers; fm check skips it when nothing under them changed since its last
pass (and says so), runs it when a covered file changed, and --fresh runs everything; a gate without paths always runs."""
import os
import unittest

from helpers import ForemanTestCase


class CheckPaths(ForemanTestCase):
    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def count(self, name):
        path = os.path.join(self.tmp, name)
        return open(path).read().count("x") if os.path.exists(path) else 0

    def test_a_gate_runs_only_when_its_paths_changed(self):
        self.fm("init")
        self.write("src/app.py", "a = 1\n")
        self.fm("check", "add", f"echo x >> {os.path.join(self.tmp, 'src-gate')}")
        self.fm("check", "add", f"echo x >> {os.path.join(self.tmp, 'all-gate')}")
        self.fm("check", "paths", "1", "src/**")
        self.assertIn("src/**", self.fm("check", "list").stdout)
        self.fm("check")
        self.assertEqual((self.count("src-gate"), self.count("all-gate")), (1, 1))
        self.write("docs/notes.md", "n\n")  # outside src/
        out = self.fm("check").stdout
        self.assertEqual((self.count("src-gate"), self.count("all-gate")), (1, 2))
        self.assertIn("skipped: nothing under src/** changed", out)
        self.write("src/app.py", "a = 2\n")
        self.fm("check")
        self.assertEqual(self.count("src-gate"), 2)
        self.write("docs/notes.md", "m\n")
        self.fm("check", "--fresh")
        self.assertEqual(self.count("src-gate"), 3)

    def test_a_rename_out_of_the_paths_runs_it_and_skips_keep_the_real_runs_time(self):
        import fmcore as c
        self.fm("init")
        self.write("src/app.py", "a = 1\n")
        self.fm("check", "add", f"echo x >> {os.path.join(self.tmp, 'src-gate')}")
        self.fm("check", "paths", "1", "src/**")
        self.fm("check")
        first = [e for e in c.ledger_tail(c.find_project(self.repo), 50) if e.get("event") == "check_run"][-1]["ts"]
        self.write("docs/a.md", "a\n")
        self.fm("check")  # skipped
        self.write("docs/a.md", "b\n")
        self.fm("check")  # skipped again: it still ages from the first, real run (review)
        last = [e for e in c.ledger_tail(c.find_project(self.repo), 50) if e.get("event") == "check_run"][-1]
        self.assertEqual(last["data"]["results"][0]["since"], first)
        os.makedirs(os.path.join(self.repo, "lib"))
        os.rename(os.path.join(self.repo, "src", "app.py"), os.path.join(self.repo, "lib", "app.py"))
        self.fm("check")
        self.assertEqual(self.count("src-gate"), 2, "a file moved out of src/ changed src/")

    def test_a_write_by_another_gate_under_its_paths_runs_it_next_time(self):
        self.fm("init")
        self.write("src/app.py", "a = 1\n")
        self.fm("check", "add", f"echo x >> {os.path.join(self.tmp, 'src-gate')}")
        self.fm("check", "add", "date +%N >> src/gen.py")  # a gate that writes (codegen)
        self.fm("check", "paths", "1", "src/**")
        self.fm("check")
        self.write("docs/a.md", "a\n")
        self.fm("check")  # gate 1 skipped; gate 2 rewrote src/gen.py after it
        self.write("docs/a.md", "b\n")
        self.fm("check")
        self.assertEqual(self.count("src-gate"), 2)


if __name__ == "__main__":
    unittest.main()
