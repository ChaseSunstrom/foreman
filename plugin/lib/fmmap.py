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
