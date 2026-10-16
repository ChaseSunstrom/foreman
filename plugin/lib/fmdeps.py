"""Dependency-install check (T-1049): a package named in an npm/pip/cargo install that is new to the project gets a
typosquat, registry and age look before the command runs. Notes only: a wrong guess never blocks work, and the age
lookup fails open ("age unknown"), is skipped in sensitive projects and under FOREMAN_NO_NET=1."""
import json
import os
import re
import shlex
import time
import urllib.request
from datetime import datetime, timezone

import fmcore as c

YOUNG_DAYS = 14
MAX_FETCH = 3  # packages looked up per command; each lookup is at most 2 s
TOP = {
    "npm": "react lodash express axios chalk commander debug moment request typescript webpack eslint prettier jest "
           "vue next underscore async uuid dotenv jquery bluebird yargs rxjs tslib semver mkdirp glob minimist "
           "classnames zod vite".split(),
    "pypi": "requests numpy pandas flask django pytest boto3 urllib3 setuptools pyyaml scipy pillow click jinja2 "
            "cryptography sqlalchemy matplotlib certifi idna six pydantic fastapi httpx aiohttp redis tqdm black "
            "rich colorama".split(),
    "cargo": "serde serde_json tokio rand clap regex anyhow thiserror reqwest log syn quote itertools chrono "
             "lazy_static once_cell futures tracing bytes hyper".split(),
}
_NPM = {"npm", "pnpm", "yarn", "bun"}
_VERBS = {"npm": {"install", "i", "add"}, "pypi": {"install"}, "cargo": {"add", "install"}}
_REG_FLAGS = ("--registry", "--index-url", "--extra-index-url", "-i", "--index", "--find-links", "-f", "--git", "--path")
_VALUE_FLAGS = set(_REG_FLAGS) | {"-r", "--requirement", "-e", "--editable", "-c", "--constraint", "--target", "-t",
                                  "--prefix", "--tag", "-w", "--workspace", "--features", "-F", "--package", "-p",
                                  "--rev", "--branch", "--root", "--version", "--vers"}


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
    """(ecosystem, index after the verb) for an install-looking command, else None."""
    if not words:
        return None
    prog = os.path.basename(words[0])
    rest = words[1:]
    if prog in _NPM:
        eco = "npm"
    elif prog == "cargo":
        eco = "cargo"
    elif re.fullmatch(r"pip[0-9.]*", prog):
        eco = "pypi"
    elif prog in ("python", "python3") and rest[:2] == ["-m", "pip"]:
        eco, rest = "pypi", rest[2:]
        return (eco, len(words) - len(rest) + 1) if rest[:1] == ["install"] else None
    elif prog == "uv" and rest[:2] == ["pip", "install"]:
        return "pypi", 3
    else:
        return None
    return (eco, 2) if rest[:1] and rest[0] in _VERBS[eco] else None


def _name(eco, spec):
    if eco == "npm":
        m = re.match(r"(@[^/@]+/[^@]+|[^@]+)", spec)
    elif eco == "pypi":
        m = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", spec)
    else:
        m = re.match(r"[^@=<>~^\s]+", spec)
    return m.group(0).lower() if m else None


def parse_install(cmd):
    """[{eco, name, spec, registry}] for each package a command installs; registry is the custom-source reason or ''."""
    out = []
    for seg in re.split(r"&&|\|\||[;|\n]", cmd or ""):
        try:
            words = shlex.split(seg)
        except ValueError:
            continue
        while words and re.fullmatch(r"\w+=\S*|sudo|env|command", words[0]):
            words = words[1:]
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
            if flag in _REG_FLAGS and flag not in ("-r",):
                custom = custom or f"custom source {flag}"
            if w.startswith("-"):
                skip = flag in _VALUE_FLAGS and "=" not in w
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


def fetch_created(eco, name):
    """ISO creation time of a package from its registry, or None; raises on network failure (caller fails open)."""
    url = {"npm": f"https://registry.npmjs.org/{name}", "pypi": f"https://pypi.org/pypi/{name}/json",
           "cargo": f"https://crates.io/api/v1/crates/{name}"}[eco]
    req = urllib.request.Request(url, headers={"User-Agent": "foreman-deps-check", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=2) as r:
        d = json.load(r)
    if eco == "npm":
        return (d.get("time") or {}).get("created")
    if eco == "cargo":
        return (d.get("crate") or {}).get("created_at")
    ups = [f["upload_time_iso_8601"] for fs in (d.get("releases") or {}).values() for f in fs
           if f.get("upload_time_iso_8601")]
    return min(ups) if ups else None


def _days(iso):
    t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).days


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
        if n not in known and len(n) > 3:
            near = sorted(m for m in known if len(m) > 3 and lev1(n, m))
            if near:
                found.append({"kind": "typosquat", "package": n, "why": f"{n} is one edit from {near[0]}"})
        if net and not k["registry"] and looked < MAX_FETCH:
            looked += 1
            try:
                created = fetch(eco, n)
                if created and _days(created) < YOUNG_DAYS:
                    found.append({"kind": "age", "package": n, "why": f"{n} was first published {_days(created)} days ago"})
            except Exception:
                pass  # age unknown: fails open
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
