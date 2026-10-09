"""fm ideas: tool-less brainstorm children, one per lens, run in parallel (skills/brainstorm).

A Claude Code subagent can't have zero tools (an empty `tools:` list means every tool), so each lens runs as a
fresh `claude -p` session with no built-in tools and no MCP servers, in a scratch directory outside any project.
"""
import glob
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

LENSES = ["user value", "unspoken needs", "delight", "capability map", "approaches", "reliability", "performance",
          "security and safety", "simplicity", "bold bets", "beautiful UI and motion", "every device and surface",
          "agents of agents", "privacy and local-first", "reframe", "flip assumptions", "oblique provocation",
          "devil's idea", "worst-bugs persona"]
# T-0627/T-0628: what a lens whose name isn't enough asks for
LENS_NOTES = {
    "reframe": "restate the problem three different ways (as the user's goal, as a constraint to remove, as a question "
               "nobody asked) and give the ideas each framing opens",
    "flip assumptions": "list the assumptions the request rests on, flip each one, and give the ideas that only exist "
                        "once it's false",
    "oblique provocation": "take one past lesson or failure from the pack as a provocation and follow it somewhere "
                           "unexpected",
    "devil's idea": "propose what a rival who wanted this project to win would ship that its owner would never dare to",
    "worst-bugs persona": "be the user who hits the worst bugs: what breaks, confuses or loses work, and what would "
                          "have prevented it",
}
# T-0605: the capability axes a complete catalogue covers; thin ones are named for the next round
AXES = ["user value", "reliability", "performance", "security", "privacy", "ui", "devices", "agents", "simplicity",
        "developer experience", "observability", "docs", "delight"]
PACK_WORDS = 2000
# T-0099: unspoken needs and delight by default (the user wanted what they can't put into words, and more creative ideas)
# T-0375: fm mission adds the UI, device, agent and privacy lenses when the project has those surfaces
# T-0364: capability map (everything a complete version has) and approaches (every way to solve it): breadth
DEFAULT_LENSES = ["user value", "unspoken needs", "delight", "capability map", "approaches", "reliability", "simplicity",
                  "bold bets"]
PROMPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "skills", "brainstorm", "references", "ideas-prompt.md")
# No built-in tools, no MCP servers, and no user settings (so other plugins' hooks and prompts don't bias the lens).
NO_TOOLS = ["--setting-sources", "project,local", "--tools", "", "--strict-mcp-config",
            "--mcp-config", json.dumps({"mcpServers": {}})]


def child_cmd(model, system):
    """The prompt (lens + pack) goes in on stdin: packs can exceed the per-argument size limit."""
    c.refuse_if_paused()  # T-0591: fm relate's child comes through here too
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
                try:
                    pr.stdin.write(stdin)
                    pr.stdin.close()
                finally:
                    pr.stdin = None  # before 3.13, communicate() flushes a closed stdin and raises
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
    note = f" — {LENS_NOTES[lens]}" if lens in LENS_NOTES else ""
    return f"Context pack:\n{pack}\n\nLens: {lens}{note}\n\nReturn 10-15 ideas in the required format, at least 3 of them wild."


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
            "corrected": [fit((e.get("data") or {}).get("text"), 200) for e in ledger if e.get("event") == "correction"][-n:],
            "lenses": lens_rates(p, briefs)}


def lens_rates(p, briefs):
    """T-0607: per brainstorm lens, how many of its ideas became tasks that were built, dropped or are still open — an
    idea matches a brief whose title holds most of its words."""
    rates = {}
    briefs = [(b, _words(b.title)) for b in briefs]
    for path in glob.glob(os.path.join(p.dir, "research", "brainstorm-*", "ideas.json")):
        try:
            with open(path, encoding="utf-8") as f:
                lenses = json.load(f).get("lenses") or {}
        except (OSError, ValueError):
            continue
        for lens, titles in lenses.items():
            r = rates.setdefault(lens, {"ideas": 0, "built": 0, "dropped": 0, "open": 0})
            for t in titles:
                r["ideas"] += 1
                w = _words(t)
                b = next((b for b, bw in briefs if w and len(w & bw) / len(w) >= 0.6), None)
                if b:
                    r["built" if b.status == "done" else "dropped" if b.status == "dropped" else "open"] += 1
    return rates


# T-0439: a no the user keeps steering with becomes a veto to propose; their other steers and finished requests say
# which option they'd pick
TASTE_REPEATS = 3
_NO = re.compile(r"(?i)\b(?:no|not|never|don['’]?t|do not|stop|avoid|without)\b")
_STEER_STOP = {"keep", "prefer", "instead", "rather", "should", "shouldn", "want", "avoid", "never", "don", "not",
               "stop", "more", "less", "only", "please", "let", "lets", "like", "better", "steer"}


def _key_words(text):
    return list(dict.fromkeys(w for w in re.findall(r"[a-z0-9]{3,}", (text or "").lower())
                              if w not in c._VETO_STOP and w not in _STEER_STOP))


def proposals(p):
    """[{words, count, said}]: key words shared by TASTE_REPEATS or more steers that say no, as vetoes to propose; none
    a recorded veto or a declined proposal already covers (its words a subset of the shape)."""
    notes = [str((e.get("data") or {}).get("text") or "") for e in c.ledger_tail(p, 3000) if e.get("event") == "note"]
    sets = [(s, _key_words(s)) for s in (t[len("steer:"):].strip() for t in notes if t.startswith("steer:")) if _NO.search(s)]
    covered = [set(v["words"]) for v in c.vetoes(p)] + [set(w) for w in c.read_meta(p).get("taste_declined") or []]
    out, seen = [], set()
    for w in dict.fromkeys(x for _, ws in sets for x in ws):
        group = [(s, ws) for s, ws in sets if w in ws]
        shape = [x for x in group[-1][1] if all(x in ws for _, ws in group)][:3]
        if len(group) < TASTE_REPEATS or tuple(sorted(shape)) in seen or any(h <= set(shape) for h in covered):
            continue
        seen.add(tuple(sorted(shape)))
        out.append({"words": shape, "count": len(group), "said": c.fit(c.plain(group[-1][0]), 160)})
    return out


def taste_default(p, options):
    """(option, why): the option the user's record favours — none a recorded veto covers (unless every one is), then the
    most key words shared with their finished requests and their steers that aren't a no; a tie keeps the caller's order."""
    vetoed = {o: c.veto_hits(p, o) for o in options}
    free = [o for o in options if not vetoed[o]] or list(options)
    t = taste(p, 50)
    liked = {w for s in [k["title"] for k in t["kept"]] + [s for s in t["steered"] if not _NO.search(s)]
             for w in _key_words(s)}
    best = max(free, key=lambda o: sum(w in liked for w in _key_words(o)))
    why = ["avoids the veto " + "; ".join(f"\"{vetoed[o][0]['said']}\"" for o in options if o not in free)] \
        if len(free) < len(options) else [f"every option hits a veto (\"{vetoed[options[0]][0]['said']}\"): the "
                                          f"least bad by your record"] if options and all(vetoed.values()) else []
    hits = [w for w in _key_words(best) if w in liked]
    why += [f"like your steers and finished requests ({', '.join(hits)})"] if hits else []
    return best, ("taste record: " + "; ".join(why)) if why else "no signal in your taste record: the first option"


def cmd_taste(args):
    import fmcli
    p = fmcli.resolve(args)
    props = proposals(p)
    if args.action:  # the user's one yes (or no), asked through AskUserQuestion: vetoes only add caution
        pick = props if args.which is None else props[args.which - 1:args.which] if args.which > 0 else []
        if not pick:
            raise fmcli.UsageError(f"no proposal {args.which or ''} to {args.action}; fm taste lists them".replace("  ", " "))
        if args.action == "adopt":
            for x in pick:
                c.add_veto(p, f"{x['said']} (steered {x['count']} times)", words=x["words"])
        else:
            with c.lock(p.dir):
                meta = c.read_meta(p)
                meta["taste_declined"] = ((meta.get("taste_declined") or []) + [x["words"] for x in pick])[-c.VETOES_KEEP:]
                c.write_meta(p, meta)
        c.log_event(p, f"taste_{args.action}", data={"words": [x["words"] for x in pick]}, session=c.session_id())
        return fmcli.out(args, {"action": args.action, "proposals": pick},
                         f"{'Adopted' if args.action == 'adopt' else 'Declined'}: "
                         + "; ".join(f"never {' '.join(x['words'])}" for x in pick) + ".")
    t = dict(taste(p, args.n), proposed=props)
    lines = ["Kept (your requests, finished): " + ("; ".join(f"{k['id']} {k['title']}" for k in t["kept"]) or "none yet")]
    for head, rows in (("Dropped", [f"{d['id']} {d['title']}" + (f" — {d['why']}" if d["why"] else "") for d in t["dropped"]]),
                       ("Steered", t["steered"]), ("Corrected", t["corrected"])):
        lines += [f"{head}:"] + [f"  {r}" for r in rows] if rows else []
    if t["lenses"]:  # T-0607: which lenses' ideas the user keeps
        lines += ["Brainstorm lenses (ideas that became tasks):"] + [
            f"  {k}: {r['built']}/{r['ideas']} built, {r['dropped']} dropped, {r['open']} open"
            for k, r in sorted(t["lenses"].items(), key=lambda kv: -kv[1]["built"] / max(kv[1]["ideas"], 1))]
    if props:
        lines += ["Proposed vetoes (a no you keep steering with):"]
        lines += [f"  {i}. never {' '.join(x['words'])} — steered {x['count']} times, last: {x['said']}"
                  for i, x in enumerate(props, 1)]
        lines += ["Ask the user once (one AskUserQuestion, adopt first): yes → fm taste adopt (all) or fm taste adopt N; "
                  "no → fm taste decline N."]
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


def later_round_pack(pack, titles, n, thin=()):
    return (pack + "\n\n## Ideas so far (don't repeat these; go past them)\n" + "\n".join(f"- {t}" for t in titles)
            + (f"\n\nThin so far (fill these first): {', '.join(thin)}" if thin else "")
            + f"\n\nRound {n}: propose only NEW ideas: gaps nobody covered, second-order improvements on the ideas "
              f"above, combinations worth more together, and what a genuinely fully featured version would still lack.")


def coverage(results):
    """T-0605: ({category: ideas}, the axes with at most one idea)."""
    of, cats = {}, {}
    for r in results:  # distinct ideas: a later round repeating one doesn't count twice
        of.update(r.get("categories", {}))
    for cat in of.values():
        cats[cat] = cats.get(cat, 0) + 1
    thin = [a for a in AXES if sum(n for cat, n in cats.items() if a in cat or cat in a) <= 1]
    return cats, thin


FALSIFY = ("You kill ideas fast. For each numbered idea, give the quickest observation or experiment that would show "
           "it isn't worth building. Output only lines `N: <one line>`.")


def _falsify(titles, args, p):
    prompt = "KILL IT FAST\n" + "\n".join(f"{i}: {t}" for i, t in enumerate(titles[:60], 1))
    text = run_child("ideas", FALSIFY, prompt, args.model, args.timeout, project=p.slug, detail="falsify")
    found = {int(m.group(1)): c.fit(c.plain(m.group(2)), 200) for m in re.finditer(r"(?m)^\s*(\d+):\s*(.+)$", text)}
    return {titles[i - 1]: f for i, f in found.items() if 0 < i <= min(len(titles), 60)}


def _crossbreed(titles, system, args, p):
    prompt = ("CROSS-BREED: combine the strongest of these ideas into 3-6 new ideas worth more together, in the "
              "required format.\n" + "\n".join(f"- {t}" for t in titles[:30]))
    text = run_child("ideas", system, prompt, args.model, args.timeout, project=p.slug, detail="crossbreed")
    return [c.plain(t).strip() for t in _TITLE.findall(c.redact(text))]


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
    c.refuse_if_paused()  # T-0591
    p = fmcli.resolve(args)
    pack = sys.stdin.read() if args.pack == "-" else open(args.pack, encoding="utf-8").read()
    pack += user_voice(p)
    lenses = list(dict.fromkeys(args.lens or DEFAULT_LENSES))
    if "oblique provocation" in lenses:  # T-0628: its provocations are the project's own lessons
        lessons = [ln.strip("- ").strip() for b in sorted(c.load_briefs(p), key=lambda b: b.meta.get("updated") or "")
                   for ln in b.section("Lessons").splitlines() if ln.strip()][-8:]
        if lessons:
            pack += "\n\n## Past lessons (provocations for the oblique lens)\n" + "\n".join(
                f"- {c.fit(c.plain(x), 200)}" for x in lessons)
    deepen = max(0, getattr(args, "deepen", 0) or 0)
    pace = fmbudget.degrade() if deepen else None
    if pace:  # T-0449: optional rounds go first; the caps below still refuse what's over one
        print(f"fm: usage ahead of pace ({pace}): --deepen dropped (0 rounds, optional work); the lenses still run",
              file=sys.stderr)
        deepen = 0
    runs = len(lenses) * max(1, args.rounds) + deepen
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
        got = _run_round(lenses, pack if not titles else later_round_pack(pack, titles, n, coverage(results)[1]),
                         system, args, out_dir, prefix, fmcli)
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
    if deepen:  # T-0099: build off the biggest categories, one yes-and child each
        cats = {}
        for r in results:
            for t, cat in r.get("categories", {}).items():
                cats.setdefault(cat, []).append(t)
        top = sorted(cats, key=lambda k: -len(cats[k]))[:deepen]
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
    kills, bred = {}, []
    try:
        kills = _falsify(titles[known:], args, p) if getattr(args, "falsify", False) and titles[known:] else {}
        bred = [t for t in (_crossbreed(titles[known:], system, args, p) if getattr(args, "crossbreed", False)
                            and titles[known:] else []) if _is_new(t, seen)]
    except ValueError as e:  # an optional pass that fails leaves the catalogue as it is
        print(f"fm: {e}", file=sys.stderr)
    titles += bred
    cats, thin = coverage(results)
    near = fmrecall.nearest_done(p, titles[known:])  # T-0208: what may already be built, before grounding
    item = lambda t: f"- {t}" + (f" — near {near[t][0]} (done): {c.fit(near[t][1], 60)}" if t in near else "") + "\n"
    with open(os.path.join(out_dir, "ideas.md"), "w", encoding="utf-8") as f:
        f.write("# Ideas by round (deduplicated titles; details in the lens files; \"near T-…\" names a finished task "
                "that shares most of an idea's words)\n"
                + "".join(f"\n## Round {i}\n" + "".join(map(item, ts)) for i, ts in enumerate(by_round, 1))
                + "".join(f"\n## Deepened: {cat}\n" + "".join(map(item, ts)) for cat, ts in deepened.items())
                + "".join(f"\n## Cross-bred\n" + "".join(map(item, bred)) for _ in [0] if bred)
                + "\n## New ideas per lens\n" + "".join(f"- {k}: {v}\n" for k, v in lens_yield.items())
                + "\n## Coverage (ideas per category)\n" + "".join(f"- {k} {v}\n" for k, v in
                                                                   sorted(cats.items(), key=lambda kv: -kv[1]))
                + f"Thin (0-1 ideas): {', '.join(thin) or 'none'}\n"
                + ("\n## Kill it fast (the quickest test that would show it isn't worth building)\n"
                   + "".join(f"- {t} — {k}\n" for t, k in kills.items()) if kills else ""))
    with open(os.path.join(out_dir, "ideas.json"), "w", encoding="utf-8") as f:  # T-0607: for fm taste's keep rates
        json.dump({"lenses": {r["lens"]: r["titles"] for r in results if r["ok"]}, "crossbred": bred,
                   "kills": kills, "created": c.now()}, f)
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
    c.refuse_if_paused()  # T-0591
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
