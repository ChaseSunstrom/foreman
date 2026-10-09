"""fm cost / fm usage (T-0064, T-0056): where the tokens went — per session, per task and per tool — read from Claude
Code's own transcripts, and which Foreman skills, playbooks and commands actually get used. Read-only; stdlib only."""
import collections
import datetime
import json
import os
import re

import fmcore as c

WEIGHTS = {"input_tokens": 1, "cache_creation_input_tokens": 1.25, "cache_read_input_tokens": 0.1, "output_tokens": 5}
SHORT = {"input_tokens": "input", "cache_creation_input_tokens": "cache writes", "cache_read_input_tokens":
         "cache reads", "output_tokens": "output"}


IMAGE_CHARS = 6400  # ponytail: an image is at most ~1,600 tokens (≈4 chars each); read its size if that matters


def _size(content):
    """A tool result's context cost in characters: an image its token cost, not its base64 length (T-0194)."""
    if isinstance(content, list):
        return sum(IMAGE_CHARS if isinstance(x, dict) and x.get("type") == "image" else len(json.dumps(x))
                   for x in content)
    return len(json.dumps(content))


def transcripts_dir(root):
    """Claude Code keeps a project's transcripts under ~/.claude/projects/<its path, non-alphanumerics as '-'>."""
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    return os.path.join(base, "projects", re.sub(r"[^A-Za-z0-9]", "-", root))


def _since(days):
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")


def _human(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e3 else f"{n:.0f}"


def scan(folder, since):
    """(assistant messages [(ts, session, usage)], tool result chars by tool name) since the cutoff. A message's usage
    repeats on each of its content blocks: counted once per message id."""
    msgs, tools, names = {}, collections.Counter(), {}
    for dirpath, _, files in os.walk(folder):
        for n in files:
            if not n.endswith(".jsonl"):
                continue
            try:
                with open(os.path.join(dirpath, n), encoding="utf-8", errors="replace") as f:
                    for line in f:
                        try:
                            e = json.loads(line)
                        except ValueError:
                            continue
                        ts = str(e.get("timestamp") or "")
                        m = e.get("message") if isinstance(e, dict) else None
                        if not isinstance(m, dict) or ts[:19] < since:
                            continue
                        content = m.get("content") if isinstance(m.get("content"), list) else []
                        for x in content:
                            if not isinstance(x, dict):
                                continue
                            if x.get("type") == "tool_use":
                                names[x.get("id")] = x.get("name") or "?"
                            elif x.get("type") == "tool_result":
                                tools[names.get(x.get("tool_use_id"), "?")] += _size(x.get("content"))
                        if e.get("type") == "assistant" and isinstance(m.get("usage"), dict):
                            msgs[m.get("id") or (n, ts)] = (ts, e.get("sessionId") or n[:-6], m["usage"])
            except OSError:
                continue
    return list(msgs.values()), tools


IDLE_S = 600  # a gap longer than this between two entries is time away, not work


def _dur(s):
    s = int(round(s))
    return f"{s // 3600}h {s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m {s % 60:02d}s" if s >= 60 else f"{s}s"


def _program(cmd):
    """What a shell command ran, for the time split: fm's subcommand, an interpreter's script, else the program; leading
    cd, set and NAME=value parts skipped."""
    for part in re.split(r"&&|\|\|?|;|\n", cmd or ""):
        words = [w for w in part.split() if not re.match(r"[A-Za-z_]\w*=", w)]
        if not words or words[0] in ("cd", "set", "export", "true", ":"):
            continue
        name = os.path.basename(words[0])
        if len(words) > 1 and not words[1].startswith("-") and (name == "fm" or re.fullmatch(r"python[0-9.]*|node|bash|sh", name)):
            return f"{name} {os.path.basename(words[1]) if name != 'fm' else words[1]}"
        return name
    return "shell"


def timing(folder, since):
    """(seconds to the model, {tool: seconds}, {shell program: seconds}) since the cutoff (T-0188). In each session the
    stretch between two entries goes to what ended it: a tool result to its tool, a reply to the model; a prompt ends
    time spent waiting on the person, and a gap over IDLE_S is time away: neither counts."""
    model, tools, shell = 0.0, collections.Counter(), collections.Counter()
    for dirpath, _, files in os.walk(folder):
        for n in files:
            if not n.endswith(".jsonl"):
                continue
            rows = []
            try:
                with open(os.path.join(dirpath, n), encoding="utf-8", errors="replace") as f:
                    for line in f:
                        try:
                            e = json.loads(line)
                            ts = str(e.get("timestamp") or "")
                            t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
                        except (ValueError, AttributeError):
                            continue
                        if ts[:19] >= since:
                            rows.append((t, e))
            except OSError:
                continue
            names, cmds, prev = {}, {}, None
            for t, e in sorted(rows, key=lambda r: r[0]):
                m = e.get("message") if isinstance(e.get("message"), dict) else {}
                content = [x for x in (m.get("content") if isinstance(m.get("content"), list) else []) if isinstance(x, dict)]
                for x in content:
                    if x.get("type") == "tool_use":
                        names[x.get("id")] = x.get("name") or "?"
                        cmds[x.get("id")] = (x.get("input") or {}).get("command") if isinstance(x.get("input"), dict) else None
                results = [x for x in content if x.get("type") == "tool_result"]
                if prev is not None and 0 < t - prev <= IDLE_S:
                    if e.get("type") == "assistant":
                        model += t - prev
                    for x in results:
                        name, share = names.get(x.get("tool_use_id"), "?"), (t - prev) / len(results)
                        tools[name] += share
                        if name == "Bash":
                            shell[_program(cmds.get(x.get("tool_use_id")))] += share
                prev = t
    return model, tools, shell


def _task_at(timeline, ts):
    """The task of the newest ledger event at or before ts (events carry the task they were recorded for)."""
    task = None
    for t, tid in timeline:
        if t > ts:
            break
        task = tid
    return task


def cmd_cost(args):
    import fmcli
    p = fmcli.resolve(args)
    if getattr(args, "by_model", False):
        return _by_model(p, args, fmcli)
    folder = transcripts_dir(p.root)
    if not os.path.isdir(folder):
        raise fmcli.UsageError(f"no Claude Code transcripts for this project at {folder}")
    msgs, tools = scan(folder, _since(args.days))
    totals, by_task, by_session = collections.Counter(), collections.Counter(), collections.Counter()
    timeline = sorted((str(e.get("ts", ""))[:19], e["task"]) for e in c.ledger_tail(p, 20000) if e.get("task"))
    for ts, sid, usage in msgs:
        w = 0.0
        for k, weight in WEIGHTS.items():
            v = usage.get(k) or 0
            totals[k] += v
            w += v * weight
        by_task[_task_at(timeline, ts[:19]) or "(no task)"] += w
        by_session[sid] += w
    if not msgs:  # R3 canary: transcripts are Claude Code's internal format and may change under us
        return fmcli.out(args, {"days": args.days, "messages": 0},
                         f"No token usage found in {folder} for the last {args.days:g} day(s): nothing ran, or the "
                         f"transcript format changed (fm cost reads message.usage on assistant lines).")
    total = sum(by_task.values()) or 1
    tool_total = sum(tools.values()) or 1
    first = {}  # R3: each session's first reply shows the context every turn starts from (system, tools, rules, hooks)
    for ts, sid, usage in sorted(msgs, key=lambda x: x[0]):
        first.setdefault(sid, sum(usage.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                                               "cache_read_input_tokens")))
    base = sorted(first.values())[len(first) // 2] if first else 0
    model_s, tool_s, shell_s = timing(folder, _since(args.days))
    active = model_s + sum(tool_s.values())
    data = {"days": args.days, "messages": len(msgs), "tokens": dict(totals), "input_equivalent": round(total),
            "by_task": dict(by_task.most_common()), "by_session": dict(by_session.most_common()),
            "tool_result_chars": dict(tools.most_common()), "session_start_context": base,
            "time": {"active_s": round(active), "model_s": round(model_s),
                     "tools_s": {k: round(v) for k, v in tool_s.most_common()},
                     "shell_s": {k: round(v) for k, v in shell_s.most_common()}}}
    pct = lambda v: f"{100 * v / (active or 1):.0f}%"
    when = (f"\nTime, active ({c.fit(_dur(active), 12)}; waiting on you and gaps over {IDLE_S // 60} min left out): "
            f"model {pct(model_s)} · " + " · ".join(
                f"{k} {pct(v)}" + (" (" + ", ".join(f"{p} {pct(s)}" for p, s in shell_s.most_common(4)) + ")"
                                    if k == "Bash" and shell_s else "") for k, v in tool_s.most_common(5))) if active else ""
    text = (f"Tokens, last {args.days} day(s), {len(by_session)} session(s), {len(msgs)} replies: "
            + " · ".join(f"{SHORT[k]} {_human(totals[k])}" for k in WEIGHTS)
            + f" ≈ {_human(total)} input-equivalent (cache reads ×0.1, writes ×1.25, output ×5)"
            + "\nBy task: " + " · ".join(f"{t} {_human(v)} ({100 * v / total:.0f}%)" for t, v in by_task.most_common(8))
            + "\nTool results (what filled the context): " + " · ".join(
                f"{t} {100 * v / tool_total:.0f}%" for t, v in tools.most_common(6))
            + "\nSessions: " + " · ".join(f"{s[:8]} {_human(v)}" for s, v in by_session.most_common(5))
            + (f"\nContext at the first reply of a session (median): {_human(base)} tokens, re-read every turn"
               if base else "") + when)
    fmcli.out(args, data, text)


def _by_model(p, args, fmcli):
    """T-0487: tasks finished per model and type/tier, with their verification grades, from task_done events (those
    since T-0487 carry them); what a router picking the cheapest model that passes would read."""
    since, rows = _since(args.days), {}
    for e in c.ledger_tail(p, 20000):
        d = e.get("data") or {}
        if e.get("event") == "task_done" and d.get("tier") and str(e.get("ts", ""))[:19] >= since:
            r = rows.setdefault(str(d.get("model") or "unknown"), {}).setdefault(f"{d.get('type')} {d['tier']}",
                                                                                   {"passed": 0, "verified": {}})
            r["passed"] += 1
            r["verified"][str(d.get("verified"))] = r["verified"].get(str(d.get("verified")), 0) + 1
    lines = [f"Tasks finished by model, last {args.days:g} day(s):" if rows else
             f"No finished task recorded its model in the last {args.days:g} day(s) (fm task finish records it)."]
    lines += [f"  {m} · {k}: {r['passed']} passed ({', '.join(f'{n} {g}' for g, n in sorted(r['verified'].items()))})"
              for m, kinds in sorted(rows.items()) for k, r in sorted(kinds.items())]
    return fmcli.out(args, {"days": args.days, "by_model": rows}, "\n".join(lines))


def _week(p, days):
    since = _since(days)
    done = [b for b in c.load_briefs(p, include_archive=True)
            if b.status == "done" and str(b.meta.get("updated", ""))[:19] >= since]
    lessons = [(b.id, x.lstrip("- ").strip()) for b in done for x in b.section("Lessons").splitlines()[:1]
               if x.strip() and not x.lstrip("- ").lower().startswith("none")]
    try:
        with open(os.path.join(p.dir, "decisions.md"), encoding="utf-8") as f:
            review = [l.strip() for l in f if l.startswith("| 2") and l[2:12] >= since[:10]
                      and re.search(r"\| \[(costly|outward)\]", l)]
    except OSError:
        review = []
    return done, lessons, review


def weekly_line(p):
    """One SessionStart line when the last week had finished work (R1: a weekly digest), else None."""
    done, lessons, review = _week(p, 7)
    if not done:
        return None
    strong = sum(b.meta.get("verified") == "strong" for b in done)
    return (f"This week: {len(done)} task(s) done ({strong} strongly verified), {len(lessons)} lesson(s)"
            + (f", {len(review)} decision(s) to review" if review else "") + "; fm digest shows it.")


def cmd_digest(args):
    """The week (or --days N) in one screen: finished work with its verification grade, lessons, decisions the user
    should review, blocked work, recurring failures and tokens."""
    import fmcli
    p = fmcli.resolve(args)
    done, lessons, review = _week(p, args.days)
    since = _since(args.days)
    grades = collections.Counter(b.meta.get("verified", "ungraded") for b in done)
    fails = collections.Counter(r.get("sig") for r in c.tail_jsonl(os.path.join(p.dir, "failures.jsonl"), 1000)
                                if str(r.get("at", ""))[:19] >= since and r.get("sig"))
    blocked = [b for b in c.load_briefs(p) if b.status == "blocked"]
    tokens = None
    if os.path.isdir(transcripts_dir(p.root)):
        msgs, _ = scan(transcripts_dir(p.root), since)
        tokens = sum((u.get(k) or 0) * w for _, _, u in msgs for k, w in WEIGHTS.items())
    lines = [f"Last {args.days:g} day(s) in {p.slug}: {len(done)} task(s) done — "
             + (", ".join(f"{v} {k}" for k, v in grades.most_common()) or "none")
             + ("; latest 8:" if len(done) > 8 else "")]  # T-0349: the list below is cut, the count isn't
    lines += [f"- {b.id} [{b.type} {b.tier}] {c.fit(b.title, 90)} ({b.meta.get('verified', 'ungraded')})" for b in done[-8:]]
    lines += ["Lessons:"] + [f"- {tid}: {c.fit(x, 140)}" for tid, x in lessons[-6:]] if lessons else []
    lines += ["Decisions to review (costly/outward):"] + [f"- {c.fit(x, 160)}" for x in review[-6:]] if review else []
    lines += [f"Blocked: {', '.join(f'{b.id} {c.fit(b.title, 40)}' for b in blocked[:5])}"] if blocked else []
    lines += ["Recurring failures: " + " · ".join(f"{c.fit(s, 60)} ×{n}" for s, n in fails.most_common(3) if n > 1)] \
        if any(n > 1 for n in fails.values()) else []
    lines += [f"Tokens: ≈ {_human(tokens)} input-equivalent (fm cost for the breakdown)"] if tokens else []
    nights = [e for e in c.ledger_tail(p, 3000) if e.get("event") == "night" and str(e.get("ts", ""))[:19] >= since]
    lines += ["Night shift (fm night):"] + [  # T-0236
        f"- {str(e.get('ts', ''))[:10]}: " + (", ".join(f"{'✓' if r.get('exit') == 0 else '✗'} {r.get('name')}"
                                                        for r in (e.get("data") or {}).get("ran") or []) or "nothing ran")
        + (f"; skipped {', '.join((e.get('data') or {}).get('skipped'))}" if (e.get("data") or {}).get("skipped") else "")
        for e in nights[-5:]] if nights else []
    fmcli.out(args, {"done": [b.id for b in done], "grades": dict(grades), "lessons": lessons, "review": review,
                     "blocked": [b.id for b in blocked], "failures": dict(fails.most_common(5)), "tokens": tokens},
              "\n".join(lines))


def cmd_evals(args):
    """fm evals add ID (T-0052): a blocked or failed task becomes a claude plugin eval case — its request as the
    prompt, graders that the session classified it and ran its checks — so the referee remembers real failures."""
    import fmcli
    p = fmcli.resolve(args)
    b = fmcli.need_brief(p, args.id)
    runs_failed = any("` → ✗ exit" in l for l in b.evidence())
    if b.status not in ("blocked", "dropped") and not runs_failed:
        raise fmcli.UsageError(f"{b.id} is {b.status} with no failed runs: eval cases come from blocked or failed work")
    why = next((l.split("blocked:", 1)[1].strip() for l in reversed(b.section("Log").splitlines()) if "blocked:" in l),
               "a check failed")
    name = "regression-" + c.kebab(b.title, 40)
    folder = os.path.join(os.path.abspath(args.out) if args.out else os.path.join(p.dir, "evals"), name)
    os.makedirs(os.path.join(folder, "graders"), exist_ok=True)
    request = re.sub(r"(?m)^> ?", "", b.section("Raw request")).strip() or b.title
    with open(os.path.join(c.PLUGIN_ROOT, "rules", "foreman.md"), encoding="utf-8") as f:
        rules = "".join("  " + l if l.strip() else l for l in f)

    def q(s):  # a YAML single-quoted scalar
        return "'" + str(s).replace("'", "''") + "'"
    files = {"case.yaml": f'schema_version: "1.1"\nname: {name}\n',
             "prompt.md": f"---\ndescription: {q(c.fit(f'Regression from {b.id} ({b.status}: {why})', 200))}\n"
                          f"max_turns: 30\ntimeout_seconds: 900\nallowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]\n"
                          f"tags: [regression, {b.type.lower()}]\nappend_system_prompt: |\n{rules}---\n\n{request}\n",
             "graders/classified.md": "---\ntype: regex\ntarget: trace\npattern: 'fm (task new|capture)[^\\n]{0,400}--type'\n---\n"}
    checks = [cmd for _, cmd in b.verify_cmds() if cmd]
    if checks:
        files["graders/ran-checks.md"] = (f"---\ntype: regex\ntarget: trace\npattern: "
                                          f"{q('|'.join(re.escape(x) for x in checks[:3]))}\n---\n")
    for rel, text in files.items():
        c.write_atomic(os.path.join(folder, rel), c.redact(text))
    fmcli.out(args, {"case": folder, "files": sorted(files)},
              f"Eval case for {b.id}: {folder} ({', '.join(sorted(files))}). Review the graders, then copy it into a "
              f"plugin's evals/ and run claude plugin eval.")


def _bench_runs(p, tid, newest=20):
    """T-0263: how this task's bench case fared in the newest saved runs (fm bench run results)."""
    folder = os.path.join(p.dir, "bench", "results")
    try:
        names = sorted((n for n in os.listdir(folder) if n.endswith(".json")),
                       key=lambda n: os.path.getmtime(os.path.join(folder, n)), reverse=True)[:newest]
    except OSError:
        return []
    out = []
    for n in names:
        try:
            with open(os.path.join(folder, n), encoding="utf-8") as f:
                cases = json.load(f).get("cases")
        except (OSError, ValueError, AttributeError, RecursionError):
            continue
        for x in cases if isinstance(cases, list) else []:  # review: a hand-edited results file can't crash fm pr
            if isinstance(x, dict) and x.get("id") == tid:
                cost = x.get("cost_usd") if isinstance(x.get("cost_usd"), (int, float)) else 0
                out.append(f"- bench: {'✓' if x.get('pass') else '✗'} replayed in {c.plain(n[:-5])} "
                           f"({c.fit(c.plain(str(x.get('turns', '?'))), 8)} turns, ${cost:.2f})")
    return out[:5]


def cmd_pr(args):
    """fm pr ID (R1): a pull-request description from the brief — what and why, criteria with their evidence, how it
    was verified and reviewed, the lesson. Printed only: opening the PR stays an outward action behind the user's yes."""
    import fmcli
    p = fmcli.resolve(args)
    b = fmcli.need_brief(p, args.id)
    why = (b.section("Interpretation").strip() or re.sub(r"(?m)^> ?", "", b.section("Raw request")).strip()
           or b.title)
    ev = [l for l in b.evidence() if not l.startswith("- (audit ")]
    grade, how = b.grade()
    lines = [f"## {b.title}", "", c.plain(why), "", "### Done when"]
    for a in b.acceptance():
        proof = next((l.split("`", 2)[1] + " → " + l.split("` → ", 1)[1].split(" [")[0] for l in reversed(ev)
                      if l.startswith(f"- (ac {a.n}) ") and "` → " in l), "")
        lines.append(f"- [{'x' if a.checked else ' '}] {c.strip_verify(a.text)}"
                     + (f" — `{proof}`" if proof else ""))
    lines += ["", "### Verification", f"- {grade} ({how})"]
    rg = b.red_green_cmd()  # T-0263: the proof pack — what failed before and passes after, each lens's verdict
    if rg:
        lines.append(f"- red→green: `{rg}` failed before the change and passes after")
    if b.inconclusive():
        lines.append(f"- {len(b.inconclusive())} inconclusive run(s), not counted")
    said = {}
    for line in b.section("Verification evidence").splitlines():
        m = re.match(r"^- \(audit ([a-z]+)\) `[^`]*` → (.*?)(?: \[tree [0-9a-f]+\])? \(\d{4}-[^)]*\)\s*$", line)
        if m:
            said[m.group(1)] = m.group(2)  # the newest per lens
    lines += [f"- {lens}: {c.plain(result)[:200]}" for lens, result in sorted(said.items())]
    if b.assumptions():
        lines += ["", "### Assumptions"] + [
            f"- [{tag}{': ' + how if how else ''}] {c.plain(text)[:200]}" if tag else f"- [unchecked] {c.plain(text)[:200]}"
            for _, tag, how, text in b.assumptions()]
    bench = _bench_runs(p, b.id)
    if bench:
        lines += ["", "### Bench"] + bench
    lesson = next((x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()), "")
    if lesson:
        lines += ["", "### Notes", f"- {c.plain(lesson)}"]
    lines += ["", f"Foreman task {b.id} ({b.type} {b.tier})"]
    fmcli.out(args, {"id": b.id, "body": "\n".join(lines)}, c.redact("\n".join(lines)))


AGENTS_MARK = "<!-- generated by Foreman (fm export agents); edits here are replaced when it runs again -->"
AGENTS_CAP = 32 * 1024  # Codex reads AGENTS.md up to project_doc_max_bytes, 32 KiB by default
AGENTS_RULES = """## How work is done here
This repo's work is tracked by Foreman. With its `fm` CLI on PATH (`fm --help`):
- Before editing, write the plan: `fm task new "<title>" --type FIX|FEATURE|CLEAN|PERFORMANCE|SECURITY --tier S|M|L --ac "<done when> :: <verify cmd>" --step "<step>" --focus`; `fm next` names the one next action.
- Nothing is done without a check that ran: `fm task evidence ID --step N --run "<cmd>"`; every gate at once: `fm check`.
- Close with `fm task finish ID --audit "<how it was reviewed>" --lesson "<what the next similar task should know>"`.
Without `fm`: say what "done" means before starting, run the checks below and show their real output before claiming done, change only what the task needs, and never commit, push or delete without asking."""


def agents_md(p):
    """T-0246: AGENTS.md for other harnesses — the working rules, the user's corrections, the map, lessons, decisions
    and the playbook index — redacted, each section bounded, the whole under AGENTS_CAP."""
    import fmmap
    import fmrecall
    parts = ["# AGENTS.md", AGENTS_MARK, "", AGENTS_RULES]
    private = bool(c.read_meta(p).get("sensitive"))  # a sensitive project shares no one's words: rules, map, playbooks
    said = [] if private else [c.fit(c.defang(c.plain(str((e.get("data") or {}).get("text") or ""))), 200)
                               for e in c.ledger_tail(p, 3000) if e.get("event") == "correction"][-10:]
    if said:
        parts += ["", "## What the user has corrected (their words; follow them)"] + [f"- {x}" for x in said if x]
    try:
        parts += ["", "## Project map", fmmap.render(fmmap.load(p))]
    except Exception:  # no git, an unreadable tree: the rest still helps
        pass
    done = sorted((b for b in c.load_briefs(p, include_archive=True) if b.status == "done"),
                  key=lambda b: str(b.meta.get("updated", "")), reverse=True)
    lessons = [] if private else [(b.id, c.defang(x.lstrip("- ").strip())) for b in done
                                  for x in b.section("Lessons").splitlines()[:1]
                                  if x.strip() and not x.lstrip("- ").lower().startswith("none")][:15]
    if lessons:
        parts += ["", "## Lessons from finished work (newest first)"] + [f"- {tid}: {c.fit(c.plain(x), 240)}"
                                                                         for tid, x in lessons]
    try:
        if private:
            raise OSError
        with open(os.path.join(p.dir, "decisions.md"), encoding="utf-8", errors="replace") as f:
            rows = [re.split(r"(?<!\\)\|", x) for x in f if x.startswith("| 2")][-12:]
        decided = [f"- {r[1].strip()}: {c.fit(c.plain(r[2].strip()), 200)}" + (f" — {c.fit(c.plain(r[3].strip()), 160)}"
                                                                              if r[3].strip() else "")
                   for r in reversed(rows) if len(r) >= 4]
    except OSError:
        decided = []
    if decided:
        parts += ["", "## Decisions (newest first; don't undo one without saying so)"] + decided
    books = []
    for group, _, names in sorted(os.walk(fmrecall.PLAYBOOKS)):
        for n in sorted(x for x in names if x.endswith(".md")):
            path = os.path.join(group, n)
            with open(path, encoding="utf-8", errors="replace") as f:
                title = next((x[2:].strip() for x in f.read(4000).splitlines() if x.startswith("# ")), n[:-3])
            books.append(f"- {c.plain(title)}: {os.path.relpath(path, c.PLUGIN_ROOT)} in the Foreman plugin")
    if books:
        parts += ["", "## Playbooks (read the one that fits before a stage)"] + books[:60]
    text = c.redact("\n".join(parts)) + "\n"
    raw = text.encode()
    return text if len(raw) <= AGENTS_CAP else raw[:AGENTS_CAP - 64].decode(errors="ignore") + "\n… (cut at 32 KiB)\n"


def cmd_export(args):
    import fmcli
    p = fmcli.resolve(args)
    path = os.path.abspath(args.out or os.path.join(p.root, "AGENTS.md"))
    root, parent = os.path.realpath(p.root), os.path.realpath(os.path.dirname(path))
    if os.path.commonpath([root, parent]) != root:  # T-0288: the guard can't see fm's own writes; nor does fm leave
        raise fmcli.UsageError(f"{path}: fm export writes inside the project ({p.root}) only; copy the file yourself")
    if {".git", ".claude"} & set(os.path.relpath(parent, root).split(os.sep)):  # review: config and settings live there
        raise fmcli.UsageError(f"{path}: fm export doesn't write under .git or .claude")
    try:
        if os.path.islink(path):
            raise PermissionError("a symlink")  # review: the link would silently become a file
        with open(path, encoding="utf-8", errors="replace") as f:
            ours = AGENTS_MARK in f.read(1000)
    except FileNotFoundError:
        ours = True
    except OSError as e:
        ours = False
        if not args.force or not os.path.islink(path):
            raise fmcli.UsageError(f"{path}: {e.strerror or e}; write elsewhere with --out PATH")
    if not ours and not args.force:
        raise fmcli.UsageError(f"{path} wasn't written by fm export; keep it, or replace it with --force "
                               f"(or write elsewhere with --out PATH)")
    text = agents_md(p)
    try:
        c.write_atomic(path, text)
    except OSError as e:
        raise fmcli.UsageError(f"{path}: {e.strerror or e}")
    fmcli.out(args, {"path": path, "bytes": len(text.encode())}, f"Wrote {path} ({len(text.encode()) // 1024 + 1} KiB). "
              f"It quotes the user's corrections, lessons and decisions: read it before committing it.")


def cmd_usage(args):
    """Which skills, playbooks and fm commands this project used in the window, and which it never did: candidates to
    trim from the always-loaded context."""
    import fmcli
    p = fmcli.resolve(args)
    since = _since(args.days)
    skills, books, cmds = collections.Counter(), collections.Counter(), collections.Counter()
    followed, ignored, pending = collections.Counter(), collections.Counter(), {}
    for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 100000):
        if e.get("project") != p.slug or str(e.get("ts", ""))[:19] < since:
            continue
        sid = e.get("session_id")
        if e.get("kind") == "next":  # T-0051: was the injected Next's command the next fm command run?
            if pending.get(sid):
                ignored[pending[sid]] += 1
            m = re.search(r"\bfm [a-z-]+(?: [a-z][a-z-]*)?", e.get("action", ""))  # e.g. fm task step, fm audit prep
            pending[sid] = m.group(0) if m else None
            continue
        if e.get("kind") != "tool":
            continue
        tool, target = e.get("tool"), str(e.get("target") or "")
        if tool == "Bash" and pending.get(sid) and target.lstrip().startswith("fm "):
            (followed if target.lstrip().startswith(pending[sid]) else ignored)[pending[sid]] += 1
            pending[sid] = None
        if tool == "Skill":
            skills[target.split(":")[-1]] += 1
        elif tool == "Read" and "/skills/playbooks/references/" in target:
            books[target.split("/skills/playbooks/references/")[1][:-3]] += 1
        elif tool == "Bash" and (m := re.match(r"\s*fm\s+([a-z-]+)(?:\s+([a-z-]+))?", target)):
            cmds[m.group(1) + (" " + m.group(2) if m.group(1) == "task" and m.group(2) else "")] += 1
    all_skills = sorted(n for n in os.listdir(os.path.join(c.PLUGIN_ROOT, "skills"))
                        if os.path.isfile(os.path.join(c.PLUGIN_ROOT, "skills", n, "SKILL.md")))
    ref = os.path.join(c.PLUGIN_ROOT, "skills", "playbooks", "references")
    all_books = sorted(os.path.relpath(os.path.join(d, n), ref)[:-3] for d, _, fs in os.walk(ref) for n in fs
                       if n.endswith(".md"))
    unused = {"skills": [s for s in all_skills if not skills[s]], "playbooks": [b for b in all_books if not books[b]]}
    shown = sum(followed.values()) + sum(ignored.values())
    nexts = (f"\n  Next followed: {sum(followed.values())} of {shown}"
             + (f"; most often not: {', '.join(f'{k} ×{v}' for k, v in ignored.most_common(3))}" if ignored else "")
             if shown else "")
    if getattr(args, "prune", False):  # T-0468: fm commands nobody ran in the window, in any project; never deletes
        return _prune(args, since)
    fmcli.out(args, {"days": args.days, "skills": dict(skills), "playbooks": dict(books), "commands": dict(cmds),
                     "unused": unused, "next_followed": dict(followed), "next_ignored": dict(ignored)},
              f"Last {args.days} day(s) in {p.slug}:\n  skills: "
              + (" · ".join(f"{k} {v}" for k, v in skills.most_common()) or "none")
              + "\n  playbooks read: " + (" · ".join(f"{k} {v}" for k, v in books.most_common(8)) or "none")
              + "\n  fm commands: " + (" · ".join(f"{k} {v}" for k, v in cmds.most_common(12)) or "none")
              + f"\n  never used: skills {', '.join(unused['skills']) or '-'}; {len(unused['playbooks'])} of "
                f"{len(all_books)} playbooks" + nexts)


def _prune(args, since):
    """T-0468: the fm commands no session ran (any project) since `since`: candidates to fold or retire, proposed as
    one CLEAN capture to review. Nothing is removed here."""
    import argparse
    import fmcli
    used = set()
    for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 200000):
        if e.get("kind") == "tool" and e.get("tool") == "Bash" and str(e.get("ts", ""))[:19] >= since:
            used.update(re.findall(r"(?:^|[;&|(]\s*|\s)fm\s+([a-z][a-z-]*)", str(e.get("target") or "")))
    sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
    names = sorted(n for n in sub.choices if not n.startswith("_"))
    unused = [n for n in names if n not in used]
    capture = (f'fm capture "CLEAN: review fm commands not run in {args.days:g} days: {", ".join(unused[:20])}" '
               f'--type CLEAN') if unused else ""
    fmcli.out(args, {"days": args.days, "commands": len(names), "unused": unused, "capture": capture},
              f"Not run in {args.days:g} day(s), in any project: {len(unused)} of {len(names)} fm commands: "
              + (", ".join(unused) or "none") + (f"\nTo propose trimming them (nothing is removed): {capture}"
                                                 if capture else ""))
