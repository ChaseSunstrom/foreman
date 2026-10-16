"""fm release VERSION (T-1188): release.py's ritual as named steps with a checkpoint after each (state/release.json),
so `--resume` continues from the first unfinished one and `--dry-run` only prints the plan. Foreman's own repo only
(release.py at its root). --push merges into origin's main from a temporary worktree behind the active task's
publish grant, which the push spends."""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

import fmcore as c

FM = [sys.executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "fm")]
STEPS = [("tree", "the working tree is clean"),
         ("check", "fm check passes (the full gates)"),
         ("bump", "plugin.json, both marketplace.json entries, and foreman-ui's version when it changed"),
         ("changelog", "CHANGELOG.md's Unreleased entries are headed VERSION"),
         ("commit", "commit 'Foreman VERSION' with the Foreman-Task trailer"),
         ("release-check", "fm release-check: doctor and demo in a temporary HOME"),
         ("canary", "fm sentinel in every local project (reported, never fatal)"),
         ("push", "--push: merge into origin's main (--no-ff) from a temporary worktree, push; spends the publish grant"),
         ("round", "fm round close: tag HEAD round-N")]
MARK = r"^Foreman [0-9]+\.[0-9]+\.[0-9]+"  # a release commit's subject


def _err(msg):
    import fmcli
    raise fmcli.UsageError(msg)


def _git(root, *a, ok=False):
    r = c._git(root, *a, timeout=300, proc=True)
    if r.returncode and not ok:
        _err(f"git {' '.join(a)} failed: {(r.stderr or r.stdout).strip()[:300]}")
    return r.stdout


def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _dump(path, data):
    c.write_atomic(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def _grant(p):
    """The active task, when it holds the publish grant; else None."""
    b = c.active_brief_fast(p, p.lane)
    return b if b and "publish" in (b.meta.get("allow") or []) else None


def _spend(p, tid):
    with c.lock(p.dir):
        b = c.find_brief(p, tid)
        b.meta["allow"] = [x for x in b.meta.get("allow") or [] if x != "publish"]
        b.append_log("publish grant used by fm release --push")
        c.save_brief(p, b)


def _gate(root, verb):
    if subprocess.run([*FM, verb], cwd=root).returncode:
        _err(f"fm {verb} failed")


def _ui_changed(root):
    last = _git(root, "log", "-1", "--format=%H", "-E", f"--grep={MARK}").strip()
    return bool(_git(root, "diff", "--name-only", f"{last}..HEAD" if last else "HEAD", "--", "mods/foreman-ui").strip())


def _bump(ctx):
    root, v, ui = ctx["root"], ctx["version"], ctx["ui"]
    if ui is None and _ui_changed(root):
        _err("mods/foreman-ui changed since the last release: pass --ui VERSION")
    pj = os.path.join(root, "plugin", ".claude-plugin", "plugin.json")
    mk = os.path.join(root, ".claude-plugin", "marketplace.json")
    uj = os.path.join(root, "mods", "foreman-ui", ".claude-plugin", "plugin.json")
    text, data = open(pj, encoding="utf-8").read(), _json(mk)  # everything read before anything is written
    if ui and not os.path.isfile(uj):
        _err("no mods/foreman-ui to give --ui to")
    data.setdefault("metadata", {})["version"] = v
    for e in data.get("plugins", []):
        if e.get("name") == "foreman":
            e["version"] = v
        elif e.get("name") == "foreman-ui" and ui:
            e["version"] = ui
    open(pj, "w", encoding="utf-8").write(re.sub(r'"version": "[^"]*"', f'"version": "{v}"', text, 1))
    _dump(mk, data)
    if ui:
        t = open(uj, encoding="utf-8").read()
        open(uj, "w", encoding="utf-8").write(re.sub(r'"version": "[^"]*"', f'"version": "{ui}"', t, 1))


def _changelog(ctx):
    import datetime
    path = os.path.join(ctx["root"], "CHANGELOG.md")
    text = open(path, encoding="utf-8").read()
    if re.search(rf"(?m)^## {re.escape(ctx['version'])} ", text):
        return  # a resumed run
    if "## Unreleased\n" not in text:
        _err("CHANGELOG.md has no '## Unreleased' heading")
    head = f"## Unreleased\n\n## {ctx['version']} — {datetime.date.today().isoformat()}\n"
    open(path, "w", encoding="utf-8").write(text.replace("## Unreleased\n", head, 1).replace(head + "\n", head, 1))


def _commit(ctx):
    root, v = ctx["root"], ctx["version"]
    if _git(root, "log", "-1", "--format=%s").strip() == f"Foreman {v}":
        return
    files = ["plugin/.claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "CHANGELOG.md"]
    if ctx["ui"]:
        files.append("mods/foreman-ui/.claude-plugin/plugin.json")
    _git(root, "add", *files)
    b = c.active_brief_fast(ctx["p"], ctx["p"].lane)
    _git(root, "commit", "-qm", f"Foreman {v}", *(["--trailer", f"Foreman-Task: {b.id}"] if b else []))


def _canary(ctx):
    spec = importlib.util.spec_from_file_location("fm_release_py", os.path.join(ctx["root"], "release.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.FM = FM
    mod.canary()


def _push(ctx):
    root, v, p = ctx["root"], ctx["version"], ctx["p"]
    if not ctx["push"]:
        print("  (no --push: nothing published)")
        return
    b = _grant(p)
    if not b:
        _err("--push needs the active task's publish grant (fm ask ID publish)")
    sha = _git(root, "rev-parse", "HEAD").strip()
    _git(root, "fetch", "-q", "origin", "main")
    with tempfile.TemporaryDirectory() as tmp:
        wt = os.path.join(tmp, "rel")
        _git(root, "worktree", "add", "-q", "--detach", wt, "origin/main")
        try:
            _git(wt, "merge", "-q", "--no-ff", sha, "-m", f"Foreman {v}")
            _git(wt, "push", "-q", "origin", "HEAD:main")
        finally:
            _git(root, "worktree", "remove", "--force", wt, ok=True)
    _spend(p, b.id)
    print(f"  pushed Foreman {v} to origin main")


def _round(ctx):
    import argparse
    import fmcli
    fmcli.cmd_round(argparse.Namespace(**{**vars(ctx["args"]), "action": "close"}))


def run(p, args):
    v = args.version
    if not re.fullmatch(r"\d+\.\d+\.\d+", v):
        _err("VERSION is MAJOR.MINOR.PATCH, e.g. 1.2.20")
    root = c.git_root(p.root)
    if not root or not os.path.isfile(os.path.join(root, "release.py")):
        _err("fm release runs in Foreman's own repo (no release.py here)")
    if args.dry_run:
        print(f"fm release {v}: {len(STEPS)} steps, a checkpoint after each (--resume continues)")
        for i, (name, what) in enumerate(STEPS, 1):
            print(f"  {i}. {name}: {what}")
        return 0
    if args.push and not _grant(p):
        _err("--push needs the active task's publish grant (fm ask ID publish); nothing was changed")
    state_path = os.path.join(p.dir, "release.json")
    state = _json(state_path) if os.path.isfile(state_path) else None
    if args.resume:
        if not state or state.get("version") != v:
            _err(f"no unfinished release of {v} to resume" + (f" (the one in progress is {state['version']})" if state else ""))
    else:
        cur = _json(os.path.join(root, "plugin", ".claude-plugin", "plugin.json"))["version"]
        if tuple(map(int, v.split("."))) <= tuple(map(int, cur.split("."))):
            _err(f"{v} isn't newer than {cur}")
        state = {"version": v, "done": []}
    ctx = {"root": root, "version": v, "ui": args.ui, "push": args.push, "p": p, "args": args}

    def tree(_):
        if _git(root, "status", "--porcelain").strip():
            _err("the tree has uncommitted changes; commit or finish them first")

    fns = {"tree": tree, "check": lambda _: _gate(root, "check"), "bump": _bump, "changelog": _changelog,
           "commit": _commit, "release-check": lambda _: _gate(root, "release-check"), "canary": _canary,
           "push": _push, "round": _round}
    gates = {"check", "release-check", "canary"}
    todo = [i for i, (n, _) in enumerate(STEPS) if n not in state["done"]]
    if not todo:
        print(f"Foreman {v} is already released: every step is done")
        return 0
    if args.resume:
        print(f"resuming at step {todo[0] + 1} ({STEPS[todo[0]][0]})")
    for i in todo:
        name = STEPS[i][0]
        print(f"step {i + 1}/{len(STEPS)} {name}")
        if args.no_check and name in gates:
            print("  skipped (--no-check)")
        else:
            try:
                fns[name](ctx)
            except Exception as e:
                state_note = f"stopped at step {i + 1} ({name}); fix it, then: fm release {v} --resume"
                _dump(state_path, state)
                if type(e).__name__ == "UsageError":
                    raise type(e)(f"step {i + 1} {name}: {e}\n{state_note}")
                raise
        state["done"].append(name)
        _dump(state_path, state)
    print(f"Foreman {v} released: all {len(STEPS)} steps done")
    return 0
