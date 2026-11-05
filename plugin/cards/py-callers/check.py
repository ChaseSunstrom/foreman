"""py-callers' checker: every site names a real line, and the calls and definitions match an independent token scan
(NAME followed by '(', not after def or class; def or class NAME)."""
import io
import tokenize

from cardkit import def_lines, fail, read_input, source

inp = read_input()
facts, files, name = inp["facts"], set(inp["files"]), inp["inputs"]["name"]
if not isinstance(facts, dict):
    fail("the result isn't an object")
kinds = ("definitions", "calls", "imports", "references")
for k in kinds:
    if not isinstance(facts.get(k), list):
        fail(f"the result has no {k} list")
skipped = {str(s).split(" line ", 1)[0] for s in facts.get("skipped") or []}
texts = {}
for rel in skipped:
    try:
        compile(texts.setdefault(rel, source(rel)) if rel in files else "", rel, "exec", dont_inherit=True)
    except SyntaxError:
        continue
    fail(f"the result skips {rel!r} as unparseable, but it parses")
for k in kinds:
    for site in facts[k]:
        rel, n, code = (site.get(x) if isinstance(site, dict) else None for x in ("file", "line", "code"))
        if rel not in files:
            fail(f"{k} site {site!r:.160} names {rel!r}, which isn't a Python file of the worktree")
        lines = texts.setdefault(rel, source(rel)).splitlines()
        if not isinstance(n, int) or not 1 <= n <= len(lines):
            fail(f"{rel} has no line {n!r} ({len(lines)} lines)")
        if lines[n - 1].strip()[:200] != str(code).strip():
            fail(f"{rel} line {n} reads {lines[n - 1].strip()[:100]!r}, not {str(code)[:100]!r}")
        if name not in lines[n - 1]:
            fail(f"{rel} line {n} doesn't hold {name!r}, so it isn't a {k[:-1]} of it")


def scan(text):
    """(call lines, definition lines) found by tokens."""
    calls = set()
    toks = [t for t in tokenize.generate_tokens(io.StringIO(text).readline)
            if t.type not in (tokenize.NL, tokenize.COMMENT)]
    for i, t in enumerate(toks[:-1]):
        if t.type == tokenize.NAME and t.string == name and toks[i + 1].string == "(" \
                and not (i and toks[i - 1].type == tokenize.NAME and toks[i - 1].string in ("def", "class")):
            calls.add(t.start[0])
    return calls, {n for n, d in def_lines(text) if d == name}


want_calls, want_defs = set(), set()
for rel in sorted(files - skipped):
    c, d = scan(texts.setdefault(rel, source(rel)))
    want_calls |= {(rel, n) for n in c}
    want_defs |= {(rel, n) for n in d}
for k, want in (("calls", want_calls), ("definitions", want_defs)):
    got = {(s["file"], s["line"]) for s in facts[k]}
    extra, missing = sorted(got - want), sorted(want - got)
    if extra:
        fail(f"{k} lists {extra[0][0]}:{extra[0][1]}, which holds no {k[:-1]} of {name!r}")
    if missing and not facts.get("truncated"):
        fail(f"{k} misses {missing[0][0]}:{missing[0][1]}" + (f" and {len(missing) - 1} more" if len(missing) > 1 else ""))
