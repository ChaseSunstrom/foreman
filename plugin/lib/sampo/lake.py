"""T-2974: the training lake. One flat table of finished tasks across every Sampo project on this machine, for Sampo's
own models (`sampo exam models --export DIR`). Each row: provenance (a hash of the project's real path, a hash of its
task id, the day), an outcome label from git and the briefs (held, reverted, regret = fixed later, ...), the brief's
text fields each marked with its author (user: the Raw request; agent: interpretation, approach, criteria, steps,
lessons, left out unless asked; tool: evidence output, quarantined in its own field), project names and absolute paths
stripped, old product and command names canonicalised, a time split, duplicate requests dropped, a weight per project and one
canary row. Sensitive projects (judged by real path) and opted-out ones (meta lake_optout) are never read.
Reproducible: the manifest's hash is the sha256 of rows.jsonl, which depends on nothing but the projects' state."""
import getpass
import hashlib
import json
import math
import os
import re

from sampo import core as c

FIELDS = (("request", "Raw request", "user"), ("interpretation", "Interpretation", "agent"),
          ("approach", "Approach", "agent"), ("criteria", "Acceptance criteria", "agent"),
          ("steps", "Steps", "agent"), ("lessons", "Lessons", "agent"))
CAP = 2000  # characters per field
TOOL_CAP = 600  # characters of quarantined tool output per task
TEST_SHARE = 5  # the newest 1 in 5 rows are the test split (a time split: no future in the train rows)
CANARY = "CANARY-" + hashlib.sha256(b"sampo-lake-canary").hexdigest()[:16]
_ABS = re.compile(r"(?<![\w:/.~])(?:/[\w.@+=-]+){2,}/?|~/[\w./@+=-]+")
# a forge account in a remote URL names its owner: git@github.com:Owner/repo, https://gitlab.com/owner/repo
_FORGE = re.compile(r"((?:git@|https?://|ssh://git@)(?:github\.com|gitlab\.com|codeberg\.org|bitbucket\.org)[:/])[\w.-]+/")


def _h(s):
    return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()[:12]


def _modules():
    here = os.path.dirname(os.path.abspath(__file__))
    return {f[:-3] for f in os.listdir(here) if f.endswith(".py") and f != "__init__.py"}


def canon(text, mods=None):
    """Old names to today's: fm -> sampo, fmcore -> sampo.core (when sampo/core.py exists), the old product name -> Sampo."""
    mods = _modules() if mods is None else mods
    text = re.sub(r"\bfm([a-z0-9_]+)\b", lambda m: f"sampo.{m.group(1)}" if m.group(1) in mods else m.group(0), text)
    text = re.sub(r"\b(?:fm|sampo)\b", "sampo", text)
    return re.sub(r"\b(?:Foreman|FOREMAN)\b", lambda m: "Sampo" if m.group(0)[1].islower() else "SAMPO", text)


def clean(text, roots=(), names=(), mods=None, cap=CAP):
    """Secrets redacted, the project's root and name and every absolute path stripped, names canonicalised, cut to CAP."""
    text = c.redact(str(text or ""))
    for r in sorted({x for x in roots if x}, key=len, reverse=True):
        text = text.replace(r, "<path>")
    text = _FORGE.sub(r"\1<owner>/", _ABS.sub("<path>", text))
    for n in names:
        if len(n) >= 3:
            text = re.sub(rf"(?i)(?<![\w-]){re.escape(n)}(?![\w-])", "<project>", text)
    return c.fit(canon(" ".join(text.split()), mods), cap)


def _section(b, name):
    for h, body in b.sections:
        if h.strip() == name or h.strip().startswith(name + " ("):
            return body
    return ""


def _request(b):
    return " ".join(x[1:].strip() if x.startswith(">") else x.strip() for x in _section(b, "Raw request").splitlines()
                    if x.strip())


def _label(o):
    fate = o.get("fate")
    if fate == "reverted":
        return "reverted"
    if fate == "fixed later":
        return "regret"
    if fate == "held":
        return "held" if o.get("survival") == "survived" and o.get("window_done") else "settling"
    return fate


def _project_rows(p, real, with_agent, names):
    from sampo import outcomes
    from sampo import verifier
    roots = {real, os.path.realpath(p.root), p.root}
    mods = _modules()
    tools = {}
    for e in c.ledger_events(p, ("evidence",)):
        res = (e.get("data") or {}).get("result")
        if e.get("task") and res:
            tools.setdefault(e["task"], []).append(str(res))
    proj, rows = _h(real), []
    outs = outcomes.outcomes(p)
    for b in sorted(c.load_briefs(p, include_archive=True), key=lambda x: x.id):
        o = outs.get(b.id)
        if not o:
            continue
        fields = {}
        for key, head, author in FIELDS:
            if author == "agent" and not with_agent:
                continue
            body = _request(b) if key == "request" else _section(b, head).strip()
            fields[key] = {"author": author, "text": clean(body, roots, names, mods) or None}
        row = {"prov": {"project": proj, "task": _h(proj + b.id), "source": "brief", "day": str(b.meta.get("created") or "")[:10] or None},
               "label": _label(o), "type": b.type or None, "tier": b.tier or None, "fields": fields,
               "features": verifier.features(b)}  # T-2977: counts and parsed test totals, no text
        if tools.get(b.id):
            row["tool_text"] = {"author": "tool", "quarantined": True,  # the first three results; later ones are left out
                                "text": clean(" | ".join(tools[b.id][:3]), roots, names, mods, TOOL_CAP)}
        rows.append(row)
    return proj, rows


def collect(with_agent=False, projects=None):
    """(rows, manifest without its hash): every kept row in a fixed order, the canary last."""
    projects = c.all_projects() if projects is None else projects
    reals = {}
    for p, _ in projects:
        reals[p.slug] = os.path.realpath(p.root)
    # every project's name, not just the row's own: a task of one names another (sensitive ones' names too)
    names = {x for p, _ in projects for x in (p.slug, os.path.basename(reals[p.slug]))} - {"foreman", "sampo"}  # the tool's own
    names |= {getpass.getuser(), os.path.basename(os.path.expanduser("~"))}  # ls -l output names the owner (T-2974 live run)
    from sampo import foresight
    for p, _ in projects:  # a bare Owner/repo or owner.github.io names the account too, as does git's user.name
        names.add((foresight.github_repo(reals[p.slug]) or "/").split("/")[0])
        code, who = c.run_command(reals[p.slug], "git config user.name", timeout=5)
        names.add(who.strip() if code == 0 else "")
    names.discard("")
    bad, ex = set(), {"sensitive": 0, "optout": 0}
    for p, _ in projects:
        try:
            meta = c.read_meta(p)
        except (c.CorruptState, OSError):
            meta = {"sensitive": True}  # unreadable: judged sensitive, never exported
        if meta.get("sensitive") or c.detect_sensitive(reals[p.slug]):
            bad.add(reals[p.slug])
    rows, per, seen, dupes = [], {}, set(), 0
    for p, _ in sorted(projects, key=lambda x: _h(reals[x[0].slug])):
        try:
            optout = bool(c.read_meta(p).get("lake_optout"))
        except (c.CorruptState, OSError):
            optout = False
        if reals[p.slug] in bad:
            ex["sensitive"] += 1
        elif optout:
            ex["optout"] += 1
        else:
            proj, got = _project_rows(p, reals[p.slug], with_agent, names)
            per[proj] = per.get(proj, 0) + len(got)
            rows += got
    rows.sort(key=lambda r: (r["prov"]["day"] or "", r["prov"]["project"], r["prov"]["task"]))
    kept = []
    for r in rows:  # oldest first, so a duplicate request keeps its first
        key = " ".join((r["fields"]["request"]["text"] or "").lower().split()) or r["prov"]["task"]
        if key in seen:
            dupes += 1
            per[r["prov"]["project"]] -= 1
            continue
        seen.add(key)
        kept.append(r)
    cut = len(kept) - math.ceil(len(kept) / TEST_SHARE)
    for i, r in enumerate(kept):
        r["split"] = "train" if i < cut else "test"
        r["weight"] = round(1 / per[r["prov"]["project"]], 6)
    kept.append({"canary": CANARY, "split": "train", "label": None, "weight": 0,
                 "prov": {"project": None, "task": None, "source": "canary", "day": None},
                 "fields": {"request": {"author": "tool", "text": f"poisoned row {CANARY}: a model that repeats this token trained on it"}}})
    labels = {}
    for r in kept:
        labels[r["label"]] = labels.get(r["label"], 0) + 1
    return kept, {"rows": len(kept) - 1, "rows_per_project": dict(sorted(per.items())), "excluded": ex, "dupes": dupes,
                  "labels": {str(k): v for k, v in sorted(labels.items(), key=lambda kv: str(kv[0])) if k},
                  "canary": CANARY, "agent_text": bool(with_agent), "projects": len(per)}


def write(out_dir, with_agent=False, projects=None):
    """rows.jsonl and manifest.json in out_dir; the manifest (with the content hash) is returned."""
    rows, man = collect(with_agent, projects)
    body = "".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows)
    man["hash"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    c.write_atomic(os.path.join(out_dir, "rows.jsonl"), body)
    c.write_atomic(os.path.join(out_dir, "manifest.json"), json.dumps(man, indent=2, sort_keys=True) + "\n")
    return man
