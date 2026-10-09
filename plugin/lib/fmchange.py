"""T-0713 (Frontier 13, first slice): intent and change skills.
fm spec: a one-line wish becomes a red, executable spec — one tool-less child proposes assertions about a module, only
safe ones are kept (comparisons over calls into that module and literals), written as a unittest file and run once.
fm rewrite: a mechanical rename as one rule — Python by tokens (strings and comments are left alone), other code by
whole word — with every leftover named (strings, comments, case and separator variants); --convert hands the leftover
lines to a cheap child and keeps only the lines that lose the old name."""
import ast
import fnmatch
import io
import os
import re
import shlex
import tokenize

import fmcore as c

SAFE_CALLS = {"len", "abs", "round", "sorted", "list", "dict", "set", "tuple", "str", "int", "float", "bool", "sum",
              "min", "max", "isinstance", "repr", "range"}
SAFE_NODES = (ast.Expression, ast.Compare, ast.Call, ast.Name, ast.Attribute, ast.Constant, ast.List, ast.Tuple,
              ast.Dict, ast.Set, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Subscript, ast.Slice, ast.keyword, ast.Load,
              ast.operator, ast.unaryop, ast.boolop, ast.cmpop, ast.IfExp)
SPEC_SYSTEM = ("You turn a one-line wish into concrete, executable examples. Output only lines of the form "
               "`assert <expression>`, one per line, nothing else.")
CONVERT_SYSTEM = ("You rewrite source lines for a rename. Return each numbered line as `N: <rewritten line>`, keeping "
                  "everything else on the line exactly as it was. Output nothing else.")


# ---------------------------------------------------------------- fm spec

def safe(line, module):
    """The assert line when it only compares calls into module and literals, else None."""
    if not line.startswith("assert "):
        return None
    try:
        tree = ast.parse(line[len("assert "):].split("  #")[0], mode="eval")
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if not isinstance(node, SAFE_NODES):
            return None
        if isinstance(node, ast.Name) and node.id not in SAFE_CALLS | {module, "True", "False", "None"}:
            return None
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            return None
    return "assert " + ast.unparse(tree.body)


def cmd_spec(args):
    import fmcli
    import fmideas
    p = fmcli.resolve(args)
    if not re.fullmatch(r"[A-Za-z_][\w.]*", args.module) or any(x.startswith("_") for x in args.module.split(".")):
        raise fmcli.UsageError("--module takes an importable module name, e.g. calc or app.billing")
    prompt = (f"Wish: {args.wish}\nModule under test: `{args.module}` (already imported as `{args.module}`).\n"
              f"Write 3 to 8 assertions with concrete inputs and expected outputs that will hold once the wish is done. "
              f"Call only functions of `{args.module}` and literals.")
    try:
        text = fmideas.run_child("spec", SPEC_SYSTEM, prompt, args.model, args.timeout, project=p.slug)
    except ValueError as e:
        raise fmcli.UsageError(str(e))
    lines = [x.strip().strip("`") for x in text.splitlines() if x.strip()]
    kept = [s for x in lines if (s := safe(x, args.module.split(".")[0]))]
    dropped = len([x for x in lines if x.startswith(("assert", "import", "from"))]) - len(kept)
    if not kept:
        raise fmcli.UsageError(f"no safe assertion came back ({c.fit(c.plain(text), 160)})")
    slug = re.sub(r"[^a-z0-9]+", "_", args.wish.lower()).strip("_")[:40] or "wish"
    out = args.out or os.path.join("tests" if os.path.isdir(os.path.join(p.root, "tests")) else "", f"test_spec_{slug}.py")
    body = (f"\"\"\"Spec from the wish: {c.plain(args.wish)[:200]} (fm spec; red until it's done).\"\"\"\n"
            f"import unittest\n\nimport {args.module}\n\n\nclass Spec(unittest.TestCase):\n"
            + "".join(f"    def test_{i}(self):\n        {s}\n\n" for i, s in enumerate(kept, 1))
            + "\nif __name__ == \"__main__\":\n    unittest.main()\n")
    path = os.path.join(p.root, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c.write_atomic(path, body)
    code, output = c.run_command(p.root, f"PYTHONPATH=. python3 {shlex.quote(out)}", 120)
    state = (f"red ({c.run_result(code, output)}): it fails until the wish is done" if code else
             "already green: the wish may be done already, or the examples don't test it")
    return fmcli.out(args, {"path": out, "assertions": kept, "dropped": dropped, "red": bool(code)},
                     f"{out}: {len(kept)} assertion(s) kept" + (f", {dropped} dropped as unsafe" if dropped else "")
                     + f"; {state}\n" + "\n".join(f"  {s}" for s in kept))


# ---------------------------------------------------------------- fm rewrite

def _words(name):
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", name)]


def variants(name):
    """The spellings of the same words: snake, Pascal, camel, SCREAMING and kebab."""
    w = _words(name)
    if not w:
        return {name}
    return {name, "_".join(w), "".join(x.title() for x in w), w[0] + "".join(x.title() for x in w[1:]),
            "_".join(w).upper(), "-".join(w)}


def _spell_like(old_variant, old, new):
    """new spelled the way old_variant spells old."""
    for f in (lambda w: "_".join(w), lambda w: "".join(x.title() for x in w), lambda w: w[0] + "".join(
            x.title() for x in w[1:]), lambda w: "_".join(w).upper(), lambda w: "-".join(w)):
        if f(_words(old)) == old_variant:
            return f(_words(new))
    return new


def _py_rename(text, old, new):
    """(text with NAME tokens old → new, count); strings and comments untouched."""
    try:
        toks = [t for t in tokenize.generate_tokens(io.StringIO(text).readline)
                if t.type == tokenize.NAME and t.string == old]
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return text, 0
    lines = text.splitlines(keepends=True)
    for t in sorted(toks, key=lambda t: t.start, reverse=True):
        r, col = t.start
        lines[r - 1] = lines[r - 1][:col] + new + lines[r - 1][col + len(old):]
    return "".join(lines), len(toks)


def _files(p, glob):
    names = c._git(p.root, "ls-files", "-co", "--exclude-standard", timeout=60).splitlines()
    return [f for f in names if (not glob or fnmatch.fnmatch(f, glob)) and os.path.isfile(os.path.join(p.root, f))
            and not f.startswith((".foreman/", ".git/"))]


def _residual_re(old):
    return re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(sorted(map(re.escape, variants(old)), key=len, reverse=True))
                      + r")(?![A-Za-z0-9_])")


def rewrite(p, old, new, glob=None):
    """{file: new text} for the files the rule changes, the number of code sites, and the residual sites
    [(file, line number, line)] in the result."""
    changed, sites, residual = {}, 0, []
    rx = _residual_re(old)
    for f in _files(p, glob):
        try:
            with open(os.path.join(p.root, f), encoding="utf-8") as fh:
                text = fh.read(2_000_000)
        except (OSError, UnicodeDecodeError):
            continue
        if not rx.search(text):
            continue
        if f.endswith(".py"):
            out, n = _py_rename(text, old, new)
        elif c.CODE.search(f):
            out, n = re.subn(rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])", new, text)
        else:
            out, n = text, 0
        if n:
            changed[f], sites = out, sites + n
        residual += [(f, i, ln) for i, ln in enumerate(out.splitlines(), 1) if rx.search(ln)]
    return changed, sites, residual


def convert(p, old, new, residual, model, timeout):
    """Residual lines rewritten by a cheap child; only lines that lose every spelling of old are kept: {file: text}."""
    import fmideas
    rx = _residual_re(old)
    pairs = ", ".join(f"{v} → {_spell_like(v, old, new)}" for v in sorted(variants(old)))
    prompt = (f"RESIDUAL lines left by renaming {old} to {new} (spellings: {pairs}). Rewrite each so it uses the new "
              f"name wherever it means the old one.\n" + "\n".join(f"{i}: {ln}" for i, (_, _, ln) in
                                                                  enumerate(residual[:200], 1)))
    text = fmideas.run_child("rewrite", CONVERT_SYSTEM, prompt, model, timeout, project=p.slug)
    fixes = {int(m.group(1)): m.group(2) for m in re.finditer(r"(?m)^(\d+): (.*)$", text)}
    files = {}
    for i, (f, n, ln) in enumerate(residual[:200], 1):
        line = fixes.get(i)
        if line is None or rx.search(line) or line == ln:
            continue
        if f not in files:
            with open(os.path.join(p.root, f), encoding="utf-8") as fh:
                files[f] = fh.read().splitlines(keepends=True)
        end = files[f][n - 1][len(files[f][n - 1].rstrip("\r\n")):]
        files[f][n - 1] = line + end
    return {f: "".join(ls) for f, ls in files.items()}


def cmd_rewrite(args):
    import fmcli
    p = fmcli.resolve(args)
    if not re.fullmatch(r"[A-Za-z_]\w*", args.old) or not re.fullmatch(r"[A-Za-z_]\w*", args.new):
        raise fmcli.UsageError("fm rewrite takes identifiers: fm rewrite OLD NEW [--glob G] [--apply] [--convert]")
    changed, sites, residual = rewrite(p, args.old, args.new, args.glob)
    if args.apply:
        for f, text in changed.items():
            c.write_atomic(os.path.join(p.root, f), text)
        if args.convert and residual:
            try:
                fixed = convert(p, args.old, args.new, residual, args.model, args.timeout)
            except ValueError as e:
                raise fmcli.UsageError(f"the converter didn't run: {e}")
            for f, text in fixed.items():
                c.write_atomic(os.path.join(p.root, f), text)
            _, _, residual = rewrite(p, args.old, args.new, args.glob)
    text = (f"{args.old} → {args.new}: {sites} code site(s) in {len(changed)} file(s)"
            + ("" if args.apply else " (dry run: --apply writes them)")
            + f"; {len(residual)} residual site(s) the rule leaves (strings, comments, other spellings)"
            + (": --convert hands them to a cheap child" if residual and not args.convert else "")
            + "".join(f"\n  {f}:{n}: {c.fit(ln.strip(), 120)}" for f, n, ln in residual[:20])
            + (f"\n  … {len(residual) - 20} more" if len(residual) > 20 else ""))
    return fmcli.out(args, {"sites": sites, "files": sorted(changed), "applied": bool(args.apply),
                            "residual": [{"file": f, "line": n, "text": ln} for f, n, ln in residual]}, text)
