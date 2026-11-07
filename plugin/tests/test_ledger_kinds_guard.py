"""T-3586: a ledger_tail(..., kinds=(...)) call must name every event kind its function then tests for; a missing one
silently drops those events (catch_rates lost its evidence and finish rows)."""
import ast
import glob
import os
import unittest

LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "sampo")


def _strs(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return {x.value for x in node.elts if isinstance(x, ast.Constant) and isinstance(x.value, str)}
    return set()


def _is_event(node):  # e.get("event") or e["event"]
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get"
            and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == "event") or (
        isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and node.slice.value == "event")


def problems(tree, name="?"):
    """Per kinds= call: the event literals tested in its enclosing loop or comprehension (else its function)."""
    out, up = [], {}
    for n in ast.walk(tree):
        for ch in ast.iter_child_nodes(n):
            up[ch] = n
    loops = (ast.For, ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)
    funcs = (ast.FunctionDef, ast.AsyncFunctionDef)
    for call in ast.walk(tree):
        if not (isinstance(call, ast.Call) and getattr(call.func, "attr", "") == "ledger_tail"):
            continue
        kinds = set().union(*[_strs(kw.value) for kw in call.keywords if kw.arg == "kinds"]) if call.keywords else set()
        if not kinds:
            continue
        scope = up.get(call)
        while scope is not None and not isinstance(scope, loops + funcs):
            scope = up.get(scope)
        used = set()
        for n in ast.walk(scope) if scope is not None else ():
            if isinstance(n, ast.Compare) and (_is_event(n.left) or any(_is_event(x) for x in n.comparators)):
                for x in [n.left] + n.comparators:
                    used |= _strs(x)
        if used - kinds:
            out.append(f"{name}:{call.lineno} tests {sorted(used - kinds)} but reads only {sorted(kinds)}")
    return out


class LedgerKindsGuard(unittest.TestCase):
    def test_every_event_a_function_tests_for_is_in_its_kinds(self):
        bad = []
        for path in sorted(glob.glob(os.path.join(LIB, "*.py"))):
            with open(path, encoding="utf-8") as f:
                bad += problems(ast.parse(f.read()), os.path.basename(path))
        self.assertEqual(bad, [])

    def test_catch_rates_counts_evidence_finish_and_prove_rows(self):
        import json
        import sys
        import tempfile
        import types
        sys.path.insert(0, os.path.join(LIB, ".."))
        from sampo import cli
        rows = [{"event": "evidence", "task": "T-1", "data": {"cmd": "a", "result": "exit 1"}},
                {"event": "evidence", "task": "T-1", "data": {"cmd": "a", "result": "exit 0"}},
                {"event": "finish", "task": "T-1", "data": {"ran": [["b", 0]]}},
                {"event": "prove", "task": "T-1", "data": {"cmd": "c", "red": True, "green": False}},
                {"event": "note", "task": "T-1"}]
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "ledger.jsonl"), "w") as f:
                f.write("".join(json.dumps(r) + "\n" for r in rows))
            rates, proven = cli.catch_rates(types.SimpleNamespace(dir=d, root=d))
        self.assertEqual(rates, {"a": (2, 1), "b": (1, 0), "c": (2, 1)})
        self.assertEqual(proven, {"T-1"})

    def test_the_guard_sees_the_catch_rates_mistake(self):
        src = ("def f(p):\n for e in c.ledger_tail(p, 5, kinds=('prove',)):\n"
               "  if e.get('event') == 'prove': pass\n  elif e.get('event') in ('evidence', 'finish'): pass\n")
        self.assertEqual(len(problems(ast.parse(src))), 1)


if __name__ == "__main__":
    unittest.main()
