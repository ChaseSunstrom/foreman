"""Dependency-install check (T-1049): a package named in an npm/pip/cargo install that is new to the project gets a
typosquat, registry and age look before the command runs. Notes only: a wrong guess never blocks work (the hook has a
5 s limit, so all lookups share one ~1.2 s budget). The age lookup fails open ("age unknown") and is skipped in
sensitive projects, under FOREMAN_NO_NET=1 (the off switch: no registry is contacted at all), for popular and
@scoped names, and wherever a registry is configured (.npmrc, pip.conf, PIP_*INDEX_URL, cargo [registries]/[source])."""
import json
import os
import re
import shlex
import socket
import threading
import time
import urllib.request
from datetime import datetime, timezone

import fmcore as c

YOUNG_DAYS = 14
MAX_FETCH = 2  # packages looked up per command
BUDGET = 1.2  # seconds, all lookups together
TOP = {
    "npm": "react lodash express axios chalk commander debug moment request typescript webpack eslint prettier jest "
           "vue next underscore async uuid dotenv jquery bluebird yargs rxjs tslib semver mkdirp glob minimist "
           "classnames zod vite".split(),
    "pypi": "requests numpy pandas flask django pytest boto3 urllib3 setuptools pyyaml scipy pillow click jinja2 "
            "cryptography sqlalchemy matplotlib certifi idna six pydantic fastapi httpx aiohttp redis tqdm black "
            "rich colorama".split(),
    "crates": "serde serde_json tokio rand clap regex anyhow thiserror reqwest log syn quote itertools chrono "
              "lazy_static once_cell futures tracing bytes hyper".split(),
}
LEGIT = {"boto", "pyaml"}  # real packages one edit from a popular one
_NPM = {"npm", "pnpm", "yarn", "bun"}
_VERBS = {"npm": {"install", "i", "add"}, "pypi": {"install", "add"}, "crates": {"add", "install"}}
# per ecosystem: flags that take a value, and the ones that name a non-registry source
_VALUE = {"npm": {"--registry", "--prefix", "--tag", "-w", "--workspace", "--omit", "--include", "--cache",
                  "--userconfig", "--loglevel", "--save-prefix", "--cwd", "--dir", "-C", "--filter"},
          "pypi": {"--index-url", "-i", "--extra-index-url", "-f", "--find-links", "-r", "--requirement", "-e",
                   "--editable", "-c", "--constraint", "-t", "--target", "--trusted-host", "--prefix", "--root",
                   "--python", "--platform", "--only-binary", "--no-binary", "--proxy", "--cert", "--src", "--group",
                   "--index", "--default-index", "--python-version", "--implementation", "--abi", "-p", "--python-version"},
          "crates": {"--git", "--path", "--registry", "--index", "--rev", "--branch", "--tag", "--features", "-F",
                     "--package", "-p", "--root", "--version", "--vers", "--bin", "--example", "--profile", "--target",
                     "--target-dir", "-j", "--jobs", "--manifest-path", "--rename", "--color"}}
_CUSTOM = {"npm": {"--registry"},
           "pypi": {"--index-url", "-i", "--extra-index-url", "-f", "--find-links", "--index", "--default-index"},
           "crates": {"--git", "--path", "--registry", "--index"}}


def lev1(a, b):
    """True when a and b differ by one insert, delete, substitution or adjacent swap (not equal)."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        d = [i for i in range(len(a)) if a[i] != b[i]]
        return len(d) == 1 or (len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]])
    s, l = sorted((a, b), key=len)
    return any(l[:i] + l[i + 1:] == s for i in range(len(l)))


def _eco(words):
    """(ecosystem, index of the first argument after the verb) for an install-looking command, else None."""
    if not words:
        return None
    prog, rest = os.path.basename(words[0]), words[1:]
    if prog in _NPM:
        i = 2 if rest[:1] == ["global"] else 1  # yarn global add
        return ("npm", i + 1) if rest[i - 1:i] and rest[i - 1] in _VERBS["npm"] else None
    if prog == "cargo":
        return ("crates", 2) if rest[:1] and rest[0] in _VERBS["crates"] else None
    if re.fullmatch(r"pip[0-9.]*", prog):
        return ("pypi", 2) if rest[:1] == ["install"] else None
    if re.fullmatch(r"python[0-9.]*", prog) and rest[:2] == ["-m", "pip"]:
        return ("pypi", 4) if rest[2:3] == ["install"] else None
    if prog == "uv":
        if rest[:2] == ["pip", "install"]:
            return "pypi", 3
        return ("pypi", 2) if rest[:1] == ["add"] else None
    if prog == "poetry":
        return ("pypi", 2) if rest[:1] == ["add"] else None
    if prog == "pipx":
        return ("pypi", 2) if rest[:1] == ["install"] else None
    return None


def _name(eco, spec):
    if eco == "npm":
        m = re.match(r"(@[^/@]+/[^@]+|[^@]+)", spec)
    elif eco == "pypi":
        m = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", spec)
    else:
        m = re.match(r"[^@=<>~^\s]+", spec)
    return m.group(0).lower() if m else None


def parse_install(cmd, _depth=0):
    """[{eco, name, spec, registry}] for each package a command installs; registry is the custom-source reason or ''."""
    out = []
    for seg in re.split(r"&&|\|\||[;|\n]", cmd or ""):
        try:
            words = shlex.split(seg)
        except ValueError:
            continue
        while words and re.fullmatch(r"\w+=\S*|sudo|env|command", words[0]):
            words = words[1:]
        if _depth < 2 and len(words) > 2 and os.path.basename(words[0]) in ("bash", "sh", "zsh") and words[1] == "-c":
            out += parse_install(words[2], _depth + 1)
            continue
        hit = _eco(words)
        if not hit:
            continue
        eco, i = hit
        custom, specs, skip = "", [], False
        for w in words[i:]:
            if skip:
                skip = False
                continue
            flag = w.split("=", 1)[0]
            if flag in _CUSTOM[eco]:
                custom = custom or f"custom source {flag}"
            if w.startswith("-"):
                skip = flag in _VALUE[eco] and "=" not in w
            else:
                specs.append(w)
        for s in specs:
            if re.match(r"(git\+|https?://|file:|git@|\.{0,2}/)", s) or s.startswith(("github:", "git:")):
                out.append({"eco": eco, "name": None, "spec": s, "registry": f"{s[:60]} is not a registry package"})
                continue
            n = _name(eco, s)
            if n:
                out.append({"eco": eco, "name": n, "spec": s, "registry": custom})
    return out


def manifest_names(p):
    try:
        import fmoutside
        return {(e, n.lower()) for e, n, *_ in fmoutside.dependencies(p.root)}
    except Exception:
        return set()


def _grep(paths, pat):
    for f in paths:
        try:
            with open(os.path.expanduser(f), encoding="utf-8", errors="replace") as fh:
                if re.search(pat, fh.read(), re.M):
                    return True
        except OSError:
            pass
    return False


def configured_registry(p, eco):
    """True when this project or machine points the ecosystem at a registry of its own: the name would leak to it, and
    the public one wouldn't know it."""
    r = p.root
    if eco == "npm":
        return _grep([f"{r}/.npmrc", "~/.npmrc", f"{r}/.yarnrc.yml", "~/.yarnrc"], r"registry")
    if eco == "pypi":
        return bool(os.environ.get("PIP_INDEX_URL") or os.environ.get("PIP_EXTRA_INDEX_URL")) or _grep(
            [f"{r}/pip.conf", "~/.config/pip/pip.conf", "~/.pip/pip.conf", "/etc/pip.conf", f"{r}/uv.toml",
             "~/.config/uv/uv.toml"], r"index")
    return _grep([f"{r}/.cargo/config.toml", f"{r}/.cargo/config", "~/.cargo/config.toml", "~/.cargo/config"],
                 r"^\s*\[(registries|source)")


def _get(url, accept="application/json"):
    import fmresearch  # its redirect handler re-checks every hop as public https
    req = urllib.request.Request(url, headers={"User-Agent": "foreman-deps-check", "Accept": accept})
    with urllib.request.build_opener(fmresearch._Redirect).open(req, timeout=BUDGET) as r:
        return json.loads(r.read(2_000_000))


def fetch_created(eco, name):
    """ISO creation time of a package from its public registry, or None; raises on network failure (caller fails open).
    Runs in a worker thread, so the socket default timeout is set here (DNS ignores urlopen's)."""
    socket.setdefaulttimeout(BUDGET)
    if eco == "npm":
        # the abbreviated document is small and has "modified": older than the window means the package is too
        small = _get(f"https://registry.npmjs.org/{name}", "application/vnd.npm.install-v1+json")
        if small.get("modified") and _days(small["modified"]) >= YOUNG_DAYS:
            return small["modified"]
        return (_get(f"https://registry.npmjs.org/{name}").get("time") or {}).get("created")
    if eco == "crates":
        return (_get(f"https://crates.io/api/v1/crates/{name}").get("crate") or {}).get("created_at")
    d = _get(f"https://pypi.org/pypi/{name}/json")
    ups = [f["upload_time_iso_8601"] for fs in (d.get("releases") or {}).values() for f in fs
           if f.get("upload_time_iso_8601")]
    return min(ups) if ups else None


def _days(iso):
    t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).days


def _timed(fetch, eco, name, deadline):
    """fetch(eco, name) in a worker thread abandoned at the deadline; None when it ran out, failed or found nothing."""
    box = []

    def run():
        try:
            box.append(fetch(eco, name))
        except Exception:
            pass  # age unknown: fails open
    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(max(0.0, deadline - time.monotonic()))
    return box[0] if box else None


def check(p, cmd, fetch=None):
    """Findings [{kind: typosquat|registry|age, package, why}] for the packages `cmd` installs that the project's
    manifests don't already have."""
    pkgs = parse_install(cmd)
    if not pkgs:
        return []
    have = manifest_names(p)
    try:
        net = not os.environ.get("FOREMAN_NO_NET") and not c.read_meta(p).get("sensitive")
    except Exception:
        net = False
    fetch = fetch or fetch_created
    deadline = time.monotonic() + BUDGET
    found, looked = [], 0
    for k in pkgs:
        eco, n = k["eco"], k["name"]
        if k["registry"] and n is None:
            found.append({"kind": "registry", "package": k["spec"], "why": k["registry"]})
            continue
        if (eco, n) in have:
            continue
        if k["registry"]:
            found.append({"kind": "registry", "package": n, "why": k["registry"]})
        known = set(TOP[eco]) | {m for e, m in have if e == eco}
        if n not in known and n not in LEGIT and len(n) > 3:
            near = sorted(m for m in known if len(m) > 3 and lev1(n, m))
            if near:
                found.append({"kind": "typosquat", "package": n, "why": f"{n} is one edit from {near[0]}"})
        if (net and not k["registry"] and looked < MAX_FETCH and n not in TOP[eco] and not n.startswith("@")
                and time.monotonic() < deadline and not configured_registry(p, eco)):
            looked += 1
            created = _timed(fetch, eco, n, deadline)
            try:
                if created and _days(created) < YOUNG_DAYS:
                    found.append({"kind": "age", "package": n, "why": f"{n} was first published {_days(created)} days ago"})
            except (ValueError, TypeError):
                pass
    return found


def note(p, cmd):
    f = check(p, cmd)
    if not f:
        return None
    return "Foreman: install check (a note, not a block): " + "; ".join(
        f"{x['kind']}: {x['why']}" for x in f[:4]) + ". Make sure these are the packages meant."


def cmd_deps(args):
    import fmcli
    p = fmcli.resolve(args)
    cmd = " ".join(args.words[1:])
    f = check(p, cmd)
    fmcli.out(args, {"command": cmd, "findings": f},
              "\n".join(f"{x['kind']}: {x['package']}: {x['why']}" for x in f) or "No install concerns found.")
    return 0
