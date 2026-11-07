"""T-3316: headroom census. census(root) lists a project's bounded sets and caps, found from the code: module-level
UPPER_CASE ints >= 2 used as caps (compared with < > <= >=, passed to min/max, or a slice bound) and UPPER tuples/lists
of >= 3 strings (ast for .py, one regex per line for other languages); raised(root) reads `git log -p -U0` over 180 days
and counts, per (file, name), how often a constant's value went up. Never called from a hook (the git log is the cost,
so both results are cached in the project state: census per file by size+mtime, raised by HEAD sha and extended with
`git log <cached>..HEAD`; a cold first run on a big repo takes several seconds, a warm one well under 3); no CLI yet
(T-3328). A plain display slice like xs[:5] is not a cap: only a named constant is. A failing git raises HeadroomError."""
import ast
import hashlib
import json
import os
import re
import subprocess
import threading
import time

from . import core

OTHER = (".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".h", ".cpp", ".kt", ".swift", ".rb", ".sh")
SKIP = {"node_modules", "vendor", "third_party", "dist", "build", "site-packages", ".venv", "venv", "__pycache__"}
NUM = r"(0[xX][0-9a-fA-F_]+|\d[\d_]*)"
LEAD = r"^\s*(?:export\s+|(?:pub\s+)?(?:const|let|var|static|final)\s+(?:\w+\s+)?|#define\s+)*"
DEF = re.compile(LEAD + r"([A-Z][A-Z0-9_]+)\s*(?::[^=]+)?(?:=|\s)\s*" + NUM + r"\b")
DEF_ANY = re.compile(LEAD + r"[A-Z][A-Z0-9_]+\s*(?::[^=]+)?=?\s*\d", re.M)
USE = re.compile(r"(?<![=-])[<>]=?|\bmin\(|\bmax\(|\[[^\]]*:|:[^\]]*\]|\.slice\(|\.take\(")
TOP = re.compile(r"^[A-Z][A-Z0-9_]*(?::[^=\n]+)? = (?:[2-9]|\d\d|[(\[])", re.M)
GREP = r"^[[:space:]]*([#a-z]+[[:space:]]+)*[A-Z][A-Z0-9_]+[[:space:]]*(:[^=]+)?=?[[:space:]]*[0-9]"
LIMIT = 64 * 1024 * 1024
GLOBS = [":(glob)**/*" + e for e in (".py", ".js", ".ts", ".go", ".rs", ".java", ".c", ".h")]


class HeadroomError(RuntimeError):
    """git failed, timed out, or printed more than LIMIT bytes."""


def _git(root, *args, timeout=120):
    p = subprocess.Popen(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = threading.Timer(timeout, p.kill)
    timer.start()
    try:
        out = p.stdout.read(LIMIT + 1)
        p.wait()
    finally:
        timer.cancel()
        p.stdout.close()
        p.stderr.close()
    if len(out) > LIMIT:
        p.kill()
        raise HeadroomError(f"git {args[0]} printed over {LIMIT} bytes")
    if p.returncode != 0:
        raise HeadroomError(f"git {args[0]} failed (exit {p.returncode})")
    return out.decode("utf-8", "replace")


def _code(f):
    return (f.endswith(".py") or f.endswith(OTHER)) and not SKIP.intersection(f.split("/"))


def _files(root):
    return [f for f in _git(root, "ls-files").split("\n") if _code(f)]


def _num(s):
    try:
        return int(s.replace("_", ""), 0)
    except ValueError:
        return int(s.replace("_", "") or 0)  # 010 style: decimal


def _upper(node):
    return isinstance(node, ast.Name) and node.id.isupper()


def _py(path, text):
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return []
    consts, sets = {}, {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1:
            tgt, v = st.targets[0], st.value
        elif isinstance(st, ast.AnnAssign) and st.value is not None:
            tgt, v = st.target, st.value
        else:
            continue
        if not _upper(tgt):
            continue
        name = tgt.id
        if isinstance(v, ast.Constant) and type(v.value) is int and v.value >= 2:
            consts[name] = v.value
        elif isinstance(v, (ast.Tuple, ast.List)):
            m = [e.value for e in v.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            if len(m) >= 3 and len(m) == len(v.elts):
                sets[name] = m
    used = set()
    ordered = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)
    for n in ast.walk(tree):
        if isinstance(n, ast.Compare):
            ops = [n.left, *n.comparators]
            for i, op in enumerate(n.ops):
                if isinstance(op, ordered):
                    used |= {x.id for x in ops[i:i + 2] if _upper(x)}
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("min", "max"):
            used |= {x.id for x in n.args if _upper(x)}
        elif isinstance(n, ast.Slice):
            used |= {x.id for x in (n.lower, n.upper, n.step) if x is not None and _upper(x)}
    return ([{"name": k, "file": path, "kind": "cap", "value": v} for k, v in consts.items() if k in used]
            + [{"name": k, "file": path, "kind": "set", "members": m} for k, m in sets.items()])


def _other(path, text):
    lines = text.split("\n")
    out = []
    for i, ln in enumerate(lines):
        m = DEF.match(ln)
        if m and _num(m.group(2)) >= 2 and any(USE.search(o) for j, o in enumerate(lines)
                                               if j != i and m.group(1) in o):
            out.append({"name": m.group(1), "file": path, "kind": "cap", "value": _num(m.group(2))})
    return out


def _cache_path(root):
    key = hashlib.sha1(os.path.realpath(root).encode()).hexdigest()[:16]
    return os.path.join(core.state_dir(), "headroom", key + ".json")


def _load(root):
    try:
        with open(_cache_path(root), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _save(root, data):
    p = _cache_path(root)
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p + ".tmp", "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        os.replace(p + ".tmp", p)
    except OSError:
        pass  # a read-only state folder just means every run is cold


def census(root):
    cache = _load(root)
    seen, found, dirty = cache.get("census", {}), [], False
    fresh = {}
    for f in _files(root):
        try:
            st = os.stat(f"{root}/{f}")
        except OSError:
            continue
        sig = [st.st_size, st.st_mtime_ns]
        hit = seen.get(f)
        if hit and hit[0] == sig:
            fresh[f] = hit
            found += hit[1]
            continue
        dirty = True
        entries = []
        try:
            with open(f"{root}/{f}", encoding="utf-8") as fh:
                text = fh.read()
            ok = len(text) <= 300_000 and (TOP.search(text) if f.endswith(".py") else DEF_ANY.search(text))
            if ok:  # ponytail: skips generated/huge files and files with no top-level constant (the cost saver)
                entries = _py(f, text) if f.endswith(".py") else _other(f, text)
        except (OSError, UnicodeDecodeError):
            pass
        fresh[f] = [sig, entries]
        found += entries
    if dirty or len(fresh) != len(seen):
        _save(root, {**cache, "census": fresh})
    return found


def _events(log):
    """[(ts, file, name)] for each commit that removed `NAME = a` and added `NAME = b`, b > a, in one file."""
    out = []
    # a commit header starts its line; diff lines start with + - space or "@@ ", so a diff that adds this very line
    # (headroom.py's own history) can't split a commit in two (T-3316: IndexError on the repo's own log)
    for chunk in re.split(r"(?m)^@@commit ", log)[1:]:
        head, _, body = chunk.partition("\n")
        ts = int(head.split()[1])
        f, old = None, {}
        for ln in body.split("\n"):
            if ln.startswith("+++ b/"):
                f = ln[6:]
            elif ln.startswith("--- "):
                old = {}
            elif ln[:1] in "-+" and f and (m := DEF.match(ln[1:])):
                n = _num(m.group(2))
                if ln[0] == "-":
                    old[m.group(1)] = n
                elif n > old.get(m.group(1), n):
                    out.append([ts, f, m.group(1)])
    return out


def raised(root, entries=None, days=180):
    """{(file, NAME): times its value went up in the last `days`}; with `entries` (a census), only those caps."""
    head = _git(root, "rev-parse", "HEAD").strip()
    cache = _load(root)
    ev, last = cache.get("events", []), cache.get("head")
    if last != head:
        rng = [f"{last}..{head}"] if last and _git_ok(root, "merge-base", "--is-ancestor", last, head) else []
        if not rng:
            ev = []
        log = _git(root, "log", "-p", "-U0", f"-G{GREP}", "--pretty=format:@@commit %H %ct", "--no-color",
                   "--no-renames", "--diff-filter=M", "--no-merges", *([] if rng else [f"--since={days}.days"]),
                   *rng, "--", *GLOBS)
        ev = ev + [e for e in _events(log) if _code(e[1])]
        _save(root, {**cache, "head": head, "events": ev})
    cutoff = time.time() - days * 86400
    keep = {(e["file"], e["name"]) for e in entries} if entries is not None else None
    counts = {}
    for ts, f, name in ev:
        if ts >= cutoff and (keep is None or (f, name) in keep):
            counts[(f, name)] = counts.get((f, name), 0) + 1
    return counts


def _git_ok(root, *args):
    try:
        _git(root, *args)
        return True
    except HeadroomError:
        return False
