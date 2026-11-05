"""py-none-guard: insert 'if PARAM is None: <mode>' as the function's first statement after its docstring."""
import ast
import difflib

from cardkit import body_start, eol, fail, find, indent_of, params, parse, read_input, save, source

inp = read_input()["inputs"]
path, qual, param = inp["path"], inp["function"], inp["param"]
mode, value = inp.get("mode", "return"), (inp.get("value") or "").strip()
text = source(path)
tree = parse(text, path)
fn = find(tree, qual, path, kinds=(ast.FunctionDef, ast.AsyncFunctionDef))
names = params(fn)
if param not in names:
    near = difflib.get_close_matches(param, names, n=1, cutoff=0.0)
    fail(f"{qual} has no parameter {param!r}" + (f": did you mean {near[0]!r}?" if near else " (it takes none)"))
if value:
    try:
        ast.parse(value, mode="eval")
    except SyntaxError as e:
        fail(f"value {value!r} isn't a Python expression: {e.msg}")
elif mode == "default":
    fail("mode 'default' needs value, the expression to use when it is None, e.g. [] or 0")
for st in ast.walk(fn):
    if isinstance(st, ast.If) and isinstance(st.test, ast.Compare) and isinstance(st.test.left, ast.Name) \
            and st.test.left.id == param and isinstance(st.test.ops[0], ast.Is) \
            and isinstance(st.test.comparators[0], ast.Constant) and st.test.comparators[0].value is None:
        fail(f"{qual} already checks 'if {param} is None' at line {st.lineno}")
lines, nl = text.splitlines(keepends=True), eol(text)
first = body_start(fn)
if first is None:  # only a docstring: the guard goes after it
    doc = fn.body[0]
    at, ind = doc.end_lineno, indent_of(lines[doc.lineno - 1])
else:
    at = min([first.lineno] + [d.lineno for d in getattr(first, "decorator_list", [])]) - 1
    ind = indent_of(lines[at])
if (first or fn.body[0]).lineno == fn.lineno or not ind:
    fail(f"{qual}'s body is on its def line: put it on its own lines first")
unit = ind[len(indent_of(lines[fn.lineno - 1])):] or "    "
do = {"return": f"return {value}" if value else "return None",
      "raise": "raise " + (value or 'ValueError("' + param + ' must not be None")'),
      "default": f"{param} = {value}"}[mode]
if at == len(lines) and lines and not lines[-1].endswith(("\n", "\r")):
    lines[-1] += nl
lines[at:at] = [f"{ind}if {param} is None:{nl}", f"{ind}{unit}{do}{nl}"]
save(path, "".join(lines))
