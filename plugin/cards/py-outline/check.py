"""py-outline's checker, from the file's tokens rather than its ast: every def and class is listed at its real line,
nothing else is, each block ends where it says, and each import sits on its line."""
import re

from cardkit import def_lines, fail, indent_of, read_input, source

inp = read_input()
facts, path, symbol = inp["facts"], inp["inputs"]["path"], inp["inputs"].get("symbol")
if not isinstance(facts, dict) or not isinstance(facts.get("symbols"), list) or not isinstance(facts.get("imports"),
                                                                                              list):
    fail("the outline isn't an object with symbols and imports lists")
text = source(path)
lines = text.splitlines()
if facts.get("path") != path or facts.get("lines") != len(lines):
    fail(f"the outline says {facts.get('path')!r} has {facts.get('lines')} lines; {path} has {len(lines)}")


def code_after(n):
    """The first line after line n that holds code, or None."""
    for x in lines[n:]:
        if x.strip() and not x.strip().startswith("#"):
            return x
    return None


seen = set()
for s in facts["symbols"]:
    name, line, end = (s.get(k) if isinstance(s, dict) else None for k in ("name", "line", "end_line"))
    if not isinstance(name, str) or not all(isinstance(x, int) and not isinstance(x, bool) for x in (line, end)) \
            or not 1 <= line <= end <= len(lines):
        fail(f"symbol {s!r:.200} has no name or no line range inside the file's {len(lines)} lines")
    short = name.rsplit(".", 1)[-1]
    if not re.search(rf"\b(def|class)\s+{re.escape(short)}\b", lines[line - 1]):
        fail(f"{name} is said to start at line {line}, which reads {lines[line - 1].strip()[:80]!r}")
    nxt = code_after(end)
    if nxt is not None and len(indent_of(nxt).expandtabs()) > len(indent_of(lines[line - 1]).expandtabs()):
        fail(f"{name} is said to end at line {end}, but its block goes on: {nxt.strip()[:80]!r}")
    seen.add((line, short))

want = set(def_lines(text))
if symbol:
    tops = [s for s in facts["symbols"] if s["name"] == symbol]
    if not tops:
        fail(f"the outline lacks {symbol} itself")
    want = {(n, w) for n, w in want if any(t["line"] <= n <= t["end_line"] for t in tops)}
for n, w in sorted(want - seen):
    fail(f"the outline lacks {w}, defined at line {n}")
for n, w in sorted(seen - want):
    fail(f"the outline lists {w} at line {n}, where the file defines nothing")
for imp in facts["imports"]:
    n = imp.get("line") if isinstance(imp, dict) else None
    if not isinstance(n, int) or not 1 <= n <= len(lines) or not re.search(r"\b(import|from)\b", lines[n - 1]):
        fail(f"import {imp!r:.120} isn't on its line")
