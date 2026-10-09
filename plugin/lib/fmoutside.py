"""The outside view (T-0278): fm landscape — what people want from coding-agent harnesses now, diffed against the
last scan (T-0237) — and fm deps — a project's dependencies against their registries' latest majors, with the
migration researched before it bites (T-0238). Stdlib only."""
import argparse
import glob
import http.client
import json
import os
import re
import subprocess
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import fmcore as c
import fmresearch

QUESTION = ("What do developers want from AI coding-agent harnesses and plugins (Claude Code, Codex, Cursor, Aider, "
            "Cline) that they say is missing or unreliable today ({month})? Name concrete capabilities and who asks "
            "for them.")
LANDSCAPE_DAYS = 30
_NOTE = re.compile(r"^(?:harness-)?landscape-(\d{8})(?:-\d+)?$")


def items(text):
    """The bullet and numbered lines of a note — fm research's or a hand-written one — with marks, bold and links
    stripped and cut at ' — ' (the claim, not its source); recall hits and an earlier diff section left out."""
    text = re.split(r"\n## (?:Since |First scan)", text or "", maxsplit=1)[0]
    text = re.sub(r"## (?:Already known|Possible conflicts).*?(?=\n## |\Z)", "", text, flags=re.S)
    text = re.sub(r"(?m)^(?:Against|Open):\n(?:[-*] .*\n?)*", "", text)  # review: claims, not what argues with them
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(?:[✓✗?]\s+)?(.+)$", line)
        if not m:
            continue
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1)).replace("**", "").split(" — ")[0].strip()
        if len(t) >= 12 and not t.startswith("("):
            out.append(c.fit(c.plain(t), 200))
    return out


def _same(a, b):
    """Two items about the same thing: ≥ 3 shared stems and half of the shorter one's (wordings differ across scans)."""
    import fmrecall
    x, y = set(fmrecall._tokens(a)), set(fmrecall._tokens(b))
    return len(x & y) >= 3 and len(x & y) >= 0.5 * min(len(x), len(y))


def _previous(p, exclude):
    d = os.path.join(p.dir, "research")
    names = sorted((m.group(1), n[:-3]) for n in (os.listdir(d) if os.path.isdir(d) else [])
                   if n.endswith(".md") and n[:-3] != exclude and (m := _NOTE.match(n[:-3])))
    return names[-1][1] if names else None


def cmd_landscape(args):
    import fmcli
    import fmrecall
    p = fmcli.resolve(args)
    last = c.read_meta(p).get("landscape_at")
    age = c.age_days(last)
    if args.if_due and age is not None and age < LANDSCAPE_DAYS:
        return fmcli.out(args, {"skipped": True, "last": last},
                         f"The landscape scan ran {str(last)[:10]}; the next is due after {LANDSCAPE_DAYS} days.")
    name = "landscape-" + time.strftime("%Y%m%d")
    prev = _previous(p, name)
    ask = argparse.Namespace(sub=None, fanout=args.fanout, model=args.model, quorum=None, timeout=args.timeout,
                             no_verify=args.no_verify, name=name, task=None, question=None, file=None)
    res, text, _ = fmresearch._ask(p, ask, QUESTION.format(month=time.strftime("%B %Y")))
    with open(res["path"], encoding="utf-8") as f:
        now_items = items(f.read())
    new, gone = now_items, []
    if prev:
        with open(os.path.join(p.dir, "research", prev + ".md"), encoding="utf-8", errors="replace") as f:
            before = items(f.read())
        new = [x for x in now_items if not any(_same(x, y) for y in before)]
        gone = [y for y in before if not any(_same(y, x) for x in now_items)]
    covered = {x: fmrecall.covered(x) for x in new}
    section = ([f"## Since {prev}" if prev else "## First scan (nothing to compare with)"]
               + [f"- new: {x}" + (f" (Foreman: fm {covered[x][0][0]})" if covered[x] else "") for x in new]
               + (["", "Gone (in the last scan, not this one):"] + [f"- {y}" for y in gone] if gone else []) + [""])
    with c.lock(p.dir):
        with open(res["path"], encoding="utf-8") as f:
            body = f.read()
        c.write_atomic(res["path"], body.rstrip("\n") + "\n\n" + c.defang(c.redact("\n".join(section))) + "\n")
        meta = c.read_meta(p)
        meta["landscape_at"] = c.now()
        c.write_meta(p, meta)
    lacking = [x for x in new if not covered[x]]
    fmcli.out(args, dict(res, previous=prev, new=new, gone=gone, lacking=lacking),
              text + f"\n  since {prev or 'nothing'}: {len(new)} new ({len(lacking)} Foreman lacks), {len(gone)} gone"
              + "".join(f"\n  lacks: {x}" for x in lacking[:5]))


# ---------------------------------------------------------------- deps

_REQ = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*(===|==|>=|~=|>)\s*v?([0-9][^\s,;#]*)([^;#\n]*)")
# T-0281: a cloned repo's manifest and a registry's answer are untrusted: names and versions reach the terminal and the
# research question only in these shapes
_NAME = re.compile(r"^(?:@[A-Za-z0-9][\w.-]*/)?[A-Za-z0-9][\w.-]{0,100}$")
_VERSION = re.compile(r"^v?\d[\w.+-]{0,40}$")


def _pip(m):
    """(name, version, capped): a lower bound (>=, >) caps the major only with an upper bound beside it — `>=2.0`
    already allows 23.x, so it is never behind (review)."""
    return m.group(1), m.group(3), m.group(2) not in (">=", ">") or "<" in m.group(4)


def _capped(spec):
    """npm/Cargo/poetry: caret, tilde and exact versions stay in their major; `>=`/`>` alone doesn't."""
    return not re.match(r"\s*>", spec) or "<" in spec
REGISTRY = {"pypi": ("FOREMAN_PYPI_URL", "https://pypi.org/pypi", "/{name}/json", ("info", "version")),
            "npm": ("FOREMAN_NPM_URL", "https://registry.npmjs.org", "/{name}/latest", ("version",)),
            "crates": ("FOREMAN_CRATES_URL", "https://crates.io/api/v1", "/crates/{name}", ("crate", "max_stable_version"))}


def _toml(path):
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def dependencies(root):
    """[(ecosystem, name, version, capped)] from requirements*.txt, pyproject.toml, package.json and Cargo.toml at the
    root — the version as written, and whether the spec keeps the dependency in that major."""
    out = []
    for path in sorted(glob.glob(os.path.join(root, "requirements*.txt"))):
        with open(path, encoding="utf-8", errors="replace") as f:
            out += [("pypi", *_pip(m)) for m in map(_REQ.match, f) if m]
    py = _toml(os.path.join(root, "pyproject.toml"))
    out += [("pypi", *_pip(m)) for m in map(_REQ.match, (py.get("project") or {}).get("dependencies") or []) if m]
    for n, v in ((py.get("tool") or {}).get("poetry", {}).get("dependencies") or {}).items():
        v = v.get("version", "") if isinstance(v, dict) else v
        if n != "python" and isinstance(v, str) and re.search(r"\d", v):
            out.append(("pypi", n, re.sub(r"^[^\d]*", "", v), _capped(v)))
    try:
        with open(os.path.join(root, "package.json"), encoding="utf-8") as f:
            pkg = json.load(f)
    except (OSError, ValueError):
        pkg = {}
    for key in ("dependencies", "devDependencies"):
        for n, v in (pkg.get(key) or {}).items() if isinstance(pkg, dict) else []:
            if isinstance(v, str) and re.match(r"^[\^~>=<v ]*\d", v):  # not git:, file:, workspace:, *, latest
                out.append(("npm", n, re.sub(r"^[\^~>=<v ]*", "", v), _capped(v)))
    cargo = _toml(os.path.join(root, "Cargo.toml"))
    for key in ("dependencies", "dev-dependencies"):
        for n, v in (cargo.get(key) or {}).items():
            v = v.get("version", "") if isinstance(v, dict) else v
            if isinstance(v, str) and re.search(r"\d", v):
                out.append(("crates", n, re.sub(r"^[^\d]*", "", v), _capped(v)))
    out = [(e, n, m.group(0), cap) for e, n, v, cap in out
           if isinstance(n, str) and _NAME.match(n) and (m := re.search(r"\d[\w.+-]{0,40}", v))]
    return list(dict.fromkeys(out))[:200]


def _major(v):
    m = re.match(r"\D*(\d+)", v or "")
    return int(m.group(1)) if m else None


def latest(eco, name, timeout=10):
    """(version, None) or (None, why) from the ecosystem's registry (its base URL overridable by environment)."""
    env, base, path, keys = REGISTRY[eco]
    url = os.environ.get(env, base).rstrip("/") + path.format(name=urllib.parse.quote(name, safe=""))
    u = urllib.parse.urlsplit(url)
    # an override (a mirror, a test) may be any https host or loopback http; nothing else (T-0281: no metadata or LAN
    # endpoint over plain http, no file:). ponytail: an https override isn't resolved and checked; pin it if it matters
    if not (fmresearch.public_https(url) or env in os.environ and (
            u.scheme == "https" or u.scheme == "http" and u.hostname in ("localhost", "127.0.0.1", "::1"))):
        return None, "not a public https URL (or a loopback override)"
    req = urllib.request.Request(url, headers={"User-Agent": "Foreman fm deps (dependency release check)",
                                               "Accept": "application/json"})
    try:  # review: redirects re-checked as public https, like fm research's fetch
        with urllib.request.build_opener(fmresearch._Redirect).open(req, timeout=timeout) as resp:
            data = json.loads(resp.read(2_000_000))
        for k in keys:
            data = data.get(k) if isinstance(data, dict) else None
        return (data, None) if isinstance(data, str) and _VERSION.match(data) else (None, "no usable version in the answer")
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException) as e:
        return None, c.fit(c.plain(str(getattr(e, "reason", e))), 60)


def _installed(root, eco, name):
    """The version installed here, read locally (no network), or None."""
    if eco == "pypi":
        try:
            import importlib.metadata
            return importlib.metadata.version(name)
        except Exception:  # not installed in this interpreter
            return None
    if eco == "npm":
        try:
            with open(os.path.join(root, "node_modules", name, "package.json"), encoding="utf-8") as f:
                return json.load(f).get("version")
        except (OSError, ValueError, AttributeError):
            return None
    return None


def call_sites(root, eco, name):
    """T-0594: ([file:line], [names used]) where the project imports the dependency, by git grep (local only)."""
    mod = re.escape(name.lower().replace("-", "_") if eco == "pypi" else name)
    pats = {"pypi": [rf"^\s*(from\s+{mod}(\.[\w.]+)?\s+import\s|import\s+{mod}\b)"],
            "npm": [rf"(require\(|from\s+|import\s+)['\"]{mod}(/[^'\"]*)?['\"]"],
            "crates": [rf"\buse\s+{mod}::"]}.get(eco, [])
    sites, names = [], set()
    for pat in pats:
        try:
            r = subprocess.run(["git", "-C", root, "grep", "-n", "-I", "-E", "-e", pat], capture_output=True, text=True,
                               timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        for line in r.stdout.splitlines()[:200]:
            path, n, text = (line.split(":", 2) + ["", ""])[:3]
            sites.append(f"{path}:{n}")
            m = re.search(r"import\s+(.+)$", text) if eco == "pypi" and text.lstrip().startswith("from") else None
            names.update(x.strip().split(" as ")[0] for x in (m.group(1).strip("() ").split(",") if m else []) if x.strip())
            try:
                with open(os.path.join(root, path), encoding="utf-8", errors="replace") as f:
                    names.update(re.findall(rf"\b{mod}\.(\w+)", f.read(200_000)))
            except OSError:
                pass
    return list(dict.fromkeys(sites)), sorted(names)


def _calls(p, args, fmcli):
    rows, lines = [], []
    for eco, name, want, _ in dependencies(p.root):
        sites, names = call_sites(p.root, eco, name)
        have = _installed(p.root, eco, name)
        rows.append({"name": name, "ecosystem": eco, "requires": want, "installed": have, "sites": sites,
                     "names": names})
        files = len({x.rsplit(":", 1)[0] for x in sites})
        lines.append(f"{name} (requires {want}, installed {have or 'not here'}): " + (
            f"{files} file(s) — {', '.join(sites[:5])}" + (f"; names used: {', '.join(names[:12])}" if names else "")
            if sites else "no import site (unused, or imported under another name)"))
    return fmcli.out(args, {"dependencies": rows}, "\n".join(lines) + (
        "\nBefore trusting docs for one of these, read the installed version's source or --help (planning.md R2)."
        if rows else "") if rows else "No dependencies found in requirements*.txt, pyproject.toml, package.json or Cargo.toml.")


def cmd_deps(args):
    import fmcli
    p = fmcli.resolve(args)
    if getattr(args, "calls", False):  # T-0594: local only, no registry lookups
        return _calls(p, args, fmcli)
    deps = dependencies(p.root)
    with ThreadPoolExecutor(8) as pool:
        found = list(pool.map(lambda d: latest(d[0], d[1]), deps))
    outdated, failed, uncapped = [], [], []
    for (eco, name, cur, capped), (new, why) in zip(deps, found):
        if new is None:
            failed.append({"name": name, "ecosystem": eco, "why": why})
        elif not capped:
            uncapped.append(name)
        elif _major(cur) is not None and _major(new) is not None and _major(new) > _major(cur):
            q = f"Migrating {name} from {_major(cur)}.x to {new}: what breaks and how to upgrade"
            outdated.append({"name": name, "ecosystem": eco, "current": cur, "latest": new, "question": q})
    asked = []
    if args.research:  # T-0238: the migration researched before it bites (each ask budgeted)
        for d in outdated[:args.research]:
            ask = argparse.Namespace(sub=None, fanout=2, model=args.model, quorum=None, timeout=args.timeout,
                                     no_verify=False, name=None, task=None, question=None, file=None)
            try:
                asked.append(fmresearch._ask(p, ask, d["question"])[0]["path"])
            except fmcli.UsageError as e:
                asked.append(f"failed: {d['name']}: {e}")
    fmcli.out(args, {"checked": len(deps), "outdated": outdated, "failed": failed, "uncapped": uncapped,
                     "researched": asked},
              f"{len(deps)} dependencies checked; {len(outdated)} behind a major"
              + "".join(f"\n  {d['name']} {d['current']} → {d['latest']} ({d['ecosystem']})\n    "
                        f"fm research ask \"{d['question']}\"" for d in outdated)
              + (f"\n  no upper bound (a new major installs as is): {', '.join(uncapped[:8])}" if uncapped else "")
              + (f"\n  not checked: {', '.join(x['name'] + ' (' + x['why'] + ')' for x in failed[:8])}" if failed else "")
              + "".join(f"\n  researched: {x}" for x in asked))
