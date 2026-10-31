"""T-2369 (Mission 6, #5): a capability miss during an active task is that task's to resolve. The PostToolUseFailure hook
logs `capability_miss` with the task and the failing command; fm next leads with the open ones, and fm task finish (and
done) refuse the task while one is unresolved. A miss resolves only by run evidence, never by a typed line or a flag:
  - a later exit 0 of the same command (a [ran] evidence line, or a Bash run the hook saw pass),
  - a later `fix_paired` event (fmfixes paired the failure with the command that got past it, T-1032),
  - a later `tool_proved` event naming it (a tool built and proved from runs),
  - a later `grant_queued` event naming it plus a later passing [ran] run of the step that used the fallback.
A missing module the task then writes (the name is a code file in the tree) is the red-first test, not a miss. The way
out short of resolving is fm task block with the diagnosis. No miss logged on the task: nothing here runs."""
import os
import re

import fmcore as c
import fmfixes

KINDS = ("capability_miss", "fix_paired", "tool_proved", "grant_queued")
CODE_EXT = (".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".rb", ".go", ".rs", ".sh", ".lua", ".php")
_PASS = re.compile(r"^- (?:\((step|ac) (\d+)\) )?`([^`]*)` → exit 0\b")


def key(cmd):
    """What two runs of one command share: no leading cd, one space between words, redacted as the ledger keeps it,
    cut where the hook's event target is."""
    return c.redact(fmfixes._norm(str(cmd or "").replace("`", "'")).strip())[:120]


def _data(e):
    return e.get("data") if isinstance(e.get("data"), dict) else {}


def _written(p, name):
    """The module the task wrote: a code file or package of that name anywhere in the tree (tracked or not)."""
    import fmmap
    stem = name.replace(".", "/")
    for f in fmmap._git(p.root, "ls-files", "--cached", "--others", "--exclude-standard").splitlines():
        base, ext = os.path.splitext(f)
        if ext in CODE_EXT and (base == stem or base.endswith("/" + stem)
                                or re.search(rf"(^|/){re.escape(stem)}/(__init__|index)$", base)):
            return True
    return False


def _bash_ok(p, since):
    """Keys of the Bash commands the hook saw pass (kind tool) since `since`; only read when a miss is open."""
    return {key(e.get("target")) for e in c.global_events(since)
            if e.get("kind") == "tool" and e.get("tool") == "Bash" and e.get("ok") and e.get("project") == p.slug
            and str(e.get("ts") or "") > since}


def open_misses(p, b):
    """[{name, cmd, kind, ts}], the newest miss of each command logged on this task that nothing has resolved."""
    evs = [e for e in c.ledger_events(p, KINDS, since=str(b.meta.get("created") or "")) if e.get("task") == b.id]
    latest = {}
    for i, e in enumerate(evs):
        d = _data(e)
        if e.get("event") == "capability_miss" and d.get("name"):
            latest[(d["name"], key(d.get("cmd")))] = (i, e)
    if not latest:
        return []
    passes = []  # (ts, step or None, key) of each passing run fm recorded: a [ran] line, which a typed line can't be
    for line in b.evidence():
        m = _PASS.match(line)
        t = c._TS_TAIL.search(line)
        if m and t and c._RAN_MARK in line:
            passes.append((t.group(1), int(m.group(2)) if m.group(1) == "step" else None, key(m.group(3))))
    bash, out = None, []
    for (name, k), (i, miss) in sorted(latest.items(), key=lambda kv: kv[1][0]):
        ts, d, later, done = str(miss.get("ts") or ""), _data(miss), evs[i + 1:], False
        if d.get("kind") == "module" and _written(p, name):
            continue
        for e in later:
            x = _data(e)
            ev = e.get("event")
            if ev == "fix_paired" and key(x.get("failed")) == k or ev == "tool_proved" and x.get("name") == name:
                done = True
            elif ev == "grant_queued" and x.get("name") == name:
                gts = str(e.get("ts") or "")
                done = done or any(t > gts and (not x.get("step") or s == int(x["step"])) and s is not None
                                   for t, s, _ in passes)
        if not done and any(t > ts and pk == k for t, _, pk in passes):  # strictly: a run in the miss's own second is no later
            done = True
        if not done:
            bash = _bash_ok(p, ts) if bash is None else bash
            done = k in bash
        if not done:
            out.append({"name": name, "cmd": d.get("cmd") or "", "kind": d.get("kind") or "command", "ts": ts})
    return out


def gaps(p, b):
    """One line per open miss, for the refusal fm task finish and fm task done give."""
    return [f"capability miss: `{m['name']}` ({c.fit(m['cmd'], 80)}) is unresolved; find it (fm which \"{m['name']}\"), or "
            f"build and test it (fm new tool NAME) and run it green, or queue the grant with a fallback step that passes "
            f"(fm ask {b.id} plugin); only a later passing run closes it, no flag or typed line does; "
            f"fm task block {b.id} \"<why>\" is the way out" for m in open_misses(p, b)]


def lead(p, b):
    """The open miss fm next leads with, or ''."""
    ms = open_misses(p, b)
    if not ms:
        return ""
    m = ms[0]
    return (f"{b.id} has an open miss `{m['name']}`: fm which \"{m['name']}\" (find) or fm new tool NAME (build, test), "
            f"then run it green; it can't finish while open" + (f" (+{len(ms) - 1} more)" if len(ms) > 1 else ""))
