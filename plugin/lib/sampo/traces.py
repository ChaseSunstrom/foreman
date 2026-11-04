"""T-2995: the exam's green Smith runs as training data. `keep` copies a run's journal (the messages the model saw and
wrote) from its throwaway Smith home to answers/smith/<scenario>.journal.jsonl, stripped and capped; `export` turns the
kept journals into chat JSONL for SFT (`sampo exam models --traces DIR`). A run with a Claude slot is never kept or
exported (Anthropic's terms, a recorded decision). Models advise and proof decides: nothing here gates a close."""
import getpass
import hashlib
import json
import os
import re

from sampo import core as c
from sampo import lake

CAP = 1 << 20  # bytes of one scenario's journal kept
STR_CAP = 20000  # characters of one message's text
CLAUDE = re.compile(r"claude|anthropic|sonnet|opus|haiku", re.I)
SUFFIX = ".journal.jsonl"


def is_claude(*xs):
    """Any of the names (model, planner, worker, profile fields) is a Claude model."""
    return any(CLAUDE.search(str(x)) for x in xs if x)


HOME = re.compile(r"/(?:home|Users)/[^/\s'\"`<>]+")  # T-2995 review: only a home's owner goes; code keeps /api/x, /usr/bin


def _clean(text, roots, names, cap):
    """Secrets redacted, the run's temp roots and home owners stripped, the user's name and forge owners masked; whitespace
    kept (it is code). Unlike the lake's clean, other absolute paths stay: a model trained on <path> learns to write it."""
    text = c.redact(str(text or ""))
    for r in sorted({x for x in roots if x}, key=len, reverse=True):
        text = text.replace(r, "<tmp>")
    text = lake._FORGE.sub(r"\1<owner>/", HOME.sub("~", text))
    for n in names:
        if n and len(n) >= 3:
            text = re.sub(rf"(?i)(?<![\w-]){re.escape(n)}(?![\w-])", "<user>", text)
    return text if cap is None else text[:cap]


def _strip(o, roots, names, key=None):
    if isinstance(o, str):  # a tool call's arguments are JSON: cut, they stop parsing; the journal's CAP bounds them
        return _clean(o, roots, names, None if key == "arguments" else STR_CAP)
    if isinstance(o, list):
        return [_strip(x, roots, names) for x in o]
    if isinstance(o, dict):
        return {k: _strip(v, roots, names, k) for k, v in o.items()}
    return o


def _user():
    try:
        return getpass.getuser()
    except (KeyError, OSError):  # no passwd entry and no USER (a bare container)
        return ""


def _slots(recs):
    out = []
    for r in recs:
        if r.get("kind") == "start":
            o = r.get("options") or {}
            out += [r.get("model"), r.get("planner"), o.get("worker"), o.get("escalate"), o.get("planner")]
        elif r.get("kind") in ("route", "failover"):
            out.append(r.get("worker"))
        elif r.get("kind") == "escalate":
            out.append(r.get("model"))
    return out


def _find(tmp):
    """The journal in Smith's own home (tmp/foreman/state/code), never under the repo the model could write (T-2995
    review: a planted repo/code/T-0001.jsonl would become training data labelled green); no symlinks."""
    d = os.path.join(tmp, "foreman", "state", "code")
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return None
    for f in names:
        path = os.path.join(d, f)
        if re.fullmatch(r"T-\d+\.jsonl", f) and os.path.isfile(path) and not os.path.islink(path):
            return path
    return None


def keep(tmp, dest, meta, profiles=()):
    """Copy the journal under tmp to dest when no slot is Claude; True when kept. meta: scenario, language, kind, origin,
    model, planner. profiles: resolved profile dicts of the model and planner (their fields are checked too)."""
    src = _find(tmp)
    if not src:
        return False
    recs = []
    with open(src, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                recs.append(json.loads(line))
            except ValueError:
                pass
    fields = [v for p in profiles if isinstance(p, dict) for v in p.values() if isinstance(v, str)]
    if is_claude(*_slots(recs), *meta.values(), *fields):
        return False
    roots, names = [tmp, os.path.realpath(tmp)], [_user()]
    lines = [json.dumps({"meta": {**meta, "worker": next((x for x in _slots(recs)[2:3] if x), None),
                                  "outcome": meta.get("outcome") or "green"}})]
    size = len(lines[0])
    for r in recs:
        if r.get("kind") != "msg":
            continue
        line = json.dumps({"kind": "msg", "phase": r.get("phase"), "msg": _strip(r.get("msg"), roots, names)})
        if size + len(line) > CAP:  # an oversized run's tail goes, back to its last assistant turn: never mid-call
            while len(lines) > 1 and (json.loads(lines[-1]).get("msg") or {}).get("role") != "assistant":
                lines.pop()
            break
        lines.append(line)
        size += len(line) + 1
    c.write_atomic(dest, "\n".join(lines) + "\n")
    return True


def _conversations(path):
    meta, phases = {}, {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if "meta" in r:
                meta = r["meta"]
            elif r.get("kind") == "msg" and isinstance(r.get("msg"), dict):
                m = {k: v for k, v in r["msg"].items() if k in ("role", "content", "tool_calls", "tool_call_id")}
                phases.setdefault(r.get("phase"), []).append(m)
    return meta, [m for m in phases.values() if any(x.get("role") == "assistant" for x in m)]


def export(answers, outdir):
    """Chat JSONL (traces.jsonl in outdir) from every <scenario>.journal.jsonl under answers: one conversation per line,
    {messages, provenance}; Claude runs refused, duplicates (a hash of the messages) dropped."""
    seen, rows, refused, dupes = set(), [], 0, 0
    dirs = [answers] if isinstance(answers, str) else answers  # one answers folder, or one per run
    files = [os.path.join(d, n) for d in dirs if os.path.isdir(d) for n in sorted(os.listdir(d)) if n.endswith(SUFFIX)]
    for path in files:
        meta, convs = _conversations(path)
        if not meta.get("model") or is_claude(*(v for v in meta.values())):  # no meta: fail closed (T-2995 review)
            refused += 1
            continue
        prov = {"scenario": meta.get("scenario"), "language": meta.get("language"), "kind": meta.get("kind"),
                "origin": meta.get("origin"), "model": meta.get("model"), "outcome": meta.get("outcome")}
        for msgs in convs:
            h = hashlib.sha256(json.dumps(msgs, sort_keys=True).encode()).hexdigest()
            if h in seen:
                dupes += 1
                continue
            seen.add(h)
            rows.append(json.dumps({"messages": msgs, "provenance": prov}))
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "traces.jsonl")
    c.write_atomic(out, "".join(r + "\n" for r in rows))
    return {"file": out, "conversations": len(rows), "dupes": dupes, "refused": refused}
