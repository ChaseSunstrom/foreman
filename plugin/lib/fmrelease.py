"""fm release VERSION (T-1188): the release ritual as named steps with a checkpoint after each (state/release.json),
so `--resume` continues from the first unfinished one and `--dry-run` only prints the plan. Foreman's own repo only
(plugin/.claude-plugin/plugin.json at its root; release.py is a thin wrapper over this). --push merges into the
remote's main (origin by default) from a temporary worktree behind the active task's publish grant, which it spends
before the push. The first run's flags (--ui, --push, --remote, --no-check) are kept in release.json for a resume;
a skipped step is never recorded as done, and a release with skipped gates can't push."""
import json
import os
import re
import subprocess
import sys
import tempfile

import fmcore as c

# FOREMAN_RELEASE_FM: tests point the gates and the canary at a stub fm
FM = [sys.executable, os.environ.get("FOREMAN_RELEASE_FM") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "fm")]
STEPS = [("tree", "the working tree is clean"),
         ("check", "fm check passes (the full gates)"),
         ("bump", "plugin.json, both marketplace.json entries, and foreman-ui's version when it changed"),
         ("changelog", "CHANGELOG.md's Unreleased entries are headed VERSION"),
         ("commit", "commit 'Foreman VERSION' with the Foreman-Task trailer"),
         ("release-check", "fm release-check: doctor and demo in a temporary HOME"),
         ("canary", "fm sentinel in every local project (reported, never fatal)"),
         ("push", "--push: merge into the remote's main (--no-ff) from a temporary worktree, push; spends the publish grant"),
         ("round", "fm round close: tag HEAD round-N")]
GATES = ("check", "release-check", "canary")
MARK = r"^Foreman [0-9]+\.[0-9]+\.[0-9]+"  # a release commit's subject
SEMVER = r"\d+\.\d+\.\d+"


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


def _setver(path, v):
    text = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(re.sub(r'"version": "[^"]*"', lambda _: f'"version": "{v}"', text, 1))


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
        c.log_event(p, "grant_spent", task=tid, data={"allow": "publish", "by": "fm release --push"})


def _gate(root, verb):
    if subprocess.run([*FM, verb], cwd=root).returncode:
        _err(f"fm {verb} failed")


def _ui_changed(root):
    last = _git(root, "log", "-1", "--format=%H", "-E", f"--grep={MARK}").strip()
    return bool(_git(root, "diff", "--name-only", f"{last}..HEAD" if last else "HEAD", "--", "mods/foreman-ui").strip())


def _bump(ctx):
    root, v, ui, old = ctx["root"], ctx["version"], ctx["ui"], ctx["old"]
    if ui is None and _ui_changed(root):
        _err("mods/foreman-ui changed since the last release: pass --ui VERSION")
    pj = os.path.join(root, "plugin", ".claude-plugin", "plugin.json")
    mk = os.path.join(root, ".claude-plugin", "marketplace.json")
    uj = os.path.join(root, "mods", "foreman-ui", ".claude-plugin", "plugin.json")
    data = _json(mk)  # everything read before anything is written
    if ui and not os.path.isfile(uj):
        _err("no mods/foreman-ui to give --ui to")
    meta = data.get("metadata") or {}
    if meta.get("version") == old:  # only what is at the old version moves, as release.py always did
        meta["version"] = v
    for e in data.get("plugins", []):
        if e.get("name") == "foreman" and e.get("version") == old:
            e["version"] = v
        elif e.get("name") == "foreman-ui" and ui:
            e["version"] = ui
    _setver(pj, v)
    _dump(mk, data)
    if ui:
        _setver(uj, ui)


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
    """`fm sentinel` in every local project fm knows: what an earlier task proved that fails there now. Never fatal."""
    try:
        listed = json.loads(subprocess.run([*FM, "projects", "--json"], capture_output=True, text=True, timeout=120,
                                           ).stdout or "{}").get("projects", [])
    except (ValueError, OSError, subprocess.TimeoutExpired):
        listed = []
    print(f"canary: fm sentinel in {len(listed)} project(s)")
    for x in listed:
        if not x.get("exists"):
            continue
        try:
            r = subprocess.run([*FM, "sentinel"], cwd=x["root"], capture_output=True, text=True, timeout=1800)
            first = (r.stdout.strip().splitlines() or ["(no output)"])[0]
            print(f"  {'✗' if r.returncode else '✓'} {x['project']}: {first}")
        except (OSError, subprocess.TimeoutExpired) as e:
            print(f"  ✗ {x['project']}: sentinel couldn't run ({type(e).__name__})")


def _push(ctx):
    root, v, p, remote = ctx["root"], ctx["version"], ctx["p"], ctx["remote"]
    b = _grant(p)
    if not b:
        _err("--push needs the active task's publish grant (fm ask ID publish)")
    sha = _git(root, "rev-parse", "HEAD").strip()
    _git(root, "fetch", "-q", remote, "main")
    _spend(p, b.id)  # the yes covers this one push: spent before it, as fm pr train does
    with tempfile.TemporaryDirectory() as tmp:
        wt = os.path.join(tmp, "rel")
        _git(root, "worktree", "add", "-q", "--detach", wt, "FETCH_HEAD")
        try:
            _git(wt, "merge", "-q", "--no-ff", sha, "-m", f"Foreman {v}")
            _git(wt, "push", "-q", remote, "HEAD:main")
        finally:
            _git(root, "worktree", "remove", "--force", wt, ok=True)
    print(f"  pushed Foreman {v} to {remote} main (the publish grant is spent)")


def _round(ctx):
    import argparse
    import fmcli
    fmcli.cmd_round(argparse.Namespace(**{**vars(ctx["args"]), "action": "close"}))


def _unfinished(state):
    return [n for n, _ in STEPS if n != "push" and n not in state["done"] and n not in state["skipped"]]


def _changed(state):
    """The tree was written to (a bump, changelog or commit step is done): another version can't start over it."""
    return bool({"bump", "changelog", "commit"} & set(state["done"]))


def run(p, args):
    state_path = os.path.join(p.dir, "release.json")
    state = _json(state_path) if os.path.isfile(state_path) else None
    if state:
        state.setdefault("skipped", [])
    if args.abandon:
        if state:
            os.remove(state_path)
        print(f"abandoned the release of {state['version']}" if state else "no release in progress")
        return 0
    v = args.version
    if not v:
        _err("fm release VERSION (or --abandon)")
    for what, x in (("VERSION", v), ("--ui", args.ui)):
        if x and not re.fullmatch(SEMVER, x):
            _err(f"{what} is MAJOR.MINOR.PATCH, e.g. 1.2.20")
    root = c.git_root(p.root)
    pj = os.path.join(root or "", "plugin", ".claude-plugin", "plugin.json")
    if not root or not os.path.isfile(pj):
        _err("fm release runs in Foreman's own repo (no plugin/.claude-plugin/plugin.json here)")
    if args.dry_run:
        print(f"fm release {v}: {len(STEPS)} steps, a checkpoint after each (--resume continues)")
        for i, (name, what) in enumerate(STEPS, 1):
            print(f"  {i}. {name}: {what}")
        return 0
    resume = args.resume
    if not resume and state:
        if state["version"] != v and _unfinished(state) and _changed(state):
            _err(f"the release of {state['version']} is unfinished: fm release {state['version']} --resume, or fm release --abandon")
        if state["version"] == v and not _unfinished(state) and args.push and "push" not in state["done"]:
            resume = True  # released but never pushed: only the push is left
    if resume:
        if not state or state["version"] != v:
            _err(f"no unfinished release of {v} to resume" + (f" (the one in progress is {state['version']})" if state else ""))
        for k, new in (("ui", args.ui), ("remote", args.remote)):
            state[k] = new or state.get(k)
        state["push"] = bool(args.push or state.get("push"))
        state["no_check"] = bool(args.no_check or state.get("no_check"))
    else:
        cur = _json(pj).get("version", "")
        if not re.fullmatch(SEMVER, cur):
            _err(f"plugin.json's version {cur!r} isn't MAJOR.MINOR.PATCH; fix it first")
        if tuple(map(int, v.split("."))) <= tuple(map(int, cur.split("."))):
            _err(f"{v} isn't newer than {cur}")
        state = {"version": v, "old": cur, "done": [], "skipped": [], "ui": args.ui, "push": bool(args.push),
                 "remote": args.remote, "no_check": bool(args.no_check)}
    state["remote"] = state.get("remote") or "origin"
    if state["push"]:
        if state["no_check"] or state["skipped"]:
            _err("a release with skipped gates (--no-check) can't --push; nothing was changed")
        if not _grant(p):
            _err("--push needs the active task's publish grant (fm ask ID publish); nothing was changed")
    ctx = {"root": root, "version": v, "ui": state["ui"], "push": state["push"], "remote": state["remote"],
           "old": state["old"], "p": p, "args": args}

    def tree(_):
        if _git(root, "status", "--porcelain").strip():
            _err("the tree has uncommitted changes; commit or finish them first")

    fns = {"tree": tree, "check": lambda _: _gate(root, "check"), "bump": _bump, "changelog": _changelog,
           "commit": _commit, "release-check": lambda _: _gate(root, "release-check"), "canary": _canary,
           "push": _push, "round": _round}
    todo = [i for i, (n, _) in enumerate(STEPS)
            if n not in state["done"] and n not in state["skipped"] and (n != "push" or state["push"])]
    if not todo:
        print(f"Foreman {v} is already released: every step is done")
        return 0
    if resume:
        print(f"resuming at step {todo[0] + 1} ({STEPS[todo[0]][0]})")
    for i in range(len(STEPS)):
        name = STEPS[i][0]
        if i not in todo and not (name == "push" and not state["push"]):
            continue
        print(f"step {i + 1}/{len(STEPS)} {name}")
        if name == "push" and not state["push"]:
            print("  (no --push: nothing published; fm release V --push does it later)")
            continue  # not recorded: a later --push still has it to do
        if state["no_check"] and name in GATES:
            print("  skipped (--no-check)")
            state["skipped"].append(name)
        else:
            try:
                fns[name](ctx)
            except Exception as e:
                _dump(state_path, state)
                if type(e).__name__ == "UsageError":
                    raise type(e)(f"step {i + 1} {name}: {e}\nstopped at step {i + 1} ({name}); fix it, then: "
                                  f"fm release {v} --resume")
                raise
            state["done"].append(name)
        _dump(state_path, state)
    print(f"Foreman {v} released: " + (f"{len(state['skipped'])} gate(s) skipped ({', '.join(state['skipped'])}); "
                                       if state["skipped"] else "") + ("pushed" if "push" in state["done"] else "not pushed"))
    return 0
