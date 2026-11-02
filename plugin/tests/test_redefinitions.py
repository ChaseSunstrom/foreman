"""T-2553: a top-level name a module defines twice is a silent replacement: the later def wins, and the earlier one's
callers get it. Twice in one session a new helper was shadowed this way (_grounded in fmgenesis, _TID in fmrecall)."""
import ast
import glob
import os
import unittest

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")


def redefinitions(src):
    """[(line, name, first line)] for top-level defs, classes and plain assignments that replace an earlier one. A
    rebinding that reads the old value (DEFS = {k: … for k, v in DEFS.items()}) is deliberate and passes."""
    seen, out = {}, []
    for node in ast.parse(src).body:
        names = []
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names = [node.name]
        elif isinstance(node, ast.Assign):
            reads = {n.id for n in ast.walk(node.value) if isinstance(n, ast.Name)}
            names = [t.id for t in node.targets if isinstance(t, ast.Name) and t.id not in reads]
        for name in names:
            if name in seen:
                out.append((node.lineno, name, seen[name]))
            seen[name] = node.lineno
    return out


class Redefinitions(unittest.TestCase):
    def test_a_shadowed_helper_is_caught_and_an_in_place_rebinding_is_not(self):
        shadowed = "import re\n\ndef _grounded(a):\n    return a\n\n_TID = re.compile('x')\n\ndef _grounded(b):\n    return b\n"
        self.assertEqual(redefinitions(shadowed), [(8, "_grounded", 3)])
        self.assertEqual(redefinitions("A = 1\nA = 2\n"), [(2, "A", 1)])
        self.assertEqual(redefinitions("DEFS = {'py': ['x']}\nDEFS = {k: v for k, v in DEFS.items()}\n"), [])

    def test_no_plugin_lib_module_redefines_a_top_level_name(self):
        bad = []
        for path in sorted(glob.glob(os.path.join(LIB, "*.py"))):
            with open(path, encoding="utf-8") as f:
                bad += [f"{os.path.basename(path)}:{line} {name} (first at {first})"
                        for line, name, first in redefinitions(f.read())]
        self.assertEqual(bad, [], "a later definition silently replaces an earlier one: rename one of them")


if __name__ == "__main__":
    unittest.main()
