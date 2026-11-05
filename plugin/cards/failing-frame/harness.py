"""failing-frame's harness, run in a copy of the worktree (the cwd): run the tests one way and write the first failure
as JSON. argv: mode (pytest, unittest or script), target ('' for every test), the result file."""
import inspect
import json
import os
import runpy
import sys
import traceback
import unittest

mode, target, out = sys.argv[1:4]
name = target  # the test's id in the report: the path relative to the worktree
sys.path.insert(0, os.getcwd())  # as python -m pytest from the root would: tests/ can import the root's modules
if mode == "script":
    target = os.path.abspath(target)  # absolute, so its frames name a file the report can map back
    sys.path.insert(0, os.path.dirname(target))
state = {"ran": 0, "failure": None}


def record(exc, tb, test):
    if state["failure"] is not None or exc is None:
        return
    f = {"test": test, "exception": type(exc).__name__, "message": str(exc)[:2000],
         "frames": [[fr.filename, fr.lineno, fr.name, fr.line or ""] for fr in traceback.extract_tb(tb)]}
    if isinstance(exc, SyntaxError) and exc.filename:
        f["syntax"] = [exc.filename, exc.lineno or 0, (exc.text or "").strip()]
    state["failure"] = f


_add_error, _add_failure, _start = unittest.TestResult.addError, unittest.TestResult.addFailure, \
    unittest.TestResult.startTest


def add_error(self, test, err):
    record(err[1], err[2], test.id())
    return _add_error(self, test, err)


def add_failure(self, test, err):
    record(err[1], err[2], test.id())
    return _add_failure(self, test, err)


def start(self, test):
    state["ran"] += 1
    return _start(self, test)


unittest.TestResult.addError, unittest.TestResult.addFailure, unittest.TestResult.startTest = \
    add_error, add_failure, start  # a script that calls unittest.main() is traced too

try:
    if mode == "pytest":
        import pytest

        class Plugin:
            def pytest_exception_interact(self, node, call, report):
                record(call.excinfo.value, call.excinfo.tb, node.nodeid)

            def pytest_runtest_logreport(self, report):
                state["ran"] += report.when == "call"

        pytest.main(["-x", "-q", "-p", "no:cacheprovider"] + ([target] if target else []), plugins=[Plugin()])
    elif mode == "unittest":
        top = (os.path.dirname(target) or ".") if target else "."
        suite = unittest.TestLoader().discover(top, pattern=os.path.basename(target) or "test*.py", top_level_dir=top)
        unittest.TextTestRunner(stream=sys.stderr, failfast=True, verbosity=0).run(suite)
    else:
        with open(target, encoding="utf-8") as f:
            text = f.read()
        sys.argv = [target]
        try:
            g = runpy.run_path(target, run_name="__main__")
            state["ran"] += 1
            if "__main__" not in text:  # pytest-style test functions and no main block: call each, as pytest would
                for name, fn in list(g.items()):
                    if name.startswith("test") and inspect.isfunction(fn) and not any(
                            p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                            for p in inspect.signature(fn).parameters.values()):
                        state["ran"] += 1
                        fn()
        except SystemExit as e:
            if e.code not in (0, None):
                record(e, e.__traceback__, name)
        except BaseException as e:
            record(e, e.__traceback__, name)
finally:
    with open(out, "w") as f:
        json.dump(state, f)
