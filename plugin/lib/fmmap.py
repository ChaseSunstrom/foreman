"""fm map / fm impact (T-0044): a small map of the project for grounding — its gates, layout, entry points, the
files that change most, and which tests go with which source files (by name) — kept in the project's state dir and
rebuilt only when HEAD moves. Stdlib and git only; run by fm commands, never by a hook."""
import collections
import json
import os
import re

import fmcore as c

_TEST = re.compile(r"(^|/)(tests?/|test_[^/]+$|[^/]+_test\.\w+$|[^/]+\.(test|spec)\.\w+$)")
_ENTRY = re.compile(r"(^|/)(__main__\.py|main\.\w+|cli\.\w+|app\.\w+|index\.\w+|manage\.py|bin/[^/]+)$")
_CODE = re.compile(r"\.(py|js|jsx|ts|tsx|go|rs|rb|java|kt|c|cc|cpp|h|hpp|cs|swift|php|sh|lua|zig)$")
HOT = 8
OUT_MAX = 1500


def _git(root, *args):
    return c._git(root, *args, timeout=30)


def _name_stem(path):
    base = os.path.basename(path).split(".")[0]
    return re.sub(r"^test_|_test$", "", base)


def _gates(root, files, checks):
    found = list(checks)
    names = set(files)
    if names & {"pyproject.toml", "pytest.ini", "setup.cfg", "tox.ini"} or any(f.startswith("tests/") and f.endswith(".py") for f in files):
        found.append("pytest (or python3 -m unittest)")
    if "package.json" in names:
        try:
            scripts = json.load(open(os.path.join(root, "package.json"))).get("scripts") or {}
            found += [f"npm run {k}" for k in ("test", "lint", "typecheck", "build") if k in scripts]
        except (OSError, ValueError, AttributeError):
            pass
    if "Cargo.toml" in names:
        found.append("cargo test")
    if "go.mod" in names:
        found.append("go test ./...")
    if "Makefile" in names:
        try:
            with open(os.path.join(root, "Makefile"), encoding="utf-8", errors="replace") as f:
                targets = re.findall(r"(?m)^(test|lint|check)\s*:", f.read())
            found += [f"make {t}" for t in targets]
        except OSError:
            pass
    return list(dict.fromkeys(found))


def build(p):
    root = p.root
    files = _git(root, "ls-files").splitlines()
    churn = collections.Counter(f for f in _git(root, "log", "--since=180.days", "--name-only", "--pretty=format:").splitlines()
                                if f and f in set(files))
    layout = collections.Counter(f.split("/", 1)[0] + "/" if "/" in f else "." for f in files)
    big = next((d for d, n in layout.items() if d != "." and n > 0.6 * len(files)), None)
    if big:  # one folder holds most of the repo: show what's inside it instead
        del layout[big]
        layout.update("/".join(f.split("/")[:2]) + "/" if f.count("/") >= 2 else big for f in files if f.startswith(big))
    sources = [f for f in files if _CODE.search(f) and not _TEST.search(f)]
    links = {}
    for t in (f for f in files if _TEST.search(f) and _CODE.search(f)):
        stem, ext = _name_stem(t), os.path.splitext(t)[1]
        # same language; the source's name is the test's, or ends with it (test_guard.py → fmguard.py)
        srcs = [s for s in sources if s.endswith(ext) and (_name_stem(s) == stem or (len(stem) >= 4 and _name_stem(s).endswith(stem)))]
        if srcs:
            links[t] = srcs
    return {"version": VERSION, "head": _git(root, "rev-parse", "HEAD").strip(), "gates": _gates(root, files, c.read_meta(p).get("checks") or []),
            "layout": layout.most_common(12), "entry": [f for f in files if _ENTRY.search(f)][:8],
            "hot": [f for f, _ in churn.most_common(HOT)], "tests": links, "files": len(files)}


VERSION = 2  # bump when build() changes, so older maps are rebuilt


def load(p, rebuild=False):
    """The map, rebuilt when HEAD has moved since it was built, it was built by older code, or on request."""
    path = os.path.join(p.dir, "map.json")
    try:
        m = json.load(open(path))
    except (OSError, ValueError):
        m = None
    head = _git(p.root, "rev-parse", "HEAD").strip()
    if rebuild or not m or m.get("head") != head or m.get("version") != VERSION:
        m = build(p)
        c.write_atomic(path, json.dumps(m))
    return m


def tests_for(m, paths):
    """Tests linked by name to any of paths (files or globs)."""
    import fnmatch
    return sorted({t for t, srcs in m["tests"].items()
                   if any(fnmatch.fnmatch(s, g) or s == g.rstrip("/") or s.startswith(g.rstrip("*/") + "/")
                          for s in srcs for g in paths)})


def render(m):
    lines = [f"Project map ({m['files']} files, HEAD {m['head'][:8]}; data, rebuilt when HEAD moves):"]
    lines.append("gates: " + ("; ".join(m["gates"]) or "none found (fm check add '<cmd>')"))
    lines.append("layout: " + ", ".join(f"{d} ({n})" for d, n in m["layout"]))
    if m["entry"]:
        lines.append("entry points: " + ", ".join(m["entry"]))
    if m["hot"]:
        lines.append("most changed (180 days): " + ", ".join(m["hot"]))
    if m["tests"]:
        lines.append("tests → sources: " + "; ".join(f"{t} → {', '.join(s[:2])}" for t, s in list(m["tests"].items())[:10]))
    out = "\n".join(c.plain(x) for x in lines)
    return out if len(out) <= OUT_MAX else out[:OUT_MAX - 1] + "…"


def cmd_map(args):
    import fmcli
    p = fmcli.resolve(args)
    if not c.git_root(p.root):
        raise fmcli.UsageError("fm map needs a git repository")
    m = load(p, args.rebuild)
    fmcli.out(args, m, render(m))


def cmd_impact(args):
    """Likely tests (by name) and dependents (files that name the module) for a path."""
    import fmcli
    p = fmcli.resolve(args)
    m = load(p)
    rel = os.path.relpath(os.path.abspath(args.path), p.root) if os.path.isabs(args.path) or os.path.exists(args.path) \
        else args.path
    stem = _name_stem(rel)
    users = [f for f in _git(p.root, "grep", "-l", "-w", "-I", "-e", stem).splitlines() if f != rel and _CODE.search(f)]
    tests = tests_for(m, [rel])
    data = {"path": rel, "tests": tests, "dependents": users[:15]}
    fmcli.out(args, data, c.plain_lines(f"{rel}\n  likely tests: {', '.join(tests) or 'none linked by name'}\n  mention "
                                 f"'{stem}': {', '.join(users[:15]) or 'none'}"))


_DEF = re.compile(r"^(\s*)(?:(?:export|default|pub(?:\([\w:]+\))?|async|static|public|private|protected|abstract|final|"
                  r"override|inline|unsafe|extern)\s+)*(def|class|function|fn|func|struct|enum|trait|impl|interface|"
                  r"module|type|object)\s+([\w.$:<>]+)")


def outline(path):
    """[(first line, last line, depth, "kind name")] for a source file (T-0067): exact for Python (ast), by
    definition keywords and indentation for other languages."""
    import ast
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.splitlines()
    if path.endswith(".py"):
        try:
            out = []

            def walk(node, depth):
                for n in ast.iter_child_nodes(node):
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        out.append((n.lineno, n.end_lineno, depth, ("class " if isinstance(n, ast.ClassDef) else
                                                                    "def ") + n.name))
                        walk(n, depth + 1)
            walk(ast.parse(text), 0)
            return out, len(lines)
        except (SyntaxError, ValueError):
            pass
    hits = [(i + 1, len(m.group(1).expandtabs()), f"{m.group(2)} {m.group(3)}")
            for i, line in enumerate(lines) if (m := _DEF.match(line))]
    indents = sorted({h[1] for h in hits})
    out = []
    for k, (n, ind, name) in enumerate(hits):
        end = next((h[0] - 1 for h in hits[k + 1:] if h[1] <= ind), len(lines))
        while end > n and not lines[end - 1].strip():
            end -= 1
        out.append((n, end, indents.index(ind), name))
    return out, len(lines)


def cmd_outline(args):
    import fmcli
    try:
        defs, total = outline(args.path)
    except OSError as e:
        raise fmcli.UsageError(f"can't read {args.path}: {e.strerror}")
    rows = [f"{a:>6}-{b:<6} {'  ' * d}{name}" for a, b, d, name in defs[:400]]
    fmcli.out(args, {"path": args.path, "lines": total, "defs": [dict(zip(("start", "end", "depth", "name"), x))
                                                                 for x in defs]},
              c.plain_lines(f"{args.path}: {total} lines, {len(defs)} definitions (Read a range with offset/limit)\n"
                            + "\n".join(rows) + ("\n  …" if len(defs) > 400 else "")))


_ADDED = re.compile(r"(?m)^\+(?!\+\+)(.*)$")
_DEBUG = re.compile(r"\b(breakpoint\(\)|pdb\.set_trace|ipdb|console\.log\(|debugger;|dbg!\(|var_dump\(|binding\.pry)")
_MARKER = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")


def pre_audit(root, diff, files, m=None):
    """Mechanical findings from a task's diff (T-0068), so the reviewer spends its reading on judgement: debug
    leftovers, conflict markers, new TODOs, secret-looking values, changed source with no test changed, big files,
    security-sensitive code."""
    found = []
    cur = ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            cur = line[6:] if line.startswith("+++ b/") else line[4:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added = line[1:]
        if _DEBUG.search(added):
            found.append(f"debug leftover in {cur}: {c.fit(added.strip(), 100)}")
        if re.match(r"^(<<<<<<<|>>>>>>>)( |$)|^=======$", added):
            found.append(f"conflict marker in {cur}")
        if _MARKER.search(added):
            found.append(f"new {_MARKER.search(added).group(1)} in {cur}: {c.fit(added.strip(), 100)}")
        if c.redact(added) != added:
            found.append(f"secret-looking value added in {cur}")
    code = [f for f in files if _CODE.search(f) and not _TEST.search(f)]
    if code and not any(_TEST.search(f) for f in files):
        found.append(f"source changed with no test changed: {', '.join(code[:6])}")
    for f in files:
        try:
            if os.path.getsize(os.path.join(root, f)) > 200_000:
                found.append(f"large file in the change: {f} ({os.path.getsize(os.path.join(root, f)) // 1024} KB)")
        except OSError:
            pass
    risky = c.sensitive(files, diff)
    if risky:
        found.append(f"security-sensitive: {', '.join(risky)} (adversary lens required)")
    return list(dict.fromkeys(found))[:30]


def changed(root, base):
    """Files changed since base (committed or not) plus untracked ones, relative to root."""
    return sorted(set(_git(root, "diff", "--name-only", base).splitlines())
                  | set(_git(root, "ls-files", "--others", "--exclude-standard").splitlines()))


def cmd_why(args):
    """fm why FILE[:LINE] (R2): the commits behind a line (or a file's last five), the Foreman tasks they name, and
    each task's title, outcome and lesson — why the code is the way it is, without reading history by hand."""
    import fmcli
    p = fmcli.resolve(args)
    path, _, line = args.target.rpartition(":")
    if not line.isdigit():
        path, line = args.target, ""
    rel = os.path.relpath(os.path.abspath(path), p.root) if os.path.exists(path) else path
    if line:
        blame = _git(p.root, "blame", "-L", f"{line},{line}", "--porcelain", "--", rel)
        shas = [blame.split()[0]] if blame.strip() and not blame.startswith("0" * 40) else []
    else:
        shas = _git(p.root, "log", "-n", "5", "--format=%H", "--", rel).split()
    briefs = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    rows, lines = [], []
    for sha in shas:
        msg = _git(p.root, "log", "-1", "--format=%h %as %s%n%b", sha).strip()
        if not msg:
            continue
        ids = list(dict.fromkeys(re.findall(r"\bT-\d{4,}\b", msg)))
        rows.append({"commit": msg.split()[0], "subject": msg.splitlines()[0], "tasks": ids})
        lines.append(c.fit(msg.splitlines()[0], 160))
        for tid in ids:
            b = briefs.get(tid)
            if b:
                lesson = next((x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()), "")
                lines.append(c.fit(f"  {tid} [{b.type} {b.tier}, {b.status}] {b.title}"
                                   + (f" — lesson: {lesson}" if lesson else ""), 220))
    fmcli.out(args, {"path": rel, "line": int(line) if line else None, "commits": rows},
              c.plain_lines("\n".join(lines)) if lines else f"No commits found for {rel}{':' + line if line else ''} "
                                                            f"(uncommitted, or not in git).")
