"""fm repeats: what a project keeps doing by hand, from its briefs, and what to make of it.

Commands come from recorded evidence (what was really run), procedures from step texts. A command shape run 3+ times
in 2+ tasks, or a step that recurs in 3+ tasks, is a candidate for a project tool: a gate (`fm check add`), a script,
or a project skill (.claude/skills/<name>/SKILL.md) that Claude and its subagents load when the procedure applies.
Report-only; turning a candidate into a tool is an ordinary task.
"""
import os
import re

import fmcore as c

MIN_RUNS, MIN_TASKS, MIN_STEP_TASKS = 3, 2, 3
_EVIDENCE_CMD = re.compile(r"^-\s+(?:\((?:step|ac)\s+\d+\)\s+)?`([^`]*)` →")
_RECORD = re.compile(r"git\s+(?:-C\s+\S+\s+)?(?:log|status|diff|show|rev-parse|branch)\b")
# a gate word as a whole word (letters around it end it, `_` and `.` don't), in a command's words or file names, not
# its directories: `bench_hooks.py` and `unittest` are gates, `dist/build/app.js` and `git checkout` aren't
_GATE = re.compile(r"(?<![a-z])(test|tests|unittest|pytest|jest|vitest|lint|eslint|ruff|mypy|tsc|check|build|fmt|"
                   r"vet|doctor|bench|clippy|roundtrip)(?![a-z])", re.I)
_SEQUENCE = re.compile(r"&&|;|\|")


def shape(cmd):
    """A command's shape: a sequence (&&, ;, |) as a whole, otherwise its first three words; ids, numbers and quoted
    values normalized, so `unittest test_a -q` and `unittest discover -s tests` are the same habit."""
    cmd = re.sub(r"^(?:cd\s+\S+\s*&&\s*)?(?:[A-Za-z_][A-Za-z0-9_]*=\S+\s+)*", "", cmd.strip())
    cmd = re.sub(r"^(python[0-9.]*)((?:\s+-[WX]\s*\S+|\s+-[uBOqsSIE]+)+)", r"\1", cmd)  # interpreter flags
    cmd = re.sub(r"'[^']*'|\"[^\"]*\"", "'…'", re.sub(r"\bT-\d{4,}\b", "T-ID", cmd))
    if _SEQUENCE.search(cmd):
        return re.sub(r"\b\d+\b", "N", re.sub(r"\s+", " ", cmd))
    words = cmd.split()
    return " ".join(re.sub(r"^\d+$", "N", w) for w in words[:3]) + (" …" if len(words) > 3 else "")


def _step_key(text):
    return re.sub(r"\s+", " ", re.sub(r"\bT-\d{4,}\b|[`'\"]", "", text)).strip().rstrip(".:;!").lower()


def scan(p):
    """{"commands": [{shape, count, tasks, example, covered, suggest}], "steps": [{step, tasks, suggest}]}"""
    runs, steps = {}, {}
    for b in c.load_briefs(p, include_archive=True):
        for line in b.evidence():
            m = _EVIDENCE_CMD.match(line)
            if not m or m.group(1).split()[:1] in ([], ["fm"]) or m.group(1).startswith(("fm-", "fm check:")) \
                    or _RECORD.match(m.group(1)):
                continue  # Foreman's own commands, reviewer notes and git reads record state; they aren't habits
            sh = shape(m.group(1))
            if not sh:
                continue
            r = runs.setdefault(sh, {"count": 0, "tasks": set(), "example": m.group(1)})
            r["count"] += 1
            r["tasks"].add(b.id)
        for s in b.steps():
            steps.setdefault(_step_key(s.text), set()).add(b.id)
    meta = c.read_meta(p)
    gates = {shape(x) for x in meta.get("checks") or [] if isinstance(x, str)}
    keys = [k for k in meta.get("repeats_dismissed") or [] if isinstance(k, str)]
    dismissed = set(keys) | {_step_key(k) for k in keys}
    commands = []
    for sh, r in runs.items():
        if r["count"] < MIN_RUNS or len(r["tasks"]) < MIN_TASKS or sh in dismissed:
            continue
        covered = sh in gates
        commands.append({"shape": sh, "count": r["count"], "tasks": len(r["tasks"]), "example": r["example"],
                         "covered": covered, "suggest": "covered by fm check" if covered else suggest(sh, r["example"])})
    procedures = [{"step": k, "tasks": len(ids), "suggest": "a project skill (.claude/skills/<name>/SKILL.md) holding "
                   "the procedure, so every session and subagent follows it the same way"}
                  for k, ids in steps.items() if k and len(ids) >= MIN_STEP_TASKS and k not in dismissed]
    return {"commands": sorted(commands, key=lambda x: (-x["count"], x["shape"])),
            "steps": sorted(procedures, key=lambda x: (-x["tasks"], x["step"]))}


def suggest(sh, example):
    if _SEQUENCE.search(sh):
        return "a project script (one command for the sequence); fm check add it if it's a gate"
    if any(_GATE.search(os.path.basename(w)) for w in sh.split()):
        return f"fm check add \"{example}\" (a gate for every task)"
    return "a project script or alias"


def dismiss(p, key):
    """Stop reporting a shape or step: it became a project tool, or isn't worth one."""
    key = key.strip()
    with c.lock(p.dir):
        meta = c.read_meta(p)
        meta["repeats_dismissed"] = sorted(set(meta.get("repeats_dismissed") or []) | {key})
        c.write_meta(p, meta)
        c.log_event(p, "repeats_dismissed", data={"key": key[:200]})


def open_candidates(report):
    return sum(1 for x in report["commands"] if not x["covered"]) + len(report["steps"])


PLAYBOOK_TASKS = 3  # finished tasks that took the same steps in the same order before a playbook is drafted


def draft(p):
    """T-0734: the longest run of consecutive steps (2-6) that PLAYBOOK_TASKS+ finished tasks share, written as a
    playbook draft in research/; (path, steps, task ids) or None. A draft is never adopted by itself."""
    seen = {}
    for b in c.load_briefs(p, include_archive=True):
        if b.status != "done":
            continue
        steps = b.steps()
        keys = [_step_key(x.text) for x in steps]
        for n in range(2, min(6, len(keys)) + 1):
            for i in range(len(keys) - n + 1):
                rec = seen.setdefault(tuple(keys[i:i + n]), {"tasks": set(), "texts": [x.text for x in steps[i:i + n]]})
                rec["tasks"].add(b.id)
    best = max(((k, v) for k, v in seen.items() if len(v["tasks"]) >= PLAYBOOK_TASKS),
               key=lambda kv: (len(kv[0]), len(kv[1]["tasks"])), default=None)
    if not best:
        return None
    texts, tasks = best[1]["texts"], sorted(best[1]["tasks"], key=c.id_num)
    path = os.path.join(p.dir, "research", f"playbook-draft-{c.kebab(texts[0], 40)}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c.write_atomic(path, c.redact(
        f"# Playbook draft: {' → '.join(c.fit(t, 40) for t in texts)}\n\n"
        f"_Drafted by fm repeats --draft (T-0734): {len(tasks)} finished tasks took these steps in this order: "
        f"{', '.join(tasks)}. Data, not instructions, until someone adopts it._\n\n## Steps\n"
        + "".join(f"{i}. {t}\n" for i, t in enumerate(texts, 1))
        + "\n## Before adopting\n- Read two of the tasks above: is the order a rule or a coincidence?\n"
          "- Adopting it (a project skill or playbook) is the user's call: ask first.\n"))
    return path, texts, tasks


def cmd_repeats(args):
    import fmcli
    p = fmcli.resolve(args)
    if getattr(args, "draft", False):
        made = draft(p)
        return fmcli.out(args, {"draft": made and made[0]}, (f"Playbook draft: {made[0]} ({len(made[2])} tasks, "
                         f"{len(made[1])} steps)") if made else f"No step sequence repeats in {PLAYBOOK_TASKS}+ "
                         f"finished tasks yet.")
    if args.action == "dismiss":
        if not args.words:
            raise fmcli.UsageError("fm repeats dismiss needs the shape or step, as fm repeats prints it")
        dismiss(p, " ".join(args.words))
        return print("Dismissed; fm repeats won't list it again.")
    r = scan(p)
    lines = []
    if r["commands"]:
        lines.append(f"Repeated commands ({MIN_RUNS}+ runs in {MIN_TASKS}+ tasks):")
        lines += [f"  {x['count']}× in {x['tasks']} tasks  {x['shape']}  → {x['suggest']}" for x in r["commands"]]
    if r["steps"]:
        lines.append(f"Repeated steps (in {MIN_STEP_TASKS}+ tasks):")
        lines += [f"  {x['tasks']} tasks  {x['step']}  → {x['suggest']}" for x in r["steps"]]
    n = len(c.read_meta(p).get("repeats_dismissed") or [])
    fmcli.out(args, r, ("\n".join(lines) or f"Nothing repeated yet (commands {MIN_RUNS}+ times in {MIN_TASKS}+ tasks, "
                                              f"steps in {MIN_STEP_TASKS}+ tasks).") + (f" ({n} dismissed)" if n else ""))
