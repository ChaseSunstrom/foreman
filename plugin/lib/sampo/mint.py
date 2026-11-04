"""T-2978: scenarios minted in real repos. `sampo exam gen --from-repo PATH --n N --seed S` takes the repo's HEAD
(git archive, so the main checkout and its index are never touched), applies one deterministic mutation per candidate
in a throwaway copy, and keeps it only when the repo's own test command goes red on the mutant while the unmutated copy
passes twice. A mutant the tests miss is dropped and counted. A kept mutant is Louhi's seeded shape (repo/, key.json,
hidden/clean) with origin "minted", so `sampo exam run` grades it by the planted file and symbol."""
import ast
import fnmatch
import json
import os
import random
import re
import shlex
import shutil
import subprocess
import tarfile
import tempfile

from sampo import core as c

CAP_S = 120  # seconds one suite run may take; a run past it gives no verdict, and the mutant is skipped
SAMPLE = 40  # mutants tried per gen at most: the sample bound
GREEN_RUNS = 2  # the unmutated copy must pass this many times, or the repo is skipped as flaky
MAX_BYTES = 200_000  # bigger files are not mutated
SKIP_DIRS = (".git", "node_modules", "target", ".venv", "venv", "__pycache__")
DEP_DIRS = (".venv", "venv", "node_modules")  # T-2987: untracked deps linked into each copy, never copied or written
LANG = {".py": "python", ".js": "js", ".jsx": "js", ".mjs": "js", ".ts": "ts", ".tsx": "ts", ".rb": "ruby",
        ".rs": "rust", ".c": "c"}
DEFS_KEY = {"js": "js", "ts": "ts", "ruby": "rb", "rust": "rs", "c": "c"}  # louhi.DEFS, by language
TEST_PATH = re.compile(r"(^|/)(tests?|spec|__tests__)/|(^|/)(test_\w*|\w*_test|\w*\.test|\w*\.spec)\.\w+$")
CMP = {"<": ("<=", ">"), "<=": ("<", ">="), ">": (">=", "<"), ">=": (">", "<="), "==": ("!=",), "!=": ("==",),
       "===": ("!==",), "!==": ("===",)}
TOK_CMP = re.compile(r"(?<=\s)(===|!==|<=|>=|==|!=|<|>)(?=\s)")  # spaced on both sides: no generics, no arrows
DIGIT = re.compile(r"(?<![\w.])(\d)(?![\w.])")
BOUND_LINE = re.compile(r"\b(for|while|until|range|len|length|size|if|elif|unless)\b")
# T-3004: a bug report names what went red: without the command a model hunts the wrong suite in a big repo
REQUEST = ("The project's own tests went red after a recent change: `{cmd}` fails. Find what broke them and fix it; "
           "keep the tests as they are.")


def _sha(s):
    import hashlib
    return hashlib.sha1(s.encode()).hexdigest()


def _git(src, *args):
    r = subprocess.run(["git", "-C", src, *args], capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise ValueError(f"git {' '.join(args)} failed in {src}: {(r.stderr or r.stdout).strip()[:200]}")
    return r.stdout


def _files(root):
    out = []
    for d, dirs, names in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
        out += [os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/") for n in names]
    return sorted(out)


def _symbol(lines, ln, lang):
    """The function a line sits in: a Python def around it, or the nearest function header above it."""
    from sampo import louhi
    rx = re.compile(louhi.DEFS[DEFS_KEY[lang]])
    for i in range(ln - 1, -1, -1):
        if rx.search(lines[i]):
            m = re.search(r"\b(?:fn|function|def)\s+(\w+)|\bconst\s+(\w+)|\b(\w+)\s*\(", lines[i])
            return next((g for g in m.groups() if g), None) if m else None
    return None


def _span(lines, ln, a, b, pat):
    """The char span of a regex match between two UTF-8 byte offsets of one line (ast offsets are bytes)."""
    raw = lines[ln - 1].encode()
    if not 0 <= a <= b <= len(raw):
        return None
    m = re.search(pat, raw[a:b].decode())
    if not m:
        return None
    pre = len(raw[:a].decode())
    return pre + m.start(), pre + m.end()


def _cand(rel, lines, ln, start, end, old, new, op, symbol):
    before = lines[ln - 1]
    after = before[:start] + new + before[end:]
    key = _sha(f"{rel}:{ln}:{' '.join(before.split())}=>{' '.join(after.split())}")  # the normalized diff
    return {"rel": rel, "line": ln, "start": start, "end": end, "old": old, "new": new, "op": op, "symbol": symbol,
            "key": key}


def _candidates(rel, text):
    """Every mutant of one source file: a comparison flipped (python via ast, the rest by spaced tokens) or an
    integer bound (a 1 in a loop or bound line, or a 'so + 1' step) moved by one. Symbol-less lines are skipped."""
    lang = LANG[os.path.splitext(rel)[1]]
    lines, out = text.split("\n"), []
    if lang == "python":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            return []
        defs = [(n.lineno, n.end_lineno, n.name) for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 and \
                    node.left.end_lineno == node.lineno == node.comparators[0].lineno:
                span = _span(lines, node.lineno, node.left.end_col_offset, node.comparators[0].col_offset,
                             r"<=|>=|==|!=|<|>")
                if span:
                    old = lines[node.lineno - 1][span[0]:span[1]]
                    inside = [d for d in defs if d[0] <= node.lineno <= d[1]]
                    if inside and old in CMP:
                        for new in CMP[old]:
                            out.append(_cand(rel, lines, node.lineno, *span, old, new, "comparison",
                                             max(inside, key=lambda d: d[0])[2]))
            elif isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)) and \
                    isinstance(node.right, ast.Constant) and type(node.right.value) is int and node.right.value == 1 and \
                    node.left.end_lineno == node.lineno == node.right.lineno:
                span = _span(lines, node.lineno, node.left.end_col_offset, node.right.col_offset, r"[+-]")
                inside = [d for d in defs if d[0] <= node.lineno <= d[1]]
                if span and inside:
                    old = lines[node.lineno - 1][span[0]:span[1]]
                    new = "-" if old == "+" else "+"
                    out.append(_cand(rel, lines, node.lineno, *span, old, new, "off-by-one",
                                     max(inside, key=lambda d: d[0])[2]))
        return out
    for ln, line in enumerate(lines, 1):
        if len(line) > 300:
            continue
        symbol = _symbol(lines, ln, lang)
        if not symbol:
            continue
        for m in TOK_CMP.finditer(line):
            for new in CMP[m.group(1)]:
                out.append(_cand(rel, lines, ln, m.start(1), m.end(1), m.group(1), new, "comparison", symbol))
        if BOUND_LINE.search(line):
            for m in DIGIT.finditer(line):
                v = int(m.group(1))
                if 1 <= v <= 9:
                    for new in (v - 1, v + 1):
                        out.append(_cand(rel, lines, ln, m.start(1), m.end(1), m.group(1), str(new), "off-by-one",
                                         symbol))
    return out


def _apply(path, x):
    """Rewrite one token of one line in place; the old token must be where the candidate says."""
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    line = lines[x["line"] - 1]
    if line[x["start"]:x["end"]] != x["old"]:
        raise ValueError(f"{x['rel']}:{x['line']} changed since the mutant was made")
    lines[x["line"] - 1] = line[:x["start"]] + x["new"] + line[x["end"]:]
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))


def _unwrap(cmd):
    """T-2987: `uv run X` and its kin would re-sync the linked venv (repointing an editable install at the copy):
    run X itself, which the venv's bin, first on PATH, resolves."""
    return re.sub(r"^(?:uv|poetry|pipenv|pdm|hatch) run\s+", "", cmd)


def _deps(src, clean, target, files):
    """T-2987: real projects keep their deps out of git. Link the source's dependency dirs into the clean copy (every
    copy keeps the link; nothing installs or writes through it), put a linked venv's bin first on PATH, the copy's
    src and root first on PYTHONPATH (relative, so they name whichever copy runs: a mutant shadows an editable
    install), no bytecode written into the user's venv, and one cargo target for the run so a mutant rebuilds only
    its crate. The env, which grading uses too (the key's env)."""
    env = {"PYTHONDONTWRITEBYTECODE": "1"}
    for d in DEP_DIRS:
        if os.path.isdir(os.path.join(src, d)) and not os.path.lexists(os.path.join(clean, d)):
            os.symlink(os.path.join(src, d), os.path.join(clean, d))
            if os.path.isdir(os.path.join(src, d, "bin")):
                env["PATH"] = os.path.join(src, d, "bin") + os.pathsep + os.environ.get("PATH", "")
                env["VIRTUAL_ENV"] = os.path.join(src, d)
    if any(f.endswith(".py") for f in files):
        env["PYTHONPATH"] = "src:."
    if "Cargo.toml" in files:
        env["CARGO_TARGET_DIR"] = target
    return env


def _verdict(cmd, cwd, extra=None):
    """True when the repo's test command passes, False when it fails, None when it gives no verdict (a time cap
    or a launch error): a mutant with no verdict is skipped, never kept."""
    from sampo import bench, louhi  # the code run here is the repo's own: no forge, cloud or registry credentials
    try:
        r = subprocess.run(shlex.split(cmd), cwd=cwd, env={**louhi._model_env(bench), **(extra or {})},
                           capture_output=True, timeout=CAP_S, stdin=subprocess.DEVNULL)
    except (subprocess.TimeoutExpired, OSError):
        return None
    return r.returncode == 0


def _scenario(p, run, i, x, clean, cmd, src, head, env=None):
    from sampo import louhi
    sid = f"{run}-m{i:02d}"
    base = os.path.join(louhi.root(p), run, sid)
    shutil.copytree(clean, os.path.join(base, "repo"), symlinks=True)
    _apply(os.path.join(base, "repo", x["rel"]), x)
    shutil.copytree(clean, os.path.join(base, "hidden", "clean"), symlinks=True)
    split = "holdout" if louhi.holdout(sid) else "train"
    key = {"id": sid, "kind": "bug", "lang": LANG[os.path.splitext(x["rel"])[1]], "split": split, "origin": "minted",
           "author": "self", "request": REQUEST.format(cmd=cmd), "names": {}, "readings": [], "missing": [], "example": "",
           "done_ok": True, "claims": [], "rank": [], "commands": {"exec": cmd, "suite": ""},  # no @F@: no file to name
           "exec_t": CAP_S,  # grading gives the real suite the cap minting gave it (louhi's EXEC_T is for toy repos)
           "env": env or {},  # T-2987: the linked deps' PATH, PYTHONPATH and cargo target, as minting ran them
           "defects": [{"kind": "bug", "symbols": [x["symbol"]], "files": [os.path.basename(x["rel"])],
                        "text": f"{x['symbol']}() is wrong: the project's own tests catch it", "tf": False,
                        "check": {"type": "suite"}}],
           "mutation": {"file": x["rel"], "line": x["line"], "op": x["op"], "from": x["old"], "to": x["new"],
                        "source": src, "head": head}}
    c.write_atomic(os.path.join(base, "key.json"), json.dumps(key, indent=1))
    return {"id": sid, "kind": "bug", "lang": key["lang"], "split": split, "author": "self", "origin": "minted",
            "repo": os.path.join(base, "repo"), "request": REQUEST.format(cmd=cmd)}


def _sensitive(src):
    if c.detect_sensitive(src):
        return True
    pr = c.find_project(src)
    try:
        return bool(pr and c.read_meta(pr).get("sensitive"))
    except (c.CorruptState, OSError):
        return bool(pr)  # unreadable: judged sensitive, as the lake does


def gen(p, repo, n=6, seed=0, test_cmd=None, only=None):
    """Mint up to n scenarios from repo's HEAD into a new run under exam's root, against test_cmd or the repo's
    detected gate. Returns the run's meta."""
    from sampo import louhi, map as mapmod
    if not 1 <= n <= 50:
        raise ValueError("--n takes 1 to 50 with --from-repo")
    src = os.path.realpath(repo)
    if not os.path.isdir(src):
        raise ValueError(f"no repo at {repo}")
    if _sensitive(src):  # T-2995 review: a minted run's journal becomes training data; a sensitive repo never does
        raise ValueError(f"{repo} is a sensitive project; Sampo doesn't mint exam scenarios from it")
    head = _git(src, "rev-parse", "--verify", "HEAD").strip()
    with c.lock(p.dir):  # the run id is claimed under the lock, as in louhi.gen
        k = max([int(louhi.RUN_ID.fullmatch(r).group(1)) for r in louhi.runs(p)] or [0]) + 1
        run = f"s{seed}-{k:03d}"
        os.makedirs(os.path.join(louhi.root(p), run))
    tmp = tempfile.mkdtemp(prefix="fm-mint-")
    mint = {"tried": 0, "kept": 0, "missed": 0, "skipped": 0, "duplicates": 0, "candidates": 0, "mutations": [],
            "reason": "", "command": "", "head": head}
    scen = []
    try:
        clean = os.path.join(tmp, "clean")
        os.makedirs(clean)
        tar = os.path.join(tmp, "head.tar")
        _git(src, "archive", "-o", tar, "HEAD")
        with tarfile.open(tar) as t:
            t.extractall(clean, filter="data")
        os.remove(tar)
        files = _files(clean)
        cmd = test_cmd or next((g for g in mapmod._gates(clean, files, []) if re.search(r"test|pytest", g)), None)
        if not cmd:
            raise ValueError(f"no test command for {src}: a tests/run.py, a test script or a Makefile test target")
        cmd = _unwrap(cmd)
        env = _deps(src, clean, os.path.join(louhi.root(p), run, "target"), files)
        mint["command"] = cmd
        green = [_verdict(cmd, _copy(clean, tmp, f"green{i}"), env) for i in range(GREEN_RUNS)]
        if not all(green):
            mint["reason"] = "red or flaky at HEAD: the unmutated tests don't pass twice"
        else:
            cands, seen = [], set()
            for rel in files:
                if only and not fnmatch.fnmatch(rel, only):  # T-2987: one module of a big repo
                    continue
                if os.path.splitext(rel)[1] not in LANG or TEST_PATH.search(rel) or \
                        os.path.getsize(os.path.join(clean, rel)) > MAX_BYTES:
                    continue
                try:
                    with open(os.path.join(clean, rel), encoding="utf-8") as f:
                        text = f.read()
                except UnicodeDecodeError:  # not text: never mutated (a rewrite would change its bytes)
                    continue
                for x in _candidates(rel, text):
                    if x["key"] in seen:
                        mint["duplicates"] += 1
                    else:
                        seen.add(x["key"])
                        cands.append(x)
            mint["candidates"] = len(cands)
            random.Random(seed).shuffle(cands)  # the seed picks the order; the same seed mints the same list
            for x in cands:
                if mint["kept"] >= n or mint["tried"] >= SAMPLE:
                    break
                w = _copy(clean, tmp, f"w{mint['tried']}")
                _apply(os.path.join(w, x["rel"]), x)
                mint["tried"] += 1
                v = _verdict(cmd, w, env)
                shutil.rmtree(w, ignore_errors=True)
                if v is None:
                    mint["skipped"] += 1
                elif v:  # green on the mutant: the tests miss it, so it is dropped and counted
                    mint["missed"] += 1
                else:
                    mint["kept"] += 1
                    mint["mutations"].append(f"{x['rel']}:{x['line']} {x['old']}->{x['new']} ({x['op']})")
                    scen.append(_scenario(p, run, mint["kept"], x, clean, cmd, src, head, env))
            if not cands:
                mint["reason"] = "no mutable comparison or bound in the sources"
        meta = {"run": run, "seed": seed, "origin": "minted", "source": src, "head": head, "command": cmd, "n": n,
                "at": c.now(), "per_kind": 0, "langs": sorted({s["lang"] for s in scen}), "kinds": ["bug"],
                "split": "all", "author": "self", "scenarios": scen, "dropped": [], "minted": mint}
        c.write_atomic(os.path.join(louhi.root(p), run, "run.json"), json.dumps(meta, indent=1))
        return meta
    except BaseException:
        shutil.rmtree(os.path.join(louhi.root(p), run), ignore_errors=True)
        raise
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _copy(clean, tmp, name):
    dst = os.path.join(tmp, name)
    shutil.copytree(clean, dst, symlinks=True)
    return dst
