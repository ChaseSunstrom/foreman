"""py-none-guard's checker: the file still parses, the only change is two inserted lines, and they are the function's
first statement after its docstring: 'if PARAM is None:' doing exactly the asked mode."""
import ast

from cardkit import body_start, edits, fail, find, orig, params, parse, read_input, source

inp = read_input()
args = inp["inputs"]
path, qual, param = args["path"], args["function"], args["param"]
mode, value = args.get("mode", "return"), (args.get("value") or "").strip()
if inp["changed"] != [path] or inp["created"]:
    fail(f"the card changed {inp['changed'] + inp['created']}, not just {path}")
old, new = orig(inp, path), source(path)
tree = parse(new, path, "after the card")
ops = edits(old, new)
if len(ops) != 1 or ops[0][0] != "insert" or len(ops[0][2]) != 2:
    fail(f"{path} should gain exactly two lines, but changed: " +
         "; ".join(f"{t} {len(a)} line(s) -> {len(b)} line(s)" for t, a, b in ops)[:300])
fn = find(tree, qual, path, kinds=(ast.FunctionDef, ast.AsyncFunctionDef))
if param not in params(fn):
    fail(f"{qual} has no parameter {param!r}")
st = body_start(fn)
t = getattr(st, "test", None)
if not (isinstance(st, ast.If) and isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id == param
        and len(t.ops) == 1 and isinstance(t.ops[0], ast.Is) and isinstance(t.comparators[0], ast.Constant)
        and t.comparators[0].value is None):
    fail(f"{qual}'s first statement {('at line ' + str(st.lineno)) if st else ''} isn't 'if {param} is None:' "
         f"(it is {ast.unparse(st).splitlines()[0][:80] if st else 'missing'!r})")
if st.orelse or len(st.body) != 1:
    fail(f"the guard at line {st.lineno} should hold one statement and no else")
do = st.body[0]
want = ast.dump(ast.parse(value, mode="eval").body) if value else None
kind = {"return": ast.Return, "raise": ast.Raise, "default": ast.Assign}[mode]
if not isinstance(do, kind):
    fail(f"the guard at line {st.lineno} does {type(do).__name__.lower()}, not {mode}")
got = {"return": lambda: do.value, "raise": lambda: do.exc, "default": lambda: do.value}[mode]()
if mode == "default" and [ast.dump(x) for x in do.targets] != [ast.dump(ast.Name(param, ast.Store()))]:
    fail(f"the guard at line {st.lineno} sets {ast.unparse(do.targets[0])}, not {param}")
if want and ast.dump(got) != want:
    fail(f"the guard at line {st.lineno} uses {ast.unparse(got)!r}, not {value!r}")
if not want and mode == "return" and got is not None and not (isinstance(got, ast.Constant) and got.value is None):
    fail(f"the guard at line {st.lineno} returns {ast.unparse(got)!r}, not None")
