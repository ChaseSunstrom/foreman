"""py-callers: every definition, call, import and other reference of one name across the worktree's Python files."""
import ast
import keyword

from cardkit import DEFS, emit, fail, read_input, source

LIMIT = 200  # sites per kind; past it the list is cut and truncated says so
inp = read_input()
name = inp["inputs"]["name"]
if keyword.iskeyword(name):
    fail(f"{name!r} is a Python keyword, not a name: give the function's, method's or class's name")
out = {"definitions": [], "calls": [], "imports": [], "references": []}
skipped, truncated = [], False


def add(kind, rel, line, scope, lines):
    global truncated
    if len(out[kind]) >= LIMIT:
        truncated = True
        return
    out[kind].append({"file": rel, "line": line, "in": ".".join(scope) or "<module>",
                      "code": lines[line - 1].strip()[:200]})


for rel in sorted(inp["files"]):
    text = source(rel)
    try:
        tree = ast.parse(text, filename=rel)
    except SyntaxError as e:
        skipped.append(f"{rel} line {e.lineno}: {e.msg}")
        continue
    lines = text.splitlines()
    called = set()

    def walk(node, scope):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, DEFS):
                if ch.name == name:
                    add("definitions", rel, ch.lineno, scope, lines)
                for d in ch.decorator_list:  # decorators run in the enclosing scope
                    walk_one(d, scope)
                for part in ch.body:
                    walk_one(part, scope + [ch.name])
                for part in (ch.bases + [k.value for k in ch.keywords]) if isinstance(ch, ast.ClassDef) else \
                        [ch.args] + ([ch.returns] if ch.returns else []):  # defaults and annotations
                    walk_one(part, scope)
                continue
            walk_one(ch, scope)

    def walk_one(ch, scope):
        if isinstance(ch, ast.Call):
            f = ch.func
            if (isinstance(f, ast.Name) and f.id == name) or (isinstance(f, ast.Attribute) and f.attr == name):
                called.add(id(f))
                add("calls", rel, f.end_lineno, scope, lines)  # the line holding the name, for a.b\n.name( too
        elif isinstance(ch, (ast.Import, ast.ImportFrom)):
            if any(name in (a.name.rsplit(".", 1)[-1], a.asname) for a in ch.names):
                add("imports", rel, ch.lineno, scope, lines)
        elif (isinstance(ch, ast.Name) and ch.id == name) or (isinstance(ch, ast.Attribute) and ch.attr == name):
            if id(ch) not in called:
                add("references", rel, ch.end_lineno, scope, lines)
        if isinstance(ch, DEFS):
            walk(ast.Module(body=[ch], type_ignores=[]), scope)
        else:
            walk(ch, scope)

    walk(tree, [])

counts = {k: len(v) for k, v in out.items()}
emit({"name": name, **out, "truncated": truncated, "skipped": skipped,
      "summary": f"{name}: {counts['definitions']} definition(s), {counts['calls']} call(s), {counts['imports']} "
                 f"import(s), {counts['references']} other reference(s)" + (", cut at 200 each" if truncated else "")
                 + (f"; {len(skipped)} file(s) don't parse" if skipped else "")})
