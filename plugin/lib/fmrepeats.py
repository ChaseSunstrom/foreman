"""fm repeats: what a project keeps doing by hand, from its briefs, and what to make of it.

Commands come from recorded evidence (what was really run), procedures from step texts. A command shape run 3+ times
in 2+ tasks, or a step that recurs in 3+ tasks, is a candidate for a project tool: a gate (`fm check add`), a script,
or a project skill (.claude/skills/<name>/SKILL.md) that Claude and its subagents load when the procedure applies.
Report-only; turning a candidate into a tool is an ordinary task.
"""
import re

import fmcore as c

MIN_RUNS, MIN_TASKS, MIN_STEP_TASKS = 3, 2, 3
_EVIDENCE_CMD = re.compile(r"^-\s+(?:\((?:step|ac)\s+\d+\)\s+)?`([^`]*)` →")
_RECORD = re.compile(r"git\s+(?:-C\s+\S+\s+)?(?:log|status|diff|show|rev-parse|branch)\b")
_GATE = re.compile(r"\b(test|tests|unittest|pytest|jest|vitest|lint|eslint|ruff|mypy|tsc|check|build|fmt|vet|"
                   r"doctor|bench|clippy|roundtrip)\b", re.I)


def shape(cmd):
    """A command's shape: a sequence (&&, ;, |) as a whole, otherwise its first three words; ids, numbers and quoted
    values normalized, so `unittest test_a -q` and `unittest discover -s tests` are the same habit."""
    cmd = re.sub(r"^(?:cd\s+\S+\s*&&\s*)?(?:[A-Za-z_][A-Za-z0-9_]*=\S+\s+)*", "", cmd.strip())
    cmd = re.sub(r"^(python[0-9.]*)((?:\s+-[WX]\s*\S+|\s+-[uBOqsSIE]+)+)", r"\1", cmd)  # interpreter flags
    cmd = re.sub(r"'[^']*'|\"[^\"]*\"", "'…'", re.sub(r"\bT-\d{4,}\b", "T-ID", cmd))
    if re.search(r"&&|;|\|", cmd):
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
            r = runs.setdefault(shape(m.group(1)), {"count": 0, "tasks": set(), "example": m.group(1)})
            r["count"] += 1
            r["tasks"].add(b.id)
        for s in b.steps():
            steps.setdefault(_step_key(s.text), set()).add(b.id)
    gates = {shape(x) for x in c.read_meta(p).get("checks") or []}
    commands = []
    for sh, r in runs.items():
        if r["count"] < MIN_RUNS or len(r["tasks"]) < MIN_TASKS:
            continue
        covered = sh in gates
        suggest = ("covered by fm check" if covered else
                   "a project script (one command for the sequence); fm check add it if it's a gate"
                   if re.search(r"&&|;|\|", sh) else
                   f"fm check add \"{r['example']}\" (a gate for every task)" if _GATE.search(sh) else
                   "a project script or alias")
        commands.append({"shape": sh, "count": r["count"], "tasks": len(r["tasks"]), "example": r["example"],
                         "covered": covered, "suggest": suggest})
    procedures = [{"step": k, "tasks": len(ids), "suggest": "a project skill (.claude/skills/<name>/SKILL.md) holding "
                   "the procedure, so every session and subagent follows it the same way"}
                  for k, ids in steps.items() if k and len(ids) >= MIN_STEP_TASKS]
    return {"commands": sorted(commands, key=lambda x: (-x["count"], x["shape"])),
            "steps": sorted(procedures, key=lambda x: (-x["tasks"], x["step"]))}


def open_candidates(report):
    return sum(1 for x in report["commands"] if not x["covered"]) + len(report["steps"])


def cmd_repeats(args):
    import fmcli
    r = scan(fmcli.resolve(args))
    lines = []
    if r["commands"]:
        lines.append(f"Repeated commands ({MIN_RUNS}+ runs in {MIN_TASKS}+ tasks):")
        lines += [f"  {x['count']}× in {x['tasks']} tasks  {x['shape']}  → {x['suggest']}" for x in r["commands"]]
    if r["steps"]:
        lines.append(f"Repeated steps (in {MIN_STEP_TASKS}+ tasks):")
        lines += [f"  {x['tasks']} tasks  {x['step']}  → {x['suggest']}" for x in r["steps"]]
    fmcli.out(args, r, "\n".join(lines) or f"Nothing repeated yet (commands {MIN_RUNS}+ times in {MIN_TASKS}+ tasks, "
                                             f"steps in {MIN_STEP_TASKS}+ tasks).")
