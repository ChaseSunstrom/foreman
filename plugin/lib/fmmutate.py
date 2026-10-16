"""T-1066: mutation-test the guard. One mutant per rule site in fmguard.py (a statement that records a block: a
`cats.append("core")`, a `found.append(("pipe-shell", ...))`, a `return Block("plugin", ...)`), made by ast. Drop mode
replaces the statement with `pass`; weaken mode negates the innermost `if` test guarding it. Each mutant runs the
guard's own tests in a throwaway copy; one the tests still pass on is a rule no test catches."""
import ast
import os
import shutil
import subprocess
import sys
import tempfile


def _cat(node, cats):
    """The category a statement records, or None: x.append("cat"), x.append(("cat", ...)), return "cat" / Block("cat", ...)."""
    def lit(n):
        return n.value if isinstance(n, ast.Constant) and n.value in cats else None
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) \
            and node.value.func.attr == "append" and len(node.value.args) == 1:
        a = node.value.args[0]
        return lit(a.elts[0]) if isinstance(a, ast.Tuple) and a.elts else lit(a)
    if isinstance(node, ast.Return) and node.value is not None:
        v = node.value
        if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "Block" and v.args:
            return lit(v.args[0])
        return lit(v)
    return None


def mutants(src, cats, weaken=False):
    """[{line, category, stmt, src}]: each rule site once, the mutated source ready to write."""
    tree = ast.parse(src)
    parents = {}
    for p in ast.walk(tree):
        for ch in ast.iter_child_nodes(p):
            parents[ch] = p
    sites = [(n, _cat(n, cats)) for n in ast.walk(tree) if isinstance(n, (ast.Expr, ast.Return))]
    out = []
    for node, cat in sorted((s for s in sites if s[1]), key=lambda s: s[0].lineno):
        stmt = " ".join((ast.get_source_segment(src, node) or "").split())
        if weaken:
            p = parents.get(node)
            while p is not None and not (isinstance(p, ast.If) and any(node is x or _within(x, node) for x in p.body)):
                p = parents.get(p)
            if p is None:
                continue  # no guarding if: nothing to weaken
            old, p.test = p.test, ast.copy_location(ast.UnaryOp(ast.Not(), p.test), p.test)
            out.append({"line": node.lineno, "category": cat, "stmt": stmt, "src": ast.unparse(tree)})
            p.test = old
        else:
            body = getattr(parents[node], _field(parents[node], node))
            idx = body.index(node)
            body[idx] = ast.copy_location(ast.Pass(), node)
            out.append({"line": node.lineno, "category": cat, "stmt": stmt, "src": ast.unparse(tree)})
            body[idx] = node
    return out


def _within(top, node):
    return any(n is node for n in ast.walk(top))


def _field(parent, node):
    return next(f for f, v in ast.iter_fields(parent) if isinstance(v, list) and any(x is node for x in v))


def sample(items, n):
    """n items spread evenly across the list."""
    if n <= 0 or len(items) <= n:
        return items
    return [items[i * len(items) // n] for i in range(n)]


def run(module, rel, tree_root, dest, cmd, cats, weaken=False, only=None, limit=40, timeout=300, log=None):
    """Mutate module (a path); copy tree_root to dest in a temp dir, write each mutant at rel there and run cmd (a list,
    cwd = the copy's root). Returns {killed, survived: [mutant], timed_out, total}. The real tree is never written.
    ponytail: one full run of the tests per mutant (the guard's suite is the cost, tens of seconds each): --max caps it;
    run only the tests that import the line if that is ever too slow."""
    with open(module, encoding="utf-8") as f:
        ms = mutants(f.read(), cats, weaken)
    if only:
        ms = [m for m in ms if m["category"] == only]
    total, ms = len(ms), sample(ms, limit)
    killed, survived = 0, []
    with tempfile.TemporaryDirectory(prefix="fm-mutate-") as tmp:
        shutil.copytree(tree_root, os.path.join(tmp, dest), ignore=shutil.ignore_patterns("__pycache__"))
        target = os.path.join(tmp, rel)
        base = ast.unparse(ast.parse(open(module, encoding="utf-8").read()))  # the mutants are unparsed too
        with open(target, "w", encoding="utf-8") as f:
            f.write(base)
        if ms and subprocess.run(cmd, cwd=tmp, capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout).returncode:
            raise ValueError("the tests fail on the unmutated module in the copy: every mutant would count as killed")
        for m in ms:
            with open(target, "w", encoding="utf-8") as f:
                f.write(m["src"])
            try:
                ok = subprocess.run(cmd, cwd=tmp, capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout).returncode == 0
            except subprocess.TimeoutExpired:
                ok = False  # a mutant that hangs the tests is noticed
            if ok:
                survived.append({k: m[k] for k in ("line", "category", "stmt")})
            else:
                killed += 1
            if log:
                log(m, not ok)
    return {"total": total, "tried": len(ms), "killed": killed, "survived": survived}
