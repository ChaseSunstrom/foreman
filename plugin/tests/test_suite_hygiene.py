"""The suite itself (T-0218): a test class that redefines a TestCase method silently breaks it — a helper named fail()
made every assertion in its class pass, because assertions raise through self.fail."""
import ast
import builtins
import glob
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
MEANT = {"setUp", "tearDown", "setUpClass", "tearDownClass", "run", "runTest"}  # overriding these is the design


def unbound(src):
    """T-0698: "line name" for each name read that no builtin is and nothing in the module binds (stdlib ast, no
    pyflakes). Scopes aren't modelled, so it only misses a name also bound somewhere else; a star import skips it."""
    tree, bound = ast.parse(src), set(dir(builtins)) | {"__file__", "__builtins__"}
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and not isinstance(n.ctx, ast.Load):
            bound.add(n.id)
        for attr in ("name", "asname", "arg", "rest"):  # def, class, import, argument, except and match names
            if isinstance(getattr(n, attr, None), str):
                bound.add(getattr(n, attr).split(".")[0])
    return [] if "*" in bound else [f"{n.lineno} {n.id}" for n in ast.walk(tree) if isinstance(n, ast.Name)
                                    and isinstance(n.ctx, ast.Load) and n.id not in bound]


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


class UndefinedNames(unittest.TestCase):
    def test_every_name_read_is_bound(self):
        # T-0698: renames left _new_context_file, _UPDATE, _veto_note, _mask_substs and _IFS_USE read but bound
        # nowhere, each a NameError at run time (in the guard, a blocked call)
        self.assertEqual(unbound("import os\ndef f(a):\n    return os, a, len, _gone\n"), ["3 _gone"])
        plugin, found = os.path.dirname(HERE), []
        for path in sorted(glob.glob(f"{plugin}/lib/*.py") + glob.glob(f"{plugin}/hooks/*")):
            with open(path, encoding="utf-8") as f:
                src = f.read()
            if path.endswith(".py") or src.startswith("#!/usr/bin/env python3"):  # the hooks are extensionless
                found += [f"{os.path.relpath(path, plugin)}:{x}" for x in unbound(src)]
        self.assertEqual(found, [])
