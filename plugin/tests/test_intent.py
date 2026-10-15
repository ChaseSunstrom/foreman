"""T-0713 (Frontier 13, first slice): a one-line wish becomes a red, executable spec; a mechanical change is one rule
with its leftovers named and converted."""
import os

from helpers import ForemanTestCase

STUB = r'''#!/usr/bin/env python3
import os, sys
prompt = sys.stdin.read()
if "RESIDUAL" in prompt:  # the converter: each numbered line back with the new name
    for line in prompt.splitlines():
        if line[:1].isdigit() and ": " in line:
            n, text = line.split(": ", 1)
            print(f"{n}: " + text.replace("old_total", "new_total").replace("OldTotal", "NewTotal"))
else:
    print("assert calc.mul(2, 3) == 6")
    print("assert calc.mul(0, 5) == 0")
    print("assert __import__('os').system('touch /tmp/pwned') == 0")
    print("import os")
'''


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"]}
        self.fm("init")

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path) or self.repo, exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def read(self, rel):
        with open(os.path.join(self.repo, rel)) as f:
            return f.read()


class Spec(Base):
    def test_a_wish_becomes_a_red_spec_with_only_safe_assertions(self):
        self.write("calc.py", "def add(a, b):\n    return a + b\n")
        r = self.fm("spec", "multiply two numbers", "--module", "calc", "--out", "test_mul_spec.py", env=self.env)
        text = self.read("test_mul_spec.py")
        self.assertIn("calc.mul(2, 3) == 6", text)
        self.assertNotIn("__import__", text)
        self.assertNotIn("import os", text)
        self.assertIn("red", r.stdout)
        self.assertIn("2 assertion", r.stdout)

    def test_the_users_own_examples_come_first_and_survive_a_failed_child(self):
        # T-0897: the wish already says what it means; those examples are the spec's first lines, verbatim
        self.write("calc.py", "def add(a, b):\n    return a + b\n")
        wish = 'multiply: mul(2, 3) -> 6, and mul(-1, 4) should return -4; also calc.mul(0, 9) == 0'
        self.fm("spec", wish, "--module", "calc", "--out", "test_ex.py", env=self.env)
        text = self.read("test_ex.py")
        first = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("assert")][:3]
        self.assertEqual(first, ["assert calc.mul(2, 3) == 6", "assert calc.mul(-1, 4) == -4",
                                 "assert calc.mul(0, 9) == 0"])
        self.assertEqual(text.count("calc.mul(2, 3) == 6"), 1, "the child's copy of the same example isn't repeated")
        broken = os.path.join(self.tmp, "broken")
        os.makedirs(broken)
        with open(os.path.join(broken, "claude"), "w") as f:
            f.write("#!/bin/sh\nexit 1\n")
        os.chmod(os.path.join(broken, "claude"), 0o755)
        r = self.fm("spec", wish, "--module", "calc", "--out", "test_ex2.py",
                    env={"PATH": broken + os.pathsep + os.environ["PATH"]})
        self.assertIn("3 assertion", r.stdout)  # the child failed: the user's examples are enough


class Rewrite(Base):
    def setUp(self):
        super().setUp()
        self.write("lib/money.py", "def old_total(xs):\n    return sum(xs)\n\n\nclass OldTotal:\n    pass\n")
        self.write("app.py", "from lib.money import old_total\n\n# old_total adds them up\n"
                             "print(old_total([1, 2]), 'old_total')\n")
        self.write("web/main.js", "const t = old_total(1);\n")

    def test_one_rule_renames_code_and_names_the_leftovers(self):
        dry = self.fm("rewrite", "old_total", "new_total").stdout
        self.assertIn("old_total(xs)", self.read("lib/money.py"), "a dry run changes nothing")
        self.assertIn("4 code site", dry)
        out = self.fm("rewrite", "old_total", "new_total", "--apply").stdout
        self.assertIn("def new_total(xs)", self.read("lib/money.py"))
        self.assertIn("from lib.money import new_total", self.read("app.py"))
        self.assertIn("new_total(1)", self.read("web/main.js"))
        self.assertIn("# old_total adds them up", self.read("app.py"), "a comment is a residual, not code")
        self.assertIn("residual", out)
        self.assertIn("OldTotal", out, "a case variant is named")

    def test_the_converter_clears_the_residuals(self):
        self.fm("rewrite", "old_total", "new_total", "--apply")
        out = self.fm("rewrite", "old_total", "new_total", "--apply", "--convert", env=self.env).stdout
        self.assertIn("0 residual", out)
        self.assertNotIn("old_total", self.read("app.py"))
        self.assertIn("class NewTotal", self.read("lib/money.py"))
