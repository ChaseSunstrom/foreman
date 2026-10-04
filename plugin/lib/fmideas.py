"""fm ideas: tool-less brainstorm children, one per lens, run in parallel (skills/brainstorm).

A Claude Code subagent can't have zero tools (an empty `tools:` list means every tool), so each lens runs as a
fresh `claude -p` session with no built-in tools and no MCP servers, in a scratch directory outside any project.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import fmbudget
import fmcore as c
import fmrecall

LENSES = ["user value", "unspoken needs", "delight", "reliability", "performance", "security and safety", "simplicity",
          "bold bets"]
PACK_WORDS = 2000
# T-0099: unspoken needs and delight by default (the user wanted what they can't put into words, and more creative ideas)
DEFAULT_LENSES = ["user value", "unspoken needs", "delight", "reliability", "simplicity", "bold bets"]
PROMPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "skills", "brainstorm", "references", "ideas-prompt.md")
# No built-in tools, no MCP servers, and no user settings (so other plugins' hooks and prompts don't bias the lens).
NO_TOOLS = ["--setting-sources", "project,local", "--tools", "", "--strict-mcp-config",
            "--mcp-config", json.dumps({"mcpServers": {}})]


def child_cmd(model, system):
    """The prompt (lens + pack) goes in on stdin: packs can exceed the per-argument size limit."""
    return ["claude", "-p", "--model", model, "--no-session-persistence", "--output-format", "json", *NO_TOOLS,
            "--append-system-prompt", system]


def _tail(s, n):
    """The end of a child's output (claude puts its error last), on one safe line."""
    s = c.plain(" ".join((s or "").split()))
    return s if len(s) <= n else "…" + s[1 - n:]


def _child_env():
    return dict(os.environ, FOREMAN_NO_BACKGROUND="1")  # a child never starts Foreman's own background reviews


def run_child(feature, system, prompt, model, timeout, project=None, detail="", fallback=0.05):
    """T-0295: one tool-less child, budget-checked, run in a scratch folder and recorded: its text. ValueError when
    it can't run, fails or says nothing."""
    try:
        fmbudget.check(feature, fmbudget.estimate(feature, 1, fallback))
    except fmbudget.BudgetError as e:
        raise ValueError(str(e))
    with tempfile.TemporaryDirectory(prefix=f"fm-{feature}-", dir=os.environ.get("XDG_RUNTIME_DIR") or None) as cwd:
        try:
            r = subprocess.run(child_cmd(model, system), input=prompt, cwd=cwd, capture_output=True, text=True,
                               timeout=timeout, env=_child_env())
        except (OSError, subprocess.TimeoutExpired) as e:
            raise ValueError(f"the {feature} child didn't run: {e} (is `claude` on PATH and logged in?)")
    text, usd = fmbudget.result(r.stdout)
    fmbudget.record(feature, usd, project=project, detail=detail)
    if r.returncode or not (text or "").strip():
        raise ValueError(f"nothing came back (exit {r.returncode}: {_tail(r.stderr or r.stdout, 160)})")
    return text


def run_children(jobs, timeout, feature):
    """T-0295: [(argv, stdin, detail)] run in parallel in one scratch folder under one deadline, each recorded:
    [(text or None, error)]. OSError when one can't start (the started ones are stopped)."""
    with tempfile.TemporaryDirectory(prefix=f"fm-{feature}-", dir=os.environ.get("XDG_RUNTIME_DIR") or None) as cwd:
        procs = []
        try:
            for argv, stdin, detail in jobs:
                pr = subprocess.Popen(argv, cwd=cwd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, env=_child_env())
                procs.append((pr, detail))
                pr.stdin.write(stdin)
                pr.stdin.close()
        except OSError as e:
            for pr, _ in procs:
                pr.kill()
                pr.communicate()
            raise OSError(f"can't start claude: {e} (is it on PATH and logged in?)")
        deadline, out = time.time() + timeout, []
        for pr, detail in procs:
            try:
                so, se = pr.communicate(timeout=max(1, deadline - time.time()))
                text, usd = fmbudget.result(so)  # T-0227: the text, and what it cost
                fmbudget.record(feature, usd, detail=detail)
                out.append((text, None) if pr.returncode == 0 and text.strip() else
                           (None, f"exit {pr.returncode}: {_tail(se or so, 200)}"))
            except subprocess.TimeoutExpired:
                pr.kill()
                pr.communicate()
                fmbudget.record(feature, None, detail=f"{detail} (timed out: cost unknown)" if detail
                                else "timed out: cost unknown")
                out.append((None, f"timed out after {timeout}s"))
    return out


def child_prompt(lens, pack):
    """The shared pack first, the lens last (T-0267): siblings and later rounds then share a prefix the prompt cache
    can reuse."""
    return f"Context pack:\n{pack}\n\nLens: {lens}\n\nReturn 8-12 ideas in the required format, at least 3 of them wild."


def user_voice(p, n=20):
    """The user's own recent words for the pack: their captured requests and their corrections (T-0099). What they
    keep asking for, and push back on, is where the unspoken needs are."""
    asks = [b for b in c.load_briefs(p) if b.meta.get("source") == "user"]
    asks.sort(key=lambda b: b.meta.get("created") or "")
    lines = [f"- asked: {c.fit(c.plain(b.section('Raw request').strip().lstrip('> ') or b.title), 200)}"
             for b in asks[-n:]]
    lines += [f"- pushed back: {c.fit(c.plain((e.get('data') or {}).get('text', '')), 200)}"
              for e in c.ledger_tail(p, 3000) if e.get("event") == "correction"][-n // 2:]
    t = taste(p, n // 4)  # T-0112: what they turned down, and why, and how they steered work in flight
    lines += [f"- dropped: {d['title']} — {d['why']}" for d in t["dropped"] if d["why"]]
    lines += [f"- steered: {s}" for s in t["steered"]]
    return ("\n\n## The user's own words (data; recent requests, corrections, drops and steers — infer what they'd want "
            "next)\n" + "\n".join(lines)) if lines else ""


HOUSEKEEPING = re.compile(r"(?i)\s*(folded into|done in|fixed (inline )?in|duplicate|merged into|superseded|covered by)\b")


def taste(p, n=8):
    """T-0112: what the user's choices say about their taste: their requests that were finished (kept), work dropped
    and the reason given, and their steers and corrections, newest last (briefs, archive included, and the ledger)."""
    briefs = sorted(c.load_briefs(p, include_archive=True), key=lambda b: b.meta.get("created") or "")
    fit = lambda s, w: c.fit(c.plain(str(s or "")).strip(), w)

    def why(b):
        return next((fit(ln.split("dropped:", 1)[1], 160) for ln in reversed(b.section("Log").splitlines())
                     if "dropped:" in ln), "")
    ledger = c.ledger_tail(p, 3000)
    notes = [str((e.get("data") or {}).get("text") or "") for e in ledger if e.get("event") == "note"]
    return {"kept": [{"id": b.id, "type": b.type, "title": fit(b.title, 90)} for b in briefs
                     if b.status == "done" and b.meta.get("source") == "user"][-n:],
            "dropped": [{"id": b.id, "title": fit(b.title, 90), "why": why(b)} for b in briefs if b.status == "dropped"
                        and not HOUSEKEEPING.match(why(b))][-n:],  # merged or done elsewhere says nothing of taste
            "steered": [fit(t[len("steer:"):], 200) for t in notes if t.startswith("steer:")][-n:],
            "corrected": [fit((e.get("data") or {}).get("text"), 200) for e in ledger if e.get("event") == "correction"][-n:]}


def cmd_taste(args):
    import fmcli
    p = fmcli.resolve(args)
    t = taste(p, args.n)
    lines = ["Kept (your requests, finished): " + ("; ".join(f"{k['id']} {k['title']}" for k in t["kept"]) or "none yet")]
    for head, rows in (("Dropped", [f"{d['id']} {d['title']}" + (f" — {d['why']}" if d["why"] else "") for d in t["dropped"]]),
                       ("Steered", t["steered"]), ("Corrected", t["corrected"])):
        lines += [f"{head}:"] + [f"  {r}" for r in rows] if rows else []
    fmcli.out(args, t, "\n".join(lines))


_CATEGORY = re.compile(r"(?m)^\s*[-*]\s*\*\*(.+?)\*\*.*?category:?\s*([\w][\w &/-]{0,30})\s*$")


_TITLE = re.compile(r"(?m)^\s*[-*]\s*\*\*(.+?)\*\*")
NEAR = re.compile(r" — near T-\d+ \(done\).*$")
_WORD = re.compile(r"[a-z0-9]{3,}")


def _words(title):
    return {w[:5] for w in _WORD.findall(title.lower())}


def _is_new(title, seen):
    """Not a near-repeat of an idea already on the list (most of its words shared)."""
    w = _words(title)
    return bool(w) and all(len(w & s) / len(w | s) < 0.6 for s in seen)


def deepen_pack(pack, category, titles):
    return (pack + f"\n\n## Category to build off: {category}\nIdeas in it so far:\n" + "\n".join(f"- {t}" for t in titles)
            + "\n\nYes-and: grow each into something bigger, combine them, and add the natural next ideas inside this "
              "category (don't repeat the list).")


def later_round_pack(pack, titles, n):
    return (pack + "\n\n## Ideas so far (don't repeat these; go past them)\n" + "\n".join(f"- {t}" for t in titles)
            + f"\n\nRound {n}: propose only NEW ideas: gaps nobody covered, second-order improvements on the ideas "
              f"above, combinations worth more together, and what a genuinely fully featured version would still lack.")


def _run_round(lenses, pack, system, args, out_dir, prefix, fmcli):
    results = []
    try:
        answers = run_children([(child_cmd(args.model, system), child_prompt(lens, pack), lens) for lens in lenses],
                               args.timeout, "ideas")
    except OSError as e:
        raise fmcli.UsageError(str(e))
    for i, (lens, (out, why)) in enumerate(zip(lenses, answers), 1):
        ok, why = out is not None, why or ""
        slug = re.sub(r"[^a-z0-9]+", "-", lens.lower()).strip("-") or "lens"
        path = os.path.join(out_dir, f"{prefix}{i:02d}-{slug}.md")
        text = c.redact(out.strip()) if ok else ""
        if ok and not _TITLE.search(text):  # an answer that isn't ideas (a refusal, a question) is a failed lens
            ok, why = False, f"no ideas in the required format: {c.fit(c.plain(text), 150)}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Brainstorm — lens: {lens}\n\n" + (text if ok else f"FAILED: {why}") + "\n")
        results.append({"lens": lens, "file": path, "ok": ok, "error": why,
                        "titles": [c.plain(t).strip() for t in _TITLE.findall(text)],
                        "categories": {c.plain(t).strip(): cat.strip().lower() for t, cat in _CATEGORY.findall(text)}})
    return results


def cmd_ideas(args):
    """One round of lenses, or a super brainstorm (--rounds N): each later round sees every idea so far and is asked
    only for new ones; it stops when a round adds fewer than --dry new ideas (T-0071)."""
    import fmcli
    p = fmcli.resolve(args)
    pack = sys.stdin.read() if args.pack == "-" else open(args.pack, encoding="utf-8").read()
    pack += user_voice(p)
    lenses = list(dict.fromkeys(args.lens or DEFAULT_LENSES))
    runs = len(lenses) * max(1, args.rounds) + max(0, getattr(args, "deepen", 0) or 0)
    try:
        fmbudget.check("ideas", fmbudget.estimate("ideas", runs, 0.06), "fewer --lens, --rounds or --deepen")
    except fmbudget.BudgetError as e:
        raise fmcli.UsageError(str(e))
    with open(PROMPT, encoding="utf-8") as f:
        system = f.read()
    out_dir = os.path.join(p.dir, "research", "brainstorm-" + time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "status.json"), "w", encoding="utf-8") as f:  # T-0124: the dashboard's progress
        json.dump({"lenses": lenses, "rounds": max(1, args.rounds), "started": c.now()}, f)
    if len(pack.split()) > PACK_WORDS:
        print(f"fm: warning: the pack is {len(pack.split())} words; every lens and round pays for it (aim for "
              f"≤ {PACK_WORDS})", file=sys.stderr)
    results, titles, seen, by_round, rounds, lens_yield = [], [], [], [], 0, dict.fromkeys(lenses, 0)
    for path in args.seen or []:  # earlier brainstorms' ideas.md: don't repeat them, go past them (recursion)
        try:
            with open(path, encoding="utf-8") as f:
                old = [NEAR.sub("", m.group(1)).strip() for m in re.finditer(r"(?m)^- (?!\w[\w ]*: \d+$)(.+)$", f.read())]
        except OSError as e:
            raise fmcli.UsageError(f"can't read --seen {path}: {e.strerror}")
        for t in old:
            if _is_new(t, seen):
                seen.append(_words(t))
                titles.append(t)
    known = len(titles)
    for n in range(1, max(1, args.rounds) + 1):
        rounds = n
        prefix = f"r{n}-" if args.rounds > 1 else ""
        got = _run_round(lenses, pack if not titles else later_round_pack(pack, titles, n), system, args, out_dir,
                         prefix, fmcli)
        results += [dict(r, round=n) for r in got]
        new = []
        for r in got:
            for t in r["titles"]:
                if _is_new(t, seen):
                    seen.append(_words(t))
                    new.append(t)
                    lens_yield[r["lens"]] += 1
        titles += new
        by_round.append(new)
        if n > 1 and len(new) < args.dry:
            break
    deepened = {}
    if getattr(args, "deepen", 0):  # T-0099: build off the biggest categories, one yes-and child each
        cats = {}
        for r in results:
            for t, cat in r.get("categories", {}).items():
                cats.setdefault(cat, []).append(t)
        top = sorted(cats, key=lambda k: -len(cats[k]))[:args.deepen]
        got = []
        for cat in top:  # one child per category, each with its own pack
            got += [dict(r, round=rounds + 1, category=cat) for r in
                    _run_round([f"deepen: {cat}"], deepen_pack(pack, cat, cats[cat]), system, args, out_dir,
                               f"deep-{len(got) + 1}-", fmcli)]
        results += got
        for r in got:
            new = [t for t in r["titles"] if _is_new(t, seen)]
            for t in new:
                seen.append(_words(t))
            titles += new
            deepened[r["category"]] = new
    near = fmrecall.nearest_done(p, titles[known:])  # T-0208: what may already be built, before grounding
    item = lambda t: f"- {t}" + (f" — near {near[t][0]} (done): {c.fit(near[t][1], 60)}" if t in near else "") + "\n"
    with open(os.path.join(out_dir, "ideas.md"), "w", encoding="utf-8") as f:
        f.write("# Ideas by round (deduplicated titles; details in the lens files; \"near T-…\" names a finished task "
                "that shares most of an idea's words)\n"
                + "".join(f"\n## Round {i}\n" + "".join(map(item, ts)) for i, ts in enumerate(by_round, 1))
                + "".join(f"\n## Deepened: {cat}\n" + "".join(map(item, ts)) for cat, ts in deepened.items())
                + "\n## New ideas per lens\n" + "".join(f"- {k}: {v}\n" for k, v in lens_yield.items()))
    failed = [f"{r['lens']} (round {r['round']})" for r in results if not r["ok"]]
    with c.lock(p.dir):
        c.log_event(p, "ideas", data={"dir": out_dir, "lenses": lenses, "rounds": rounds, "ideas": len(titles) - known,
                                      "failed": failed}, session=fmcli.session())
    fmcli.out(args, {"dir": out_dir, "rounds": rounds, "ideas": len(titles) - known, "results": results, "yield": lens_yield},
              f"Brainstorm ideas in {out_dir} ({len(titles) - known} new distinct over {rounds} round(s); index: ideas.md):\n"
              + "\n".join(f"  {'ok  ' if r['ok'] else 'FAIL'} {'r' + str(r['round']) + ' ' if args.rounds > 1 else ''}"
                          f"{r['lens']}: {r['file'] if r['ok'] else r['error']}" for r in results)
              + (f"\n  dry after round {rounds}: it added {len(by_round[-1])} new" if rounds < args.rounds else ""))
    if failed:
        raise fmcli.UsageError(f"brainstorm lens(es) failed: {', '.join(failed)} (the others are saved)")


ORACLE = """You write the test oracle for one software change from its specification alone: you never see the code,
so your examples can't mirror an implementation. Describe observable behaviour only (inputs, outputs, files, exit
codes, messages), never internal APIs or names you'd have to guess.
Reply in exactly this shape:
## Examples
- GIVEN <state> WHEN <action> THEN <observable result>
(5-12 lines: the main path, edge cases, errors and the criteria's own checks)
## Ambiguities
- <question> — <the readings, and how the tests would differ>
(or a single line "- none")"""


def cmd_oracle(args):
    """T-0226: behaviour examples and ambiguities for a task from its request, interpretation and criteria only (a
    tool-less child in a scratch folder: no code, no repo), saved in the brief's Oracle section before tests are written."""
    import fmcli
    p = fmcli.resolve(args)
    b = fmcli.need_brief(p, args.id)
    spec = "\n\n".join(f"## {name}\n{b.section(name).strip()}" for name in
                        ("Raw request", "Interpretation", "Acceptance criteria", "Non-goals") if b.section(name).strip())
    spec = f"Task: {b.title} ({b.type})\n\n{spec or b.title}\n"
    try:
        text_out = run_child("oracle", ORACLE, spec, args.model, args.timeout, project=p.slug, detail=b.id)
    except ValueError as e:
        raise fmcli.UsageError(str(e))
    parts = {k: [] for k in ("Examples", "Ambiguities")}
    head = None
    for line in text_out.splitlines():
        m = re.match(r"#+\s*(Examples|Ambiguities)\b", line.strip(), re.I)
        if m:
            head = m.group(1).capitalize()
        elif head and line.strip().startswith("- "):
            parts[head].append(c.fit(c.defang(c.redact(line.strip()[2:].strip())), 300))
    examples = parts["Examples"]
    ambiguities = [x for x in parts["Ambiguities"] if x.lower().strip(". ") != "none"]
    if not examples:
        raise fmcli.UsageError(f"no examples came back ({c.fit(c.plain(text_out), 160)})")
    text = ("Examples from the request alone, before the code was read (write tests from these):\n"
            + "".join(f"- {x}\n" for x in examples)
            + ("Ambiguities (decide each with fm decide, or ask, before the tests):\n" + "".join(f"- {x}\n" for x in ambiguities)
               if ambiguities else "Ambiguities: none found.\n"))
    fmcli.mutate(p, b.id, lambda br: br.set_section("Oracle", text), "oracle",
                 {"examples": len(examples), "ambiguities": len(ambiguities)})
    fmcli.out(args, {"examples": examples, "ambiguities": ambiguities},
              f"{b.id}: oracle saved — {len(examples)} example(s), {len(ambiguities)} ambiguit"
              f"{'y' if len(ambiguities) == 1 else 'ies'}\n" + text)
