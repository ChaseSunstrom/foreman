"""fm instruments (T-0701): zero-token instruments. Deterministic typed tools answer the common read, failure, log,
data and trace questions in a few capped lines, so the model reads the answer instead of the raw file or output.
One registry (name, line cap, JSON-schema input) drives `fm instruments`, the fm subcommands and their arguments.
Each tool puts its most telling lines first and is cut at its cap. Stdlib and git only: no network, no model calls."""
import collections
import itertools
import json
import os
import re
import sys

import fmcore as c

# name: (line cap, what it answers, [(argument, JSON type, description, required, metavar)]). The first argument is
# positional, the rest are --flags.
TOOLS = {
    "sym": (40, "a definition and its one-hop neighbourhood (the names it uses, its callers), never the whole file",
            [("target", "string", "PATH:NAME; Class.method for a method", True, "PATH:NAME")]),
    "fail": (15, "a test run's failure output as the test, the error, the repo frames and the failing source",
             [("file", "string", "the runner's output (default: stdin)", False, "FILE")]),
    "logs": (40, "a log as templates with counts, errors first; with --since-good, what's new against a good run",
             [("file", "string", "the log", True, "FILE"),
              ("since_good", "string", "a good run's log: templates new or gone since it led", False, "FILE")]),
    "data": (40, "a data file's schema, stats and first 5 rows (csv, tsv, json, jsonl, sqlite)",
             [("file", "string", "the data file", True, "FILE")]),
    "trace": (30, "a Python or JS stack trace mapped to repo lines, deepest first, with each line's commit date and "
                  "task", [("file", "string", "the pasted trace (default: stdin)", False, "FILE")]),
}
WIDTH = 200


def schema(name):
    args = TOOLS[name][2]
    return {"type": "object", "properties": {a: {"type": t, "description": d} for a, t, d, _, _ in args},
            "required": [a for a, _, _, req, _ in args if req], "additionalProperties": False}


def usage(name):
    words = [f"fm {name}"]
    for i, (a, _, _, req, meta) in enumerate(TOOLS[name][2]):
        w = meta if i == 0 else f"--{a.replace('_', '-')} {meta}"
        words.append(w if req else f"[{w}]")
    return " ".join(words)


def arguments(parser, name):
    """The tool's arguments on its fm subcommand, from the registry."""
    for i, (a, _, desc, req, meta) in enumerate(TOOLS[name][2]):
        if i == 0:
            parser.add_argument(a, nargs=None if req else "?", metavar=meta, help=desc)
        else:
            parser.add_argument("--" + a.replace("_", "-"), dest=a, required=req, metavar=meta, help=desc)


def cmd_instruments(args):
    import fmcli
    rows = [{"name": n, "usage": usage(n), "summary": s, "cap": cap, "input_schema": schema(n)}
            for n, (cap, s, _) in TOOLS.items()]
    w = max(len(r["usage"]) for r in rows)
    fmcli.out(args, {"instruments": rows},
              "Instruments: a few capped lines instead of a raw file or output (--json: the input schemas)\n"
              + "\n".join(f"  {r['name']:<6} ≤{r['cap']} lines  {r['usage']:<{w}}  {r['summary']}" for r in rows))


def _emit(args, name, lines, data):
    import fmcli
    cap = TOOLS[name][0]
    if len(lines) > cap:
        lines = lines[:cap - 1] + [f"… {len(lines) - cap + 1} more lines (fm {name} keeps {cap})"]
    text = "\n".join(c.fit(" ⏎ ".join(c.redact(ln).splitlines()), WIDTH) for ln in lines)  # redact, then cut
    fmcli.out(args, c.redact_obj(data), c.plain_lines(text))


def _root():
    return c.git_root(os.getcwd()) or os.getcwd()


MAX_TEXT, MAX_LINES = 20_000_000, 1_000_000  # ponytail: a huge input is read up to these; a streaming pass if it matters


def _input(path):
    import fmcli
    if path and path != "-":
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                return f.read(MAX_TEXT)
        except OSError as e:
            raise fmcli.UsageError(f"can't read {path}: {e.strerror}")
    if sys.stdin.isatty():
        raise fmcli.UsageError("pipe the text in or name a FILE")
    return sys.stdin.read(MAX_TEXT)


def _read_lines(root, rel, cache={}):  # noqa: B006 — one process, one read per file
    key = os.path.join(root, rel)
    if key not in cache:
        try:
            with open(key, encoding="utf-8", errors="replace") as f:
                cache[key] = f.read().splitlines()
        except OSError:
            cache[key] = []
    return cache[key]


def _src(root, rel, n):
    lines = _read_lines(root, rel)
    return lines[n - 1] if 0 < n <= len(lines) else ""


def _rel(path, root):
    rel = os.path.relpath(os.path.realpath(path), root)
    return path if rel.startswith("..") else rel


# ---------------------------------------------------------------- fm sym

def _qualify(defs):
    """fmmap.outline's [(start, end, depth, "kind name")] as [(Outer.inner, start, end, kind)]."""
    out, stack = [], []
    for start, end, depth, label in defs:
        kind, _, name = label.partition(" ")
        stack[depth:] = [name]
        out.append((".".join(stack), start, end, kind))
    return out


def _code(line, py):
    """A line without its string literals and comments (for names and braces)."""
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`[^`]*`|' + (r"#.*" if py else r"//.*"), " ", line)


def _brace_end(lines, start, end):
    """The line closing the brace a definition opens on its first lines; outline's indentation guess otherwise."""
    depth, opened = 0, False
    for i in range(start - 1, len(lines)):
        for ch in _code(lines[i], False):
            if ch in "{}":
                depth += 1 if ch == "{" else -1
                opened = True
        if opened and depth <= 0:
            return i + 1
        if not opened and i >= start + 1:
            break
    return end


def _defs(path, lines):
    import fmmap
    quals = _qualify(fmmap.outline(path)[0])
    if not path.endswith(".py"):
        quals = [(q, a, _brace_end(lines, a, b), k) for q, a, b, k in quals]
    return quals


def _py_globals(text):
    """Module-level assignments and imports: {name: line}."""
    import ast
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return {}
    out = {}
    for n in tree.body:
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            for t in n.targets if isinstance(n, ast.Assign) else [n.target]:
                if isinstance(t, ast.Name):
                    out.setdefault(t.id, n.lineno)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                out.setdefault((a.asname or a.name).split(".")[0], n.lineno)
    return out


def cmd_sym(args):
    import difflib
    import fmcli
    path, _, name = args.target.rpartition(":")
    if not path or not name:
        raise fmcli.UsageError("fm sym PATH:NAME (Class.method for a method)")
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        raise fmcli.UsageError(f"can't read {path}: {e.strerror}")
    root, lines, py = _root(), text.splitlines(), path.endswith(".py")
    quals = _defs(path, lines)
    hit = next((q for q in quals if q[0] == name), None) or next((q for q in quals if q[0].endswith("." + name)), None)
    if not hit:
        near = difflib.get_close_matches(name, [q[0] for q in quals], n=3, cutoff=0.5)
        raise fmcli.UsageError(f"no definition named {name} in {path}" + (f"; nearest: {', '.join(near)}" if near else ""))
    qual, start, end, kind = hit
    rel, short = _rel(path, root), qual.rsplit(".", 1)[-1]
    body = 20
    out = [f"{rel}:{start}-{end} {qual} ({kind}, {end - start + 1} lines)"]
    out += [f"  {n:>4}  {lines[n - 1]}" for n in range(start, min(end, start + body - 1) + 1)]
    if end - start + 1 > body:
        out.append(f"  … {end - start + 1 - body} more lines (Read offset={start + body} limit={end - start + 1 - body})")
    # uses: the names in its body that this file defines or imports (methods by their last name)
    table = {}
    for q, a, b, k in quals:
        if not start <= a <= end:
            table.setdefault(q.rsplit(".", 1)[-1], (a, b))
    for g, n in (_py_globals(text) if py else {}).items():
        table.setdefault(g, (n, n))
    words = re.findall(r"[A-Za-z_$][\w$]*", " ".join(_code(ln, py) for ln in lines[start - 1:end]))
    used = [w for w in dict.fromkeys(words) if w in table and w != short]
    out.append(f"uses ({len(used)}):" if used else "uses: nothing else defined in this file")
    for w in used[:6]:
        a, b = table[w]
        out.append(f"  {w:<16} {rel}:{a}{'-' + str(b) if b != a else ''}  {lines[a - 1].strip()}")
    if len(used) > 6:
        out.append(f"  … {len(used) - 6} more: {', '.join(used[6:])}")
    # callers: lines in the repo that call it (a method by .name()), each with the definition around it
    call = re.compile((r"\." if "." in qual else r"(?<![\w$])") + re.escape(short) + r"\s*\(")
    import fmmap
    found = c._git(root, "grep", "-n", "-I", "-w", "-F", "-e", short, *(["--untracked"] if c.git_root(root) else
                                                                        ["--no-index"]), timeout=30)
    callers, encl = [], {}
    for hit_ in found.splitlines():
        f, _, rest = hit_.partition(":")
        n, _, line = rest.partition(":")
        if not n.isdigit() or not c.CODE.search(f) or not call.search(_code(line, f.endswith(".py"))) or \
                fmmap._DEF.match(line):
            continue
        if f not in encl:
            fl = _read_lines(root, f)
            encl[f] = _defs(os.path.join(root, f), fl)
        around = [q for q in encl[f] if q[1] <= int(n) <= q[2]]
        where = max(around, key=lambda q: q[1])[0] if around else "<module>"
        callers.append(f"  {f}:{n} in {where}: {line.strip()}")
    out.append(f"callers ({len(callers)}):" if callers else f"callers: none found for {short}( in {os.path.basename(root)}")
    out += callers[:6] + ([f"  … {len(callers) - 6} more"] if len(callers) > 6 else [])  # 1+20+1+7+7 ≤ 40
    _emit(args, "sym", out, {"path": rel, "name": qual, "kind": kind, "start": start, "end": end, "uses": used,
                             "callers": [x.strip() for x in callers[:50]]})


# ---------------------------------------------------------------- frames (fm fail, fm trace)

_PY_FRAME = re.compile(r'^\s*File "([^"]+)", line (\d+)(?:, in (.+))?$')
_AT_LINE = re.compile(r"^\s*([\w./\\-]+\.\w+):(\d+):(?:\s*in (\S+))?")  # pytest's "price.py:6: KeyError", go test
_JS_FRAME = re.compile(r"^\s*at (?:(.+?) \()?(\S+?):(\d+):\d+\)?$")
_LIB = re.compile(r"(^|[/\\])(site-packages|dist-packages|node_modules|\.venv|venv|\.tox|lib[/\\]python[\d.]*)[/\\]|"
                  r"^node:|^<|^internal[/\\]")
_ERROR = re.compile(r"^(?:E\s+)?((?:[A-Za-z_]\w*\.)*[A-Z]\w*(?:Error|Exception|Failure|Exit|Interrupt)\b.*|"
                    r"panic: .*|thread '.*' panicked.*|assert .*)$")


def _frames(text):
    """[(path, line, function)] innermost first: Python and pytest list the outermost first, node the innermost."""
    outer_first, inner_first = [], []
    for ln in text.splitlines():
        if m := _PY_FRAME.match(ln) or _AT_LINE.match(ln):
            outer_first.append((m.group(1), int(m.group(2)), m.group(3) or ""))
        elif m := _JS_FRAME.match(ln):
            inner_first.append((m.group(2), int(m.group(3)), m.group(1) or ""))
    return outer_first[::-1] + inner_first


def _locate(path, root):
    """The repo file a trace's path names (relative to root), or None: a library, or nothing here. Another
    machine's checkout (a CI runner's) maps by the longest suffix that exists under the folder fm runs in, then
    under root."""
    if _LIB.search(path):
        return None
    if os.path.isabs(path) and os.path.isfile(path):
        rel = os.path.relpath(os.path.realpath(path), root)
        return None if rel.startswith("..") else rel
    parts = [p for p in re.split(r"[/\\]", path) if p not in ("", ".")]
    for base in dict.fromkeys([os.getcwd(), root]):
        for i in range(len(parts)):
            if ".." not in parts[i:] and os.path.isfile(os.path.join(base, *parts[i:])):
                rel = os.path.relpath(os.path.realpath(os.path.join(base, *parts[i:])), root)
                if not rel.startswith(".."):  # a symlink out of the repo isn't a repo line
                    return rel
    return None


def _error(text):
    return next((m.group(1).strip() for ln in text.splitlines() if (m := _ERROR.match(ln))), "")


# ---------------------------------------------------------------- fm fail

_HEADER = re.compile(r"(?m)^(?:(?:FAIL|ERROR): .*|_{3,} .+ _{3,}|--- FAIL: .*|\s*● .+)$")
_SUMMARY = re.compile(r"(?m)^(?:FAILED \(.*\)|=+ .*\b(?:failed|errors?)\b.* =+|Tests?:\s+.*\bfailed\b.*|FAIL\s*|"
                      r"FAIL\s+\S+\s+[\d.]+s)$")


def _test_id(header):
    h = header.strip()
    if m := re.match(r"(?:FAIL|ERROR): (\S+)(?: \(([\w.]+)\))?", h):
        return m.group(2) or m.group(1)
    return re.sub(r"^(?:_+ | *● |--- FAIL: )|(?: _+|\s+\(.*\))$", "", h).strip()


def cmd_fail(args):
    text, root = _input(args.file), _root()
    heads = list(_HEADER.finditer(text))
    block = text[heads[0].start():heads[1].start() if len(heads) > 1 else len(text)] if heads else text
    ids = list(dict.fromkeys([_test_id(h.group(0)) for h in heads] or c.failing_tests(text)))
    first = heads[0].group(0) if heads else ""
    kind = first.split(":")[0] if first.startswith(("FAIL:", "ERROR:")) else "FAIL"  # unittest says which
    error, summary = _error(block), (_SUMMARY.findall(text) or [""])[-1]
    frames = [(rel, n, fn) for p, n, fn in _frames(block) if (rel := _locate(p, root))]
    outside = len(_frames(block)) - len(frames)
    out = []
    if ids:
        others = ids[1:]
        out.append(f"{kind} {ids[0]}" + (f" (1 of {len(ids)} failing; also {', '.join(others[:3])}"
                                         f"{' …' if len(others) > 3 else ''})" if others else ""))
    if error:
        out.append(error)
    for rel, n, fn in frames[:5]:
        out.append(f"{rel}:{n} in {fn or '?'}: {_src(root, rel, n).strip()}")
    if len(frames) > 5 or outside:
        out.append(f"(+{max(0, len(frames) - 5) + outside} frames {'outside the repo' if outside else 'further out'})")
    if frames:
        rel, n, _ = frames[0]
        lines = _read_lines(root, rel)
        span = [i for i in range(max(1, n - 2), min(len(lines), n + 2) + 1)]
        while span and span[0] != n and not lines[span[0] - 1].strip():
            span.pop(0)
        while span and span[-1] != n and not lines[span[-1] - 1].strip():
            span.pop()
        out += [f"  {'>' if i == n else ' '} {i:>4}  {lines[i - 1]}" for i in span]
    elif heads or error:  # no frame in this repo: the block's own last lines
        out += [ln for ln in block.strip().splitlines()[1:] if ln.strip() and ln.strip() != error
                and not re.fullmatch(r"\s*[~^=_-]+\s*", ln)][-6:]
    if summary:
        out.append(summary)
    if not out:
        out = [f"No failure found in {len(text.splitlines())} lines (no failing test, error or stack frame)."]
    _emit(args, "fail", out, {"tests": ids, "error": error, "summary": summary, "outside": outside,
                              "frames": [{"path": r, "line": n, "function": fn, "source": _src(root, r, n).strip()}
                                         for r, n, fn in frames]})


# ---------------------------------------------------------------- fm logs

_VALUE = re.compile(r"[-+]?\d[\d.,:/_+T-]*[A-Za-zµ%]{0,3}|0x[0-9a-fA-F]+|(?=[a-fA-F]*\d)[0-9a-fA-F]{8,}|"
                    r"[0-9a-fA-F]{8}-[0-9a-fA-F-]{27}")
_SEVERE = re.compile(r"(?i)\b(error|fatal|crit(ical)?|panic|exception|traceback|fail(ed|ure)?|severe|emerg)\b")
_WARN = re.compile(r"(?i)\bwarn(ing)?\b")


def _mask(tok):
    key, eq, val = tok.partition("=")
    if eq and key and _VALUE.fullmatch(val):
        return key + "=<*>"
    return "<*>" if _VALUE.fullmatch(tok) else tok


def _sim(tmpl, toks):
    """Drain's similarity: the share of the template's fixed tokens the line repeats (a prefix<*> matches its prefix)."""
    same = sum(1 for a, b in zip(tmpl, toks) if a != "<*>" and (a == b or a.endswith("<*>") and b.startswith(a[:-3])))
    # T-0701 review: a line that repeats every fixed token is the template's, however many values it has (an access
    # log is mostly numbers); otherwise Drain's share of all tokens, so a template can't drift general
    return 1.0 if same == sum(a != "<*>" for a in tmpl) else same / len(tmpl)


def _wild(a, b):
    p = re.sub(r"\w+$", "", os.path.commonprefix([a[:-3] if a.endswith("<*>") else a, b]))
    return p + "<*>"


def _mine(runs):
    """Drain-style templates (He et al., 2017) over each run's lines: lines of one length and first fixed token
    share a template when at least half its fixed tokens match; the tokens that differ become <*>. Returns
    [{"tokens", "counts": per run, "first": first line per run}] in the order first seen."""
    groups, out = {}, []
    for r, lines in enumerate(runs):
        for n, line in enumerate(lines, 1):
            toks = [_mask(t) for t in line.split()]
            if not toks:
                continue
            group = groups.setdefault((len(toks), next((t for t in toks if t != "<*>"), "")), [])
            best = max(group, key=lambda t: _sim(t["tokens"], toks), default=None)
            if best is None or _sim(best["tokens"], toks) < 0.5:
                best = {"tokens": toks, "counts": [0] * len(runs), "first": [0] * len(runs)}
                group.append(best)
                out.append(best)
            else:
                best["tokens"] = [a if a == b else _wild(a, b) for a, b in zip(best["tokens"], toks)]
            best["counts"][r] += 1
            best["first"][r] = best["first"][r] or n
    return out


def cmd_logs(args):
    import fmcli
    runs = []
    for path in [args.file] + ([args.since_good] if args.since_good else []):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                runs.append([ln.rstrip("\r\n") for ln in itertools.islice(f, MAX_LINES)])
        except OSError as e:
            raise fmcli.UsageError(f"can't read {path}: {e.strerror}")
    temps = _mine(runs)
    for t in temps:
        toks = list(t["tokens"])
        while len(toks) > 1 and toks[0] == "<*>":  # a leading timestamp says nothing
            toks.pop(0)
        t["text"] = " ".join(toks)
        t["sev"] = 0 if _SEVERE.search(t["text"]) else 1 if _WARN.search(t["text"]) else 2
    order = lambda t: (t["sev"], t["first"][0] if t["sev"] < 2 else -t["counts"][0], t["first"][0])  # noqa: E731
    here = [t for t in temps if t["counts"][0]]
    name = os.path.basename(args.file)
    head = f"{name}: {len(runs[0])} lines → {len(here)} templates"
    if args.since_good:
        new = sorted((t for t in here if not t["counts"][1]), key=lambda t: (t["sev"], t["first"][0]))
        gone = sorted((t for t in temps if not t["counts"][0]), key=lambda t: (-t["counts"][1], t["first"][1]))
        rows = [("new", t) for t in new] + [("gone", t) for t in gone] + [("", t) for t in sorted(
            (t for t in here if t["counts"][1]), key=order)]
        head += (f"; since {os.path.basename(args.since_good)} ({len(runs[1])} lines): {len(new)} new, "
                 f"{len(gone)} gone")
        out = [head] + [f"{m:<4}{t['counts'][1] if m == 'gone' else t['counts'][0]:>6}  {t['text']}  " +
                        (f"(line {t['first'][1]} of the good run)" if m == "gone" else f"(line {t['first'][0]}"
                         + (f"; good run {t['counts'][1]})" if not m else ")")) for m, t in rows]
    else:
        out = [head + " (errors and warnings first, then by count)"] + [
            f"{t['counts'][0]:>6}  {t['text']}  (line {t['first'][0]})" for t in sorted(here, key=order)]
    _emit(args, "logs", out, {"lines": len(runs[0]), "good_lines": len(runs[1]) if args.since_good else None,
                              "templates": [{"template": t["text"], "count": t["counts"][0], "first": t["first"][0],
                                             "good": t["counts"][1] if args.since_good else None}
                                            for t in sorted(temps, key=order)[:500]]})


# ---------------------------------------------------------------- fm data

ROWS = 100_000  # ponytail: stats from the first 100k rows of a csv/json file; a sampling pass if that misleads
_NUMBER = re.compile(r"[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?")
_DATE = re.compile(r"\d{4}-\d\d-\d\d(?:[T ][\d:.]+(?:Z|[+-]\d\d:?\d\d)?)?")


def _flat(d, pre=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict) and v:
            out.update(_flat(v, f"{pre}{k}."))
        else:
            out[f"{pre}{k}"] = v
    return out


def _records(recs):
    """Dicts (nested keys flattened) as (columns, rows)."""
    flat = [_flat(r) if isinstance(r, dict) else {"value": r} for r in recs]
    cols = list(dict.fromkeys(k for r in flat for k in r))
    return cols, [[r.get(k) for k in cols] for r in flat]


def _tables(path):
    """(kind, [(table, columns, declared types, rows, total rows)], note)."""
    import csv
    import itertools
    with open(path, "rb") as f:
        magic = f.read(16)
    if magic.startswith(b"SQLite format 3\x00"):
        import pathlib
        import sqlite3
        con = sqlite3.connect(pathlib.Path(path).absolute().as_uri() + "?mode=ro", uri=True)
        con.text_factory = lambda b: b.decode("utf-8", "replace")  # one bad value mustn't lose the file
        try:
            out = []
            for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                                    "ORDER BY name").fetchall():
                q = '"' + t.replace('"', '""') + '"'
                info = con.execute(f"PRAGMA table_info({q})").fetchall()
                rows = [list(r) for r in con.execute(f"SELECT * FROM {q} LIMIT {ROWS}")]
                out.append((t, [r[1] for r in info], [r[2] for r in info], rows,
                            con.execute(f"SELECT COUNT(*) FROM {q}").fetchone()[0]))
            return "sqlite", out, ""
        finally:
            con.close()
    ext = os.path.splitext(path)[1].lower()
    with open(path, encoding="utf-8-sig", errors="replace", newline="") as f:
        if ext in (".jsonl", ".ndjson"):
            recs, bad, total = [], 0, 0
            for ln in f:
                if ln.strip():
                    total += 1
                    if len(recs) < ROWS:  # T-0701 review: parse the first ROWS, count the rest
                        try:
                            recs.append(json.loads(ln))
                        except ValueError:
                            bad += 1
            cols, rows = _records(recs)
            return "jsonl", [("", cols, [], rows, total - bad)], f"{bad} lines aren't JSON" if bad else ""
        if ext == ".json":
            if os.path.getsize(path) > MAX_TEXT:
                raise ValueError(f"over {MAX_TEXT // 1_000_000} MB: as JSON lines (.jsonl) it's read in part")
            data, note = json.load(f), ""
            if isinstance(data, dict):
                key = max((k for k, v in data.items() if isinstance(v, list)), key=lambda k: len(data[k]), default=None)
                data, note = (data[key], f"the list under {key!r}") if key else ([data], "one object")
            data = data if isinstance(data, list) else [data]
            cols, rows = _records(data[:ROWS])
            return "json", [("", cols, [], rows, len(data))], note
        sample = f.read(65536)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel_tab if ext == ".tsv" else csv.excel
        reader = csv.reader(f, dialect)
        cols = next(reader, [])
        rows = [[r[i] if i < len(r) else None for i in range(len(cols))] for r in itertools.islice(reader, ROWS)]
        return ("tsv" if dialect.delimiter == "\t" else "csv"), [("", cols, [], rows, len(rows) + sum(1 for _ in reader))], ""


def _kind(v):
    if v is None or v == "":
        return None
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, (int, float)):
        return "number"
    if isinstance(v, (list, dict)):
        return "list" if isinstance(v, list) else "object"
    s = str(v).strip()
    return ("bool" if s.lower() in ("true", "false") else "number" if _NUMBER.fullmatch(s) else
            "date" if _DATE.fullmatch(s) else "text")


def _column(name, vals, decl):
    kinds = [_kind(v) for v in vals]
    counts = collections.Counter(k for k in kinds if k)
    typ = counts.most_common(1)[0][0] if counts else "empty"
    vals_ = [v for v, k in zip(vals, kinds) if k == typ]
    other = collections.Counter(str(v) for v, k in zip(vals, kinds) if k and k != typ)
    parts = []
    if other:
        parts.append("other: " + ", ".join(f"{v!r}×{n}" for v, n in other.most_common(3)))
    if kinds.count(None):
        parts.append(f"{kinds.count(None)} empty")
    distinct = collections.Counter(str(v) for v in vals_)
    parts.append(f"{len(distinct)} distinct")
    if typ == "number":
        nums = [float(str(v)) for v in vals_]  # str: an int over 1e308 is inf, not an OverflowError
        parts.append(f"min {min(nums):g} max {max(nums):g} mean {sum(nums) / len(nums):.4g}")
    elif typ == "date":
        parts.append(f"{min(map(str, vals_))} → {max(map(str, vals_))}")
    elif typ in ("text", "bool") and len(distinct) <= 20:
        parts.append("top " + ", ".join(f"{c.fit(v, 40)}×{n}" for v, n in distinct.most_common(3)))
    elif typ == "text":
        parts.append("e.g. " + ", ".join(repr(c.fit(v, 30)) for v in list(distinct)[:2]))
    return f"  {name:<14} {typ:<6} " + " · ".join(parts) + (f" ({decl})" if decl else "")


def cmd_data(args):
    import csv
    import io
    import sqlite3
    import fmcli
    try:
        kind, tables, note = _tables(args.file)
    except (OSError, ValueError, csv.Error, sqlite3.Error) as e:
        raise fmcli.UsageError(f"can't read {args.file} as data: {getattr(e, 'strerror', None) or e}")
    name = os.path.basename(args.file)
    if kind == "sqlite":
        out = [f"{name}: sqlite, {len(tables)} table{'s' if len(tables) != 1 else ''}"]
    else:
        _, cols, _, _, total = tables[0]
        out = [f"{name}: {kind}, {total} row{'s' if total != 1 else ''}, {len(cols)} columns" + (f" ({note})" if note
                                                                                                else "")]
    data = {"kind": kind, "tables": []}
    for table, cols, decls, rows, total in tables:
        if kind == "sqlite":
            out.append(f"{table}: {total} rows, {len(cols)} columns")
        if total > len(rows):
            out.append(f"  (stats from the first {len(rows):,} rows)")
        shown = 28
        out += [_column(col, [r[i] for r in rows], decls[i] if decls else "") for i, col in enumerate(cols[:shown])]
        if len(cols) > shown:
            out.append(f"  … {len(cols) - shown} more columns: {', '.join(cols[shown:])}")
        out.append(f"first {min(5, len(rows))} rows:")
        for r in rows[:5]:
            buf = io.StringIO()
            csv.writer(buf, lineterminator="").writerow(["" if v is None else v for v in r])
            out.append("    " + buf.getvalue())
        data["tables"].append({"name": table, "rows": total, "columns": cols, "sample": rows[:5]})
    _emit(args, "data", out, data)


# ---------------------------------------------------------------- fm trace

def _touch(root, rel, n, cache):
    """The commit that last touched the line: date, sha, the tasks it names and its subject."""
    if (rel, n) not in cache:  # recursion repeats frames: one blame each
        cache[(rel, n)] = c._git(root, "blame", "--porcelain", "-L", f"{n},{n}", "--", rel, timeout=10)
    blame = cache[(rel, n)]
    sha = blame.split()[0] if blame.strip() else ""
    if not sha:
        return "not in git"
    if not sha.strip("0"):
        return "uncommitted"
    if sha not in cache:
        log = c._git(root, "log", "-1", "--format=%as%x00%h%x00%s%x00%b", sha, timeout=10)
        date, short, subj, body = (log.split("\x00") + ["", "", "", ""])[:4]
        ids = list(dict.fromkeys(re.findall(r"\bT-\d{4,}\b", subj + "\n" + body)))
        subj = re.sub(r"\s*\(?\bT-\d{4,}\b\)?", "", subj).strip()
        cache[sha] = " ".join(x for x in (date, short, " ".join(ids), c.fit(subj, 70)) if x)
    return cache[sha]


def cmd_trace(args):
    text, root = _input(args.file), _root()
    error, frames, cache = _error(text), _frames(text), {}
    out, outside, rows, last = [error] if error else [], [], [], None
    for path, n, fn in frames:
        rel = _locate(path, root)
        if not rel:
            outside.append("/".join(re.split(r"[/\\]", path)[-2:]))
            continue
        if rows and (rel, n, fn) == last:  # recursion: one frame, counted
            rows[-1]["repeat"] += 1
            continue
        last = (rel, n, fn)
        rows.append({"path": rel, "line": n, "function": fn, "source": _src(root, rel, n).strip(),
                     "commit": _touch(root, rel, n, cache), "repeat": 1})
    for r in rows:
        out += [f"{r['path']}:{r['line']} in {r['function'] or '?'}{' ×' + str(r['repeat']) if r['repeat'] > 1 else ''}"
                f" · {r['commit']}", f"    {r['source']}"]
    if outside:
        out.append(f"({len(outside)} frames outside the repo: {', '.join(dict.fromkeys(outside))})")
    if not frames:
        out.append("No stack frames found (Python 'File \"…\", line N' or JS 'at … (file:line:col)').")
    _emit(args, "trace", out, {"error": error, "frames": rows, "outside": len(outside)})
