# map-links: plugin/lib/sampo/cli.py plugin/lib/sampo/map.py
"""T-3306: a changed hub file (linked to over a quarter of the tests) selects tests by the symbols that changed, not by
the file: any cli.py edit used to run ~2,000 tests. When in doubt it keeps the test (a dropped test hides a regression)."""
import json
import os
import subprocess

from helpers import ForemanTestCase

from sampo import core as c

NAME = "orchestrator"
HUB = f"src/{NAME}.py"
CONVENTION = f"tests/test_{NAME}.py"
# the map links a test to a source whose stem ends with the test's (4+ letters): eight tests linked by name alone
R = [f"tests/test_{NAME[-k:]}.py" for k in range(4, 12)]
BODY = '''import os
LIMIT = 1


def deco(f):
    return f


def alpha():
    return 1


def beta():
    return 2


def gamma():
    return alpha()


def delta(x=LIMIT):
    return x


@deco
def eps():
    return 6


def where():
    return os.getcwd()


def cmd_run():
    return 4


def cmd_lz():
    return 5


def build(add, lazy):
    add("go", cmd_run)
    add("lz", lazy("m", "cmd_lz"))


class K:
    def meth(self):
        return 3
'''
USES = ["alpha()", "alpha()", "beta()", "beta()", "gamma()", "delta()", 'fm("go")', 'fm("lz")']


class AffectedSymbols(ForemanTestCase):
    def write(self, rel, body):
        os.makedirs(os.path.dirname(os.path.join(self.repo, rel)), exist_ok=True)
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(body)

    def commit(self, msg):
        for args in (["add", "-A"], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", msg]):
            subprocess.run(["git", "-C", self.repo, *args], check=True)

    def setUp(self):
        super().setUp()
        files = {HUB: BODY, "src/other.py": "N = 1\n", CONVENTION: "# convention\n", "tests/test_other.py": "N = 1\n"}
        files.update({t: use + "\n" for t, use in zip(R, USES)})
        for rel, body in files.items():
            self.write(rel, body)
        self.commit("seed")
        self.fm("init")
        self.fm("check", "affected", "echo {tests}")
        self.fm("task", "new", "note it", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        self.p = c.find_project(self.repo, create=False)

    def edit(self, old, new):
        path = os.path.join(self.repo, HUB)
        with open(path) as f:
            text = f.read()
        self.assertIn(old, text)
        with open(path, "w") as f:
            f.write(text.replace(old, new))

    def run_affected(self):
        from sampo import cli
        detail = {}
        _, tests, _ = cli.affected(self.p, detail=detail)
        return tests, detail

    def test_one_function_change_selects_the_tests_naming_it_and_the_convention_test(self):
        self.edit("return 2", "return 22")
        tests, detail = self.run_affected()
        self.assertEqual(["beta"], detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, R[2], R[3]]), tests)

    def test_a_function_pulls_in_the_functions_that_use_it(self):
        self.edit("return 1", "return 11")  # gamma() returns alpha()
        tests, detail = self.run_affected()
        self.assertEqual(["alpha", "gamma"], detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, R[0], R[1], R[4]]), tests)

    def test_a_constant_pulls_in_a_function_whose_default_reads_it(self):
        self.edit("LIMIT = 1", "LIMIT = 2")
        tests, detail = self.run_affected()
        self.assertEqual(["LIMIT", "delta"], detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, R[5]]), tests)

    def test_a_changed_default_names_its_function(self):
        self.edit("def delta(x=LIMIT)", "def delta(x=LIMIT + 1)")
        self.assertEqual(["delta"], self.run_affected()[1][HUB]["symbols"])

    def test_a_changed_decorator_line_names_the_decorated_function(self):
        self.edit("@deco\n", "@deco  # now\n")
        self.assertEqual(["eps"], self.run_affected()[1][HUB]["symbols"])

    def test_a_changed_import_pulls_in_the_functions_using_it(self):
        self.edit("import os\n", "import os, sys\n")
        self.assertEqual(["os", "sys", "where"], self.run_affected()[1][HUB]["symbols"])

    def test_a_star_import_falls_back_to_the_file(self):
        self.edit("import os\n", "import os\nfrom os.path import *\n")
        tests, detail = self.run_affected()
        self.assertIsNone(detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, *R]), tests)

    def test_a_deleted_function_selects_the_tests_naming_it(self):
        self.edit("def beta():\n    return 2\n", "")
        tests, detail = self.run_affected()
        self.assertEqual(["beta"], detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, R[2], R[3]]), tests)

    def test_a_renamed_function_names_both_names(self):
        self.edit("def beta():", "def beta2():")
        self.assertEqual(["beta", "beta2"], self.run_affected()[1][HUB]["symbols"])

    def test_a_handler_change_selects_the_tests_calling_its_verb(self):
        self.edit("return 4", "return 44")  # add("go", cmd_run)
        tests, detail = self.run_affected()
        self.assertEqual(["build", "cmd_run", "go", "run"], detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, R[6]]), tests)

    def test_a_lazy_handler_change_selects_the_tests_calling_its_verb(self):
        self.edit("return 5", "return 55")  # add("lz", lazy("m", "cmd_lz"))
        tests, detail = self.run_affected()
        self.assertEqual(["cmd_lz", "lz"],detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, R[7]]), tests)

    def test_a_test_with_a_map_links_line_is_always_kept(self):
        self.write("tests/test_declared.py", f"# map-links: {HUB}\npass\n")
        self.commit("declared")
        self.edit("return 2", "return 22")
        tests, _ = self.run_affected()
        self.assertEqual(sorted([CONVENTION, R[2], R[3], "tests/test_declared.py"]), tests)

    def test_a_method_change_names_the_method_and_its_class(self):
        self.edit("return 3", "return 33")
        self.assertEqual(["K", "meth"], self.run_affected()[1][HUB]["symbols"])

    def test_module_level_code_with_side_effects_falls_back_to_the_file(self):
        self.edit("LIMIT = 1\n", "LIMIT = 1\nprint('side effect')\n")
        tests, detail = self.run_affected()
        self.assertIsNone(detail[HUB]["symbols"])
        self.assertEqual(sorted([CONVENTION, *R]), tests)

    def test_a_syntax_error_falls_back_to_the_file(self):
        self.edit("return 1", "return (")
        self.assertIsNone(self.run_affected()[1][HUB]["symbols"])

    def test_a_file_few_tests_link_stays_file_level(self):
        self.write("src/other.py", "N = 2\n")
        tests, detail = self.run_affected()
        self.assertEqual({}, detail)
        self.assertEqual(["tests/test_other.py"], tests)

    def test_a_file_linked_to_a_few_heavy_test_files_is_a_hub_too(self):
        from sampo import cli
        heavy = "".join(f"    def test_{i}(self): pass\n" for i in range(cli.HUB_WEIGHT))
        self.write("tests/test_heavy.py", "# map-links: src/other.py\n" + heavy)
        self.commit("heavy")
        self.write("src/other.py", "N = 2\n")
        tests, detail = self.run_affected()
        self.assertEqual(["N"], detail["src/other.py"]["symbols"])
        self.assertEqual(["tests/test_other.py", "tests/test_heavy.py"], sorted(detail["src/other.py"]["tests"], reverse=True))

    def test_json_lists_per_hub_the_symbols_and_tests_chosen(self):
        self.edit("return 2", "return 22")
        out = json.loads(self.fm("check", "--affected", "--json").stdout)
        self.assertEqual({"mode": "symbols", "symbols": ["beta"], "tests": sorted([CONVENTION, R[2], R[3]])},
                         out["hubs"][HUB])
