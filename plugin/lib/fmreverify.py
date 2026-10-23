"""T-1663: the re-verify queue. A commit made after a task closed that touches a file in that task's scope queues the
task's passing criteria checks; fm sentinel runs the queue first and captures a FIX naming the task when one fails.
State: reverify.json in the project's state dir, {"head": the last commit scanned, "queue": [entries]}."""
import json
import os
import re

import fmcore as c

PER_COMMIT = 5     # closed tasks one commit can queue (a CHANGELOG edit touches most tasks' scope)
MAX_COMMITS = 50   # commits read per scan: a long gap queues its newest changes, not the whole history
MAX_QUEUE = 100    # entries kept; the oldest go first


def _path(p):
    return os.path.join(p.dir, "reverify.json")


def load(p):
    try:
        with open(_path(p), encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict) and isinstance(d.get("queue"), list):
            return {"head": str(d.get("head") or ""), "queue": [e for e in d["queue"] if isinstance(e, dict)
                                                                  and isinstance(e.get("cmd"), str)]}
    except (OSError, ValueError):
        pass
    return {"head": "", "queue": []}


def checks(b):
    """The criteria checks a closed task ran and passed (what fm sentinel reruns)."""
    return [line.split("`", 2)[1] for line in b.evidence()
            if line.startswith("- (ac ") and c._RAN_MARK in line and "` → exit 0" in line]


def _commits(root, last, head):
    """[(sha, unix time, subject, [files])] for last..head, newest first, merges skipped (their lane commits count)."""
    out = c._git(root, "log", "--no-merges", f"-n{MAX_COMMITS}", "--format=%x00%H%x00%ct%x00%s", "--name-only",
                 f"{last}..{head}", "--", timeout=10)
    parts, rows = out.split("\x00")[1:], []
    for i in range(0, len(parts) - 2, 3):
        sha, ct, rest = parts[i], parts[i + 1], parts[i + 2]
        subject, _, files = rest.partition("\n")
        rows.append((sha, int(ct) if ct.isdigit() else 0, subject, [f for f in files.splitlines() if f.strip()]))
    return rows


def scan(p):
    """Queue re-verify entries for the commits since the last scan; returns the whole queue. The first scan in a
    project only records HEAD (no flood from history)."""
    head = c._git(p.root, "rev-parse", "--verify", "-q", "HEAD").strip()
    last = load(p)["head"]
    if not head or head == last:
        return load(p)["queue"]
    new = []
    if last:  # the briefs and git read outside the lock: hooks wait on it
        closed = []
        for b in c.load_briefs(p, include_archive=True):
            scope = b.meta.get("scope") or []
            ts = c.parse_ts(b.meta.get("updated")) if b.status == "done" and isinstance(scope, list) else None
            cmds = checks(b) if ts and scope else []
            if cmds:
                closed.append((int(ts.timestamp()), b, scope, cmds))
        closed.sort(key=lambda t: -t[0])  # the most recently closed first, under the per-commit cap
        for sha, at, subject, files in reversed(_commits(p.root, last, head)):
            # ponytail: "updated" stands in for the close time; a later edit to a done brief hides older commits
            hit = [(b, cmds) for closed_at, b, scope, cmds in closed if at >= closed_at
                   and not re.search(rf"\b{re.escape(b.id)}\b", subject)
                   and any(c.glob_match(f, str(s)) for f in files for s in scope)][:PER_COMMIT]
            new += [{"task": b.id, "cmd": cmd, "sha": sha, "subject": c.defang(subject[:120])}
                    for b, cmds in hit for cmd in cmds]
    with c.lock(p.dir):
        state = load(p)
        if state["head"] != last:  # another scan got here first
            return state["queue"]
        have = {(e.get("task"), e["cmd"]) for e in state["queue"]}
        for e in new:
            if (e["task"], e["cmd"]) not in have:
                have.add((e["task"], e["cmd"]))
                state["queue"].append(e)
        state["head"], state["queue"] = head, state["queue"][-MAX_QUEUE:]
        c.write_atomic(_path(p), json.dumps(state, indent=1))
        return state["queue"]


def drop(p, handled):
    """Remove the (task, cmd) pairs the sentinel ran or refused; entries queued meanwhile stay."""
    with c.lock(p.dir):
        state = load(p)
        state["queue"] = [e for e in state["queue"] if (e.get("task"), e["cmd"]) not in handled]
        c.write_atomic(_path(p), json.dumps(state, indent=1))
