"""The suite itself (T-0218): a test class that redefines a TestCase method silently breaks it — a helper named fail()
made every assertion in its class pass, because assertions raise through self.fail."""
import ast
import glob
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
MEANT = {"setUp", "tearDown", "setUpClass", "tearDownClass", "run", "runTest"}  # overriding these is the design


class SuiteHygiene(unittest.TestCase):
    def test_no_test_class_shadows_a_testcase_method(self):
        inherited = {n for n in dir(unittest.TestCase) if not n.startswith("__")} - MEANT
        found = []
        for path in sorted(glob.glob(os.path.join(HERE, "**", "*.py"), recursive=True)):
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read(), path)
            for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
                found += [f"{os.path.relpath(path, HERE)}:{fn.lineno} {cls.name}.{fn.name}" for fn in cls.body
                          if isinstance(fn, ast.FunctionDef) and fn.name in inherited]
        self.assertEqual(found, [])
