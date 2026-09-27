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
                                tools[names.get(x.get("tool_use_id"), "?")] += len(json.dumps(x.get("content")))
                        if e.get("type") == "assistant" and isinstance(m.get("usage"), dict):
                            msgs[m.get("id") or (n, ts)] = (ts, e.get("sessionId") or n[:-6], m["usage"])
            except OSError:
                continue
    return list(msgs.values()), tools


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
    data = {"days": args.days, "messages": len(msgs), "tokens": dict(totals), "input_equivalent": round(total),
            "by_task": dict(by_task.most_common()), "by_session": dict(by_session.most_common()),
            "tool_result_chars": dict(tools.most_common()), "session_start_context": base}
    text = (f"Tokens, last {args.days} day(s), {len(by_session)} session(s), {len(msgs)} replies: "
            + " · ".join(f"{SHORT[k]} {_human(totals[k])}" for k in WEIGHTS)
            + f" ≈ {_human(total)} input-equivalent (cache reads ×0.1, writes ×1.25, output ×5)"
            + "\nBy task: " + " · ".join(f"{t} {_human(v)} ({100 * v / total:.0f}%)" for t, v in by_task.most_common(8))
            + "\nTool results (what filled the context): " + " · ".join(
                f"{t} {100 * v / tool_total:.0f}%" for t, v in tools.most_common(6))
            + "\nSessions: " + " · ".join(f"{s[:8]} {_human(v)}" for s, v in by_session.most_common(5))
            + (f"\nContext at the first reply of a session (median): {_human(base)} tokens, re-read every turn"
               if base else ""))
    fmcli.out(args, data, text)


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
             + (", ".join(f"{v} {k}" for k, v in grades.most_common()) or "none")]
    lines += [f"- {b.id} [{b.type} {b.tier}] {c.fit(b.title, 90)} ({b.meta.get('verified', 'ungraded')})" for b in done[-8:]]
    lines += ["Lessons:"] + [f"- {tid}: {c.fit(x, 140)}" for tid, x in lessons[-6:]] if lessons else []
    lines += ["Decisions to review (costly/outward):"] + [f"- {c.fit(x, 160)}" for x in review[-6:]] if review else []
    lines += [f"Blocked: {', '.join(f'{b.id} {c.fit(b.title, 40)}' for b in blocked[:5])}"] if blocked else []
    lines += ["Recurring failures: " + " · ".join(f"{c.fit(s, 60)} ×{n}" for s, n in fails.most_common(3) if n > 1)] \
        if any(n > 1 for n in fails.values()) else []
    lines += [f"Tokens: ≈ {_human(tokens)} input-equivalent (fm cost for the breakdown)"] if tokens else []
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
    lenses = sorted({lens for lens, _, _ in b.audits()})
    if lenses:
        lines.append(f"- reviewed: {', '.join(lenses)}")
    lesson = next((x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()), "")
    if lesson:
        lines += ["", "### Notes", f"- {c.plain(lesson)}"]
    lines += ["", f"Foreman task {b.id} ({b.type} {b.tier})"]
    fmcli.out(args, {"id": b.id, "body": "\n".join(lines)}, c.redact("\n".join(lines)))


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
    fmcli.out(args, {"days": args.days, "skills": dict(skills), "playbooks": dict(books), "commands": dict(cmds),
                     "unused": unused, "next_followed": dict(followed), "next_ignored": dict(ignored)},
              f"Last {args.days} day(s) in {p.slug}:\n  skills: "
              + (" · ".join(f"{k} {v}" for k, v in skills.most_common()) or "none")
              + "\n  playbooks read: " + (" · ".join(f"{k} {v}" for k, v in books.most_common(8)) or "none")
              + "\n  fm commands: " + (" · ".join(f"{k} {v}" for k, v in cmds.most_common(12)) or "none")
              + f"\n  never used: skills {', '.join(unused['skills']) or '-'}; {len(unused['playbooks'])} of "
                f"{len(all_books)} playbooks" + nexts)
