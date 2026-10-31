"""fm prove --infra (T-2385, Mission 7): the ecosystem's own validator on each infra file, on a throwaway copy, offline.

A Dockerfile, compose file, Terraform folder, Helm chart, Kubernetes manifest, CI workflow, shell script or systemd unit
is checked by the tool its ecosystem ships (hadolint, docker compose config, terraform validate, helm lint, kubeconform,
actionlint, shellcheck, systemd-analyze verify). A tool that fails fails the file; one that isn't on PATH leaves the file
unproven, names the tool and files one capability-miss task (fm plugins find); Foreman installs nothing, downloads nothing
and runs no verb that touches an account (the CLASSES table holds validate-only verbs; fmcore._LIVE and the guard stay the
boundary for what a session may run). Exit 0 none failed and one passed, 1 one failed, 2 nothing checked."""
import fnmatch
import glob
import os
import re
import stat
import time

import fmcore as c

INFRA_T, INFRA_MAX = 300, 200  # seconds for the whole run (a tool gets fmfind.TOOL_T of them), and files run (the rest: unproven)
SCHEMAS_ENV = "KUBECONFORM_SCHEMAS"  # kubeconform fetches schemas over the network unless it has a local folder
SCHEMA_PATH = "{{.NormalizedKubernetesVersion}}-standalone{{.StrictSuffix}}/{{.ResourceKind}}{{.KindSuffix}}.json"
NOT_INSTALLED = re.compile(r"is not a docker command|unknown command|unknown docker command")  # a plugin docker lacks
BENIGN = re.compile(r"is not executable|No such file or directory")  # systemd: a unit's ExecStart binary lives elsewhere
HELM_PARTS = {"Chart.yaml", "values.yaml", "values.schema.json", "templates", "crds"}
GONE = {".git", "node_modules", "target", "__pycache__", ".venv", "venv", ".terraform"}
BAD = {"fail": 1, "pass": 0, "unchecked": 2}

# One class per ecosystem, first match wins for a file. card: the stack card whose detect globs name its files (skip:
# globs of that card's that aren't the validator's, e.g. .dockerignore); globs: its own where no card has them.
# unit: dir (one run per folder) or chart (one run per Chart.yaml's folder). {f}: the file, {d}: its folder, both
# relative to the copy's root; every argv is a check that reads files: no apply, plan, init, install, push or pull.
CLASSES = {
    "dockerfile": {"card": "docker", "skip": (".dockerignore",), "tool": "hadolint", "argv": ["hadolint", "{f}"]},
    "compose": {"globs": ("docker-compose*.yml", "docker-compose*.yaml", "compose.yml", "compose.yaml", "compose.*.yml",
                          "compose.*.yaml"), "tool": "docker compose",
                "argv": ["docker", "compose", "-f", "{f}", "config", "-q"]},
    "terraform": {"card": "terraform", "skip": ("*.tfvars", ".terraform.lock.hcl"), "tool": "terraform validate",
                  "unit": "dir", "argv": ["terraform", "-chdir={d}", "validate", "-no-color"]},
    "helm": {"globs": ("Chart.yaml",), "tool": "helm lint", "unit": "chart", "argv": ["helm", "lint", "{d}"]},
    "kubernetes": {"card": "kubernetes", "tool": "kubeconform",
                   "argv": ["kubeconform", "-strict", "-ignore-missing-schemas", "-schema-location", "{schemas}", "{f}"]},
    "workflow": {"card": "github-actions", "skip": (".github/actions/*/action.yml",), "tool": "actionlint",
                 "argv": ["actionlint", "{f}"]},
    "shell": {"card": "bash", "skip": (".shellcheckrc", "*.bats"), "tool": "shellcheck", "argv": ["shellcheck", "{f}"]},
    "systemd": {"card": "systemd", "tool": "systemd-analyze verify", "argv": ["systemd-analyze", "verify", "--man=no", "{f}"]},
}


def _signals(k):
    """[(kind, value)] from the class's card (its file: and ext: detect signals) and its own globs."""
    out = [("file", g) for g in k.get("globs", ())]
    if k.get("card"):
        import fmlib
        for path in glob.glob(os.path.join(fmlib.CARDS, "*", k["card"] + ".md")):
            try:
                with open(path, encoding="utf-8") as f:
                    detect = fmlib.parse(f.read()).get("detect") or []
            except OSError:
                continue
            out += [tuple(s.split(":", 1)) for s in detect if isinstance(s, str) and s.startswith(("file:", "ext:"))]
    return out


def _hit(sigs, rel):
    base, ext = os.path.basename(rel), os.path.splitext(rel)[1].lower()
    return any((kind == "ext" and ext == v.lower()) or (kind == "file" and fnmatch.fnmatchcase(rel if "/" in v else base, v))
               for kind, v in sigs)


def _regular(root, rel):
    try:
        return stat.S_ISREG(os.lstat(os.path.join(root, rel)).st_mode)
    except OSError:
        return False


def classify(root, only=None):
    """[(rel, class)] sorted: the tree's infra files, each in the first class that takes it. only (a list of repo-relative
    paths, e.g. what a task touched) narrows to those files, a Helm chart to the one a touched part of it belongs to.
    Symlinks and files inside .git, node_modules, .terraform and the like are left out."""
    import fmlib
    sel = {x.replace(os.sep, "/") for x in only} if only is not None else None
    files = sorted({f.replace(os.sep, "/") for f in fmlib._files(root)})
    files = [f for f in files if not GONE & set(f.split("/")[:-1])]
    sigs = {n: (_signals(k), _signals({"globs": k.get("skip", ())})) for n, k in CLASSES.items()}
    out = []
    for rel in files:
        name = next((n for n, (yes, no) in sigs.items() if _hit(yes, rel) and not (no and _hit(no, rel))), None)
        if not name or not _regular(root, rel):
            continue
        if sel is not None:
            if name == "helm":
                d = os.path.dirname(rel) or "."
                under = [f[len(d) + 1:] if d != "." else f for f in sel if d == "." or f.startswith(d + "/")]
                if not any(u.split("/")[0] in HELM_PARTS or u.startswith("values") for u in under):
                    continue
            elif rel not in sel:
                continue
        out.append((rel, name))
    return out


def _which(name, env, root):
    """The tool's path on the user's PATH (env's: absolute entries outside the tree), or None: a link into the tree is
    the tree's own file, not the user's tool."""
    import shutil
    exe = shutil.which(name, path=env["PATH"])
    if exe and os.path.commonpath([os.path.realpath(exe), root]) == root:
        return None
    return exe


def _first(text, n=3):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return c.fit(c.plain(" | ".join(lines[:n])), 240)


def infra(root, allowed=False, p=None, only=None):
    """{"root", "files": [{"file", "class", "tool", "verdict": pass|fail|unproven, "why"}], "verdict": fail|pass|unchecked}.
    allowed: the tree is trusted (terraform validate loads the folder's own provider plugins, the tree's code, so it
    runs only then). p: a Foreman project that gets one capability-miss task per missing tool. Nothing runs outside a
    throwaway copy of root; the environment is Foreman's minimal one (no credentials), HOME the copy's folder."""
    import fmfind
    import fmprove
    root = os.path.realpath(root)
    env, end = fmfind._tool_env(root), time.monotonic() + INFRA_T
    units, rows, held = {}, [], []

    def copy():
        if not held:
            held.append(fmprove._copy(root))  # ponytail: the whole tree, .terraform and all; a path list when copies hurt
        return held[0]

    def miss(name):
        if p:
            import fmeco
            fmeco.capture_once(p, f"Missing tool {name}: find it (fm plugins find {name}) or build it (script + test)\n"
                               f"capability-miss: {name}", "FEATURE", "self", key=f"capability-miss: {name}")

    def check(rel, name, k, n):
        d = os.path.dirname(rel) or "."
        exe = _which(k["argv"][0], env, root)
        if not exe:
            miss(k["argv"][0])
            return "unproven", f"{k['argv'][0]} is not on PATH (Foreman installs nothing: fm plugins find {k['argv'][0]})"
        schemas = os.environ.get(SCHEMAS_ENV, "")
        if name == "terraform":
            if not os.path.isdir(os.path.join(root, d, ".terraform")) or os.path.islink(os.path.join(root, d, ".terraform")):
                return "unproven", "the folder isn't initialised (terraform init downloads providers: run it yourself first)"
            if not allowed:
                return "unproven", ("terraform validate loads the folder's own provider plugins, the tree's code: "
                                    "fm prove --yes-run PATH says yes to the tree")
        if name == "helm":
            try:
                with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
                    deps = re.search(r"(?m)^dependencies:", f.read(1 << 16))
            except OSError:
                deps = None
            if deps and not os.path.isdir(os.path.join(root, d, "charts")):
                return "unproven", "the chart's dependencies aren't vendored (helm dependency build needs the network)"
        if name == "kubernetes" and not (os.path.isabs(schemas) and os.path.isdir(schemas)):
            return "unproven", (f"kubeconform fetches schemas over the network unless it has a local folder: set "
                                f"{SCHEMAS_ENV}=DIR to an absolute path (yannh/kubernetes-json-schema layout)")
        if n >= INFRA_MAX:
            return "unproven", f"over the {INFRA_MAX}-file cap of one run"
        if time.monotonic() >= end:
            return "unproven", f"time budget ({INFRA_T}s) spent"
        try:
            tmp, dst = copy()
        except (OSError, __import__("shutil").Error) as e:
            return "unproven", f"couldn't copy the tree: {c.fit(c.plain(str(e)), 120)}"
        safe = lambda x: "./" + x if x.startswith("-") else x  # noqa: E731  a file named -x is not an option
        argv = [exe] + [a.replace("{f}", safe(rel)).replace("{d}", d).replace("{schemas}", os.path.join(schemas, SCHEMA_PATH))
                        for a in k["argv"][1:]]
        out, err, rc, why = fmfind._run_tool(argv, dst, dict(env, HOME=tmp, NO_COLOR="1", CHECKPOINT_DISABLE="1",
                                                             TF_IN_AUTOMATION="1"))
        if why:
            return "unproven", f"{k['tool']} {why}"
        if rc == 0:
            return "pass", ""
        if NOT_INSTALLED.search(err):
            miss(k["tool"])
            return "unproven", f"{k['tool']} isn't installed ({_first(err, 1)})"
        bad = [l for l in (out + "\n" + err).splitlines() if l.strip() and not (name == "systemd" and BENIGN.search(l))]
        return ("fail", _first("\n".join(bad))) if bad else ("pass", "")

    try:
        for rel, name in classify(root, only):
            k = CLASSES[name]
            key = (name, os.path.dirname(rel)) if k.get("unit") else (name, rel)
            if key not in units:
                units[key] = check(rel, name, k, len(units))
            rows.append({"file": rel, "class": name, "tool": k["tool"], "verdict": units[key][0], "why": units[key][1]})
    finally:
        if held:
            import shutil
            shutil.rmtree(held[0][0], ignore_errors=True)
    got = {x["verdict"] for x in rows}
    return {"root": root, "files": rows, "verdict": "fail" if "fail" in got else "pass" if "pass" in got else "unchecked"}


def render(r):
    lines = [f"{x['verdict']:<8} {c.fit(c.plain(x['file']), 100)} [{x['tool']}]" + (f": {x['why']}" if x["why"] else "")
             for x in r["files"]]
    n = lambda v: sum(1 for x in r["files"] if x["verdict"] == v)  # noqa: E731
    return lines + [f"infra: {n('pass')} passed, {n('fail')} failed, {n('unproven')} unproven"
                    if r["files"] else "infra: no Dockerfile, compose, Terraform, Helm, Kubernetes, workflow, shell or "
                    "systemd file here"]


def cmd_infra(args, root):
    """fm prove --infra [PATH]: exit 0 none failed (one passed), 1 one failed, 2 nothing checked."""
    import fmprove
    if args.yes_run:
        try:
            fmprove.remember(root)
        except OSError as e:
            import sys
            print(f"fm prove: ran on your yes, but couldn't keep it for {root}: {c.plain(str(e))[:300]}", file=sys.stderr)
    p = c.find_project(os.getcwd())
    r = infra(root, args.yes_run or fmprove.trusted(root) or fmprove._lane_trusted(p, root), p=p)
    import fmcli
    fmcli.out(args, r, "\n".join(render(r)))
    return BAD[r["verdict"]]


def for_task(p, b, say=print):
    """(code, text) for fm task finish, or None: the infra files the task touched, proved. A missing validator is said
    (and filed once as a capability-miss), never installed; all-unproven records no run. A failing file refuses the close."""
    import fmmap
    import fmprove
    base = c.task_base(p.root, b) if c.git_root(p.root) else None
    touched = fmmap.changed(p.root, base) if base else []
    r = infra(p.root, fmprove.trusted(p.root) or fmprove._lane_trusted(p, p.root), p=p, only=touched) if touched else None
    if not r or not r["files"]:
        return None
    lines = render(r)
    for x, line in zip(r["files"], lines):
        if x["verdict"] == "unproven":
            say("infra: " + line)
    return None if r["verdict"] == "unchecked" else (BAD[r["verdict"]], "\n".join(lines))
