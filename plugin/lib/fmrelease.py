"""fm release VERSION (T-1188): the release ritual as named steps with a checkpoint after each (state/release.json),
so `--resume` continues from the first unfinished one and `--dry-run` only prints the plan. Foreman's own repo only
(plugin/.claude-plugin/plugin.json at its root; release.py is a thin wrapper over this). --push merges into the
remote's main (origin by default) from a temporary worktree behind the active task's publish grant, which it spends
before the push. The first run's flags (--ui, --push, --remote, --no-check) are kept in release.json for a resume;
a skipped step is never recorded as done, and a release with skipped gates can't push."""
import codecs
import json
import os
import re
import subprocess
import sys
import tempfile
import time

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
         ("push", "--push: merge into the remote's main (--no-ff) from a temporary worktree, push; spends the publish grant"),
         ("round", "fm round close: tag HEAD round-N"),
         # T-1199: never fatal, so it never holds the push; 12 projects one by one held 1.2.34's for ~35 min
         ("canary", "fm sentinel in every local project, 4 at a time, started detached (report: fm release --canary-status)")]
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


DESIGN_PJ = "plugins/foreman-design/.claude-plugin/plugin.json"  # T-1652: links to plugin/skills, so foreman's version


def _setver(path, v):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    c.write_atomic(path, re.sub(r'"version": "[^"]*"', lambda _: f'"version": "{v}"', text, 1))


def _grant(p):
    """The active task, when it holds the publish grant; else None."""
    b = c.active_brief_fast(p, p.lane)
    return b if b and "publish" in (b.meta.get("allow") or []) else None


def _named_grant(p, tid):
    """T-2007: fm ship --task ID: that task (closed or active) when it holds the publish grant."""
    b = c.find_brief(p, tid) or _err(f"no task {tid.upper()}; nothing was pushed")
    return b if "publish" in (b.meta.get("allow") or []) else _err(
        f"{b.id} has no publish grant (fm task set {b.id} --allow publish); nothing was pushed")


def _spend(p, tid, by):
    with c.lock(p.dir):
        b = c.find_brief(p, tid)
        if "publish" not in (b.meta.get("allow") or []):  # another release spent it since _grant looked
            _err("the publish grant was already spent; nothing was pushed")
        b.meta["allow"] = [x for x in b.meta.get("allow") or [] if x != "publish"]
        b.append_log(f"publish grant used by {by}")
        c.save_brief(p, b)
        c.log_event(p, "grant_spent", task=tid, data={"allow": "publish", "by": by})


def _gate(root, verb):
    if subprocess.run([*FM, verb], cwd=root).returncode:
        _err(f"fm {verb} failed")


def _ui_changed(root):
    last = _git(root, "log", "-1", "--format=%H", "-E", f"--grep={MARK}").strip()
    return bool(_git(root, "diff", "--name-only", f"{last}..HEAD" if last else "HEAD", "--", "mods/foreman-ui").strip())


def bad_hour(events, hour, least=5):
    """T-1549: the user's historically bad hours: (failed, runs, overall share) when gates started at this local hour
    failed at least 40% of the time and at least twice as often as overall (5 runs in the hour and 20 in all at least),
    else None."""
    import datetime
    by, fails, total = {}, 0, 0
    for e in events:
        res = (e.get("data") or {}).get("results") if isinstance(e.get("data"), dict) else None
        try:
            h = datetime.datetime.fromisoformat(str(e.get("ts")).replace("Z", "+00:00")).astimezone().hour
        except ValueError:
            continue
        if not isinstance(res, list) or not res:
            continue
        bad = any(isinstance(r, dict) and r.get("exit") not in (0, None) for r in res)
        n, f = by.get(h, (0, 0))
        by[h], total, fails = (n + 1, f + bad), total + 1, fails + bad
    n, f = by.get(hour, (0, 0))
    if total < 20 or n < least:
        return None
    return (f, n, fails / total) if f / n >= 0.4 and f / n >= 2 * fails / total else None


def _bump(ctx):
    root, v, ui, old = ctx["root"], ctx["version"], ctx["ui"], ctx["old"]
    if ui is None and _ui_changed(root):
        _err("mods/foreman-ui changed since the last release: pass --ui VERSION")
    pj = os.path.join(root, "plugin", ".claude-plugin", "plugin.json")
    mk = os.path.join(root, ".claude-plugin", "marketplace.json")
    uj = os.path.join(root, "mods", "foreman-ui", ".claude-plugin", "plugin.json")
    dj = os.path.join(root, DESIGN_PJ)
    data = _json(mk)  # everything read before anything is written
    if ui and not os.path.isfile(uj):
        _err("no mods/foreman-ui to give --ui to")
    meta = data.get("metadata") or {}
    if meta.get("version") == old:  # only what is at the old version moves, as release.py always did
        meta["version"] = v
    for e in data.get("plugins", []):
        if e.get("name") in ("foreman", "foreman-design") and e.get("version") == old:  # T-1652: design's skills
            e["version"] = v
        elif e.get("name") == "foreman-ui" and ui:
            e["version"] = ui
    _setver(pj, v)
    if os.path.isfile(dj):
        _setver(dj, v)
    _dump(mk, data)
    if ui:
        _setver(uj, ui)


def _changelog(ctx):
    import datetime
    path = os.path.join(ctx["root"], "CHANGELOG.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if re.search(rf"(?m)^## {re.escape(ctx['version'])} ", text):
        return  # a resumed run
    if "## Unreleased\n" not in text:
        _err("CHANGELOG.md has no '## Unreleased' heading")
    import fmsettings  # T-1549: a default this release changes is named in its notes
    snap = os.path.join(ctx["root"], "plugin", "defaults.json")
    try:
        old = _json(snap) if os.path.isfile(snap) else {}
    except ValueError:
        old = {}
    moved = [f"- Default changed: {m['key']} {json.dumps(m['old'])} → {json.dumps(m['new'])} (if you never set it, "
             "this changes what you see)\n" for m in fmsettings.changed_defaults(old, mine=())]
    head = f"## Unreleased\n\n## {ctx['version']} — {datetime.date.today().isoformat()}\n" + "".join(moved)
    c.write_atomic(path, text.replace("## Unreleased\n", head, 1).replace(head + "\n", head, 1))
    _dump(snap, fmsettings.defaults())  # what the next release compares with


def _commit(ctx):
    root, v = ctx["root"], ctx["version"]
    if _git(root, "log", "-1", "--format=%s").strip() != f"Foreman {v}":
        files = ["plugin/.claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "CHANGELOG.md",
                 "plugin/defaults.json"]  # T-1549: the defaults this release ships, for the next one to compare
        if ctx["ui"]:
            files.append("mods/foreman-ui/.claude-plugin/plugin.json")
        if os.path.isfile(os.path.join(root, DESIGN_PJ)):
            files.append(DESIGN_PJ)
        b = c.active_brief_fast(ctx["p"], ctx["p"].lane)
        if os.path.isfile(os.path.join(root, "plugin", "defaults.json")):
            _git(root, "add", "--", "plugin/defaults.json")  # the first snapshot is a new file: commit -- needs it known
        # only these files: whatever else was staged between a stop and the resume stays out of the release
        _git(root, "commit", "-qm", f"Foreman {v}", *(["--trailer", f"Foreman-Task: {b.id}"] if b else []), "--", *files)
    ctx["state"]["sha"] = _git(root, "rev-parse", "HEAD").strip()  # what a later --push merges, not a moved HEAD


def _canary_log(p, v):
    return os.path.join(p.dir, "logs", f"canary-{v}.txt")


def _canary(ctx):
    """T-1362: the canary starts detached (own session, stdin closed, output in the project's logs/) so the release
    returns once pushed; the worker captures failures to each project's inbox and calls fm notify when it ends."""
    log = _canary_log(ctx["p"], ctx["version"])
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "wb") as f:
        proc = subprocess.Popen([sys.executable, os.path.abspath(__file__), "--canary-worker", ctx["version"], ctx["root"]],
                                stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    if os.environ.get("FOREMAN_NO_BACKGROUND"):  # tests: a detached child writing into a test's folder races its cleanup
        proc.wait()
    print(f"  canary (fm sentinel in every local project) started in the background; its report: {log} (fm release --canary-status)")


def _canary_status(p):
    logs = os.path.join(p.dir, "logs")
    found = [os.path.join(logs, f) for f in os.listdir(logs) if re.fullmatch(r"canary-.*\.txt", f)] if os.path.isdir(logs) else []
    if not found:
        print("no canary run yet (fm release --push starts one)")
        return
    last = max(found, key=os.path.getmtime)
    with open(last, encoding="utf-8", errors="replace") as f:
        text = f.read()
    print(f"{last}" + ("" if "canary done" in text else " (still running)") + "\n" + text.rstrip())


RERUN_S = 600  # T-1518: all the canary's load-flap reruns together


def _canary_worker(v, root):
    """`fm sentinel` in every local project fm knows: what an earlier task proved that fails there now. Never fatal."""
    try:
        listed = json.loads(subprocess.run([*FM, "projects", "--json"], capture_output=True, text=True,
                                           errors="replace", timeout=120).stdout or "{}").get("projects", [])
    except (ValueError, OSError, subprocess.TimeoutExpired):
        listed = []
    print(f"canary: fm sentinel in {len(listed)} project(s)", flush=True)

    def one(x, timeout=1800):
        """(the sentinel's exit code, None when it couldn't run or timed out; the report line)"""
        try:
            r = subprocess.run([*FM, "sentinel"], cwd=x["root"], capture_output=True, text=True, errors="replace",
                               timeout=timeout)
            first = (r.stdout.strip().splitlines() or ["(no output)"])[0]
            return r.returncode, f"  {'✗' if r.returncode else '✓'} {x['project']}: {first}"
        except (OSError, subprocess.TimeoutExpired) as e:
            return None, f"  ✗ {x['project']}: sentinel couldn't run ({type(e).__name__})"

    def load(hl):
        return f"load {hl[0]:.1f} on {hl[1]} CPUs" if hl else "load unknown"

    from concurrent.futures import ThreadPoolExecutor
    failed = []
    todo = [x for x in listed if x.get("exists")]
    with ThreadPoolExecutor(4) as pool:
        for x, (code, line) in zip(todo, pool.map(one, todo)):  # in project order, as each is ready
            print(line, flush=True)
            if code != 0:
                failed.append((x, line.strip(), code, c.host_load()))
    # T-1518: a check that failed (a real exit, not a timeout) while the host was loaded (load at least its CPUs) gets
    # one rerun alone after the pool, all reruns within RERUN_S; passing there is a load flap, reported with both
    # results and captured like a failure, so an intermittent regression still lands in the inbox. ponytail: "alone"
    # is the canary's own load gone, not an idle machine; wait for the load to fall first if flaps hide real failures.
    still, flaps, skipped, end = [], [], [], time.monotonic() + RERUN_S
    for x, line, code, hl in failed:
        if code is None or not hl or hl[0] < hl[1]:
            still.append((x, line))
            continue
        if end - time.monotonic() <= 0:
            still.append((x, line))
            skipped.append(x["project"])
            continue
        again_code, again = one(x, timeout=end - time.monotonic())
        again = f"{again.strip().split(': ', 1)[-1]} ({load(c.host_load())})"
        if again_code == 0:
            flaps.append((x, line))
            print(f"  ~ {x['project']}: load flap: failed beside the others ({line.split(': ', 1)[-1]}) ({load(hl)}), "
                  f"passed alone ({again})", flush=True)
        else:
            still.append((x, line))
            print(f"  ✗ {x['project']}: failed alone too: {again}", flush=True)
    if skipped:
        print(f"  (no rerun for {', '.join(skipped)}: the reruns' {RERUN_S:g} s were spent)", flush=True)
    failed = still
    import fmeco
    for x, title in [(x, f"Canary after Foreman {v}: {line[:200]}") for x, line in failed] + [
            (x, f"Canary load flap after Foreman {v}: {line[:200]}") for x, line in flaps]:
        try:  # a project's past check failing now, or only under load: an item in that project's inbox
            q = c.find_project(x["root"])
            if q:
                fmeco.capture_once(q, title, "FIX", "discovered")
        except Exception as e:  # never fatal: the report above still names it
            print(f"  (couldn't capture for {x['project']}: {type(e).__name__})", flush=True)
    flapped = f"{len(flaps)} load flap(s): {', '.join(x['project'] for x, _ in flaps)}" if flaps else ""
    print(f"canary done: {len(failed)} of {len(todo)} project(s) failing" + (f", {flapped}" if flaps else ""), flush=True)
    if failed or flaps:
        try:
            import fmserve
            p = c.find_project(root)
            fmserve._notify(p, f"Foreman {v} canary: " + "; ".join(
                ([f"{len(failed)} project(s) failing: " + ", ".join(x["project"] for x, _ in failed)] if failed else [])
                + ([flapped] if flaps else [])))
        except Exception:
            pass


_NEED_GRANT = ("--push needs the active task's publish grant: fm ask ID publish (the user's yes), or, where the user "
               "has given standing permission to release, fm task set ID --allow publish")


def _push(ctx):
    root, v, p, remote = ctx["root"], ctx["version"], ctx["p"], ctx["remote"]
    b = _grant(p)
    if not b:
        _err(_NEED_GRANT)
    sha = ctx["state"].get("sha") or _err(f"no release commit recorded for {v}: fm release --abandon, then release again")
    _git(root, "fetch", "-q", remote, "main")
    with tempfile.TemporaryDirectory() as tmp:
        wt = os.path.join(tmp, "rel")
        _git(root, "worktree", "add", "-q", "--detach", wt, "FETCH_HEAD")
        try:
            _git(wt, "merge", "-q", "--no-ff", sha, "-m", f"Foreman {v}")
            _push_main(p, b.id, _git(wt, "rev-parse", "HEAD").strip(), remote, "fm release --push")
        finally:
            _git(root, "worktree", "remove", "--force", wt, ok=True)
    print(f"  pushed Foreman {v} to {remote} main (the publish grant is spent)")


def _push_main(p, tid, sha, remote, by):
    """Push sha to remote's main from the repo (a relative remote URL resolves there). The grant is spent first, so one
    yes is one push even for two racing callers, and given back if git push fails (T-1943)."""
    _spend(p, tid, by)
    try:
        _git(p.root, "push", "-q", remote, f"{sha}:refs/heads/main")
    except Exception:
        with c.lock(p.dir):
            b = c.find_brief(p, tid)
            b.meta["allow"] = [*(b.meta.get("allow") or []), "publish"]
            b.append_log(f"publish grant given back: {by}'s push failed")
            c.save_brief(p, b)
        raise


SHIPPED = "refs/foreman/shipped"  # T-1945: the last commit fm ship landed; default picks start after it


def ship(p, args):
    """T-1943: fm ship — HEAD's commits the remote's main lacks (git cherry, by patch) or the named ones, cherry-picked
    onto the fetched main in a scratch worktree, their files compared, tested there, main re-checked, then pushed
    behind the publish grant. The working tree is never touched; a failure pushes nothing and keeps the grant."""
    import shlex
    root, remote = p.root, args.remote or "origin"
    if remote.startswith("-"):
        _err(f"--remote {remote!r} reads as a git option; name a remote or a URL")
    _git(root, "fetch", "-q", remote, "main")
    base = _git(root, "rev-parse", "FETCH_HEAD").strip()
    picks = []
    for x in args.commits or []:
        sha = "" if x.startswith("-") else _git(root, "rev-parse", "--verify", "-q", "--end-of-options", f"{x}^{{commit}}", ok=True).strip()
        picks.append(sha or _err(f"{x!r} isn't a commit here"))
    last = _git(root, "rev-parse", "--verify", "-q", SHIPPED, ok=True).strip()  # T-1945: main may hold these under another patch
    if last and c._git(root, "merge-base", "--is-ancestor", last, "HEAD", timeout=60, proc=True).returncode:
        last = ""  # rebased or another branch: git cherry alone
    def _files(a, b):
        return set(_git(root, "diff", "--name-only", a, b).splitlines())
    if not picks and last and not (_files(last, base) & _files(last, "HEAD")):
        # T-2054: main is where the last ship left it (T-2212: or moved only in files the branch left alone), so replay
        # the branch's own history: a merged lane's commit may not apply alone (its merge settled a conflict), but each
        # first-parent step applies in turn
        picks = _git(root, "rev-list", "--first-parent", "--reverse", f"{last}..HEAD").split()
    picks = picks or [ln[2:] for ln in _git(root, "cherry", base, "HEAD", *([last] if last else [])).splitlines() if ln.startswith("+ ")]
    if not picks:
        print(f"nothing to ship: {remote} main already has HEAD's changes" + (f" after the last shipped commit {last[:8]}" if last else ""))
        return 0
    if args.check:  # T-1960: a ship verifies without a grant: which of these main lacks, by patch
        missing = [x for x in picks if not args.commits or _git(root, "cherry", base, x, f"{x}^").startswith("+")]
        for x in missing:
            print(f"{remote} main lacks {x[:8]} {c.fit(c.plain(_git(root, 'log', '-1', '--format=%s', x).strip()), 72)}")
        if not missing:
            print(f"{remote} main has the changes of {', '.join(x[:8] for x in picks)}")
        return 1 if missing else 0
    b = (_named_grant(p, args.task) if getattr(args, "task", None)
         else _grant(p) or _err(_NEED_GRANT.replace("--push", "fm ship", 1) + "; nothing was pushed"))
    if args.test:  # T-1950: remembered per repo, so the oldest runtime's suite isn't retyped each ship
        _git(root, "config", "--local", "foreman.shiptest", args.test, ok=True)
    said = args.test or _git(root, "config", "--local", "--get", "foreman.shiptest", ok=True).strip()
    test = shlex.split(said) if said else [*FM, "check"]
    files = sorted({f for s in picks for f in _git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", "-m", s).splitlines() if f})
    n = f"{len(picks)} commit{'s' if len(picks) > 1 else ''}"
    with tempfile.TemporaryDirectory() as tmp:
        wt = os.path.join(tmp, "ship")
        _git(root, "worktree", "add", "-q", "--detach", wt, base)
        try:
            for s in picks:
                merge = len(_git(root, "rev-list", "--parents", "-n1", s).split()) > 2
                r = c._git(wt, "cherry-pick", *(["-m", "1"] if merge else []), s, timeout=300, proc=True)
                if r.returncode:
                    _git(wt, "cherry-pick", "--abort", ok=True)
                    hint = "" if args.commits else " (main may hold it under another patch: name the commits to ship)"
                    _err(f"{s[:8]} didn't cherry-pick onto {remote} main{hint}: {c.fit(c.plain(r.stderr.strip()), 200)}; nothing was pushed")
            if files and c._git(wt, "diff", "--quiet", "HEAD", picks[-1], "--", *files, timeout=300, proc=True).returncode:
                _err(f"the shipped files differ from {picks[-1][:8]}'s: a commit is missing or extra, or main changed "
                     "these files since the branch left it (rebase onto main); nothing was pushed")
            import fmambient
            c.wait_while(lambda: c.gates_live(p) or fmambient.running(p),  # T-1978: never two suites at once
                         "a running fm check or ambient test run", "fm ship", out=sys.stdout)
            print(f"testing {n} on {remote} main: {shlex.join(test)}", flush=True)
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}  # GIT_DIR from a hook: not the user's repo
            c.update_meta(p, ship_testing={"pid": os.getpid(), "at": c.now(), "root": os.path.realpath(wt)})
            env.setdefault("PYTHONUNBUFFERED", "1")
            log = os.path.join(tmp, "test.log")  # T-2255: a file, not a pipe: a background process holding it can't hang the ship
            try:  # a full fm check here waits for this run; the ship's own fm check (in wt) doesn't
                with open(log, "wb") as out, open(log, "rb") as rd:
                    try:
                        proc = subprocess.Popen(test, cwd=wt, stdin=subprocess.DEVNULL, env=env, stdout=out,
                                                stderr=subprocess.STDOUT)
                    except OSError as e:
                        _err(f"--test {test[0]!r} couldn't run ({e.strerror}); nothing was pushed")
                    dec = codecs.getincrementaldecoder("utf-8")(errors="replace")
                    while True:
                        done = proc.poll() is not None
                        chunk = rd.read()
                        if chunk:
                            print(dec.decode(chunk), end="", flush=True)
                        if done:
                            break
                        time.sleep(0.1)
                    failed = proc.returncode
                    rd.seek(max(0, os.path.getsize(log) - 1_000_000))  # the last 1 MB, for the baseline capture
                    tail = rd.read().decode("utf-8", errors="replace")
            finally:
                if (c.read_meta(p).get("ship_testing") or {}).get("pid") == os.getpid():
                    c.update_meta(p, ship_testing=None)
            import fmcli  # the shipped tree is vouchable, so the run files (or clears) what fm check would
            try:
                got = fmcli._baseline(p, [(shlex.join(test), failed, tail, None)])
            except Exception as e:  # the verdict stands; the capture is a convenience
                got = []
                print(f"baseline capture failed: {e}")
            m = re.search(r"\bT-\d+\b", " ".join(got))
            if failed:
                _err("the test failed in the scratch tree" + (f" (baseline task {m.group(0)})" if m else "")
                     + "; nothing was pushed")
            for ln in got:
                print(ln)
            rules = os.path.join(wt, "plugin", "rules", "foreman.md")
            try:  # T-2281: Foreman's own footprint, the lean ratchet's baseline; before the push, so a failed push keeps it
                import fmdoctor
                if os.path.isfile(rules):  # any other project's tree holds no Foreman plugin
                    fmdoctor.record_footprint(p, rules, os.path.join(wt, "plugin"))
            except Exception as e:  # the ship stands; the record is a convenience
                print(f"footprint record failed: {e}")
            tip = _git(wt, "rev-parse", "HEAD").strip()
            _git(root, "fetch", "-q", remote, "main")
            if c._git(root, "merge-base", "--is-ancestor", "FETCH_HEAD", tip, timeout=60, proc=True).returncode:
                _err(f"{remote} main moved while testing; nothing was pushed: run fm ship again")
            _push_main(p, b.id, tip, remote, "fm ship")
            if c._git(root, "update-ref", SHIPPED, picks[-1], timeout=60, proc=True).returncode:  # T-1951: main has them
                print(f"warning: couldn't move {SHIPPED} to {picks[-1][:8]}; the next plain fm ship may offer these again")
        finally:
            _git(root, "worktree", "remove", "--force", wt, ok=True)
    print(f"shipped {n} to {remote} main at {tip} (the publish grant is spent)."
          + ("" if args.watch else f" Watch CI in the background: fm ci-watch --commit {tip}"), flush=True)
    if not args.watch:
        return 0
    import fmci  # T-1946
    code, msg = fmci.watch(p, "main", 3, 30, commit=tip)
    print(msg)
    return code


def cmd_ship(args):
    import fmcli
    return ship(fmcli.resolve(args), args)


def _round(ctx):
    import argparse
    import fmcli
    if any(t.startswith("round-") for t in _git(ctx["root"], "tag", "--points-at", "HEAD").split()):
        return  # a resume after the tag was made but before its checkpoint
    fmcli.cmd_round(argparse.Namespace(**{**vars(ctx["args"]), "action": "close"}))


def _unfinished(state):
    return [n for n, _ in STEPS if n != "push" and n not in state["done"] and n not in state["skipped"]]


def _changed(state):
    """The tree was written to (a bump, changelog or commit step is done): another version can't start over it."""
    return bool({"bump", "changelog", "commit"} & set(state["done"]))


def run(p, args):
    if getattr(args, "canary_status", False):
        return _canary_status(p) or 0
    state_path = os.path.join(p.dir, "release.json")
    try:
        state = _json(state_path) if os.path.isfile(state_path) else None
        if state is not None and not (isinstance(state, dict) and isinstance(state.get("version"), str)):
            raise ValueError
    except ValueError:
        if not args.abandon:
            _err(f"{state_path} is unreadable: fm release --abandon forgets it")
        state = {"version": "(unreadable)"}
    if state:
        state.setdefault("skipped", [])
    if args.abandon:
        if state and args.dry_run:
            print(f"would abandon the release of {state['version']} (--dry-run: nothing changed)")
        elif state:
            os.remove(state_path)
        if not args.dry_run:
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
    import datetime
    hour = datetime.datetime.now().hour
    bad = bad_hour(c.ledger_events(p, ["check_run"]), hour)
    if bad:  # T-1549: a warning, never a stop
        print(f"fm release: careful: gates started between {hour}:00 and {hour}:59 failed {bad[0]} of {bad[1]} times "
              f"in this project (overall {bad[2]:.0%}): by its record, a bad hour for a release", file=sys.stderr)
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
        if state["version"] == v and _unfinished(state) and _changed(state):
            resume = True  # the same release stopped after its bump: starting over would say "isn't newer"
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
    if state["remote"].startswith("-"):
        _err(f"--remote {state['remote']!r} reads as a git option; name a remote or a URL")
    if getattr(args, "stale_ok", None) is not None and not state["push"]:
        _err("--stale-ok waives the safety gate of --push; without --push there is nothing to waive")
    if state["push"]:
        if state["no_check"] or state["skipped"]:
            _err("a release with skipped gates (--no-check) can't --push; nothing was changed")
        if not _grant(p):
            _err(_NEED_GRANT + "; nothing was changed")
        import fmreplay  # T-1401: the guard's own corpus replay is green and recent, or the waiver is on the ledger
        note = fmreplay.enforce(p, "fm release --push", getattr(args, "stale_ok", None))
        if note:
            print(f"  {note}")
        url = _git(root, "remote", "get-url", state["remote"], ok=True).strip() or state["remote"]
        if os.environ.get("FOREMAN_RELEASE_FM") and not os.path.isdir(url):
            _err("FOREMAN_RELEASE_FM (a stub fm for the gates, for tests) can't --push to a real remote; nothing was changed")
    ctx = {"root": root, "version": v, "ui": state["ui"], "push": state["push"], "remote": state["remote"],
           "old": state["old"], "p": p, "args": args, "state": state}

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
        print(f"step {i + 1}/{len(STEPS)} {name}", flush=True)  # a log file shows where a long run is
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


if __name__ == "__main__" and len(sys.argv) == 4 and sys.argv[1] == "--canary-worker":  # _canary's detached child
    with c.gate_lock("canary", say=lambda m: print(m, flush=True)):  # T-1668: queues behind fm check and release gates
        _canary_worker(sys.argv[2], sys.argv[3])
