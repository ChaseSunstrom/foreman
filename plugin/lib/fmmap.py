"""fm map / fm impact (T-0044): a small map of the project for grounding — its gates, layout, entry points, the
files that change most, and which tests go with which source files (by name) — kept in the project's state dir and
rebuilt only when HEAD moves. Stdlib and git only; run by fm commands, never by a hook."""
import collections
import json
import os
import subprocess
import re

import fmcore as c

_TEST = c.TESTISH  # T-0295: one test-file pattern
_ENTRY = re.compile(r"(^|/)(__main__\.py|main\.\w+|cli\.\w+|app\.\w+|index\.\w+|manage\.py|bin/[^/]+)$")
_CODE = c.CODE
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
            "hot": [f for f, _ in churn.most_common(HOT)], "tests": links, "files": len(files),
            "ci": _ci(root, files), "pairs": _co_change(root, set(files))}


_CI_FILE = re.compile(r"^(\.github/workflows/[^/]+\.ya?ml|\.gitlab-ci\.yml)$")
_CI_RUN = re.compile(r"(?m)^\s*(?:-\s+)?(?:run:\s*|-\s+)(?![|>])([^#\n]*\b(test|lint|check|typecheck|vet|clippy|fmt|"
                     r"format|build|mypy|ruff|flake8|eslint|pytest|tox)\b[^#\n]*)$")


def _ci(root, files):
    """R3 (mirror CI): the check-like commands the CI workflows run, so local gates can match what CI enforces."""
    found = []
    for f in (f for f in files if _CI_FILE.match(f)):
        try:
            with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                found += [m.group(1).strip().strip("'\"") for m in _CI_RUN.finditer(fh.read())]
        except OSError:
            pass
    return list(dict.fromkeys(x for x in found if not x.startswith(("uses:", "name:"))))[:12]


def _co_change(root, files, min_together=3, share=0.6):
    """R2 (companion edits): {file: [files it changed with in ≥ 60% of its last year's commits, ≥ 3 times]}."""
    log = _git(root, "log", "--since=365.days", "--name-only", "--pretty=format:%x00")
    alone, together = collections.Counter(), collections.Counter()
    for commit in log.split("\0"):
        names = sorted({f for f in commit.split("\n") if f in files})
        if not 2 <= len(names) <= 20:  # a sweeping commit says nothing about companions
            alone.update(names)
            continue
        alone.update(names)
        together.update((a, b) for a in names for b in names if a != b)
    pairs = {}
    for (a, b), n in together.items():
        if n >= min_together and n / alone[a] >= share:
            pairs.setdefault(a, []).append(b)
    return {a: sorted(bs)[:3] for a, bs in pairs.items()}


VERSION = 3  # bump when build() changes, so older maps are rebuilt


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
    if m.get("ci"):
        lines.append("CI runs: " + "; ".join(m["ci"]))
    out = "\n".join(c.plain(x) for x in lines)
    return out if len(out) <= OUT_MAX else out[:OUT_MAX - 1] + "…"


def compact(p, limit=500):
    """T-0215: one line of the cached map for the session-start context, or None. Never builds in the hook (1.5 s on a
    7k-file repo): a missing or stale map starts a detached `fm map`, and the next session has it."""
    try:
        with open(os.path.join(p.dir, "map.json"), encoding="utf-8") as f:
            m = json.load(f)
        if m.get("version") != VERSION:
            m = None
    except (OSError, ValueError):
        m = None
    head = _git(p.root, "rev-parse", "HEAD").strip()
    if (not m or m.get("head") != head) and not os.environ.get("FOREMAN_NO_BACKGROUND"):
        try:
            subprocess.Popen([os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "map", "--json"], cwd=p.root,
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        except OSError:
            pass
    if not m:
        return None
    parts = [f"gates: {'; '.join(m['gates'][:3]) or 'none'}"]
    if m["entry"]:
        parts.append(f"entry: {', '.join(m['entry'][:4])}")
    parts.append("layout: " + ", ".join(f"{d} ({n})" for d, n in m["layout"][:5]))
    if m["tests"]:
        parts.append("tests→src: " + "; ".join(f"{t}→{s[0]}" for t, s in list(m["tests"].items())[:4] if s))
    line = c.plain(f"Map ({m['files']} files{'' if m.get('head') == head else ', as of an older HEAD'}; fm map for "
                   f"more): " + " · ".join(parts))
    return line if len(line) <= limit else line[:limit - 1] + "…"


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


_COMMON_STEMS = {"index", "main", "init", "__init__", "utils", "util", "types", "setup", "config", "common", "helpers"}


def tour(p, b):
    """T-0248: the task's changed files in reading order — a file before the files that name it (fm impact's name-stem
    heuristic) — each with its +/- lines, the files it uses, and the step being worked when it was last edited."""
    import graphlib
    commits = _git(p.root, "log", "--format=%H", "-F", f"--grep=({b.id}").split() if b.status == "done" else []
    if len(commits) == 1:  # finished and committed: its own commit, not everything since
        numstat = _git(p.root, "show", "--numstat", "--no-renames", "--format=", commits[0])
    else:
        base = c.task_base(p.root, b)
        numstat = (c.task_diff(p.root, base, "--numstat", "--no-renames") or "") if base else ""
    sizes = {}
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            sizes[parts[2]] = (int(parts[0]) if parts[0].isdigit() else 0, int(parts[1]) if parts[1].isdigit() else 0)
    files = sorted(sizes)
    texts = {}
    for f in files:  # ponytail: today's text of each file; read it at the commit if old tours start to mislead
        try:
            with open(os.path.join(p.root, f), encoding="utf-8", errors="replace") as fh:
                texts[f] = fh.read(200_000)
        except OSError:
            texts[f] = ""  # deleted
    usable = [g for g in files if not c.TESTISH.search(g) and len(_name_stem(g)) >= 4
              and _name_stem(g).lower() not in _COMMON_STEMS]  # a test uses code; "index" or "ui" names everything
    uses = {f: sorted(g for g in usable if g != f and re.search(rf"\b{re.escape(_name_stem(g))}\b", texts[f]))
            if _CODE.search(f) else [] for f in files}
    try:
        order = list(graphlib.TopologicalSorter(uses).static_order())
    except graphlib.CycleError:  # a cycle: the most-used first
        order = sorted(files, key=lambda f: (-sum(f in u for u in uses.values()), f))
    order = [f for f in order if _CODE.search(f)] + [f for f in order if not _CODE.search(f)]  # docs and data last
    first, touched = sorted(b.first_evidence().items()), c.task_touches(p, b.id)
    rows = []
    for f in order:
        at = touched.get(f)
        step = next((n for n, ts in first if at and ts >= at), None) if at else None
        add, rm = sizes.get(f, (0, 0))
        rows.append({"path": f, "add": add, "del": rm, "uses": uses[f], "step": step,
                     "deleted": not os.path.exists(os.path.join(p.root, f))})
    return rows


def cmd_tour(args):
    import fmcli
    p = fmcli.resolve(args)
    b = fmcli.need_brief(p, args.id)
    rows = tour(p, b)
    text = "\n".join(
        f"{i}. {r['path']}  +{r['add']} −{r['del']}" + (" (deleted)" if r["deleted"] else "")
        + (f"  step {r['step']}" if r["step"] else "") + (f"  — uses {', '.join(r['uses'])}" if r["uses"] else "")
        for i, r in enumerate(rows, 1))
    fmcli.out(args, {"id": b.id, "files": rows},
              c.plain_lines(f"{b.id} reading order (a file before the files that use it):\n{text}") if rows
              else f"{b.id}: no changes since it was focused.")


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


_SKIP = re.compile(r"@(unittest\.skip|pytest\.mark\.(skip|xfail))|\bpytest\.skip\(|\b(xit|xdescribe|xtest)\(|"
                   r"\.(skip|only)\(|\bt\.Skip\(|#\[ignore\]")
_ASSERT = re.compile(r"\bassert|\bexpect\(|\.should\b|\bt\.(Error|Fatal)")


def _tampering(diff):
    """R3: weakened tests in the diff — assertions or test files removed, skips/only added."""
    found, cur, removed = [], "", collections.Counter()
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            cur = line.rsplit(" b/", 1)[-1]
        elif line.startswith("deleted file mode") and _TEST.search(cur):
            found.append(f"test file deleted: {cur}")
        elif _TEST.search(cur) and line.startswith("-") and not line.startswith("---") and _ASSERT.search(line):
            removed[cur] += 1
        elif _TEST.search(cur) and line.startswith("+") and not line.startswith("+++") and _SKIP.search(line):
            found.append(f"test skipped or narrowed in {cur}: {c.fit(line[1:].strip(), 80)}")
    added = collections.Counter()
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            cur = line.rsplit(" b/", 1)[-1]
        elif line.startswith("+") and not line.startswith("+++") and _ASSERT.search(line):
            added[cur] += 1
    found += [f"{n} assertion(s) removed from {f} ({added[f]} added)" for f, n in removed.items() if n > added[f]]
    return found


_REMOVED_DEF = re.compile(r"^-(?:export\s+)?(?:async\s+)?(?:def|class|function|func|fn)\s+([A-Za-z]\w{2,})")


def _dangling(root, diff):
    """R3: public names the diff removed that the tree still mentions (a rename or delete left callers behind)."""
    removed = {m.group(1) for line in diff.splitlines() if (m := _REMOVED_DEF.match(line))}
    readded = {m.group(1) for line in diff.splitlines() if line.startswith("+")
               and (m := _REMOVED_DEF.match("-" + line[1:]))}
    found = []
    for name in sorted(removed - readded)[:10]:
        users = _git(root, "grep", "--untracked", "-l", "-w", "-I", "-e", name).splitlines()
        if users:
            found.append(f"removed {name} is still named in {', '.join(users[:4])}")
    return found


_GENERATED_PATH = re.compile(r"(^|/)(vendor|node_modules|third_party|dist|__generated__|generated)/|\.min\.(js|css)$|"
                             r"_pb2(_grpc)?\.py$|\.pb\.go$|\.generated\.\w+$|(^|/)(package-lock\.json|yarn\.lock)$")
_GENERATED_HEAD = re.compile(r"DO NOT EDIT|@generated|auto-?generated|generated by", re.I)


def is_generated(path):
    """R4: a file a tool writes (vendored, built, generated): hand edits get overwritten or drift from the source."""
    if _GENERATED_PATH.search(path.replace(os.sep, "/")):
        return True
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = "".join(next(f, "") for _ in range(5))
    except OSError:
        return False
    return bool(_GENERATED_HEAD.search(head))


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
    found += _tampering(diff) + _dangling(root, diff)
    if m and m.get("pairs"):  # R2: files that nearly always change together, one of them left out
        changed = set(files)
        for f in sorted(changed):
            missing = [b for b in m["pairs"].get(f, []) if b not in changed]
            if missing:
                found.append(f"{f} usually changes with {', '.join(missing)} (git history); check it needs no edit")
    found += [f"generated or vendored file edited: {f} (change its source or generator instead)" for f in files
              if is_generated(os.path.join(root, f))][:5]
    risky = c.sensitive(files, diff)
    if risky:
        found.append(f"security-sensitive: {', '.join(risky)} (adversary lens required)")
    return list(dict.fromkeys(found))[:30]


def changed(root, base):
    """Files changed since base (a commit, or a task's snapshot of the working files: T-0078), committed or not,
    untracked included, relative to root."""
    names = c.task_diff(root, base, "--name-only")
    if names is not None:
        return sorted(set(names.splitlines()))
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
