"""fm map / fm impact (T-0044): a small, current map of the project for grounding, rebuilt only when HEAD moves."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


class Map(ForemanTestCase):
    def setUp(self):
        super().setUp()
        files = {"src/parser.py": "def parse(): pass\n", "src/cli.py": "from src import parser\n",
                 "src/report.py": "x = 1\n", "tests/test_parser.py": "import src.parser\n",
                 "pyproject.toml": "[tool.pytest.ini_options]\n"}
        for rel, text in files.items():
            os.makedirs(os.path.join(self.repo, os.path.dirname(rel)), exist_ok=True)
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write(text)
        self.commit("add")
        for i in range(3):
            with open(os.path.join(self.repo, "src/parser.py"), "a") as f:
                f.write(f"# change {i}\n")
            self.commit(f"parser {i}")
        self.fm("init")

    def commit(self, msg):
        for args in (["add", "-A"], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", msg]):
            subprocess.run(["git", "-C", self.repo, *args], check=True, capture_output=True)

    def test_the_map_names_gates_layout_hot_files_and_test_links(self):
        out = self.fm("map").stdout
        for needle in ("pytest", "src/ (3", "src/parser.py", "tests/test_parser.py → src/parser.py"):
            self.assertIn(needle, out)
        self.assertLessEqual(len(out), 1600)

    def test_impact_lists_likely_tests_and_dependents(self):
        out = self.fm("impact", "src/parser.py").stdout
        self.assertIn("tests/test_parser.py", out)
        self.assertIn("src/cli.py", out)
        self.assertNotIn("src/report.py", out)

    def test_the_map_is_rebuilt_only_when_head_moves(self):
        self.fm("map")
        path = os.path.join(c.find_project(self.repo).dir, "map.json")
        built = json.load(open(path))["head"]
        mtime = os.path.getmtime(path)
        self.fm("map")
        self.assertEqual(os.path.getmtime(path), mtime)
        subprocess.run(["git", "-C", self.repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q",
                        "--allow-empty", "-m", "move"], check=True)
        self.fm("map")
        self.assertNotEqual(json.load(open(path))["head"], built)

    def test_focus_names_the_likely_tests_for_the_scope(self):
        tid = json.loads(self.fm("task", "new", "Speed up parse", "--type", "PERF", "--tier", "S", "--scope",
                                 "src/parser.py", "--ac", "faster", "--step", "do", "--json").stdout)["id"]
        self.assertIn("tests/test_parser.py", self.fm("focus", tid).stdout)

    def test_odd_bytes_and_names_dont_break_the_map_or_focus(self):
        # final review: a Latin-1 Makefile crashed fm map (and so fm focus); spaced names were split apart
        with open(os.path.join(self.repo, "Makefile"), "wb") as f:
            f.write(b"# Jos\xe9\ntest:\n\tpytest\n")
        with open(os.path.join(self.repo, "src", "my parser.py"), "w") as f:
            f.write("x = 1\n")
        self.commit("odd")
        self.assertIn("make test", self.fm("map").stdout)
        with open(os.path.join(self.repo, "src", "my parser.py"), "a") as f:
            f.write("y = 2\n")
        self.fm("check", "affected", "echo {tests}")
        res = json.loads(self.fm("check", "--affected", "--json").stdout)
        self.assertIn("src/my parser.py", res["changed"])
