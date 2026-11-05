"""T-3160: what Sampo's calling cards share. A card's gen.py and check.py read one JSON object on stdin ({inputs,
files, ...}; the checker also gets changed, created, orig and facts), run in the scratch copy (the cwd), and exit 1
with one precise line on stderr when the call can't be done: that line is what the model reads next."""
import ast
import difflib
import io
import json
import os
import sys
import tokenize


def read_input():
    return json.load(sys.stdin)


def fail(msg):
    sys.stderr.write(str(msg).rstrip() + "\n")
    sys.exit(1)


def emit(facts):
    sys.stdout.write(json.dumps(facts) + "\n")


def source(path):
    """A text file as written (its line endings kept)."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            return f.read()
    except UnicodeDecodeError:
        fail(f"{path} isn't UTF-8 text")
    except OSError as e:
        fail(f"{path} can't be read: {e.strerror}")


def save(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def eol(text):
    return "\r\n" if "\r\n" in text else "\n"


def parse(text, path, when="before the card"):
    try:
        return ast.parse(text, filename=path)
    except SyntaxError as e:
        fail(f"{path} line {e.lineno}: {e.msg} ({when})")


DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def defs(tree):
    """[(qualname, node, parent node or None)] for every class and function, nested ones dotted (Class.method), in
    source order; a name defined twice (a property's setter, an if/else pair) is listed twice."""
    out = []

    def walk(node, prefix, parent):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, DEFS):
                out.append((prefix + ch.name, ch, parent))
                walk(ch, prefix + ch.name + ".", ch)
            elif not isinstance(ch, ast.expr):
                walk(ch, prefix, parent)  # defs under if, try, with and loops keep their parent's prefix
    walk(tree, "", None)
    return out


def find(tree, qualname, path, kinds=DEFS):
    """The first def or class named qualname, or fail naming the nearest one."""
    found = {}
    for q, n, _ in defs(tree):
        if isinstance(n, kinds):
            found.setdefault(q, n)
    if qualname in found:
        return found[qualname]
    near = difflib.get_close_matches(qualname, list(found), n=1, cutoff=0.0)
    what = "function" if ast.ClassDef not in kinds else "function or class"
    fail(f"{path} has no {what} {qualname!r}" + (f": did you mean {near[0]!r}?" if near else f" (it has none)"))


def signature(node):
    if isinstance(node, ast.ClassDef):
        bases = [ast.unparse(b) for b in node.bases] + [ast.unparse(k) for k in node.keywords]
        return f"class {node.name}" + (f"({', '.join(bases)})" if bases else "")
    head = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    ret = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"{head} {node.name}({ast.unparse(node.args)}){ret}"


def params(node):
    a = node.args
    names = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs]
    return names + [x.arg for x in (a.vararg, a.kwarg) if x]


def body_start(node):
    """The index (0-based line) where node's first statement after its docstring starts, and that statement."""
    body = node.body
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    return body[0] if body else None


def indent_of(line):
    return line[:len(line) - len(line.lstrip(" \t"))]


def def_lines(text):
    """[(line, name)] of every def and class statement, found by tokens (not the ast), for checkers."""
    out, prev = [], None
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, SyntaxError) as e:
        fail(f"the file doesn't tokenize: {e}")
    for i, t in enumerate(toks):
        if t.type == tokenize.NAME and t.string in ("def", "class") and i + 1 < len(toks) \
                and toks[i + 1].type == tokenize.NAME:
            if prev is None or prev.type in (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT) \
                    or (prev.type == tokenize.NAME and prev.string == "async") \
                    or (prev.type == tokenize.OP and prev.string == ":"):
                out.append((t.start[0], toks[i + 1].string))
        if t.type not in (tokenize.COMMENT,):
            prev = t
    return out


def edits(old, new):
    """[(tag, old lines, new lines)] of what changed, line by line."""
    a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
    return [(tag, a[i1:i2], b[j1:j2]) for tag, i1, i2, j1, j2 in
            difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if tag != "equal"]


def orig(inp, rel):
    """The text rel had before the generator ran (the checker's view)."""
    return source(os.path.join(inp["orig"], rel))
