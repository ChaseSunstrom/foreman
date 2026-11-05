"""py-outline: a Python file's imports and definitions as facts."""
import ast

from cardkit import defs, emit, find, parse, read_input, signature, source

inp = read_input()["inputs"]
path, symbol = inp["path"], inp.get("symbol")
text = source(path)
tree = parse(text, path)
if symbol:
    find(tree, symbol, path)  # fails naming the nearest name


def doc(node):
    d = ast.get_docstring(node)
    return d.strip().splitlines()[0] if d and d.strip() else ""


symbols = []
for q, node, parent in defs(tree):
    if symbol and q != symbol and not q.startswith(symbol + "."):
        continue
    kind = "class" if isinstance(node, ast.ClassDef) else "method" if isinstance(parent, ast.ClassDef) else "function"
    symbols.append({"name": q, "kind": kind, "line": node.lineno, "end_line": node.end_lineno,
                    "signature": signature(node), "decorators": [ast.unparse(d) for d in node.decorator_list],
                    "doc": doc(node)})
imports = sorted(({"line": n.lineno, "text": ast.unparse(n)} for n in ast.walk(tree)
                  if isinstance(n, (ast.Import, ast.ImportFrom))), key=lambda x: x["line"])
emit({"path": path, "lines": len(text.splitlines()), "doc": doc(tree), "imports": [] if symbol else imports,
      "symbols": symbols})
