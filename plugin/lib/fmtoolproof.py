"""T-2372 (Mission 6, #5): a tool built during a task (fm new tool, fm mcp new) proves itself before the task closes.
Both log `tool_built` on the active task (data name, need, kind, path, test). fm task finish and fm task done then
refuse the task until, for each tool, from the task's own ledger events and evidence (a typed line replaces none):
  - search: a `tool_search` receipt (fm which, on this task) for the tool's need, earlier in the ledger than the build,
  - red then green: the tool's test run by fm ([ran] evidence), failing and later passing, and the newest run passing,
  - stub: in a scratch copy the test passes on the real tool and fails with the tool's body replaced by nothing (a
    hang is killed and counts as a failure, but not on the real tool: no verdict then),
  - use: a Bash call of the tool (or, for a server, a call of its MCP tool) in this task's Claude Code session
    transcript, strictly after the green run, that isn't its own test or a --help.
All four hold: `tool_proved` {name, path, need} (fmmiss reads it as a resolved miss). A host with no transcript for the
task's sessions can't judge the use: `tool_unproven` is logged, the task is not refused and the tool is not marked
proved. A task that built nothing pays one filtered ledger read. Fails open on a reader error, like fmmiss.
ponytail: the scratch copy holds the tool and its test only (a stdlib script and its test: what the scaffolds make);
a test that needs a sibling file fails there with the real tool and is refused with that said."""
import json
import os
import re
import sys
import tempfile
import shutil

import fmcore as c

KINDS = ("tool_built", "tool_search", "tool_proved", "tool_unproven")
SECONDS = 30  # each scratch run (real, then stub); a hang is killed at this
READ_MAX = 256 << 20  # bytes of one transcript read: a session's worth, never more
_HELP = re.compile(r"\s(?:--help|-h)\s*$")


def built(name, tool, test, kind="tool"):
    """fm new tool / fm mcp new: log the build on the active task, if any (nothing to prove outside one)."""
    try:
        p = c.find_project(os.getcwd(), create=False)
        b = p and c.active_brief_fast(p, p.lane)
        if b:
            c.log_event(p, "tool_built", task=b.id, data={"name": name, "need": name, "kind": kind,
                                                          "path": tool, "test": test})
    except Exception:
        pass  # a ledger that can't be written must not undo a scaffold that was


def _data(e):
    return e.get("data") if isinstance(e.get("data"), dict) else {}


def _run(tool, test, body, seconds):
    """Why the test failed in a scratch copy (None: it passed): the tool (or `body` instead) and the test, in their
    own relative layout, run through the sandbox fm new check uses for a panel."""
    import fmplaybooks
    base = os.path.commonpath([os.path.dirname(tool), os.path.dirname(test)])
    with tempfile.TemporaryDirectory(prefix="fm-toolproof-") as d:
        for src, text in ((tool, body), (test, None)):
            dst = os.path.join(d, os.path.relpath(src, base))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if text is None:
                shutil.copyfile(src, dst)
            else:
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(text)
        return fmplaybooks._run(os.path.join(d, os.path.relpath(test, base)), seconds, fmplaybooks._limits(),
                                what="the test", argv=(sys.executable, "-I"))


def stub_problem(tool, test, seconds=SECONDS):
    """None when the test passes on the real tool and fails on a stub of it (its body replaced by nothing)."""
    if not (os.path.isfile(tool) and os.path.isfile(test)):
        return "stub check: the tool or its test is gone from where it was built"
    with open(tool, encoding="utf-8", errors="replace") as f:
        why = _run(tool, test, f.read(), seconds)
    if why:
        return f"stub check: the test fails in a scratch copy even with the real tool ({why}): nothing to compare"
    if _run(tool, test, "# stubbed by fm: the body is gone\n", seconds) is None:
        return "stub check: the test still passes on a stub of the tool (its body replaced by nothing): it asserts nothing about the tool"
    return None


def _red_green(b, test):
    """(ok, ts of the newest green): fm's runs of a command naming the test file: a failure, later a pass of that
    command, and the newest run a pass."""
    runs = []
    for line in b.evidence():
        if c._RAN_MARK not in line or line.count("`") < 2:
            continue
        cmd = line.split("`", 2)[1]
        if os.path.basename(test) not in cmd:
            continue
        ts = c._TS_TAIL.search(line)
        if "` → ✗ exit" in line or "` → red as expected" in line:
            runs.append((cmd, False, ""))
        elif "` → exit 0" in line:
            runs.append((cmd, True, ts.group(1) if ts else ""))
    failed = set()
    ok = False
    for cmd, passed, _ in runs:
        if not passed:
            failed.add(cmd)
        elif cmd in failed:
            ok = True
    return (ok and runs[-1][1], runs[-1][2]) if runs else (False, "")


def _transcripts(sids):
    import fmclaude
    out = []
    for sid in sids:
        try:
            out.append(fmclaude._transcript(sid))
        except ValueError:
            pass
    return out


def _used(paths, d, after):
    """Did a transcript show the tool run, successfully, strictly after `after` (a whole-second timestamp)?"""
    name, tool, test, kind = d.get("name") or "", d.get("path") or "", d.get("test") or "", d.get("kind")
    if kind == "mcp":
        hit = re.compile(re.escape(tool))
    else:
        hit = re.compile(r"(?<![\w-])" + re.escape(os.path.basename(tool)) + r"(?![\w.-])")
    seen = set()
    for path in paths:
        read = 0
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                read += len(line)
                if read > READ_MAX:
                    break
                try:
                    e = json.loads(line)
                    parts = e["message"]["content"]
                except (ValueError, KeyError, TypeError, RecursionError):
                    continue
                if not isinstance(parts, list):
                    continue
                for x in parts:
                    if not isinstance(x, dict):
                        continue
                    if x.get("type") == "tool_use" and str(e.get("timestamp") or "")[:19] > after[:19]:
                        cmd = str((x.get("input") or {}).get("command") or "") if isinstance(x.get("input"), dict) else ""
                        if x.get("name") == "Bash" and hit.search(cmd) and os.path.basename(test) not in cmd \
                                and not _HELP.search(cmd):
                            seen.add(x.get("id"))
                        elif kind == "mcp" and f"mcp__{name}__" in str(x.get("name")):
                            seen.add(x.get("id"))
                    elif x.get("type") == "tool_result" and x.get("tool_use_id") in seen and not x.get("is_error"):
                        return True
    return False


def gaps(p, b):
    """One line per unproven piece of each tool this task built, for the refusals of fm task finish and done."""
    evs = c.ledger_events(p, KINDS, since=str(b.meta.get("created") or ""))
    mine = [(i, e, e.get("event"), _data(e)) for i, e in enumerate(evs) if e.get("task") == b.id]
    builds = {}
    for i, e, ev, d in mine:
        if ev == "tool_built" and d.get("path"):
            builds[d["path"]] = (i, e, d)
    out = []
    sids = {e.get("session_id") for _, e, *_ in mine if e.get("session_id")} | ({c.session_id()} - {None})
    for path, (i, e, d) in builds.items():
        if any(ev == "tool_proved" and x.get("path") == path and j > i for j, _, ev, x in mine):
            continue
        import fmwhich
        name, test = d.get("name") or os.path.basename(path), d.get("test") or ""
        need, tag = set(fmwhich.words(re.sub(r"[_-]", " ", d.get("need") or name))), f"tool {name}"
        found = [f"{tag}: no search receipt for it before the build: fm which \"{name}\" must come first, and a search "
                 f"now can't stand in for it (delete the tool's files and build again after searching, or fm task "
                 f"block {b.id} \"<why>\")"] if not any(
            ev == "tool_search" and j < i and need & set(fmwhich.words(x.get("need") or "")) for j, _, ev, x in mine) else []
        ok, green = _red_green(b, test)
        if not ok:
            found.append(f"{tag}: no red then green run of its test by fm: run {os.path.basename(test)} failing, then "
                         f"passing, with fm task evidence {b.id} --step N --run 'python3 {test}' (a typed line is not a run)")
        else:
            why = stub_problem(path, test)
            if why:
                found.append(f"{tag}: {why}")
        unknown = False
        if ok:
            paths = _transcripts(sorted(sids))
            if not paths:
                unknown = True
            elif not _used(paths, d, green):
                found.append(f"{tag}: never used on this task's work after its green run: run {os.path.basename(path)} "
                             f"for real (a Bash call in this session; its own test and --help don't count)")
        if found:
            out += found
        elif unknown:
            if not any(ev == "tool_unproven" and x.get("path") == path for _, _, ev, x in mine):
                c.log_event(p, "tool_unproven", task=b.id, data={"name": name, "path": path, "need": name,
                                                                 "why": "no session transcript on this host"})
        else:
            c.log_event(p, "tool_proved", task=b.id, data={"name": name, "path": path, "need": name})
    return out


def safe_gaps(p, b):
    """gaps for the close gates; a reader that breaks must not stop a close: it fails open and logs where the
    hooks' errors go (fm doctor reads it)."""
    try:
        return gaps(p, b)
    except Exception:
        import traceback
        try:
            path = os.path.join(c.state_dir(), "logs", "hooks.log")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            c.append_line(path, f"{c.now()} fmtoolproof.gaps {c.redact(traceback.format_exc()).rstrip()}\n")
        except OSError:
            pass
        return []
