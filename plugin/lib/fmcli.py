"""fm — the only writer of Foreman state.

Exit codes: 0 ok · 1 usage error / not found · 2 refused by policy · 3 lock timeout · 4 state corrupt.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys
import time
import types

import fmcore as c

EDITABLE = {"type", "tier", "priority", "scope", "depends_on", "source", "status", "branch", "explore", "approved", "title",
            "confidence", "cost_cap", "predict_minutes", "predict_attempts"}
CLEARABLE = {"confidence", "cost_cap", "predict_minutes", "predict_attempts"}  # T-1126: k= removes them
LIST_FIELDS = {"scope", "depends_on"}
SETTABLE_STATUS = {"captured", "planned", "active", "verifying", "blocked", "deferred"}


class UsageError(Exception):
    """Bad input or unknown object. Exit code 1."""


def session():
    return c.session_id()


def _session_model():
    """T-0487: the model this session runs, from the statusline's snapshot (state/sessions/<id>.json), else None."""
    sid = re.sub(r"[^\w-]", "", str(session() or ""))[:80]  # as the statusline names it
    try:
        with open(os.path.join(c.state_dir(), "sessions", f"{sid or '-'}.json"), encoding="utf-8") as f:
            return json.load(f).get("model")
    except (OSError, ValueError, AttributeError):
        return None


def out(args, data, text):
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif text is not None:
        print(text)


# ---------------------------------------------------------------- project resolution

def resolve(args, create=True):
    if getattr(args, "project", None):
        p = c.project_by_slug(args.project)
        if not p:
            raise UsageError(f"unknown project {args.project!r} (see state/registry.md)")
        return p
    p = c.find_project(os.getcwd(), create=create)
    if not p and os.environ.get("FOREMAN_PROJECT"):
        p = c.project_by_slug(os.environ["FOREMAN_PROJECT"])
    if not p:
        raise UsageError("not in a Foreman project; run `fm init` here or pass -p SLUG")
    return p


def need_brief(p, tid):
    b = c.find_brief(p, tid)
    if not b:  # T-0987: name what is here, so an id from another checkout isn't guessed at again
        briefs = c.load_briefs(p)
        act = getattr(c.active_brief(briefs), "id", None)
        open_ = [x.id for x in briefs if x.status not in c.CLOSED and x.id != act][-3:]
        here = ", ".join(([f"active {act}"] if act else []) + open_)
        raise UsageError(f"no task {tid} in {p.slug}" + (f" (here: {here})" if here else ""))
    return b


def mutate(p, tid, fn, event, data=None):
    """Load a brief under the project lock, apply fn(brief), save, log, regenerate views."""
    with c.lock(p.dir):
        b = need_brief(p, tid)
        result = fn(b)
        c.save_brief(p, b)
        c.log_event(p, event, task=b.id, data=data or {}, session=session())
        c.regen_views(p)
    return b, result


# ---------------------------------------------------------------- commands

def cmd_init(args):
    path = os.path.abspath(args.path or os.getcwd())
    root = c.git_root(path) or path
    p = c.init_project(root)
    if args.sensitive:
        cmd_sensitive(argparse.Namespace(state="on", path=root, json=False, project=None))
    with c.lock(p.dir):
        c.log_event(p, "init", data={"root": root}, session=session())
        c.regen_views(p)
    out(args, {"project": p.slug, "root": root}, p.slug)
    if not args.json:  # T-0847: stdout stays the bare slug (scripts read it); the newcomer reads this
        print(f"Registered {root} as {p.slug}; its state lives in {p.dir}.\n"
              f"Next: fm capture \"<request>\" (or just give Claude a request); fm --help for the everyday commands.",
              file=sys.stderr)


def cmd_state(args):
    p = resolve(args, create=not args.line)  # T-0962: a status bar polling --line never creates a project
    sd = c.state_dict(p)
    if args.cmd == "status" and not (args.line or args.json) and not c.load_briefs(p):  # T-0847: nothing yet
        return print(f"{p.slug}: no tasks yet. Start with fm capture \"<request>\" or fm task new \"<title>\" --type FIX "
                     f"--tier S --focus (or just give Claude a request).")
    if args.line:
        print(c.state_line(sd))
    elif args.json:
        print(json.dumps(sd, indent=2, ensure_ascii=False))
    else:
        text = c.render_state(sd)
        if args.brief:
            text = "\n".join(text.splitlines()[:15])
        print(text.rstrip("\n"))


def _block(item, r, key):
    """The block's lines for every item, then the item's own (T-0259)."""
    return getattr(r, key) + (item.own or {}).get(key, [])


def _raw_with_block(item, r):
    lines = [item.raw.strip() or f"{item.type}: {item.text}"]
    lines += [f"CONTEXT: {v}" for v in _block(item, r, "context")]
    lines += [v if v.startswith(("MUST:", "NEVER:")) else f"CONSTRAINT: {v}" for v in _block(item, r, "constraints")]
    lines += [f"DONE-WHEN: {v}" for v in _block(item, r, "done_when")]
    lines += [f"SKIP: {v}" for v in _block(item, r, "skip")]
    return "\n".join(lines)


def _create(p, title, type, tier, status, raw=None, scope=(), depends=(), source="user", priority="normal", explore=False):
    tid = c.next_id(p)
    b = c.Brief.new(tid, title, type, tier, raw=raw, scope=scope, depends=depends, source=source,
                    priority=priority, status=status, explore=explore)
    c.save_brief(p, b, touch=False)
    return b


def _title(text):
    first = text.strip().splitlines()[0] if text.strip() else "untitled"
    # T-0334: a ref that leads or ends the line is a dependency marker; one inside the sentence is part of it
    first = re.sub(r"^(?:\s*#T-\d{4,}\b)+|(?:\s*#T-\d{4,}\b)+\s*$", "", first)
    first = c._SCOPE_RE.sub("", c._REF_RE.sub(r"\1", first)).strip()
    return (first[:1].upper() + first[1:])[:90] or "untitled"


def cmd_intake(args):
    text = args.text if args.text is not None else (open(args.file).read() if args.file else sys.stdin.read())
    r = c.parse_intake(text)
    p = resolve(args)
    created = []
    with c.lock(p.dir):
        for item in r.items:
            b = _create(p, _title(item.text), item.type, c.guess_tier(item.type, item.text), "captured",
                        raw=_raw_with_block(item, r), scope=item.scopes, depends=item.refs,
                        priority="urgent" if item.urgent else "normal", explore=item.explore)
            if _block(item, r, "skip"):
                b.set_section("Non-goals", "".join(f"- {s}\n" for s in _block(item, r, "skip")))
                c.save_brief(p, b, touch=False)
            created.append(b)
        c.log_event(p, "intake", data={"created": [b.id for b in created], "overrides": r.overrides,
                                       "untagged": bool(r.untagged)}, session=session())
        c.regen_views(p)
    if len(created) >= 3:  # T-0383: a batch of new work: relate it (detached, once a day)
        import fmrelate
        try:
            fmrelate.spawn(p)
        except OSError:  # the capture already happened; a relate that can't start costs it nothing
            pass
    order = sorted(created, key=lambda b: (0 if b.priority == "urgent" else 1, c.RANK.get(b.type, 99), c.id_num(b.id)))
    data = {"created": [c.brief_summary(b) for b in created], "order": [c.brief_summary(b) for b in order],
            "context": r.context, "constraints": r.constraints, "done_when": r.done_when, "skip": r.skip,
            "untagged": r.untagged, "overrides": r.overrides}
    lines = [f"Captured {len(created)} item(s). Canonical order:"] + \
            [f"  {b.id} [{b.type}{'!' if b.priority == 'urgent' else ''}{'?' if b.meta.get('explore') else ''} {b.tier}] {b.title}"
             for b in order]
    if r.untagged:
        lines.append(f"Untagged text (classify it yourself): {r.untagged[:200]}")
    out(args, data, "\n".join(lines))


def cmd_capture(args):
    if args.self_:
        home = c.foreman_home()
        p = c.find_project(home, create=True) or c.init_project(home)
    else:
        p = resolve(args)
    type_ = (args.type or "FEATURE").upper()
    type_ = c.WORK_TAGS.get(type_, type_)
    if type_ not in c.TYPES:
        raise UsageError(f"unknown type {args.type!r}; one of {', '.join(c.TYPES)}")
    text, raw = (args.text or "").strip(), args.text
    if args.from_file:
        attached, first = _attachment(p, args.from_file)
        text = text or first
        raw = (args.text + "\n\n" if args.text else "") + attached
    if not text:
        raise UsageError("fm capture \"<request>\" [--from-file PATH|-]: say what to do, or attach a file that does")
    with c.lock(p.dir):
        b = _create(p, _title(text), type_, args.tier or c.guess_tier(type_, text), "captured",
                    raw=raw, scope=args.scope or (), source=args.source,
                    depends=list(dict.fromkeys(c._REF_RE.findall(args.text or ""))),  # T-0334: as fm intake does
                    priority="urgent" if args.urgent else "normal")
        c.log_event(p, "capture", task=b.id, data={"source": args.source, "type": type_}, session=session())
        c.regen_views(p)
    _note_escapes(p, b, args.text)
    out(args, c.brief_summary(b), f"Captured as {b.id} [{b.type}, {b.tier}] (source: {args.source})."
        + _covered_note(p, b.id, text) + _reask_note(p, b.id, text))


EXCERPT_HEAD, EXCERPT_TAIL = 10, 30  # T-0477: a log's start says what ran, its end what broke
PASTE_MAX = 2_000_000


def _attachment(p, src):
    """T-0477: fm capture --from-file: (raw text, first line). A text file, or a paste on stdin (-), gives its path and
    an excerpt (the head and tail of a long one), redacted and marked as data; a paste is kept, redacted, in the
    project's attachments/. A binary file (a screenshot) is attached as its path alone."""
    if src == "-":
        data = c.redact(sys.stdin.buffer.read(PASTE_MAX).decode("utf-8", "replace"))  # T-0671 review: bounded
        import hashlib
        path = os.path.join(p.dir, "attachments", f"paste-{hashlib.sha256(data.encode()).hexdigest()[:12]}.txt")
        c.write_atomic(path, data)
        lines = _excerpt(data.splitlines())
    else:
        path = os.path.realpath(src)
        if not os.path.isfile(path):  # a FIFO or device would hang the read, a directory would crash it
            raise UsageError(f"{src} is not a regular file")
        import fmguard, types  # T-0671 review: the guard refuses reading these; so does an attachment
        if fmguard._is_credential(path, types.SimpleNamespace(home=os.path.expanduser("~"), scratch=())):
            raise UsageError(f"{src} looks like a credentials file: describe the problem, or attach a copy with "
                             f"the secrets taken out")
        with open(path, "rb") as f:
            if b"\0" in f.read(8192):
                return f"Attached: {path}", f"Attached: {os.path.basename(path)}"
            f.seek(0)
            # ponytail: streamed, so redaction sees only the excerpt: a key block cut by the elision can leak its kept
            # lines into the brief; redact the whole file first if that matters
            lines = _excerpt(x.decode("utf-8", "replace") for x in f)
    first = next((c.redact(x).strip() for x in lines if x.strip()), f"Attached: {os.path.basename(path)}")
    return f"Attached: {path}\n" + c.defang(c.redact("\n".join(lines))), first


def _excerpt(lines):
    import collections
    head, tail, n = [], collections.deque(maxlen=EXCERPT_TAIL), 0
    for line in lines:
        n += 1
        line = c.redact(line.rstrip("\r\n").replace("\t", "    "))  # before the cut: a cut secret no longer matches
        (head if n <= EXCERPT_HEAD else tail).append(c.fit(c.plain(line), 300))
    return head + ([f"… {n - len(head) - len(tail)} lines …"] if n > len(head) + len(tail) else []) + list(tail)


def _note_escapes(p, b, text):
    """T-0285: a FIX or SECURITY request that names a finished task is a defect that got past that task's gates and
    reviews: an escape, logged against it with the audit lenses it closed with (fm friction lists them)."""
    named = [t for t in dict.fromkeys(re.findall(r"\bT-\d{4,}\b", text or "")) if t != b.id]
    if b.type not in ("FIX", "SECURITY") or not named:
        return
    briefs = {x.id: x for x in c.load_briefs(p, include_archive=True)}  # an escape may surface after the archive
    for tid in named:
        done = briefs.get(tid)
        if done and done.status == "done":
            with c.lock(p.dir):
                c.log_event(p, "escape", task=tid, data={"by": b.id, "type": b.type, "title": c.fit(b.title, 160),
                                                         "lenses": sorted({x[0] for x in done.audits()})},
                            session=session())


def _reask_note(p, tid, text):
    """T-0438: a request like a dropped task, or one a standing veto covers, is said at capture, before work starts."""
    try:
        import fmrecall
        hit = fmrecall.nearest_dropped(p, text, skip=tid)
        notes = ([f"Dropped before: {hit[0]} ({c.fit(c.plain(hit[1]), 60)})"
                  + (f": {c.fit(c.defang(c.plain(hit[2])), 120)}" if hit[2] else "")] if hit else []) + \
            [f"Vetoed: \"{v['said']}\"" for v in c.veto_hits(p, text)][:2]
    except Exception:  # a note; capture never fails over it
        return ""
    return ("\n" + "; ".join(notes) + f". If that still holds, drop this: fm task drop {tid} \"<why>\".") if notes else ""


def _covered_note(p, tid, text):
    """T-0256: the request may already be an fm command; say so before anything is built."""
    try:
        import fmrecall
        hits = fmrecall.covered(text)
    except Exception:
        return ""
    if not hits:
        return ""
    return ("\nAlready covered? " + "; ".join(f"fm {name} — {help_}" for name, help_ in hits)
            + f". If it is, use it and drop this: fm task drop {tid} \"covered by fm {hits[0][0]}\".")


HYPO_STATUS = {"ruled-out": "ruled out", "confirmed": "confirmed", "open": "open"}


def task_hypo(p, args):
    """T-0207: the debugging ledger. A probe that fails is a result, recorded like any other, not an error."""
    if args.action == "add":
        claim = " ".join(args.args).strip()
        if not claim:
            raise UsageError("a hypothesis needs a claim")
        b, n = mutate(p, args.id, lambda b: b.add_hypothesis(claim, args.probe), "hypothesis",
                      {"claim": c.redact(claim)[:200]})
        return out(args, dict(c.brief_summary(b), n=n), f"{b.id}: H{n} added (open).")
    if args.action == "ruled":  # T-1075: this task's refutations and its scope's; --write hands them to fm-debugger
        b = need_brief(p, args.id)
        rows = c.refuted(p, b)
        lines = [f"- {c.refuted_line(r)}" for r in rows]
        text = (f"Refuted hypotheses ({c.REFUTED_LABEL}):\n" + "\n".join(lines) if lines
                else f"{b.id}: nothing ruled out yet, here or in tasks on its scope.")
        path = None
        if args.write:
            path = os.path.join(p.dir, "handoffs", f"{b.id}-ruled-out.md")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            c.write_atomic(path, c.redact(
                f"# Ruled out for {b.id} {c.plain(b.title)}\n\nHypotheses already refuted, by this task or earlier "
                f"tasks on its scope ({c.REFUTED_LABEL}). Each is refuted by the task named: re-test one only with new "
                f"evidence against its reason.\n\n" + ("\n".join(lines) or "(nothing yet)") + "\n"))
            text += f"\nwritten to {path}: name it in the fm-debugger brief"
        return out(args, {"task": b.id, "path": path, "ruled_out": [
            {"task": t, "n": n, "claim": claim, "why": why, "age_days": age} for t, n, claim, why, age in rows]}, text)
    if len(args.args) != 2 or not args.args[0].isdigit() or args.args[1] not in HYPO_STATUS:
        raise UsageError("fm task hypo ID mark N ruled-out|confirmed|open [--run CMD] [--why REASON]")
    n, status = int(args.args[0]), HYPO_STATUS[args.args[1]]
    if n not in {h[0] for h in need_brief(p, args.id).hypotheses()}:
        raise UsageError(f"{args.id} has no H{n}")
    result, shown = None, ""
    if args.run:
        code, output = c.run_command(p.root, args.run, args.timeout if args.timeout > 0 else None)
        result, shown = c.run_result(code, output), "\n".join(output.rstrip().splitlines()[-20:])
    b, _ = mutate(p, args.id, lambda b: b.mark_hypothesis(n, status, args.run, result, args.why), "hypothesis",
                  {"n": n, "status": status, "ran": c.redact(f"{args.run or ''} → {result or ''}")[:300],
                   "why": c.redact(args.why or "")[:200]})
    return out(args, c.brief_summary(b), (shown + "\n" if shown else "") + f"{b.id}: H{n} {status}.")


ASK_DAYS = 7  # T-0622: an unanswered ask fm second session found is deferred (never dropped) after this


def unanswered_asks(p):
    """T-0622: tasks fm second session captured from the last session's missed requests that are still captured."""
    found = {e.get("task") for e in c.ledger_tail(p, 5000) if e.get("event") == "capture"
             and (e.get("data") or {}).get("via") == "second session"}
    return [b.id for b in c.load_briefs(p) if b.id in found and b.status == "captured"]


def flag_replan(p, task, reason):
    """T-0603: an active M/L task's plan met a surprise; fm next leads with a replan until fm task log ID "replan: …"
    (a later trigger replaces the reason; the Log keeps each one)."""
    b, reason = (c.find_brief(p, task) if task else None), " ".join(c.redact(reason).split())  # one frontmatter line
    if b and b.status == "active" and b.tier in ("M", "L"):
        mutate(p, b.id, lambda x: (x.meta.update(replan=reason), x.append_log(f"plan revision needed: {reason}")),
               "replan_needed", {"reason": reason[:200]})


def task_assume(p, args):
    """T-0254: the brief's assumptions say whether they were checked. A check that fails marks it false, not an error."""
    if args.action == "add":
        fact = " ".join(args.args).strip()
        if not fact:
            raise UsageError("an assumption needs its text")
        check = getattr(args, "check", None)  # T-0489: a command that stays true while it holds
        kill = getattr(args, "kill", None)  # T-0631: what would show it false; fm next lists it while unverified
        text = fact + (f" — check: `{check}`" if check else "") + (f" — kill: {c.plain(kill)}" if kill else "")
        b, n = mutate(p, args.id, lambda b: b.add_assumption(text), "assumption", {"text": c.redact(fact)[:200]})
        return out(args, dict(c.brief_summary(b), n=n), f"{b.id}: assumption {n} added [assumed]"
                   + ("; fm sentinel re-runs its check." if check else "."))
    if len(args.args) != 1 or not args.args[0].isdigit() or (args.run is None) == (args.evidence is None):
        raise UsageError("fm task assume ID verify N --run CMD | --evidence \"<how it was checked>\"")
    n = int(args.args[0])
    if not any(a[0] == n for a in need_brief(p, args.id).assumptions()):
        raise UsageError(f"{args.id} has no assumption {n}")
    code, shown, how = 0, "", args.evidence
    if args.run is not None:
        code, output = c.run_command(p.root, args.run, args.timeout if args.timeout > 0 else None)
        shown = "\n".join(output.rstrip().splitlines()[-20:])
        how = "`" + args.run.replace("`", "'") + f"` → {c.run_result(code, output)}"
    status = "verified" if code == 0 else "false"
    def mark(b):
        if not b.mark_assumption(n, status, how):  # review: removed since the check above
            raise UsageError(f"{b.id} has no assumption {n}")
    b, _ = mutate(p, args.id, mark, "assumption",
                  {"n": n, "status": status, "how": c.redact(how)[:300]})
    if status == "false":  # T-0643: the steps that rest on it are named for re-check
        cite = [s.n for s in b.steps() if re.search(rf"\bA{n}\b", s.text)]
        flag_replan(p, b.id, f"assumption {n} is false" + (
            f"; step {', '.join(map(str, cite))} cite{'s' if len(cite) == 1 else ''} it" if cite else ""))
    return out(args, dict(c.brief_summary(b), status=status), (shown + "\n" if shown else "") + (
        f"{b.id}: assumption {n} verified." if status == "verified" else
        f"{b.id}: assumption {n} is false — re-check the plan, and log it: fm surprise \"<expected> → <observed>\"."))


def cmd_vetoes(args):
    """T-0251: what the user said never to do, as checked before matching calls; rm N drops one that no longer holds."""
    p = resolve(args)
    if args.action == "rm":
        if args.n is None or not c.drop_veto(p, args.n):
            raise UsageError("fm vetoes rm N (N from fm vetoes)")
        return out(args, {"removed": args.n}, f"Veto {args.n} removed.")
    v = c.vetoes(p)
    out(args, v, "\n".join(f"{i}. {x.get('said', '')} — key words: {' '.join(x['words'])} ({str(x.get('at', ''))[:10]})"
                           for i, x in enumerate(v, 1)) or "No vetoes recorded.")


def cmd_rule(args):
    """T-0971: the user's regex rules on Bash commands or edited paths: a block denies with the why, a warn is a note.
    rm is the user's (the guard refuses it from Claude as self-authorize)."""
    p = resolve(args)
    if args.action == "rm":
        n = int(args.arg) if str(args.arg or "").isdigit() else None
        if n is None or not c.drop_rule(p, n):
            raise UsageError("fm rule rm N (N from fm rule list)")
        return out(args, {"removed": n}, f"Rule {n} removed.")
    if args.action == "add":
        pattern, why = args.arg, args.why
        if args.from_veto is not None:
            v = c.vetoes(p)
            if not 1 <= args.from_veto <= len(v):
                raise UsageError("fm rule add --from-veto N (N from fm vetoes)")
            veto = v[args.from_veto - 1]  # its key words, each starting a word, in any order (as veto_hits reads)
            pattern = "(?i)^" + "".join(rf"(?=[\s\S]*\b{re.escape(str(w))})" for w in veto["words"])
            why = why or veto.get("said")
        try:
            rec = c.add_rule(p, pattern, args.on, "warn" if args.warn else "block", why)
        except ValueError as e:
            raise UsageError(f"fm rule add: {e}")
        n = len(c.rules(p))
        if args.moves:  # T-1059: a pre-registered trial, graded in fm digest
            import fmtrials
            fmtrials.add(p, f"rule add {pattern}", args.moves, args.by)
        return out(args, dict(rec, n=n), f"Rule {n}: {rec['action']} {rec['on']} matching {rec['pattern']}"
                                         f"{' — ' + rec['why'] if rec['why'] else ''}.")
    v = c.rules(p)
    out(args, v, "\n".join(f"{i}. {x['action']} {x['on']} /{x['pattern']}/ — {x.get('why') or 'no reason given'} "
                           f"({str(x.get('at', ''))[:10]})" for i, x in enumerate(v, 1)) or "No rules.")


def cmd_surprise(args):
    """T-0253: fm surprise "<expected> → <observed>": where the model of the code was wrong; friction and recall bring it back."""
    p = resolve(args)
    text = c.redact(c.plain(" ".join(args.text))).strip()
    if not text:
        raise UsageError('fm surprise "<expected> → <observed>"')
    task = need_brief(p, args.task).id if args.task else getattr(c.active_brief(c.load_briefs(p), p.lane), "id", None)
    rec = {"at": c.now(), "task": task, "text": text[:500]}
    with c.lock(p.dir):
        with open(os.path.join(p.dir, "surprises.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    c.log_event(p, "surprise", task=task, data={"text": text[:300]})
    flag_replan(p, task, "surprise: " + c.fit(text, 160))
    return out(args, rec, f"Surprise logged{f' on {task}' if task else ''}: fm friction and fm recall will bring it back.")


def cmd_task(args):
    p = resolve(args)
    sub = args.task_cmd
    if sub in ("done", "finish", "audit", "drop") and getattr(p, "lane", None) and getattr(args, "id", None):
        own = c.find_brief(p, args.id)  # T-0234 review: a builder hands back a commit; the main thread closes the task
        if own and own.meta.get("builder"):
            raise c.PolicyError(f"{own.id} is a builder's task: the main thread reviews, merges and closes it (fm lane "
                                f"rm {own.id}, then fm task {sub} from the main checkout); report back instead")
    if sub == "new":
        return task_new(p, args)
    if sub == "packet":
        return task_packet(p, args)
    if sub == "revert":
        return task_revert(p, args)
    if sub == "finding":  # T-0743: one reviewer finding and whether it held, for per-lens precision
        if args.lens not in c.AUDIT_LENSES:
            raise UsageError(f"unknown lens {args.lens!r}; one of {', '.join(c.AUDIT_LENSES)}")
        b = need_brief(p, args.id)
        text = c.redact(" ".join(args.text))[:300]
        c.log_event(p, "finding", task=b.id, data={"lens": args.lens, "verdict": args.verdict, "text": text})
        return out(args, {"task": b.id, "lens": args.lens, "verdict": args.verdict},
                   f"{b.id}: {args.lens} finding {args.verdict}.")
    if sub == "dissent":  # T-0642
        import fmsecond
        return fmsecond.task_dissent(p, args)
    if sub in ("split", "capsule"):  # T-0709
        import fmsplit
        return (fmsplit.task_split if sub == "split" else fmsplit.task_capsule)(p, args)
    if sub == "show":
        b = need_brief(p, args.id)
        if args.story:  # T-0483
            import fmrecall
            s = fmrecall.story(p, b)
            return out(args, s, fmrecall.render_story(s))
        if args.json:
            return print(json.dumps(dict(c.brief_detail(b), meta=b.meta, blockers=b.done_blockers()), indent=2))
        import fmcost
        return print(b.render() + (f"\n{line}\n" if (line := fmcost.cost_line(p, b)) else ""), end="")  # T-1083
    if sub == "set":
        return task_set(p, args)
    if sub == "step":
        return task_step(p, args)
    if sub == "ac":
        return task_ac(p, args)
    if sub == "log":
        def note(b):
            b.append_log(args.text)
            if args.text.strip().lower().startswith("replan:"):  # T-0603: the plan was re-read and revised
                b.meta.pop("replan", None)
        b, _ = mutate(p, args.id, note, "note", {"text": args.text[:300]})
        return out(args, c.brief_summary(b), f"{b.id}: logged.")
    if sub == "hypo":
        return task_hypo(p, args)
    if sub == "assume":
        return task_assume(p, args)
    if sub == "note":  # T-0630: the task's working memory, printed at checkpoint and resume
        text = " ".join(" ".join(args.text).split())
        b, _ = mutate(p, args.id, lambda b: b._append_line("Notes", f"- [{args.kind}] {c.redact(text)}"), "case_note",
                      {"kind": args.kind, "text": c.redact(text)[:200]})
        return out(args, c.brief_summary(b), f"{b.id}: {args.kind} noted.")
    if sub == "evidence":
        code, shown = 0, ""
        if args.run is not None:  # run it: the real exit code and output, never a typed summary
            if args.cmd is not None:
                raise UsageError("give the command either as --run CMD or as CMD RESULT, not both")
            pre = need_brief(p, args.id)
            code, output = c.run_command(p.root, args.run, args.timeout if args.timeout > 0 else None)
            cmd, result, shown = args.run, c.run_result(code, output, args.run), "\n".join(output.rstrip().splitlines()[-20:])
            result, tried = _step_checks(pre, args.step, args.run, code, output, result)
        elif args.cmd is None or args.result is None:
            raise UsageError("fm task evidence needs --run CMD (preferred) or CMD RESULT")
        else:
            cmd, result = args.cmd, args.result
        tree = c.worktree_id(p.root)
        if args.run is None:
            tried = None

        def record(b):
            b.add_evidence(cmd, result, step=args.step, ac=args.ac, tree=tree, ran=args.run is not None,
                           inconclusive=args.inconclusive)
            if tried:  # T-0632: what was tried, for whoever picks the step up
                b.append_log(f"tried: `{cmd}` ×{tried} on step {args.step}, failing the same way")
        b, _ = mutate(p, args.id, record,
                      "evidence", {"step": args.step, "ac": args.ac, "cmd": cmd, "result": result[:300],
                                   **({"inconclusive": True} if args.inconclusive else {})})
        for w in _evidence_notes(b, args.step, result, tried):
            print(f"fm: warning: {w}", file=sys.stderr)
        out(args, dict(c.brief_summary(b), exit=code), (shown + "\n" if shown else "") + f"{b.id}: evidence recorded"
            + (f" ({result})" if args.run is not None else "")
            + (" as inconclusive: it never counts as passing; a sharper check is next." if args.inconclusive else "."))
        return code
    if sub == "audit":
        if args.lens not in c.AUDIT_LENSES:
            raise UsageError(f"unknown lens {args.lens!r}; one of {', '.join(c.AUDIT_LENSES)}")
        tree = c.worktree_id(p.root)
        b, _ = mutate(p, args.id, lambda b: b.add_audit(args.lens, args.how, args.result, tree=tree),
                      "audit", {"lens": args.lens, "how": args.how[:200], "result": args.result[:300]})
        return out(args, c.brief_summary(b), f"{b.id}: audit ({args.lens}) recorded.")
    if sub == "done":
        import fmdocs
        since, tree = c.last_change(p, args.id), c.worktree_id(p.root)
        pre = need_brief(p, args.id)
        if pre.status == "dropped":  # T-0679 chaos test: a dropped task isn't finished by closing it again
            raise c.PolicyError(f"{pre.id} is dropped: reopen it first (fm task set {pre.id} status=planned)")
        drift, notes = fmdocs.task_docs(p.root, pre.section("Docs impact")) if pre.tier in ("M", "L") else ([], [])

        lesson = c.plain(args.lesson or "").strip()
        touches = c.task_touches(p, pre.id)
        base = c.task_base(p.root, pre) if c.git_root(p.root) else None
        if base:  # R1: edits made through the shell or outside Claude count too
            import fmmap
            for f in fmmap.changed(p.root, base):
                if f not in touches and not f.startswith(".foreman/"):
                    try:
                        touches[f] = c.iso(os.path.getmtime(os.path.join(p.root, f)))
                    except OSError:  # deleted
                        touches[f] = c.now()
        files = list(touches)
        diff = c.task_diff(p.root, base) if base else None
        risky = c.sensitive(files, diff or "")
        recorded = pre.meta.get("base_tree") or pre.meta.get("base")  # never focused: no start point, as before
        if diff is None and recorded and c.git_root(p.root):  # T-0078 review: what can't be read isn't passed as clean
            risky.append("diff unavailable, so its content wasn't checked")

        def done(b):
            reasons = [r + f" (security-sensitive: {', '.join(risky)})" if r.startswith("audit missing: adversary")
                       else r for r in b.done_blockers(since, tree, ("adversary",) if risky else ())] + drift
            import fmsplit  # T-0709: a parent closes after its children
            reasons += [f"child {k.id} is {k.status}: finish it first (fm task capsule {k.id} shows what it returned)"
                        for k in fmsplit.open_children(p, b)]
            outside = c.scope_drift(b, files)
            if outside and not c.scope_reason_covers(b, touches, outside):
                latest = max(outside, key=lambda f: touches.get(f, ""))  # T-0168: a reason counts after this edit
                reasons.append(f"edited outside scope [{', '.join(b.meta.get('scope') or [])}]: {', '.join(outside[:8])}"
                               f"; widen it (fm task set {b.id} scope=…) or say why after your last edit of {latest} "
                               f"(fm task log {b.id} \"scope: <why>\"; a reason logged before an edit doesn't cover it)")
            if b.type == "CLEAN" and first_edit and not b.section("Behaviour lock").strip() and not any(
                    ts <= first_edit for ts in b.ran_times()):
                reasons.append(f"no behaviour lock: a CLEAN change needs the tests run before its first edit (fm check "
                               f"--evidence {b.id} --step 1), or fm task set {b.id} --section \"Behaviour lock\" --text "
                               f"\"none: <why>\"")
            if b.type == "RESEARCH" and not b.section("Decision").strip():  # T-0896 (was a warning, T-0599)
                reasons.append(f"no Decision: research ends in a choice: fm task set {b.id} --section Decision --text "
                               f"\"Recommendation: …; would change if: …\" (or \"none: <why>\")")
            if b.tier in ("M", "L") and not lesson and not b.section("Lessons").strip():
                reasons.append(f"lesson missing: fm task done {b.id} --lesson \"<what the next similar task should "
                               f"know>\" (or \"none: <why>\"); recall shows it on related work")
            if reasons:
                lead = "" if hasattr(args, "audit") else (  # T-0849: fm task done, not finish's own close
                    f" — one call settles most of it: fm task finish {b.id} --run \"<test cmd>\" --audit \"<how>\""
                    + (" --lens \"<lens>: <result>\" … --docs \"<…>\" --lesson \"<…>\"" if b.tier in ("M", "L") else ""))
                raise c.PolicyError(f"{b.id} can't be marked done{lead}:\n  - " + "\n  - ".join(reasons))
            if lesson:
                old = b.section("Lessons").rstrip()
                b.set_section("Lessons", (old + "\n" if old else "") + f"- {lesson}")
            b.meta["status"] = "done"
            b.meta["verified"] = b.grade()[0]
            if gaps:  # T-0645: what this plan forgot, for the next similar plan (fm recall at focus)
                b.set_section("Plan gaps", gaps)
            if files:  # recall's "Start here" and edit tripwires for the next related task
                b.set_section("Files touched", "".join(f"- {f}\n" for f in files[:30]))
            b.append_log("done")  # T-0487: what passed on which model, for fm cost --by-model (and routing later)
            logged.update(model=_session_model(), type=b.type, tier=b.tier, verified=b.meta["verified"],
                          planned=len(b.meta.get("scope") or []), changed=len(files))  # T-0644
            # T-1061: the plan as it was at first focus (scope, predictions) against what happened
            if b.meta.get("plan0_at") and b.meta.get("plan0_scope"):
                logged["outside"] = len(c.scope_drift(types.SimpleNamespace(meta={"scope": b.meta["plan0_scope"]}), files))
            pm, pa = int(b.meta.get("predict_minutes") or 0), int(b.meta.get("predict_attempts") or 0)
            if pm or pa:
                evs = [e for e in c.ledger_tail(p, 5000) if e.get("task") == b.id]
                start = [i for i, e in enumerate(evs) if e.get("event") == "focus" and c.parse_ts(e.get("ts"))]
                logged.update(predict_minutes=pm, predict_attempts=pa)
                if start:  # the latest focus (a block or reopen means a re-focus); unknown start: no minutes, never a clean 0
                    # active time only: gaps of 30+ minutes between the task's events (overnight, away) don't count
                    import fmoutcomes
                    logged["minutes"] = fmoutcomes.active_minutes(
                        [c.parse_ts(e.get("ts")).timestamp() for e in evs[start[-1]:] if c.parse_ts(e.get("ts"))] + [time.time()])
                    logged["attempts"] = 1 + sum(1 for e in evs[start[-1]:]
                                                 if e.get("event") == "finish" and (e.get("data") or {}).get("failed"))
        first_edit = c.first_touch(p, pre.id)
        gaps = _plan_gaps(p, pre)
        logged = {"lesson": lesson[:300]} if lesson else {}
        b, _ = mutate(p, args.id, done, "task_done", logged)
        import fmoutcomes
        fmoutcomes.record_close(p, logged)  # T-1061
        if b.meta.get("batch"):
            _settle_batch(p, b, done=True)
        chose = " ".join(b.section("Decision").split()) if b.type == "RESEARCH" else ""
        if chose and not chose.lower().startswith("none"):  # T-0896: the project keeps what the research decided
            _write_decision(p, c.fit(chose, 400), f"research {b.id}: {c.fit(b.title, 120)}", task=b.id)
        try:
            import fmrecall
            fmrecall.write_tripwires(p)
            fmrecall.share_lesson(p, b, lesson or next((x.lstrip("- ").strip() for x in
                                                        b.section("Lessons").splitlines() if x.strip()), ""))
        except Exception as e:  # the task is done already; a derived index must not make that look failed
            print(f"fm: warning: tripwires not updated: {e}", file=sys.stderr)
        warns = _close_warnings(p, b, files)  # T-0672: seen, never a refusal
        if warns:  # T-0956: the verdict first, then the details
            kinds = dict.fromkeys(_warning_kind(w) for w in warns)
            print(f"fm: {len(warns)} warning{'' if len(warns) == 1 else 's'}: {', '.join(kinds)}", file=sys.stderr)
        for w in warns:
            print(f"fm: warning: {w}", file=sys.stderr)
        grade, why = b.grade()
        guessed = b.unverified() if b.tier in ("M", "L") else []  # T-0254: a warning, not a gate
        own = {a.n for a in b.acceptance() if c.verify_of(a.text) and any(  # T-0900: proven by its own command
            ln.startswith(f"- (ac {a.n}) ") and c._RAN_MARK in ln for ln in b.evidence())}
        by_hand = [re.sub(r" — verify with `.*`$", "", a.text) for a in b.acceptance() if a.n not in own]
        return out(args, dict(c.brief_summary(b), doc_drift=notes, verified=grade, unverified=guessed,
                              check_by_hand=by_hand, **({"ledger": _ledger_head(p)} if getattr(args, "json", False)
                                                        else {}),
                              **({"ablation": args.ablation} if getattr(args, "ablation", None) else {})),
                   f"{b.id} done (verification: {grade} — {why})." + (
            "\nCheck by hand (no command of its own proved these here):\n  - " + "\n  - ".join(by_hand[:8])
            if by_hand else "\nNothing needed from you: each criterion was proved by its own check."
            if not guessed and b.acceptance() else "") + (
            f"\n{len(guessed)} unverified assumption(s) — the plan rested on them unchecked; next time, fm task assume "
            f"{b.id} verify N --run CMD before building on one:\n  - " + "\n  - ".join(x[:140] for x in guessed[:5])
            if guessed else "") + (
            "\nDoc drift elsewhere (fm docs; not from this task):\n  - " + "\n  - ".join(notes[:10]) if notes else ""))
    if sub == "prove":
        return task_prove(p, args)
    if sub == "finish":
        return task_finish(p, args)
    if sub == "drop" and getattr(args, "done_in", None):
        return task_done_in(p, args)
    if sub == "drop" and not args.reason:
        raise UsageError("fm task drop needs a reason (or --done-in ID when another task did the work)")
    if sub in ("block", "drop", "defer"):
        status = {"block": "blocked", "drop": "dropped", "defer": "deferred"}[sub]
        reason = getattr(args, "reason", None) or ""

        def change(b):
            if status != "dropped" and b.status in ("active", "verifying"):
                c.pause_snapshot(p.root, b)  # T-0136
            b.meta["status"] = status
            until = getattr(args, "until", None)
            if until:  # T-0450: fm next names it again from then
                b.meta["revisit"] = until
            b.append_log((f"{status}: {reason}" if reason else status) + (f" (revisit {until})" if until else ""))
        until = getattr(args, "until", None)
        if until and until.startswith("when "):  # T-0958: the file's hash kept, so fm next can tell a change
            try:
                until = c.revisit_tag(p.root, until)[len("[revisit: "):-1]
            except ValueError as e:
                raise UsageError(str(e).replace("--revisit", "--until"))
            args.until = until
        elif until and not re.fullmatch(r"\d{4}-\d\d-\d\d", until):
            raise UsageError("--until takes a date, YYYY-MM-DD, or \"when PATH changes\"")
        cur = need_brief(p, args.id)
        if cur.status in c.CLOSED and status not in c.TRANSITIONS[cur.status]:  # T-0679 chaos test: dropped → blocked
            raise c.PolicyError(f"{cur.id} is {cur.status}: reopen it first (fm task set {cur.id} status=planned)")
        saved = []
        if status == "dropped" and cur.status in ("active", "verifying"):  # T-0895: its half-done work outlives a checkout
            try:
                saved = c.snapshot(p.root, f"fm task drop {cur.id}", timeout=30)
            except RuntimeError as e:
                print(f"fm: warning: {cur.id}'s work wasn't saved before the drop ({e})", file=sys.stderr)
        if saved:
            line = f"work at drop saved: {saved[0]} (restore: {c.restore_line(c.git_root(p.root), saved[0])})"
            prev = change
            change = lambda b: (prev(b), b.append_log(line))  # noqa: E731
            print(f"{cur.id}: {line}")
        b, _ = mutate(p, args.id, change, f"task_{sub}", {"reason": reason})
        if status == "blocked":  # T-0734: a block is a real failure worth an eval case, kept locally
            try:
                import fmcost
                fmcost.eval_case(p, b)
            except Exception as e:  # the block is recorded already; a case is a bonus
                print(f"fm: warning: no eval case written ({type(e).__name__})", file=sys.stderr)
        if status == "dropped" and b.meta.get("batch"):  # T-0257: a dropped batch hands its members back
            _settle_batch(p, b, done=False)
        return out(args, c.brief_summary(b), f"{b.id} {status}." + (f" Reason: {reason}" if reason else ""))
    raise UsageError(f"unknown task subcommand {sub}")


def _repro(b):
    """T-0704: the command a handoff's failure reproduces with: the newest command fm ran that failed and hasn't
    passed since, else the red run of red→green."""
    failed = None
    for line in b.evidence():
        if c._RAN_MARK in line and line.count("`") >= 2:
            cmd = line.split("`", 2)[1]
            failed = cmd if "` → ✗ exit" in line else None if cmd == failed else failed
    return failed or b.red_green_cmd()


def task_revert(p, args):
    """T-0732: what undoing a task would touch — its commits, and the open tasks that depend on or name it — and the
    command that undoes it. It never reverts by itself: reverting under a dependent is the user's call."""
    b = need_brief(p, args.id)
    log = c._git(p.root, "log", "-n", "3000", "--format=%h%x1f%s%x1f%b%x1e", fail="") if c.git_root(p.root) else ""
    own = re.compile(rf"\b{re.escape(b.id)}\b")
    rows = [(r.strip().split("\x1f") + ["", "", ""])[:3] for r in log.split("\x1e") if r.strip()]
    shas = [(h, subj) for h, subj, body in rows
            if (own.search(subj) or f"Foreman-Task: {b.id}" in body) and not subj.startswith("Revert ")]
    deps = [x for x in c.load_briefs(p) if x.id != b.id and x.status not in c.CLOSED
            and (b.id in c._deps(x) or own.search(" ".join([x.title, x.section("Raw request")])))]
    lines = [f"{b.id} {b.title}: {len(shas)} commit(s)"] + [f"  {h} {c.fit(s_, 90)}" for h, s_ in shas[:20]]
    lines += ["Open tasks that depend on or name it (check each before undoing):"] + [
        f"  {x.id} {c.fit(x.title, 70)} — " + ("depends on it" if b.id in c._deps(x) else "names it") for x in deps] \
        if deps else ["No open task depends on it."]
    lines += [f"Undo with: git revert --no-edit {' '.join(h for h, _ in shas)}" if shas else
              "No commit names it (nothing to revert by id)."]
    return out(args, {"task": b.id, "commits": [h for h, _ in shas], "dependents": [x.id for x in deps]},
               "\n".join(lines))


def task_packet(p, args):
    """T-0466: one markdown handoff for a person or another machine: what the task is, when it's done, the steps,
    the evidence, why it's blocked, what was tried and the next probe. Redacted; plain text, no instructions."""
    b = need_brief(p, args.id)
    repro = _repro(b)
    if args.check:  # T-0704: a handoff is trusted only while the failure it hands over still happens
        if not repro:
            raise UsageError(f"{b.id} has no failing run recorded to reproduce (fm task evidence {b.id} --run \"<cmd>\")")
        guard_stored(p, b, repro)  # T-0901 review: a recorded command, rerun
        code, output = c.run_command(p.root, repro, args.timeout)
        if code:
            return out(args, {"task": b.id, "cmd": repro, "reproduces": True},
                       f"{b.id}: the failure reproduces ({repro} → {c.run_result(code, output)}): handoff accepted.")
        out(args, {"task": b.id, "cmd": repro, "reproduces": False},
            f"{b.id}: stale handoff: {repro} passes now, so the failure it hands over doesn't happen here (fixed "
            f"already, or this checkout differs); re-check the task before working it.")
        raise SystemExit(1)
    hyps = b.hypotheses()
    probe = next((re.search(r"probe: `(.+?)`", t) for _, st, t in hyps if st == "open" and "probe: `" in t), None)
    step = next((s for s in b.steps() if not s.done), None)
    blocked = [x for x in b.section("Log").splitlines() if re.search(r"(?i)\bblock", x)][-3:]
    parts = [f"# Handoff: {b.id} {b.title}",
             f"{b.type} {b.tier}, {b.status}; packed {c.now()} from {p.root}",
             "## What it is", (b.section("Interpretation").strip() or re.sub(r"(?m)^> ?", "", b.section(
                 "Raw request")).strip() or b.title),
             "## Done when", "\n".join(f"- [{'x' if a.checked else ' '}] {a.text}" for a in b.acceptance()) or "(none)",
             "## Reproduce", f"`{repro}` (failed when packed; fm task packet {b.id} --check reruns it)" if repro
             else "(no failing run recorded)",
             "## Steps", b.section("Steps").strip() or "(none)",
             "## Evidence so far", "\n".join(b.evidence()) or "(none)",
             "## Blocked", "\n".join(blocked) or "(not blocked)",
             "## Tried", "\n".join(f"- H{n} [{st}] {t}" for n, st, t in hyps) or "(no hypotheses recorded)",
             "## Next probe", probe.group(1) if probe else (f"step {step.n}: {step.text}" if step else "close it"),
             "## Resume here", b.section("Resume here").strip() or "(none)"]
    text = c.redact("\n\n".join(parts)) + "\n"
    path = args.out or os.path.join(p.dir, "handoffs", f"{b.id}.md")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    c.write_atomic(path, text)
    return out(args, {"path": path, "task": b.id}, f"{b.id}: handoff packet written to {path}")


def _refuse_unrunnable(p, cmds):
    """T-0765: a verify that can't run at all is refused before the brief changes: once it has evidence it can't be
    edited (T-0342), and the only way out was dropping and recreating the task."""
    for cmd in filter(None, cmds):
        why = c.unrunnable(cmd, p.root)
        if why:
            raise UsageError(f"verify `{cmd}` can't run: {why}. Fix it before adding it: a criterion with evidence "
                             f"can't be edited later")


def _lint_verify(p, cmds):
    for cmd in filter(None, cmds):
        if cmd.lstrip().startswith("typed:"):  # T-0333: fm task finish runs a verify; a typed check is evidence
            print(f"fm: warning: verify `{cmd}` is a typed check, not a command, and fm task finish would run it: "
                  f"leave --verify off and record it with fm task evidence ID --ac N CMD RESULT", file=sys.stderr)
            continue
        problems = c.lint_verify(cmd, p.root)
        if problems:
            print(f"fm: warning: verify command `{cmd}`: {'; '.join(problems)}", file=sys.stderr)


def guard_stored(p, b, cmd):
    """T-0901: a command fm stored and is about to run (a verify, the affected template, a sentinel recheck) gets the
    guard's checks, with the task's grants, the standing yes and trust as the hook would apply them; PolicyError when
    it's refused. What never passed the hook (a brief stored before the guard read these, one fm sync brought in) is
    caught here."""
    import fmguard
    home, meta = os.path.expanduser("~"), c.read_meta(p)
    ctx = fmguard.Ctx(cwd=p.root, project_root=fmguard.project_root_for(p.root, home), home=home,
                      foreman_home=c.foreman_home(), state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks(),
                      scratch=[x for x in ("/tmp", "/var/tmp", os.environ.get("TMPDIR")) if x],
                      allow=set(b.meta.get("allow") or []) if b else set(), task_id=b.id if b else None,
                      standing=set(meta.get("standing") or {}), trusted=bool(c.trusted()))
    block = fmguard.check("Bash", {"command": cmd}, ctx)
    if block:
        raise c.PolicyError(f"fm won't run the stored command `{c.fit(cmd, 100)}`: {fmguard.message(block, ctx)}")


ABLATE_BUDGET = 600  # seconds for the whole ablation (T-1067)


def _ablate(p, b, args):
    """T-1067: after the real checks, revert each hunk alone against the linked tests. Informational: whatever goes
    wrong is one line, never a failed close; the result goes in the finish output (or its JSON), not in evidence."""
    js = getattr(args, "json", False)
    try:
        cmd, _, _ = affected(p, b)
        if cmd is None:
            raise UsageError("no linked tests")
        guard_stored(p, b, cmd)
        a = argparse.Namespace(run=cmd, max=20, step=None, ac=None, json=js, quiet=True, timeout=args.timeout,
                               deadline=time.time() + float(os.environ.get("FM_ABLATE_BUDGET", ABLATE_BUDGET)))
        task_prove_hunks(p, b, a)
        res = a.hunks_result
        text = f"{b.id}: ablation: {res['proven']}/{res['total']} hunks proven" + (
            f", {res['not_run']} not run" if res.get("not_run") else "") + "".join(
            f"\n  unproven: {u['file']} {u['at']} — {u['text']}" for u in res["unproven"])
    except Exception as e:  # noqa: BLE001 — the work is done; ablation must never fail the close
        res = {"skipped": str(e) or type(e).__name__}
        text = f"{b.id}: ablation skipped: {res['skipped']}"
    args.ablation = res
    if not js:
        print(text)


def task_finish(p, args):
    """One-call close-out (R1; any tier since T-0097): runs each open criterion's own verify command (else --run) and
    --run for each open step, records them as fm runs, checks what passed, records the audits (S: self; M/L: each
    --lens "<lens>: <result>", all done the --audit way), sets Docs impact, then fm task done. Anything that fails
    stops it before the audits; the failing runs stay recorded."""
    b = need_brief(p, args.id)
    claims = parse_claims(getattr(args, "claim", None))  # a bad tag stops it before anything runs
    if b.status == "dropped":  # T-0679 chaos test
        raise c.PolicyError(f"{b.id} is dropped: reopen it first (fm task set {b.id} status=planned)")
    if b.status == "done" and args.commit:  # T-0720: a commit refused after the close is retried on its own
        _commit_task(p, b, args.commit, stack=args.stack, check=args.stack_check)
        if not getattr(args, "json", False):
            print(_landed(p, b))
        return 0
    if not args.audit:
        raise UsageError("fm task finish needs --audit \"<how the audits were done>\"")
    lenses = []
    for spec in args.lens or []:
        lens, sep, result = spec.partition(":")
        if not sep or lens.strip() not in c.AUDIT_LENSES or not result.strip():
            raise UsageError(f"--lens takes '<lens>: <result>' with a lens of {', '.join(c.AUDIT_LENSES)}; got {spec!r}")
        lenses.append((lens.strip(), result.strip()))
    runs = {}

    def run(cmd):
        if cmd not in runs:
            guard_stored(p, b, cmd)  # T-0901
            runs[cmd] = c.run_command(p.root, cmd, args.timeout)
        return runs[cmd]
    # T-0142: an open step whose evidence is already recorded (fm task evidence --step) just closes; --run is only for
    # what has neither a verify command nor evidence, and the error names it
    def closes(n):  # evidence in, and no failed run newer than a pass
        try:
            b._refuse_failed_run(step=n)
        except c.PolicyError:
            return False
        return b.has_evidence(step=n)
    evidenced = [s.n for s in b.steps() if not s.done and closes(s.n)]
    todo = [("ac", n, cmd or args.run) for n, cmd in b.verify_cmds(unchecked=True)] + [
        ("step", s.n, args.run) for s in b.steps() if not s.done and s.n not in evidenced]
    missing = [f"{kind} {n}" + (f" ({c.fit(next(s.text for s in b.steps() if s.n == n), 50)})" if kind == "step" else "")
               for kind, n, cmd in todo if cmd is None]
    gaps = ([f"give --run \"<cmd>\" (or record evidence): {', '.join(missing)} has no verify command or evidence of "
             f"its own"] if missing else []) + _finish_gaps(b, args, lenses) + _self_docs_gaps(p, b)
    if gaps:  # T-0704: every gap in one refusal (135 finishes in 14 days were refused and retried one gap at a time)
        raise UsageError(f"{b.id} not finished, nothing ran:\n  - " + "\n  - ".join(gaps))
    if args.run and args.run not in [cmd for _, _, cmd in todo]:  # T-0742: --run is the close's final check, always
        todo.append(("final", None, args.run))
    for _, _, cmd in todo:  # T-0901 review: every one is checked before any runs, so a refusal leaves no side effects
        guard_stored(p, b, cmd)
    results = [(kind, n, cmd, *run(cmd)) for kind, n, cmd in todo]
    tree = c.worktree_id(p.root)

    def record(x):
        for n in evidenced:
            x.mark_step(n)  # refuses a failed run, as fm task step done does
        for kind, n, cmd, code, output in results:
            x.add_evidence(cmd, c.run_result(code, output, cmd), tree=tree, ran=True, **({} if kind == "final" else {kind: n}))
            if not code and kind != "final":
                x.check_ac(n) if kind == "ac" else x.mark_step(n)
        if not any(code for *_, code, _ in results):
            small = b.tier == "S" and all(lens != "self" for lens, _ in lenses)  # T-0129: --audit is S's self audit
            for lens, result in lenses + ([("self", args.result)] if small else []):
                x.add_audit(lens, args.audit, result, tree=tree)
            if args.docs:
                x.set_section("Docs impact", c.redact(args.docs))
            if getattr(args, "why_not_caught", None):  # T-0598
                x.set_section("Why not caught", c.redact(args.why_not_caught))
            if getattr(args, "followups", None):  # T-0639: the questions the user will likely ask, answered
                x.set_section("Follow-up answers", "\n".join(
                    "- " + c.redact(q.strip()).replace("=>", "→", 1) for q in args.followups))
            if getattr(args, "insight", None):
                x.set_section("Insight", c.redact(c.plain(args.insight).strip()))
            if claims:  # T-0614: what the close claims, each with how it's known
                x.set_section("Claims", "".join(f"- [{t}] {x_}" + (f" — evidence: {ev}" if ev else "") + "\n"
                                                for t, x_, ev in claims))
            if getattr(args, "differently", None):  # T-0641
                x.set_section("Would do differently", c.redact(c.plain(args.differently).strip()))
    mutate(p, b.id, record, "finish", {"runs": len(runs), "failed": sum(1 for r in results if r[3]),
                                       "ran": [[r[2][:200], r[3]] for r in results][:20]})  # T-0749: catch rates
    failed = [f"{kind}{f' {n}' if n else ''}: {cmd} → {c.run_result(code, output)}"
              for kind, n, cmd, code, output in results if code]
    if failed:
        raise c.PolicyError(f"{b.id} not finished; failing (recorded):\n  - " + "\n  - ".join(failed))
    _close_affected(p, need_brief(p, b.id), runs, args)  # T-1117: what it changed must not break what's linked to it
    if getattr(args, "ablate", False):
        _ablate(p, need_brief(p, b.id), args)
    if args.commit:  # T-0720: a credential found now leaves the task open to fix it, not done and uncommitted
        _commit_task(p, need_brief(p, b.id), args.commit, dry=True)
    args.task_cmd = "done"
    rc = cmd_task(args)
    why = (getattr(args, "why_not_caught", None) or "").strip()
    caught = next((f for f in c.task_touches(p, b.id) if c.TESTISH.search(f)), None) if why else None
    if not rc and caught:  # T-1009: the close added the catching test; a follow-up would only be dropped
        print(f"{b.id}: the catch landed with it: {caught}")
    elif not rc and why and not why.lower().startswith("none"):  # T-0598: the catch that was missing is its own task
        with c.lock(p.dir):
            f = _create(p, _title(f"Catch it earlier: {why}"), "FEATURE", "S", "captured",
                        raw=f"{b.id} ({b.title}) wasn't caught before it shipped: {why}", source="followup")
            c.log_event(p, "capture", task=f.id, data={"source": "followup", "from": b.id}, session=session())
            c.regen_views(p)
        print(f"{b.id}: captured {f.id} — catch it earlier: {c.fit(why, 80)}")
    elif not rc and b.type == "FIX" and not why and not b.section("Why not caught").strip():
        print(f"{b.id}: what would have caught this earlier? (--why-not-caught next time; M/L fixes need it)")
    if args.commit and not rc:
        _commit_task(p, need_brief(p, b.id), args.commit, stack=args.stack, check=args.stack_check)
    if not rc and not getattr(args, "json", False):
        import fmledger
        try:  # T-1065: the chain head, the anchor fm verify-ledger --head checks later
            print(fmledger.receipt(p))
        except OSError as e:  # the close has landed; an unreadable archive must not make it look failed
            print(f"Ledger: unreadable ({e.strerror or e})")
    started = None
    if not rc:
        try:
            started = _sentinel(p)
        except (OSError, subprocess.SubprocessError):
            pass  # the close has landed; the next close tries again
    if not rc and not getattr(args, "json", False):
        if started == "started":
            print("Full gates: running in the background (a red result becomes an urgent baseline task)")
        print(_landed(p, b))  # T-0956: the close's last line
    return rc


def _known_flaky(p):
    """The test names the flake ledger (c.note_flakes) has seen fail and then pass on the same tree."""
    try:
        with open(os.path.join(p.dir, "flakes.json"), encoding="utf-8") as f:
            flaky = json.load(f).get("flaky")
        return set(flaky) if isinstance(flaky, dict) else set()
    except (OSError, ValueError, AttributeError):
        return set()


def _close_affected(p, b, runs, args):
    """T-1117: the tests linked (fm map) to what this task changed run at its close (one rerun for a flake), and a
    failure refuses it unless the last full gate run of another task already had it (then it's noted: that run's
    baseline task owns it). An environment failure, or a runner whose failing tests can't be named, is said, not
    refused; --skip-affected REASON waives it on the record. No affected-tests command, nothing linked, or the same
    command already passed in this finish: nothing to run."""
    try:
        cmd, tests, _ = affected(p, b)
    except UsageError:
        return
    if not cmd or (runs.get(cmd) or (1,))[0] == 0:
        return
    waive = (getattr(args, "skip_affected", None) or "").strip()
    if waive:
        mutate(p, b.id, lambda x: x.append_log(f"affected tests waived: {c.plain(waive)[:200]}"), "close_affected",
               {"cmd": c.fit(cmd, 200), "waived": c.fit(waive, 200)})
        return
    guard_stored(p, b, cmd)
    env, timeout = _skip_env(red_first_tests(p, b, [cmd])), (args.timeout if args.timeout > 0 else None)
    code, output = c.run_command(p.root, cmd, timeout, env=env)
    if code and code != 124:
        code, output = c.run_command(p.root, cmd, timeout, env=env)  # a flake passes the second time
    names = c.failing_tests(output) if code else []
    c.log_event(p, "close_affected", task=b.id, data={"cmd": c.fit(cmd, 200), "exit": code, "failing": names[:20]},
                session=session())
    say = (lambda m: None) if getattr(args, "json", False) else print
    if not code:
        return
    if code == 124:
        raise c.PolicyError(f"{b.id} not finished: the tests linked to its changes timed out ({cmd}). Rerun with a "
                            f"longer --timeout, or waive on the record: --skip-affected \"<why>\"")
    env_why = failure_class(output)
    if env_why:
        say(f"{b.id}: the linked tests couldn't run here ({env_why}): {cmd}; not held against the close")
        return
    before = set()
    for e in reversed(c.ledger_tail(p, 3000)):  # another task's run: this task's own red run proves nothing
        if e.get("event") == "check_run" and e.get("task") != b.id:
            before = {n for r in (e.get("data") or {}).get("results") or [] for n in r.get("failing") or []}
            break
    if names and set(names) <= before:
        say(f"{b.id}: the linked tests fail, but were already red in the last full run ({', '.join(names[:4])}): "
            f"its baseline task owns them")
        return
    raise c.PolicyError(f"{b.id} not finished: the tests linked to its changes fail"
                        + (f" ({', '.join(names[:6])})" if names else " (the runner names no test)")
                        + f": {cmd} → {c.run_result(code, output)}. Fix them; if they were red before this task, a "
                        "full fm check records that and the close goes through; or waive on the record: "
                        "--skip-affected \"<why>\"")


def _sentinel(p):
    """T-1117: after a close, the full gates run in the background when the last full run is older than SENTINEL_CLOSES
    closes or SENTINEL_MIN minutes, so a break the linked tests miss is found without anyone remembering to look. One
    at a time (sentinel.pid); it carries the tree it was started on, so a run that ends after the next task's edits
    began captures no baseline. FOREMAN_SENTINEL=off skips it, =sync runs it inline (tests)."""
    mode = os.environ.get("FOREMAN_SENTINEL", "")
    if mode == "off" or (os.environ.get("FOREMAN_NO_BACKGROUND") and mode != "sync"):
        return None
    pidf = os.path.join(p.dir, "sentinel.pid")
    try:
        with open(pidf) as f:
            pid = int(f.read().strip() or 0)
        if pid and time.time() - os.path.getmtime(pidf) < 3600:
            os.kill(pid, 0)
            return None  # one is running
    except (OSError, ValueError):
        pass
    events, last, closes = c.ledger_tail(p, 5000), None, 0
    for e in reversed(events):
        if e.get("event") == "check_run":
            last = c.parse_ts(e.get("ts"))
            break
        closes += e.get("event") == "task_done"
    if last and closes < SENTINEL_CLOSES and time.time() - last.timestamp() < SENTINEL_MIN * 60:
        return None
    if c.host_strain():
        return None
    env = dict(os.environ, FOREMAN_SENTINEL_RUN="1", FOREMAN_SENTINEL_TREE=c.worktree_id(p.root) or "")
    argv = [os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "check"]
    if mode == "sync":
        c.write_atomic(pidf, str(os.getpid()))
        try:
            subprocess.run(argv, cwd=p.root, env=env, stdin=subprocess.DEVNULL, capture_output=True)
        finally:
            _unlink(pidf)
        return "ran"
    pr = subprocess.Popen(["sh", "-c", 'echo $$ > "$1"; "$2" check; rm -f "$1"', "sentinel", pidf, argv[0]],
                          cwd=p.root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL, start_new_session=True)
    return "started" if pr.pid else None


def _unlink(path):
    try:
        os.unlink(path)
    except OSError:
        pass


SENTINEL_CLOSES, SENTINEL_MIN = 3, 60


def _ledger_head(p):
    import fmledger
    try:
        r = fmledger.chain(p)
    except OSError as e:  # the task is done already: an unreadable archive is reported, never a crash
        return {"head": None, "unreadable": e.strerror or str(e)}
    return {k: r[k] for k in ("head", "chained", "broken")}


def _theirs(p, b, files):
    """T-0738: the files only another task edited (while this one was being worked): that task's to commit, even when
    this task's start snapshot couldn't be re-based past it (both changed neighbouring lines elsewhere). T-0739: from
    this task's first focus, not its capture: edits made before it started say nothing about its own changes."""
    events = c.ledger_tail(p, c.TASK_WINDOW)
    mine = set(c.task_touches(p, b.id)) | _claimed(p, b)
    first = next((i for i, e in enumerate(events) if e.get("event") == "focus" and e.get("task") == b.id), None)
    since = str(b.meta.get("created") or "")  # ledger order when its focus is in the window: seconds tie
    others = {os.path.relpath(f, p.root) for i, e in enumerate(events)
              if e.get("event") == "touched" and e.get("task") not in (None, b.id)
              and (i > first if first is not None else str(e.get("ts", "")) >= since)
              and (f := (e.get("data") or {}).get("file")) and f.startswith(p.root.rstrip("/") + "/")}
    return [f for f in files if f in others and f not in mine]


def _claimed(p, b):
    """T-1122: the files this task says are its own, its scope and the paths its 'scope:' log reasons name: an edit
    made in the same command as the finish has no touched record yet, so the record alone can't say it's this task's."""
    named = [s.rstrip("/") for s in b.meta.get("scope") or []]
    for line in b.section("Log").splitlines():
        head = line.partition(" scope: ")[2].split(" — ")[0] if " scope: " in line else ""
        named += [x.strip(" `'\"") for x in re.split(r",\s*|\s+and\s+", head) if x.strip()]
    return {n for n in named if n and not n.startswith(("/", "..")) and os.path.isfile(os.path.join(p.root, n))}


def _landed(p, b):
    """T-0956: the close's last line: where the task's own files ended up — committed (sha, pushed or not) or not.
    Another task's files are left out, as the commit leaves them out; git that can't answer says unknown."""
    import fmmap
    base = c.task_base(p.root, b) if c.git_root(p.root) else None
    if not base:
        return "Landed: unknown (no git start point on record)"
    files = [f for f in fmmap.changed(p.root, base) if not f.startswith(".foreman/")]
    files = [f for f in files if f not in set(_theirs(p, b, files))][:500]
    if not files:
        return "Landed: no file changes in git"
    dirty = c._git(p.root, "--literal-pathspecs", "status", "--porcelain", "--", *files, timeout=30).splitlines()
    if dirty:
        return f"Landed: not committed ({len(dirty)} file{'' if len(dirty) == 1 else 's'} uncommitted)"
    sha = c._git(p.root, "--literal-pathspecs", "log", "-1", "--format=%h", "--", *files, timeout=30).strip()
    if not sha:
        return "Landed: unknown (git could not say)"
    pushed = c._git(p.root, "branch", "-r", "--contains", sha, timeout=30).strip()
    return f"Landed: committed {sha} · {'pushed' if pushed else 'not pushed'}"


def _warning_kind(w):
    """A close warning's kind for the verdict line: its text before the first ':', '(', '[' or ' in '."""
    if re.match(r"T-\d+ was planned [SML], but its diff is", w):
        return "tier drift"
    return re.split(r"[:(\[]| in ", w, maxsplit=1)[0].strip()


def _finish_gaps(b, args, lenses):
    """T-0704: what fm task done would refuse that this call doesn't supply, checked before anything runs: the audit
    lenses its tier needs, docs impact and the lesson (M/L)."""
    given = {lens for lens, _ in lenses} | ({"self"} if b.tier == "S" else set())
    recorded = b.audit_blockers()
    gaps = [f"audit missing: --lens '{sorted(g)[0]}: <result>'" + (f" (or {', '.join(sorted(g)[1:])})" if len(g) > 1
                                                                  else "")
            for g in c.REQUIRED_AUDITS.get(b.tier, c.REQUIRED_AUDITS["S"])
            if not g & given and any(r.startswith(f"audit missing: {' or '.join(sorted(g))}") for r in recorded)]
    if b.docs_gap() and not args.docs:
        gaps.append("docs impact missing: --docs \"<docs updated | none: why>\"")
    if b.tier in ("M", "L") and not args.lesson and not b.section("Lessons").strip():
        gaps.append("lesson missing: --lesson \"<what the next similar task should know>\" (or \"none: <why>\")")
    if b.type == "FIX" and b.tier in ("M", "L") and not getattr(args, "why_not_caught", None) \
            and not b.section("Why not caught").strip():  # T-0598: every M/L fix asks what would have caught it
        gaps.append("why-not-caught missing: --why-not-caught \"<the test, gate or guard that would have caught it "
                    "earlier>\" (or \"none: <why>\"); it becomes a follow-up")
    return gaps


def _self_docs_gaps(p, b):
    """CLEAN T-0764: a close that touches fmcli.py or plugin/skills must leave Foreman's own docs naming real commands
    and skills (fm doctor's self docs check), so the close is refused, not caught later."""
    import fmdoctor
    import fmmap
    base = c.task_base(p.root, b) if c.git_root(p.root) else None
    if not base or not any(f == "plugin/lib/fmcli.py" or f.startswith("plugin/skills/")
                           for f in fmmap.changed(p.root, base)):
        return []
    res = fmdoctor.check_self_docs()
    return [f"self docs: {res.detail}"] if res.status == "FAIL" else []


def _commit_task(p, b, message, dry=False, stack=False, check=None):
    """T-0129: commit what this task changed (from its focus snapshot), only after it closed: a refused close commits
    nothing, and work from before the task stays out. A synced .foreman/ mirror goes with it. dry (T-0720): only the
    credential check, before the close, leaving the index as it was."""
    import fmmap
    import subprocess
    base = c.task_base(p.root, b) if c.git_root(p.root) else None
    if not base:
        if dry:
            return
        raise UsageError(f"{b.id} is done, but has no start point on record to tell its files apart: commit by hand")
    mirror = os.path.isdir(os.path.join(p.root, ".foreman")) and not c.mirror_ignored(p.root)
    files = fmmap.changed(p.root, base)
    # T-0192: a file written in the command that focused the task is in the focus snapshot; the hooks saw it touched
    touched = [f for f in c.task_touches(p, b.id) if f not in files]
    if touched:
        out = c._git(p.root, "--literal-pathspecs", "status", "--porcelain", "-z", "-uall", "--no-renames", "--", *touched,
                     timeout=30)
        files += [e[3:] for e in out.split("\0") if len(e) > 3]
    theirs = _theirs(p, b, files)
    files = [f for f in files if f not in theirs]
    if theirs and not dry:
        print(f"{b.id}: left out {len(theirs)} file(s) only other tasks edited: {', '.join(theirs[:8])}")
    files += [".foreman"] if mirror else []
    elsewhere = {}  # T-0360: edits in another checkout are that repo's to commit, so say where they are
    for e in c.ledger_tail(p, c.TASK_WINDOW):
        f = (e.get("data") or {}).get("file") if e.get("event") == "touched" and e.get("task") == b.id else None
        if f and not f.startswith(p.root.rstrip("/") + "/") and (r := c.git_root(os.path.dirname(f))):
            elsewhere.setdefault(r, set()).add(f)
    for r, fs in elsewhere.items() if not dry else ():
        print(f"{b.id}: {len(fs)} edited file(s) in {r} not committed (another repo): commit them there.")
    if not files:
        if not dry:
            print(f"{b.id}: nothing to commit{' here' if elsewhere else ''}.")
        return
    git = ["git", "--literal-pathspecs", "-C", p.root]  # session audit: a file named '*' names only itself
    # T-0837: a file untracked (git rm --cached) and deleted is on neither side: git add fails its pathspec, while
    # git commit -- <it> below takes the staged deletion as it is
    known = set(subprocess.run([*git, "ls-files", "--", *files], capture_output=True, text=True).stdout.splitlines())
    addable = [f for f in files if f in known or os.path.lexists(os.path.join(p.root, f))
               or any(k.startswith(f.rstrip("/") + "/") for k in known)]
    add = subprocess.run([*git, "add", "-A", "--", *addable], capture_output=True, text=True) if addable else \
        subprocess.CompletedProcess([], 0, "", "")
    if add.returncode == 0:  # T-0132: nothing that looks like a credential goes into a commit Foreman makes
        import fmsecrets
        leaks = fmsecrets.staged_leaks(p.root, files)
        if dry or leaks is None or leaks:
            subprocess.run([*git, "reset", "-q", "--", *files], capture_output=True)
        state = "not finished (still open, so fix it there)" if dry else "done, but not committed"
        if leaks is None or leaks:
            raise UsageError(f"{b.id} is {state}: git couldn't show the staged lines to check them"
                             if leaks is None else
                             f"{b.id} is {state}: {len(leaks)} added line(s) look like a credential (not "
                             f"printed): " + ", ".join(f"{f}:{n} ({k})" for f, n, k in leaks[:10])
                             + f". Remove it (and rotate a real one), or mark a test fixture's line "
                               f"`{fmsecrets.ALLOW}`, then commit"
                             + ("." if dry else f" (fm task finish {b.id} --commit \"<message>\" retries it)."))
    if dry:
        return
    if add.returncode == 0 and not subprocess.run([*git, "diff", "--cached", "--quiet", "--", *files]).returncode:
        print(f"{b.id}: nothing to commit (its files are as committed already).")  # T-0738: not a blank failure
        return
    if stack:  # T-0710: one commit per step group, each checked alone
        import fmstack
        subprocess.run([*git, "reset", "-q", "--", *files], capture_output=True)  # the stack builds its own index
        try:
            print("\n".join(fmstack.commit(p, b, files, message, check)))
        except ValueError as e:
            raise UsageError(f"{b.id} is done, but the stack wasn't committed: {e}")
        return
    trailer =[] if "Foreman-Task:" in message else ["--trailer", f"Foreman-Task: {b.id}"]  # fm why reads it
    # only the task's files (and so only what was scanned), whatever else was staged before (T-0132 review)
    done = add.returncode == 0 and subprocess.run([*git, "commit", "-q", "-m", message, *trailer, "--",
                                                   *files], capture_output=True, text=True)
    if not done or done.returncode:
        raise UsageError(f"{b.id} is done, but the commit failed: {((done and done.stderr) or add.stderr).strip()[:300]}")
    sha = c._git(p.root, "rev-parse", "--short", "HEAD").strip()
    n = len([x for x in c._git(p.root, "show", "--name-only", "--format=", "HEAD").split("\n") if x.strip()])
    held = f"{n} file{'' if n == 1 else 's'}"  # T-0380: what the commit holds, not the paths it was given
    mutate(p, b.id, lambda x: x.append_log(f"committed {sha} ({held})"), "commit", {"sha": sha})
    print(f"{b.id}: committed {sha} ({held}). Undo: git revert --no-edit {sha}")  # T-0918: the way back, named


def _hunks(diff):
    """[(file, header, hunk)] from a -U0 git diff: each hunk with its file's header, so it applies on its own."""
    out = []
    for block in re.split(r"(?m)^(?=diff --git )", diff):
        head, _, body = block.partition("\n@@")
        m = re.search(r"(?m)^\+\+\+ b/(.+?)\t?$", head) or re.search(r"(?m)^--- a/(.+?)\t?$", head)  # a\tb: spaces
        if not m or not body:
            continue
        for h in re.split(r"(?m)^(?=@@)", "@@" + body):
            if h.startswith("@@"):
                out.append((m.group(1), head + "\n", h if h.endswith("\n") else h + "\n"))
    return out


def _revert_hunk(path, head, hunk):
    """Put one -U0 hunk back where the diff says it is (T-0286: git apply -R --unidiff-zero picked the nearest identical
    line from the old file's position, so a hunk after an insertion mutated another line): its + lines, found at
    their place in the new file, become its - lines. None, or why it couldn't."""
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", hunk)
    if not m:
        return "no hunk header"
    start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
    body = [x for x in hunk.split("\n")[1:] if x[:1] in ("+", "-")]
    old, new = [x[1:] for x in body if x[0] == "-"], [x[1:] for x in body if x[0] == "+"]
    try:
        with open(path, encoding="utf-8", errors="surrogateescape") as fh:
            lines = fh.read().split("\n")
    except FileNotFoundError:  # a file the task deleted comes back
        lines = [""]
    at = start - 1 if count else start  # +c,0: the old lines go after line c
    if lines[at:at + count] != new:
        return "its lines aren't where the diff puts them"
    lines[at:at + count] = old
    if "\nnew file mode" in head and lines == [""]:
        os.remove(path)
        return None
    with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
        fh.write("\n".join(lines))
    return None


def _definitions(root, tree, f):
    """T-0279: a new Python file as mutations, one per top-level definition or statement (decorators included; the
    docstring and imports left alone): [(file, label, first line, (first, last line))], or None to keep the one
    whole-file hunk (not Python, or it doesn't parse)."""
    import ast
    if not f.endswith(".py"):
        return None
    src = c._git(root, "show", f"{tree}:{f}", fail=None, timeout=60)
    try:
        body = ast.parse(src or "").body
    except (SyntaxError, ValueError):
        return None
    lines = (src or "").split("\n")
    out = []
    for i, node in enumerate(body):
        if isinstance(node, (ast.Import, ast.ImportFrom)) or i == 0 and isinstance(node, ast.Expr) and \
                isinstance(getattr(node, "value", None), ast.Constant) and isinstance(node.value.value, str):
            continue
        first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
        out.append((f, f"@@ new file, lines {first}-{node.end_lineno} @@", c.fit(c.plain(" ".join(
            x.strip() for x in lines[first - 1:node.end_lineno] if x.strip())), 120), (first, node.end_lineno)))
    return out or None


def task_prove_hunks(p, b, args):
    """T-0271: revert each code hunk of the task's diff alone, in a detached worktree of the current tree, and run the
    check: a hunk whose removal still passes is unproven — the check doesn't test that part of the change."""
    # ponytail: git -U0 hunks (a new Python file per top-level definition), so a whole changed function body is one
    # hunk; split big added hunks into statements if coarse hunks start hiding untested branches
    import tempfile
    base, tree = c.task_base(p.root, b), c.worktree_tree(p.root)
    if not base or not tree:
        raise UsageError(f"{b.id} has no start snapshot or the working tree can't be read: prove --hunks needs both")
    files = [f for f in c._git(p.root, "diff", "--name-only", "--no-renames", base, tree, timeout=60).splitlines()
             if c.CODE.search(f) and not c.TESTISH.search(f)]
    hunks = _hunks(c._git(p.root, "--literal-pathspecs", "diff", "--no-color", "--no-ext-diff", "--no-renames", "-U0",
                          base, tree, "--", *files, timeout=120)) if files else []
    hunks = [m for f, head, h in hunks for m in (_definitions(p.root, tree, f) if "\nnew file mode" in head else None)
             or [(f, h.split("\n", 1)[0], c.fit(c.plain(" ".join(x[1:].strip() for x in h.splitlines()[1:]
                                                                if x[:1] in "+-")), 120), (head, h))]]
    if not hunks:
        args.hunks_result = {"total": 0, "proven": 0, "unproven": []}
        return 0 if getattr(args, "quiet", False) else out(
            args, args.hunks_result, f"{b.id}: no code hunks to prove (tests and docs aren't mutated)")
    shown = hunks[:args.max]
    commit = c._git(p.root, "-c", "user.name=Foreman", "-c", "user.email=foreman@localhost", "-c", "commit.gpgsign=false",
                    "commit-tree", "--no-gpg-sign", tree, "-m", "fm prove --hunks", timeout=60).strip()
    if not commit:
        raise UsageError("git commit-tree of the current tree failed: prove --hunks needs a scratch commit of it")
    unproven, skipped, tick, unreached = [], [], [time.time() + 2], 0

    def touch(path):  # each version gets its own whole second: caches keyed on mtime + size (Python's .pyc, make)
        tick[0] += 2  # would otherwise reuse the other version's build when the edit keeps the size
        if os.path.exists(path):
            os.utime(path, (tick[0], tick[0]))

    def restore(wt, f):  # files and index back to the scratch commit (HEAD may be the base: T-0297), new files gone
        ok = c._git(wt, "read-tree", "-u", "--reset", commit, fail=None, timeout=60) is not None
        ok = c._git(wt, "clean", "-fdq", fail=None, timeout=60) is not None and ok
        touch(os.path.join(wt, f))
        return ok
    with tempfile.TemporaryDirectory(prefix="fm-hunks-") as t:
        wt = os.path.join(t, "wt")
        c._git(p.root, "worktree", "add", "--detach", "-q", wt, commit, timeout=120)
        if not os.path.isdir(wt):
            raise UsageError("git worktree add for the current tree failed")
        hook = os.path.join(wt, "plugin", "hooks", "hook")
        try:
            with open(hook, encoding="utf-8", errors="replace") as fh:
                foreman = "committed_library" in fh.read()
        except OSError:
            foreman = False
        if foreman:  # T-0297: Foreman's hook falls back to HEAD's library when the working copy crashes; HEAD must be
            # the task's base, or a crashing mutation runs the unmutated code and passes (the scratch commit stays in
            # the index and the files)
            base_commit = c._git(p.root, "-c", "user.name=Foreman", "-c", "user.email=foreman@localhost",
                                 "commit-tree", "--no-gpg-sign", f"{base}^{{tree}}", "-m", "fm prove --hunks base",
                                 timeout=60).strip()
            if not base_commit or c._git(wt, "reset", "-q", "--soft", base_commit, fail=None, timeout=60) is None:
                raise UsageError("couldn't point the scratch worktree's HEAD at the task's base")
        try:
            code, output = c.run_command(wt, args.run, args.timeout)  # review: a check that fails anyway proves nothing
            if code:
                raise UsageError(f"the check fails on the unchanged tree in the scratch worktree ({c.run_result(code, output)})"
                                 f": fix it first — ignored files (.venv, node_modules, builds) aren't copied there")
            for f, at, text, patch in shown:
                if time.time() > getattr(args, "deadline", float("inf")):  # T-1067: one budget for the whole run
                    unreached += 1
                    continue
                if isinstance(patch[0], int):  # T-0279: one top-level definition of a new file, cut out
                    with open(os.path.join(wt, f), encoding="utf-8") as fh:
                        lines = fh.read().split("\n")
                    with open(os.path.join(wt, f), "w", encoding="utf-8") as fh:
                        fh.write("\n".join(lines[:patch[0] - 1] + lines[patch[1]:]))
                else:
                    why = _revert_hunk(os.path.join(wt, f), *patch)
                    if why:
                        skipped.append(f"{f} {at}: not applied ({why})")
                        continue
                touch(os.path.join(wt, f))
                code, _ = c.run_command(wt, args.run, min(args.timeout, getattr(args, "deadline", float("inf")) - time.time()))
                if not restore(wt, f):
                    skipped.append(f"{f}: the scratch tree couldn't be restored; stopped")
                    break
                if code == 124:  # a timeout isn't a failure the check caught
                    skipped.append(f"{f} {at}: the check timed out")
                elif code == 0:
                    unproven.append({"file": f, "at": at, "text": text})
        finally:
            c._git(p.root, "worktree", "remove", "--force", wt, timeout=60)
            c._git(p.root, "worktree", "prune", timeout=30)
    tested = len(shown) - len(skipped) - unreached
    proven = tested - len(unproven)
    left = len(hunks) - len(shown) + unreached
    summary = f"{proven}/{tested} hunks proven" + (f", {len(skipped)} not tested" if skipped else "") + (
        f", {left} more not run (--max)" if left else "")
    complete = not unproven and not skipped and not left and tested > 0  # review: only a full run is a pass
    detail = "; unproven: " + "; ".join(f"{u['file']} {u['at']}" for u in unproven) if unproven else ""
    quiet = getattr(args, "quiet", False)  # T-1067: at close the finish output carries it; no evidence line
    if not quiet:
        mutate(p, b.id, lambda x: x.add_evidence(f"fm task prove --hunks: {args.run}",
                                                 ("exit 0 · " if complete else "") + summary + detail,
                                                 step=args.step, ac=args.ac, tree=c.worktree_id(p.root), ran=True,
                                                 inconclusive=not complete),
               "prove", {"cmd": args.run[:200], "hunks": tested, "proven": proven})
    args.hunks_result = {"total": tested, "proven": proven, "unproven": unproven, "skipped": skipped, "not_run": left}
    if quiet:
        return 0 if complete else 1
    out(args, args.hunks_result,
        f"{b.id}: {summary}" + "".join(f"\n  unproven: {u['file']} {u['at']} — {u['text']}" for u in unproven)
        + "".join(f"\n  not tested: {x}" for x in skipped)
        + ("\n  Each unproven hunk can be removed without the check noticing: test it, or say why not." if unproven else ""))
    return 0 if complete else 1


def task_prove(p, args):
    """T-0059: run a test on the tree the task started from with only this task's test files brought over (it must
    fail there) and on the current tree (it must pass). Both runs are recorded, so red→green holds for FIX tasks."""
    import shutil
    import tempfile
    import fmmap
    b = need_brief(p, args.id)
    if args.hunks:
        return task_prove_hunks(p, b, args)
    if getattr(args, "vacuous", False):
        return task_prove_vacuous(p, b, args)
    if getattr(args, "same", None):
        return task_prove_same(p, b, args)
    if not args.run:
        raise UsageError("fm task prove ID --run CMD (or --hunks, --vacuous, --same CMD)")
    base = b.meta.get("base")
    if not base:
        raise UsageError(f"{b.id} has no start commit on record: prove needs the tree the task started from")
    tests = [f for f in fmmap.changed(p.root, base) if fmmap._TEST.search(f) and os.path.isfile(os.path.join(p.root, f))]
    if not tests:
        raise UsageError(f"{b.id} changed no test files since {base[:12]}: write the test that proves it first")
    with tempfile.TemporaryDirectory(prefix="fm-prove-") as t:
        wt = os.path.join(t, "base")
        c._git(p.root, "worktree", "add", "--detach", "-q", wt, base, timeout=120)
        if not os.path.isdir(wt):
            raise UsageError(f"git worktree add at {base[:12]} failed")
        try:
            for f in tests:
                os.makedirs(os.path.dirname(os.path.join(wt, f)), exist_ok=True)
                shutil.copy2(os.path.join(p.root, f), os.path.join(wt, f))
            red = c.run_command(wt, args.run, args.timeout)
        finally:
            c._git(p.root, "worktree", "remove", "--force", wt, timeout=60)
            c._git(p.root, "worktree", "prune", timeout=30)
    green = c.run_command(p.root, args.run, args.timeout)
    tree = c.worktree_id(p.root)

    def record(b):
        b.add_evidence(args.run, c.run_result(*red) + " (start tree + this task's tests)", step=args.step, ac=args.ac,
                       tree=tree, ran=True)
        b.add_evidence(args.run, c.run_result(*green), step=args.step, ac=args.ac, tree=tree, ran=True)
    mutate(p, b.id, record, "prove", {"cmd": args.run[:200], "red": red[0], "green": green[0], "tests": tests[:10]})
    proved = bool(red[0]) and not green[0]
    verdict = ("proved: fails without the change, passes with it" if proved else
               "not proved: it passes without the change too, so it doesn't test the fix" if not red[0] else
               "not proved: it fails on the current tree")
    out(args, {"proved": proved, "red": red[0], "green": green[0], "tests": tests},
        f"{b.id}: {verdict}\n  start tree + {len(tests)} test file(s): {c.run_result(*red)}\n  current tree: "
        f"{c.run_result(*green)}")
    return 0 if proved else 1


def _run_at(p, rev, cmd, timeout):
    """(exit, output) of cmd in a throwaway worktree of rev (a commit, or a tree such as a task's start snapshot)."""
    import tempfile
    guard_stored(p, c.active_brief(c.load_briefs(p), p.lane), cmd)  # T-0901 review: --vacuous runs stored verifies
    if c._git(p.root, "cat-file", "-t", rev, timeout=10).strip() == "tree":
        rev = c._git(p.root, "commit-tree", "--no-gpg-sign", rev, "-m", "fm scratch", timeout=60).strip()
    if not rev:
        raise UsageError("git couldn't make a scratch commit of the start tree")
    with tempfile.TemporaryDirectory(prefix="fm-at-") as t:
        wt = os.path.join(t, "wt")
        c._git(p.root, "worktree", "add", "--detach", "-q", wt, rev, timeout=120)
        if not os.path.isdir(wt):
            raise UsageError(f"git worktree add at {rev[:12]} failed")
        try:
            return c.run_command(wt, cmd, timeout)
        finally:
            c._git(p.root, "worktree", "remove", "--force", wt, timeout=60)
            c._git(p.root, "worktree", "prune", timeout=30)


def cmd_at(args):
    """T-0898: CMD run in a throwaway worktree of TARGET — a task id (its start snapshot, uncommitted work included) or
    a git revision — with its exit code; the working tree isn't touched."""
    import shlex
    p = resolve(args)
    words = args.words[1:] if args.words[:1] == ["--"] else args.words
    if not words:
        raise UsageError("fm at TARGET -- <command> (TARGET: a task id, or a commit, branch or tag)")
    if re.fullmatch(r"T-\d+", args.target):
        rev = c.task_base(p.root, need_brief(p, args.target))
        if not rev:
            raise UsageError(f"{args.target} has no start point on record (it was never focused)")
    else:
        rev = c._git(p.root, "rev-parse", "--verify", "-q", f"{args.target}^{{commit}}", timeout=10).strip()
        if not rev:
            raise UsageError(f"no commit named {args.target}")
    cmd = words[0] if len(words) == 1 else shlex.join(words)
    code, output = _run_at(p, rev, cmd, args.timeout)
    out(args, {"target": args.target, "rev": rev, "exit": code, "output": output},
        f"{'✗' if code else '✓'} at {args.target} ({rev[:12]}): {cmd} → {c.run_result(code, output)}")
    return code


def task_prove_vacuous(p, b, args):
    """T-0457: a criterion whose check also passes on the tree the task started from doesn't test this change."""
    base = c.task_base(p.root, b)
    if not base:
        raise UsageError(f"{b.id} has no start snapshot: --vacuous needs the tree the task started from")
    hollow = []
    for n, cmd in [(n, cmd) for n, cmd in b.verify_cmds() if cmd and not cmd.lstrip().startswith("typed:")]:
        code, _ = _run_at(p, base, cmd, args.timeout)
        if not code:
            hollow.append((n, cmd))
    mutate(p, b.id, lambda x: x.append_log("vacuous checks: " + (", ".join(f"ac {n}" for n, _ in hollow) or "none")),
           "prove_vacuous", {"hollow": [n for n, _ in hollow]})
    out(args, {"vacuous": [{"ac": n, "cmd": cmd} for n, cmd in hollow]},
        f"{b.id}: " + ("every criterion's check fails on the start tree: each tests the change" if not hollow else
                       "\n".join(f"criterion {n} passes on the start tree too, so it doesn't test this change: {cmd}"
                                 for n, cmd in hollow)))
    return 1 if hollow else 0


_VOLATILE = re.compile(r"\d+(?:\.\d+)?\s?(?:ms|s|sec|seconds|min)\b|0x[0-9a-f]+|\d{4}-\d\d-\d\dT[\d:.]+Z?")


def task_prove_same(p, b, args):
    """T-0501: CLEAN work keeps behaviour: CMD's exit and output (timings and addresses aside) before and after."""
    import difflib
    base = c.task_base(p.root, b)
    if not base:
        raise UsageError(f"{b.id} has no start snapshot: --same needs the tree the task started from")
    before = _run_at(p, base, args.same, args.timeout)
    after = c.run_command(p.root, args.same, args.timeout)
    norm = lambda r: (r[0], _VOLATILE.sub("#", r[1]).strip())  # noqa: E731
    same = norm(before) == norm(after)
    tree = c.worktree_id(p.root)

    def record(x):
        x.add_evidence(args.same, ("same exit and output before and after" if same else
                                   f"differs: exit {before[0]} → {after[0]}"), tree=tree, ran=True)
        if same:
            x.set_section("Behaviour lock", (x.section("Behaviour lock").rstrip() + "\n" if
                                             x.section("Behaviour lock").strip() else "")
                          + f"- behaviour lock: `{args.same}` gives the same exit and output before and after")
    mutate(p, b.id, record, "prove_same", {"cmd": args.same[:200], "same": same})
    diff = "" if same else "\n".join(list(difflib.unified_diff(norm(before)[1].splitlines(), norm(after)[1].splitlines(),
                                                               "before", "after", lineterm=""))[:40])
    out(args, {"same": same, "exit_before": before[0], "exit_after": after[0]},
        f"{b.id}: " + (f"behaviour lock holds: `{args.same}` is the same before and after" if same else
                       f"behaviour changed: `{args.same}` exit {before[0]} → {after[0]}\n{diff}"))
    return 0 if same else 1


def task_done_in(p, args):
    """A request that another task did as part of its work: closed as done there, linked both ways."""
    host = args.done_in.upper()
    if host == args.id.upper():
        raise UsageError("a task can't be done inside itself")
    with c.lock(p.dir):
        b, h = need_brief(p, args.id), need_brief(p, host)
        if b.status not in ("captured", "planned") or b.evidence():
            raise c.PolicyError(f"{b.id} was started ({b.status}, {len(b.evidence())} evidence line(s)): finish it "
                                f"through its own gates (fm task done) rather than --done-in")
        if h.status in ("captured", "dropped") or not h.evidence():
            raise c.PolicyError(f"{h.id} hasn't done any work yet ({h.status}, no evidence): --done-in points at the "
                                f"task that really did it")
        if b.meta.get("source") == "user" and not args.reason:
            raise c.PolicyError(f"{b.id} is the user's own request: give the reason (how {h.id} covered every part of "
                                f"it), or plan it as its own task")
        if b.meta.get("source") == "user":  # T-0364: the host's intent audit then checks the folded ask too
            ask = b.section("Raw request").strip() or f"> {b.title}"
            h.set_section("Raw request", h.section("Raw request").rstrip() + f"\n\nAlso asked ({b.id}, done here):\n{ask}")
        b.meta["status"], b.meta["done_in"] = "done", h.id
        b.append_log(f"done in {h.id}" + (f": {args.reason}" if args.reason else ""))
        h.append_log(f"includes {b.id}: {b.title}")
        c.save_brief(p, b)
        c.save_brief(p, h)
        c.log_event(p, "task_done_in", task=b.id, data={"host": h.id, "reason": args.reason or ""}, session=session())
        c.regen_views(p)
    out(args, c.brief_summary(b), f"{b.id} done in {h.id}.")


_DONE_WHEN = re.compile(r"(?m)^>?\s*DONE-WHEN:\s*(.+)$")


def _close_warnings(p, b, files):
    """T-0672: what a close doesn't refuse but the user should see: a likely secret in a file the task changed (T-0441;
    placeholder lines aside), and ignored files made since it began, outside its scope (T-0462: untracked ones are
    scope drift, refused already; ignored output — logs, builds, scratch — slips past that)."""
    try:  # review: the task is closed by now; a surprise here costs the warning, never the exit code
        return _close_warnings_of(p, b, files)
    except Exception as e:
        return [f"close-out warnings not computed ({type(e).__name__})"]


_CACHES = re.compile(r"(?:^|/)(?:__pycache__|\.pytest_cache|\.mypy_cache|node_modules|\.venv|venv|\.tox|\.cache|"
                     r"\.foreman|\.claude|state|local|backups)(?:/|$)")  # rewritten by every run: never "left behind"


def _close_warnings_of(p, b, files):
    import fmsecrets
    out = []
    for f in files[:200]:
        try:
            path = os.path.join(p.root, f)
            if os.path.getsize(path) > 1_000_000:
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        lines = text.split("\n")
        # review: a placeholder must be in the secret-looking token itself (AKIAXXXX…), not anywhere on the line
        out += [f"possible secret ({kind}) in {f}:{n}: move it to the environment or a secret store before committing"
                for n, kind in fmsecrets.scan_text(text, bool(fmsecrets.CONFIG.search(f)))
                if not any(fmsecrets.PLACEHOLDER.search(t) for t in re.findall(r"[\w+/=-]{16,}", lines[n - 1]))][:3]
    began = c.parse_ts(c.first_touch(p, b.id) or b.meta.get("created") or "")
    if b.meta.get("scope") and began and c.git_root(p.root):
        ignored = c._git(p.root, "ls-files", "--others", "--ignored", "--exclude-standard", "--directory") or ""
        since = began.timestamp() - 1
        new = []
        for x in ignored.splitlines()[:2000]:
            try:
                if x and not _CACHES.search(x) and os.path.getmtime(os.path.join(p.root, x)) >= since:
                    new.append(x)
            except OSError:
                continue
        stray = c.scope_drift(b, new)
        if stray:
            out.append(f"ignored files outside its scope [{', '.join(b.meta['scope'])}] left behind: "
                       + ", ".join(stray[:10]))
    drift = _tier_drift(p, b, files)  # T-0488
    bare = _not_verified(p, b, files)  # T-0474
    import fmsecond
    still = fmsecond.open_dissent(b)  # T-0642: an objection nobody answered is worth one line at the close
    dissent = (f"open dissent ({len(still)}): " + "; ".join(c.fit(t, 100) for _, t in still[:3])
               + f" — answer or note each: fm task dissent {b.id} resolve N \"<how>\"") if still else None
    honest = _honest(p, b)  # T-0661
    steers = [t[6:].strip() for e in c.ledger_tail(p, 3000) if e.get("event") == "note" and e.get("task") == b.id
              and (t := str((e.get("data") or {}).get("text") or "")).startswith("steer:")]
    standing = [x for x in steers if c.STANDING_STEER.search(x)]
    if standing:  # T-0601: a steer meant to last should outlive this task
        honest.append("Standing steer(s) on this task, rule candidates: " + "; ".join(f"\"{c.fit(x, 90)}\"" for x in
                      standing[:3]) + " — a 'no' is now a proposed veto (fm taste; adopted only on the user's yes), "
                      "anything else a line for the project's CLAUDE.md or memory, asked first")
    honest += [f"stale evidence: {path} changed after step {n}'s check last ran (`{c.fit(cmd, 60)}`): run it again"
               for n, path, cmd in _stale_evidence(p, b)[:3]]  # T-0634
    rates, said = catch_rates(p), []
    for _, cmd in b.verify_cmds():  # T-0653: has this check ever caught anything here?
        n, k = rates.get(cmd, (0, 0)) if cmd else (0, 0)
        if k:
            said.append(f"`{c.fit(cmd, 50)}` caught a failure in {k} task(s) here")
        elif n >= 3:
            said.append(f"`{c.fit(cmd, 50)}` never failed in {n} run(s) here (does it test the change?)")
    if said:
        honest.append("Check track record: " + "; ".join(said[:4]))
    debug, conflict = _scaffolding(p, b, files)
    if debug:
        honest.append(f"debug scaffolding in added lines: {', '.join(debug[:6])} — remove it, or say why it stays")
    if conflict:  # T-0956
        honest.append(f"conflict marker in added lines: {', '.join(conflict[:6])} — finish the merge")
    gone = _deleted(p, b)
    why = b.section("Origins")
    unexplained = [f for f in gone if f not in why]
    if unexplained:  # T-0600: a Chesterton check — say why a thing existed before it goes
        honest.append(f"deleted without saying why it existed: {', '.join(unexplained[:6])} — fm why <file>, then fm task "
                      f"set {b.id} --section Origins --text \"- <file>: <why it was there>\"")
    if b.tier == "L" and not b.section("Risks and rollback").strip():  # T-0626
        honest.append("an L task closed with no Risks and rollback section: what undoes it if it goes wrong?")
    if b.meta.get("replan"):  # T-0603: a surprise the plan never answered
        honest.append(f"closed with a replan never answered ({c.fit(b.meta['replan'], 100)}): fm task log {b.id} "
                      f"\"replan: <what changed, or why nothing had to>\"")
    return out + ([drift] if drift else []) + ([bare] if bare else []) + ([dissent] if dissent else []) + honest


_CLAIM = re.compile(r"^\s*(checked|inferred|unchecked)\s*:\s*(.+?)\s*(?:::\s*(.+))?$", re.I)


def parse_claims(raw):
    """T-0614: [(tag, claim, evidence or "")] from --claim values; a UsageError names a bad tag."""
    out = []
    for x in raw or []:
        m = _CLAIM.match(x)
        if not m:
            raise UsageError(f"--claim takes 'checked|inferred|unchecked: <claim> [:: <evidence>]', got {x!r}")
        out.append((m.group(1).lower(), c.redact(c.plain(m.group(2))), c.redact(c.plain(m.group(3) or ""))))
    return out


def _stale_evidence(p, b):
    """T-0634: [(step, path, cmd)]: a file a step's newest check names changed after that check ran."""
    newest = {}
    for line in b.evidence():
        m, t = c._EV_RE.match(line), c._TS_TAIL.search(line)
        if m and m.group(1) == "step" and t and c._RAN_MARK in line and line.count("`") >= 2:
            newest[int(m.group(2))] = (line.split("`", 2)[1], t.group(1))
    out = []
    for n, (cmd, ts) in sorted(newest.items()):
        at = c.parse_ts(ts)
        for tok in re.findall(r"[\w./-]+\.[A-Za-z0-9]{1,8}\b", cmd):
            path = os.path.join(p.root, tok)
            if at and os.path.isfile(path) and os.path.getmtime(path) > at.timestamp() + 1:
                out.append((n, tok, cmd))
    return out


def catch_rates(p):
    """T-0653: {command: (runs, tasks where it failed and later passed)} over this project's evidence."""
    runs, seq = collections.Counter(), collections.defaultdict(list)
    for e in c.ledger_tail(p, 50000):
        d = e.get("data") or {}
        if e.get("event") == "evidence" and d.get("cmd") and c.result_exit(d.get("result")) is not None:
            runs[d["cmd"]] += 1
            seq[(d["cmd"], e.get("task"))].append(c.result_exit(d["result"]) == 0)
        elif e.get("event") == "finish":  # T-0749: the close's own runs count too
            for cmd, code in d.get("ran") or []:
                runs[cmd] += 1
                seq[(cmd, e.get("task"))].append(not code)
        elif e.get("event") == "prove" and d.get("cmd") and "red" in d:  # T-0880: its start-tree run failed first
            runs[d["cmd"]] += 2
            seq[(d["cmd"], e.get("task"))] += [not d["red"], not d.get("green")]
    caught = collections.Counter(cmd for (cmd, _), ok in seq.items() if False in ok and ok[-1])
    return {cmd: (n, caught[cmd]) for cmd, n in runs.items()}


_EXPECT = re.compile(r"\(expect:\s*([^)]+)\)")
_FAILED_RUN = re.compile(r"^- \(step (\d+)\) `(.+?)` → ✗ exit")


def _step_checks(b, step, cmd, code, output, result):
    """T-0596, T-0632: (result with the step's expectation marked, how many times this exact command has now failed on
    the step when that's 3 or more, else None)."""
    s = next((x for x in b.steps() if x.n == step), None) if step else None
    m = _EXPECT.search(s.text) if s else None
    if m:
        want = m.group(1).strip()
        result += " · expect ✓" if want.lower() in (output or "").lower() else f" · expect missed: \"{c.fit(want, 60)}\""
    if not code or not step:
        return result, None
    same = 1 + sum(1 for line in b.evidence() if (r := _FAILED_RUN.match(line)) and int(r.group(1)) == step
                   and r.group(2) == cmd.replace("`", "'").strip())
    return result, same if same >= 3 else None


def _evidence_notes(b, step, result, tried):
    notes = []
    m = re.search(r"expect missed: \"(.*)\"$", result)
    if m:
        notes.append(f"step {step} expected \"{m.group(1)}\" in the output and it wasn't there: check before calling the "
                     f"step done")
    if tried:
        notes.append(f"this exact command has now failed {tried} times on step {step}: change something first (a "
                     f"hypothesis with its probe, fm task hypo {b.id} add …, or a smaller step)")
    return notes


def _tried(b):
    """T-0632: [(command, failures)] on the current step that failed twice or more."""
    cur = b.current_step()
    seen = collections.Counter(r.group(2) for line in b.evidence() if (r := _FAILED_RUN.match(line)) and cur
                               and int(r.group(1)) == cur.n)
    return cur.n if cur else None, [(x, n) for x, n in seen.most_common(4) if n >= 2]


def _last_green(b):
    """The newest command fm ran for this task that passed."""
    return next((r.group(1) for line in reversed(b.evidence()) if c._RAN_MARK in line
                 and (r := re.match(r"^- \((?:step|ac) \d+\) `(.+?)` → exit 0\b", line))), None)


_DEBUG = re.compile(r"\bbreakpoint\(\)|\bi?pdb\.set_trace\(|^\s*debugger\b\s*;?\s*(?:\/\/.*)?$|TODO[- ]?debug")
_DEBUG_PRINT = re.compile(r"^\s*(print|console\.\w+|logger?\.\w+)\(\s*f?[\"']DEBUG\b")  # matched on the raw line
_JS_LOG = re.compile(r"\bconsole\.(log|debug)\(")
_PROSE = (".md", ".markdown", ".rst", ".txt", ".adoc")
_QUOTED = re.compile(r"""(["'])(?:\\.|(?!\1).)*\1""")
_CONFLICT = re.compile(r"^(?:<{7}|>{7})(?: |$)|^={7}$")  # T-0956


def _scaffolding(p, b, files):
    """T-0650: added lines in the task's files that look like debug scaffolding, and (T-0956) merge conflict markers:
    ([file:line], [file:line])."""
    import subprocess
    base = b.meta.get("base")
    files = [f for f in files if not f.lower().endswith(_PROSE)]  # docs may name debug calls; only code runs them
    if not base or not files or not c.git_root(p.root):
        return [], []
    try:
        diff = subprocess.run(["git", "-C", p.root, "diff", "-U0", base, "--", *files[:200]], capture_output=True,
                              text=True, errors="replace", timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return [], []
    hits, conflicts, path, n = [], [], None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            n = int(m.group(1)) if m else 0
        elif line.startswith("+") and path:
            text = _QUOTED.sub("''", line[1:])  # T-0747: a string that names a debug call isn't one
            if _DEBUG.search(text) or _DEBUG_PRINT.search(line[1:]) or (path.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs")) and _JS_LOG.search(text)
                                       and "/test" not in path):
                hits.append(f"{path}:{n}")
            if _CONFLICT.match(line[1:]):
                conflicts.append(f"{path}:{n}")
            n += 1
    return hits, conflicts


def _preflight(p, b):
    """T-0633: before step 1 — scope paths that don't exist, uncommitted files outside the scope, and whether the gates
    already ran green on this exact tree (a baseline to compare against)."""
    notes = [f"{s} doesn't exist (fine if a step creates it)" for s in b.meta.get("scope") or []
             if not re.search(r"[*?\[]", s) and not os.path.exists(os.path.join(p.root, s))]
    if c.git_root(p.root):
        dirty = [x[3:] for x in c._git(p.root, "status", "--porcelain", fail="").splitlines() if x[3:]]
        stray = c.scope_drift(b, dirty) if b.meta.get("scope") else []
        notes += [f"{len(stray)} uncommitted file(s) outside the scope already: {', '.join(stray[:3])}"] if stray else []
    tree = c.worktree_id(p.root)
    green = any(e.get("event") == "check_run" and (e.get("data") or {}).get("tree") == tree
                and not any(r.get("exit") for r in (e.get("data") or {}).get("results") or [])
                for e in c.ledger_tail(p, 3000))
    notes.append("gates ran green on this tree (baseline cached)" if green else
                 "no fm check on this tree yet: fm check now gives a baseline to compare against")
    return "Preflight: " + "; ".join(notes)


def _forge_brief(p, b, args):
    """T-0652: a read-only brief asking a reviewer for the smallest change that keeps each check green while breaking
    its criterion — a forged pass means the check is too weak."""
    rows = [(a.n, c.strip_verify(a.text), cmd) for a, (_, cmd) in zip(b.acceptance(), b.verify_cmds())]
    body = [f"# Forge a pass: {b.id} \"{b.title}\" in {p.root} (read-only)", "",
            "For each criterion below, read its check and the code it exercises, then name the smallest change to the "
            "code that would keep the check passing while breaking the criterion: a forged pass. If you find one, the "
            "check is too weak: say what a stronger check would assert. If none exists, say why the check pins it.", ""]
    body += [f"## Criterion {n}: {text}\nCheck: `{cmd}`" if cmd else f"## Criterion {n}: {text}\nCheck: none (forge "
             f"trivially: anything passes)" for n, text, cmd in rows]
    body += ["", "Output per criterion: \"forged pass: <change> — stronger check: <assertion>\" or \"holds: <why>\"."]
    path = os.path.join(p.dir, "audits", f"{b.id}.forge.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c.write_atomic(path, "\n".join(body) + "\n")
    return out(args, {"brief": path}, f"Forge brief: {path}\nRun one foreman:fm-reviewer with the prompt \"Read {path} "
                                      f"and do what it asks.\"; a forged pass becomes a stronger check before the close.")


def _files_vs_steps(b, files):
    """T-0610: each changed file against the steps that name it (by path, file name or stem) and the scope."""
    if not files:
        return ""
    steps, scope = b.steps(), b.meta.get("scope") or []
    rows = []
    for f in files[:40]:
        name, stem = os.path.basename(f).lower(), os.path.splitext(os.path.basename(f))[0].lower()
        hit = [s.n for s in steps if any(k in s.text.lower() for k in (f.lower(), name)) or
               (len(stem) >= 4 and re.search(rf"\b{re.escape(stem)}\b", s.text.lower()))]
        out_of_scope = scope and c.scope_drift(b, [f])
        rows.append(f"- {f} — " + (f"step {', '.join(map(str, hit))}" if hit else "no step names it")
                    + (" (outside the scope)" if out_of_scope else ""))
    return ("\n\n## Files vs steps\n" + "\n".join(rows) + "\nFor each hunk, say which step it serves; a hunk that "
            "serves none is a finding (scope creep, or a step the plan is missing).")


def _deleted(p, b):
    """Files tracked at the task's start that are gone now (committed or not)."""
    import subprocess
    base = b.meta.get("base")
    if not base or not c.git_root(p.root):
        return []
    try:
        r = subprocess.run(["git", "-C", p.root, "diff", "--name-only", "--diff-filter=D", base], capture_output=True,
                           text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return []
    return [x for x in r.stdout.splitlines() if x.strip()]


def _plan_gaps(p, b):
    """T-0645: the steps this plan didn't foresee — added after work started — and the steps whose first run failed,
    from the ledger, as the brief's Plan gaps lines ("" when the plan held)."""
    started, late, failed = False, [], {}
    for e in c.ledger_tail(p, 20000):
        if e.get("task") != b.id:
            continue
        d = e.get("data") or {}
        started = started or e.get("event") == "focus"
        if started and e.get("event") == "step_add" and d.get("text"):
            late.append(c.fit(c.plain(str(d["text"])), 120))
        elif e.get("event") == "evidence" and d.get("step") and d["step"] not in failed:
            failed[d["step"]] = bool(c.result_exit(d.get("result")))  # a typed result is no failure
    steps = {s.n: s.text for s in b.steps()}
    lines = [f"- added late: {t}" for t in late] + [f"- failed first: step {n} {c.fit(steps[n], 100)}"
                                                    for n, bad in sorted(failed.items()) if bad and n in steps]
    return "\n".join(lines[:12]) + "\n" if lines else ""


_CONTRACT = re.compile(r"\((produces|requires):\s*([^)]+)\)")


def step_contracts(p, b):
    """T-0666: steps may name what they produce and require, "(produces: PATH, …)" / "(requires: PATH, …)". An undone
    step whose products already exist may not be needed; a requirement that neither exists nor comes from an earlier
    step has no source. Hints only."""
    made, notes = set(), []
    for s in b.steps():
        for kind, paths in _CONTRACT.findall(s.text):
            for path in (x.strip() for x in paths.split(",") if x.strip()):
                there = os.path.exists(os.path.join(p.root, path))
                if kind == "produces" and not s.done and there:
                    notes.append(f"step {s.n} produces {path}, which already exists: is the step still needed?")
                if kind == "requires" and not there and path not in made:
                    notes.append(f"step {s.n} requires {path}: it doesn't exist and no earlier step produces it")
                if kind == "produces":
                    made.add(path)
    return ("Step contracts: " + "; ".join(notes[:4])) if notes else ""


_HARD = re.compile(r"(?i)\b(deploy|release|publish|push|migrat(?:e|ion)|delete|drop|merge|send)(?:s|es|d|ed|ing)?\b")
_UNKNOWN = re.compile(r"(?i)\b(spike|probe|prototype|investigate|measure|find out|unknown)\w*")


def step_order(b):
    """T-0623: a step that explores an unknown placed after one that's hard to undo (a fixed vocabulary; a hint)."""
    steps = b.steps()
    for i, s in enumerate(steps):
        if _HARD.search(s.text):
            late = next((t for t in steps[i + 1:] if _UNKNOWN.search(t.text) and not _HARD.search(t.text)), None)
            if late:
                return (f"Step order: step {late.n} ({c.fit(late.text, 50)}) explores an unknown after step {s.n} "
                        f"({c.fit(s.text, 50)}) does something hard to undo — unknowns first, then reversible, then "
                        f"irreversible (planning.md R2).")
    return ""


def _honest(p, b):
    """T-0661: hindsight rewriting (criteria text or checks edited after work started) and suspiciously smooth results
    (an M/L task other than a FIX whose every recorded run passed first time); logged as closeout_flags."""
    log = b.section("Log").splitlines()
    start = next((i for i, x in enumerate(log) if re.match(r"- \S+ focused\b", x)), None)
    edits = [re.sub(r"^- \S+ ", "", x) for x in log[start:]] if start is not None else []
    edits = [x for x in edits if re.match(r"criterion \d+ (text|verify):", x)]
    runs = [x for x in b.evidence() if c._RAN_MARK in x]
    smooth = b.tier in ("M", "L") and b.type != "FIX" and runs and not any("✗" in x for x in runs)
    out = ([f"criteria edited after work started (re-check they weren't loosened to fit the result): "
            + "; ".join(c.fit(x, 140) for x in edits[:3])] if edits else []) + (
        [f"suspiciously smooth: all {len(runs)} recorded run(s) passed the first time; was a test seen failing "
         f"before the change?"] if smooth else [])
    if out:
        c.log_event(p, "closeout_flags", task=b.id, data={"kinds": (["criteria_edited"] if edits else [])
                                                          + (["smooth"] if smooth else [])})
    return out


def _not_verified(p, b, files):
    """T-0474: changed source files no linked test (by name, fmmap) changed or ran in this task's evidence."""
    import fmmap
    try:
        m = fmmap.load(p)
    except Exception:  # the map is a hint: no map, no warning
        return None
    import fnmatch
    ran = " ".join(b.evidence())
    meta = c.read_meta(p)
    passed = {l.split("`", 2)[1] for l in b.evidence() if c._RAN_MARK in l and "` → exit 0" in l}
    gates = [(meta.get("check_paths") or {}).get(g) or ["*"] for g in meta.get("checks") or [] if g in passed]
    bare = [f for f in files if c.CODE.search(f) and not fmmap._TEST.search(f)  # T-0736: a passing gate covers its paths
            and not any(fnmatch.fnmatch(f, g) for globs in gates for g in globs)
            and not any(t in files or t in ran for t in fmmap.tests_for(m, [f]))]
    return (f"not verified: {', '.join(bare[:8])}{' …' if len(bare) > 8 else ''} — no linked test changed or ran "
            f"(fm task prove {b.id} --hunks names the hunks no check notices)") if bare else None


def _tier_drift(p, b, files):
    """T-0488: the diff's size against the planned tier (S: a few files and lines; M: up to a large batch), so the
    next plan of this kind is sized from what it really took."""
    base = c.task_base(p.root, b) if files and c.git_root(p.root) else None
    if not base:
        return None
    lines, seen = 0, set()
    for row in (c._git(p.root, "diff", "--numstat", base, "--", *files[:500], timeout=30) or "").splitlines():
        add, rem, name = (row.split("\t") + ["", "", ""])[:3]
        seen.add(name)
        lines += (int(add) if add.isdigit() else 0) + (int(rem) if rem.isdigit() else 0)
    at_base = set((c._git(p.root, "ls-tree", "-r", "--name-only", base, "--", *files[:500], timeout=30)
                   or "").splitlines())
    for f in files[:500]:  # new files: every line is added (one at the start and not in the diff is unchanged: T-0812)
        if f not in seen and f not in at_base:
            try:
                with open(os.path.join(p.root, f), "rb") as fh:
                    lines += fh.read(2_000_000).count(b"\n")
            except OSError:
                pass
    size = "L" if len(files) > 20 or lines > 1500 else "M" if len(files) > 3 or lines > 150 else "S"
    if "SML".index(size) > "SML".index(b.tier):
        return (f"{b.id} was planned {b.tier}, but its diff is {size}-sized ({len(files)} files, {lines} lines): "
                f"plan this kind of change as {size} next time")
    return None


def cmd_batch(args):
    """T-0257: several requests not started yet worked as one host task — one plan read, one gate run, one review,
    one commit — with every member's criteria and a step each; the members leave the inbox and queue while batched and
    are closed done-in the host when it is done (handed back if it is dropped)."""
    p = resolve(args)
    c.hint_used(p, "batch")  # T-0250
    if args.suggest:  # T-0670: every related group in the inbox and queue, made into batches with --apply
        groups = c.related_groups(c.load_briefs(p))
        if not args.apply:
            return out(args, {"groups": [[x.id for x in g] for g in groups]}, "\n".join(
                f"fm batch {' '.join(x.id for x in g)}  # {c.fit(g[0].title, 60)}" for g in groups)
                or "nothing related enough to batch")
        made = [_make_batch(p, [x.id for x in g], None) for g in groups]
        return out(args, {"batches": [dict(c.brief_summary(h), members=m) for h, m in made]}, "\n".join(
            f"{h.id} [{h.type} {h.tier}] {c.fit(h.title, 70)} — batch of {', '.join(m)}" for h, m in made)
            or "nothing related enough to batch")
    if args.apply:
        raise UsageError("--apply goes with --suggest")
    h, ids = _make_batch(p, args.ids, args.title)
    out(args, dict(c.brief_summary(h), members=ids),
        f"{h.id} [{h.type} {h.tier}] {h.title} — batch of {', '.join(ids)} (plan its verify commands, then fm focus "
        f"{h.id}; each member closes done in {h.id})")


def _make_batch(p, ids, title):
    ids = list(dict.fromkeys(x.upper() for x in ids))
    if len(ids) < 2:
        raise UsageError("a batch is two or more items")
    with c.lock(p.dir):
        members = [need_brief(p, i) for i in ids]
        everything = c.load_briefs(p)
        act, by_id = c.active_brief(everything, p.lane), {x.id: x for x in everything}
        waits = lambda b: b.meta.get("explore") or b.meta.get("confirm") and c.needs_approval(b, "full")  # T-0289
        bad = [f"{b.id} ({'waits for the user: confirm it first' if waits(b) else b.status})" for b in members
               if b.status not in ("captured", "planned") or b.evidence() or (act and act.id == b.id)
               or c.batched(b, by_id) or b.meta.get("batch") or waits(b)]
        if bad:
            raise UsageError("only items not started, not batched and not waiting on the user can be batched: "
                             + ", ".join(bad))
        types = [b.type for b in members]
        type_ = max(sorted(set(types)), key=types.count)
        tiers = {b.tier for b in members}
        tier = "L" if "L" in tiers else "M" if "M" in tiers or len(members) > 2 else "S"
        title = title or "Batch: " + "; ".join(c.fit(b.title, 40) for b in members)
        raw = "\n".join(f"{b.id}: " + re.sub(r"(?m)^> ?", "", b.section("Raw request")).strip() for b in members)
        source = "user" if any(b.meta.get("source") == "user" for b in members) else members[0].meta.get("source", "user")
        h = _create(p, c.fit(title, 120), type_, tier, "planned", raw=raw, source=source,
                    priority="urgent" if any(b.priority == "urgent" for b in members) else "normal",
                    scope=sorted({s for b in members for s in b.meta.get("scope") or []}),
                    depends=sorted({d for b in members for d in b.meta.get("depends_on") or []} - set(ids)))
        h.set_section("Interpretation", f"Do {', '.join(ids)} as one batch: one plan read, one gate run, one review and "
                                        f"one commit; each keeps its own criteria and is closed done in {h.id}. Write "
                                        "the failing tests for every member first, together. Per step, run only that "
                                        "step's own new tests (fast, -k); the full gates, replays and the review run "
                                        "once, at close (T-0670).")
        for b in members:
            crit = [(c._VERIFY_OF.sub("", a.text).strip(), c.verify_of(a.text)) for a in b.acceptance()] or \
                [(x.strip(), None) for x in _DONE_WHEN.findall(b.section("Raw request"))] or [(f"{b.title} works", None)]
            for text, verify in crit:
                h.add_ac(f"{b.id}: {text}", verify)
            for s in b.steps() or [None]:  # a planned member's own steps, else one step for it
                h.add_step(f"{b.id}: {s.text if s else b.title}")
        h.meta["batch"] = ids
        c.save_brief(p, h)
        for b in members:
            b.meta["batched_in"] = h.id
            b.append_log(f"batched into {h.id}")
            c.save_brief(p, b)
        c.log_event(p, "batch", task=h.id, data={"members": ids}, session=session())
        c.regen_views(p)
    return h, ids


def _settle_batch(p, h, done):
    """A batch host finished: its members are done in it; dropped: they go back to the inbox or queue."""
    with c.lock(p.dir):
        for mid in h.meta.get("batch") or []:
            b = c.find_brief(p, mid)
            if not b or b.status == "done" or b.meta.get("batched_in") != h.id:
                continue
            b.meta.pop("batched_in", None)
            if done:
                b.meta["status"], b.meta["done_in"] = "done", h.id
                b.append_log(f"done in {h.id} (batch)")
                c.log_event(p, "task_done_in", task=b.id, data={"host": h.id, "reason": "batch"}, session=session())
            else:
                b.append_log(f"unbatched: {h.id} was dropped")
            c.save_brief(p, b)
        c.regen_views(p)


def task_new(p, args):
    type_ = c.WORK_TAGS.get(args.type.upper(), args.type.upper())
    if type_ not in c.TYPES:
        raise UsageError(f"unknown type {args.type!r}; one of {', '.join(c.TYPES)}")
    if args.tier not in ("S", "M", "L"):
        raise UsageError("tier must be S, M or L")
    reused = ""
    if not args.from_id and not getattr(args, "redo", None):  # T-0848: the capture this request already is
        key = " ".join(c.plain(args.title).lower().split())
        same = next((x for x in c.load_briefs(p) if x.status == "captured" and " ".join(x.title.lower().split()) == key),
                    None)
        if same:
            args.from_id, reused = same.id, f" (from inbox capture {same.id}: same title)"
    _refuse_unrunnable(p, [t.rpartition(" :: ")[2] for t in args.ac or [] if " :: " in t])
    redo = need_brief(p, args.redo) if getattr(args, "redo", None) else None
    if redo and redo.status != "dropped":
        raise UsageError(f"--redo takes a dropped task; {redo.id} is {redo.status}")
    with c.lock(p.dir):
        if args.from_id:
            b = need_brief(p, args.from_id)
            if b.status != "captured":
                raise UsageError(f"{b.id} is {b.status}, not captured")
            b.meta.update(type=type_, tier=args.tier, status="planned")
            if args.scope:
                b.meta["scope"] = args.scope
            if args.depends:
                b.meta["depends_on"] = args.depends
            b.preamble = f"# {c.plain(args.title).strip() or 'untitled'}\n"
            b.append_log("planned from capture")
            c.save_brief(p, b)
        else:
            b = _create(p, args.title, type_, args.tier, "planned", raw=args.raw, scope=args.scope or (),
                        depends=args.depends or (), source=args.source)
        if redo:  # T-0767: its diff starts where the dropped task's did, and the files it edited are this task's
            b.meta.update({k: redo.meta[k] for k in ("base", "base_tree") if redo.meta.get(k)})
            b.append_log(f"redo of {redo.id}: takes over its start point and edited files")
            c.save_brief(p, b)
            for rel, at in c.task_touches(p, redo.id).items():
                c.log_event(p, "touched", task=b.id, data={"file": os.path.join(p.root, rel), "tool": "redo", "at": at},
                            session=session())
        c.log_event(p, "task_new", task=b.id, data={"type": type_, "tier": args.tier, "from": args.from_id},
                    session=session())
        c.regen_views(p)
    if args.ac or args.step or args.interpretation or args.approach:
        def plan(b):
            for name, text in (("Interpretation", args.interpretation), ("Approach", args.approach)):
                if text:  # an M/L brief plans in one call (T-0083)
                    b.set_section(name, c.redact(text))
            for text in args.ac or []:  # "criterion :: verify command" (T-0042)
                done_when, sep, verify = text.rpartition(" :: ")
                b.add_ac(done_when, verify.strip()) if sep else b.add_ac(text)
            for text in args.step or []:
                b.add_step(text)
        b, _ = mutate(p, b.id, plan, "task_plan", {"ac": len(args.ac or []), "step": len(args.step or [])})
        _lint_verify(p, [t.rpartition(" :: ")[2] for t in args.ac or [] if " :: " in t])
    if not args.from_id:
        _note_escapes(p, b, " ".join(filter(None, [args.title, args.raw])))
    out(args, c.brief_summary(b), f"{b.id} [{b.type} {b.tier}] {b.title} — planned ({b.path}){reused}"
        + ("" if args.from_id else _covered_note(p, b.id, " ".join(filter(None, [args.title, args.raw])))))
    if args.focus:
        cmd_focus(argparse.Namespace(id=b.id, project=getattr(args, "project", None), json=False))


def _section_pairs(args):
    """T-1124: [(section, text)] in the order given: each --section takes its own --text (or the one --file)."""
    secs, texts = args.section or [], list(args.text or [])
    if isinstance(secs, str):  # a caller building its own Namespace
        secs, texts = [secs], [texts] if isinstance(texts, str) else texts
    if args.file and len(secs) == 1 and not texts:
        with open(args.file, encoding="utf-8") as f:
            texts = [f.read()]
    if len(texts) != len(secs):
        raise UsageError(f"each --section needs its own --text: {len(secs)} section(s), {len(texts)} text(s)")
    return list(zip(secs, texts))


def task_set(p, args):
    import fmguard
    for cat in args.allow or []:
        if cat in fmguard.USER_ONLY:
            raise c.PolicyError(f"{cat} can't be granted from the command line (whoever runs it); request it with "
                                f"`fm ask ID {cat} --why \"…\"` and the user's yes grants it")
        if cat not in fmguard.CATEGORIES or cat in fmguard.NOT_AUTHORIZABLE:
            raise UsageError(f"can't allow {cat!r}; authorizable: " + ", ".join(
                x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE | fmguard.USER_ONLY))
    changes = {}
    for kv in args.assignments:
        if "=" not in kv:
            raise UsageError(f"expected key=value, got {kv!r}")
        k, v = kv.split("=", 1)
        if k not in EDITABLE:
            raise UsageError(f"can't set {k!r}; editable: {', '.join(sorted(EDITABLE))} (authorizations via --allow)")
        if v == "" and k in CLEARABLE:  # T-1126: an empty value clears an optional field
            if k.startswith("predict_") and need_brief(p, args.id).meta.get("plan0_at"):
                raise UsageError(f"{k} is fixed once work has started (fm focus); the close scores it as planned")
            changes[k] = None
            continue
        if k == "status" and v not in SETTABLE_STATUS:
            raise UsageError(f"status {v!r} not settable here (use fm task done/drop, or one of {sorted(SETTABLE_STATUS)})")
        if k == "type":
            v = c.WORK_TAGS.get(v.upper(), v.upper())
            if v not in c.TYPES:
                raise UsageError(f"unknown type {v!r}")
        if k == "tier" and v not in ("S", "M", "L"):
            raise UsageError("tier must be S, M or L")
        if k == "approved" and v == "true":  # T-0490: an L feature names what it builds on before it's approved
            b = need_brief(p, args.id)
            if b.type == "FEATURE" and b.tier == "L" and not b.section("Build vs reuse").strip() and \
                    not any(sec == "Build vs reuse" and txt.strip() for sec, txt in _section_pairs(args)):
                raise UsageError(f"{b.id} is a FEATURE L: before it's approved, say what it builds on — fm task set "
                                 f"{b.id} --section \"Build vs reuse\" --text \"<the fm command, module or library it "
                                 f"reuses, or why nothing fits (fm recall, fm map)>\"")
        if k == "confidence" and not (v.isdecimal() and 0 <= int(v) <= 100):  # T-0619
            raise UsageError("confidence is a whole percent, 0-100: how likely the task holds on its first finish")
        if k == "cost_cap":  # T-1083: tokens, like fm cost; stored as the count
            import fmcost
            if (n := fmcost.parse_tokens(v)) is None:
                raise UsageError("cost_cap is input-equivalent tokens, fm cost's unit: 200k, 2M or 150000 "
                                 "(empty or 0 removes it)")
            if n == 0:
                changes[k] = None
                continue
            v = str(n)
        if k in ("predict_minutes", "predict_attempts"):  # T-1061: a guess made before the work, never moved after
            cap = 10080 if k == "predict_minutes" else 20
            if not (v.isdecimal() and 0 < int(v) <= cap):
                raise UsageError(f"{k} is a whole number from 1 to {cap}: the plan's guess, compared at the close")
            if need_brief(p, args.id).meta.get("plan0_at"):
                raise UsageError(f"{k} is fixed once work has started (fm focus); the close scores it as planned")
        if k == "priority" and v not in ("normal", "urgent"):
            raise UsageError("priority must be normal or urgent")
        changes[k] = _list_value(v) if k in LIST_FIELDS else (v == "true" if k in ("explore", "approved") else v)
    pairs = _section_pairs(args)

    def apply(b):
        if changes.get("status") in ("active", "verifying") and b.status not in ("active", "verifying"):
            raise c.PolicyError(f"{b.id}: start a task with fm focus {b.id}, which keeps one active task per checkout "
                                f"(T-0134 review)")
        tiers = "SML"
        if "tier" in changes and changes["tier"] in tiers and b.tier in tiers and \
                tiers.index(changes["tier"]) < tiers.index(b.tier) and b.evidence():
            raise c.PolicyError(f"{b.id}: tier can't be lowered ({b.tier} → {changes['tier']}) once work has "
                                f"evidence; it sets which audits are required")
        for k, v in changes.items():
            if k == "title":
                b.preamble = f"# {c.plain(v)}\n"
            elif v is None:
                b.meta.pop(k, None)
            else:
                if k == "cost_cap" and b.meta.get(k) and str(b.meta[k]) != v:  # T-1083 review: a raise is on record
                    b.append_log(f"cost_cap {b.meta[k]} → {v}")
                    c.log_event(p, "cost_cap_changed", task=b.id, data={"from": int(b.meta[k]), "to": int(v)})
                b.meta[k] = v
        for cat in args.allow or []:
            allow = list(b.meta.get("allow") or [])
            if cat not in allow:
                allow.append(cat)
            b.meta["allow"] = allow
            b.append_log(f"guard authorization added: {cat}")
        for sec, raw in pairs:
            text = c.redact(raw)
            b.set_section(sec, b.keep_ticks(text) if sec == "Acceptance criteria" else text)
        if changes:
            b.append_log("set " + ", ".join(f"{k}={v}" for k, v in changes.items()))
    b, _ = mutate(p, args.id, apply, "task_set", {"changes": changes, "allow": args.allow or [],
                                                  "section": [sec for sec, _ in pairs] or None})
    out(args, c.brief_summary(b), f"{b.id} updated.")


def _list_value(v):
    """T-0810: a,b or [a, b] or ["a","b"]: the items, without one pair of brackets or the quotes around each."""
    v = v.strip()
    v = v[1:-1] if v.startswith("[") and v.endswith("]") else v
    return [x.strip().strip("'\"").strip() for x in v.split(",") if x.strip().strip("'\"").strip()]


def task_step(p, args):
    if args.action == "add":
        b, n = mutate(p, args.id, lambda b: b.add_step(args.arg), "step_add", {"text": args.arg})
        return out(args, c.brief_summary(b), f"{b.id}: added step {n}.")
    try:
        n = int(args.arg)
    except ValueError:
        raise UsageError(f"step number expected, got {args.arg!r}")
    if args.action == "current":
        b, _ = mutate(p, args.id, lambda b: b.set_current(n), "step_current", {"step": n})
        return out(args, c.brief_summary(b), f"{b.id}: current step {n}.")
    ev = args.evidence

    def done(b):
        if ev:
            b.add_evidence(ev[0], ev[1], step=n)
        b.mark_step(n)
    b, _ = mutate(p, args.id, done, "step_done", {"step": n, "evidence": ev})
    s = c.brief_summary(b)
    nxt = f" Next: step {s['step']['n']}/{s['step']['of']} {s['step']['text']}" if s["step"] else " All steps done."
    out(args, s, f"{b.id}: step {n} done.{nxt}")


def task_ac(p, args):
    if args.action == "add":
        text, sep, verify = args.arg.rpartition(" :: ")  # "criterion :: verify cmd", as with task new --ac
        text, verify = (text, verify.strip()) if sep and not args.verify else (args.arg, args.verify)
        _refuse_unrunnable(p, [verify])
        b, _ = mutate(p, args.id, lambda b: b.add_ac(text, verify), "ac_add", {"text": text})
        _lint_verify(p, [verify])
        return out(args, c.brief_summary(b), f"{b.id}: criterion added.")
    try:
        n = int(args.arg)
    except ValueError:
        raise UsageError(f"criterion number expected, got {args.arg!r}")
    if args.action == "edit":
        if args.verify is None and not args.text:
            raise UsageError("fm task ac ID edit N needs --verify CMD and/or --text TEXT")
        _refuse_unrunnable(p, [args.verify])
        try:
            b, _ = mutate(p, args.id, lambda b: b.edit_ac(n, args.text, args.verify), "ac_edit", {"ac": n})
        except KeyError as e:
            raise UsageError(str(e).strip("'\""))
        _lint_verify(p, [args.verify])
        return out(args, c.brief_summary(b), f"{b.id}: criterion {n} edited.")
    ev = args.evidence

    def check(b):
        if ev:
            b.add_evidence(ev[0], ev[1], ac=n)
        b.check_ac(n)
    b, _ = mutate(p, args.id, check, "ac_check", {"ac": n})
    out(args, c.brief_summary(b), f"{b.id}: criterion {n} checked.")


def cmd_focus(args):
    p = resolve(args)
    warn = None
    with c.lock(p.dir):
        target = need_brief(p, args.id)
        if target.status in c.CLOSED:
            raise UsageError(f"{target.id} is {target.status}")
        gaps = [] if target.status in ("active", "verifying") else \
            c.plan_gaps(target, c.effective_autonomy(p))
        if gaps:
            raise c.PolicyError(f"{target.id} isn't planned enough to start: missing {', '.join(gaps)} "
                                f"(fm task set/ac/step, or /foreman:intake; fm next says what's next)")
        if c.held_elsewhere(target, p.lane):  # T-0134: one checkout works a task at a time
            where = target.meta.get("lane") or "the main checkout"
            raise c.PolicyError(f"{target.id} is held by {'lane ' if target.meta.get('lane') else ''}{where}: work on it "
                                f"there (fm lane list), or fm lane rm it first")
        if target.meta.get("lane") != p.lane:  # moving between checkouts: its start point is taken here, afresh
            for k in ("base", "base_tree", "paused_tree"):
                target.meta.pop(k, None)
        if p.lane:  # T-0234 review: the branch it was bound on is the one fm lane rm may delete later
            target.meta.update(lane=p.lane, lane_branch=(c._git(p.lane, "branch", "--show-current", fail=None,
                                                                 timeout=10) or "").strip() or None)
        else:
            target.meta.pop("lane", None)
        for b in c.load_briefs(p):
            if b.status in ("active", "verifying") and b.id != target.id and b.meta.get("lane") == p.lane:
                c.pause_snapshot(p.root, b)  # T-0136
                b.meta["status"] = "planned"
                b.append_log(f"paused: focus moved to {target.id}")
                c.save_brief(p, b)
        resumed = target.status not in ("active", "verifying")  # set active by hand: its pause point is stale (review)
        target.meta["status"] = "active"
        first_focus = not target.meta.get("base")
        if not target.meta.get("base") and (head := c.git_head(p.root)):
            target.meta["base"] = head  # where the task's diff starts (fm audit prep)
        paused = target.meta.pop("paused_tree", None)
        if resumed and paused and target.meta.get("base_tree") and (now := c.worktree_tree(p.root)) and now != paused:
            moved = c.rebase_snapshot(p.root, target.meta["base_tree"], paused, now)  # T-0136
            if moved:
                target.meta["base_tree"] = moved
                target.append_log("re-based: what other work changed while it was paused isn't its own change")
            else:
                target.append_log("its pause snapshot is gone (git pruned it): its diff may include work done meanwhile"
                                  if moved is False else
                                  "other work changed the same lines while it was paused: its diff still includes that work")
        if not target.meta.get("base_tree") and c.git_root(p.root):
            snap = c.worktree_tree(p.root)  # T-0078: its own changes are measured from the files as they are now
            if snap:
                target.meta["base_tree"] = snap
            else:
                target.append_log("snapshot of the working files failed (git add): its diff starts at the start commit")
        import fmeco
        mach = fmeco.machine()  # T-0574: a named machine shows in the log fm sync carries: which machine ran what
        target.append_log("focused" + (f" on {mach['name']}" if mach["named"] else ""))
        related = ""
        if not target.section("Related").strip():  # recall at planning time, kept for fresh sessions (T-0043)
            import fmrecall
            hits = fmrecall.recall(p, fmrecall.brief_query(target), skip=target.id)
            related = fmrecall.render(hits, target.tier)
            fmrecall.log_shown(p, hits, target.id)  # T-0617
            if target.meta.get("scope") and c.git_root(p.root):  # the tests that go with the scope (T-0044)
                import fmmap
                try:
                    tests = fmmap.tests_for(fmmap.load(p), target.meta["scope"])
                except Exception:  # the map is a hint: it never stops a focus
                    tests = []
                if tests:
                    related = (related or "Related (data):") + "\n- likely tests for the scope: " + c.fit(
                        ", ".join(tests), 200)
            if related:
                target.set_section("Related", related)
        moved = _moved_since_planned(p, target)
        if moved:  # R2/R3 preflight: the plan was grounded on files that have changed since (kept for fresh sessions)
            related = (related + "\n" if related else "") + moved
            target.set_section("Preflight", moved + "\n")
        if not target.meta.get("plan0_at"):  # T-1061: the plan at first focus, which the close is scored against
            target.meta.update(plan0_at=c.now(), plan0_scope=list(target.meta.get("scope") or []))
        c.save_brief(p, target)
        other = c.read_meta(p).get("session") or {}
        age = c.age_days(other.get("seen"))
        import fmbus
        if other.get("id") and session() and other["id"] != session() and age is not None and age < 10 / 1440 \
                and not (other.get("pid") and other["pid"] == fmbus.claude_pid()):  # T-0841: a resume is no other
            warn = f"note: another Claude Code session ({other['id'][:8]}) was active in this project within 10 minutes"
        c.log_event(p, "focus", task=target.id, session=session())
        c.regen_views(p)
    if warn:
        print(warn, file=sys.stderr)
    stale = c.stale_refs(p, target) if resumed and target.meta.get("base") else []  # T-0113: picked up again
    import fmoutcomes
    try:
        record = "\n".join(filter(None, [fmoutcomes.track_line(p, target.type, target.tier),  # T-0641
                                          fmoutcomes.caution(p, target.meta.get("scope") or []),  # T-0620
                                          step_order(target), step_contracts(p, target),  # T-0623, T-0666
                                          _preflight(p, target) if first_focus else "",  # T-0633
                                          __import__("fmcost").cost_line(p, target)]))  # T-1083
    except Exception:  # a report: it never stops a focus
        record = ""
    out(args, c.brief_summary(target), f"Focus: {target.id} [{target.type} {target.tier}] {target.title}"
        + (f"\nStale since it started (gone from the repo now): {', '.join(stale)} — re-check the brief." if stale else "")
        + (f"\n{related}" if related else "") + (f"\n{record}" if record else "")
        + f"\nDone needs: {', '.join(g for g, _ in gates(target.type, target.tier))} (fm gates)")


def cmd_quiet(args):
    """R3: a noisy command's output costs context on every run; show one line when it passes, the tail when not."""
    import time
    words = args.words[1:] if args.words[:1] == ["--"] else args.words
    if not words:
        raise UsageError("fm quiet -- <command>")
    t0 = time.monotonic()
    import shlex  # one word is a shell string ("pytest | tail"); several are argv, quoted as given
    code, output = c.run_command(os.getcwd(), words[0] if len(words) == 1 else shlex.join(words), args.timeout)
    secs = time.monotonic() - t0
    lines = [l for l in output.rstrip().splitlines() if l.strip()]
    if code:
        timed = f"{lines[-1]}; " if code == 124 and lines and lines[-1].startswith("timed out after") else ""
        print("\n".join(lines[-args.tail:]) + f"\n✗ exit {code} ({timed}{secs:.1f} s; last {min(len(lines), args.tail)} "
                                                 f"of {len(lines)} lines)")
    else:
        print(f"✓ exit 0 ({secs:.1f} s) · {lines[-1][:200] if lines else '(no output)'}")
    return code


def gates(type_, tier):
    """What fm task done checks for this type and tier: [(short, how)]."""
    audits = " + ".join(" or ".join(sorted(g)) for g in c.REQUIRED_AUDITS[tier])
    need = [("evidence", "every step and criterion has a check fm ran (--run) or a typed one for what can't run here"),
            ("audits", f"{audits}, recorded after the last change (fm audit prep ID); adversary as well when the "
                       f"change touches auth, crypto, secrets, exec or deserialization")]
    if tier in ("M", "L"):
        need += [("docs impact", "--section \"Docs impact\" (updated docs, or none: why)"),
                 ("lesson", "fm task done ID --lesson \"…\"")]
    need += {"FIX": [("red→green", "fm task prove ID --run \"<test>\" (or --section \"Regression test\" none: why)")],
             "PERFORMANCE": [("numbers", "--section \"Measurements\": <metric> before → after")],
             "CLEAN": [("behaviour lock", "tests run (fm check --evidence ID --step 1) before the first edit")]
             }.get(type_, [])
    need.append(("scope", "a reason for edits outside the scope globs (fm task log ID \"scope: …\")"))
    return need


def cmd_gates(args):
    p = resolve(args)
    act = c.active_brief(c.load_briefs(p), p.lane)
    type_, tier = args.type or (act.type if act else "FEATURE"), args.tier or (act.tier if act else "S")
    need = gates(type_, tier)
    out(args, {"type": type_, "tier": tier, "gates": [{"gate": g, "how": h} for g, h in need]},
        f"fm task done needs ({type_} {tier}):\n" + "\n".join(f"- {g}: {h}" for g, h in need)
        + ("\nS shortcut: fm task finish ID --run \"<check>\" --audit \"<how>\"" if tier == "S" else ""))


def _moved_since_planned(p, b):
    """Commits since the brief was written that changed files in its scope (an hour's grace for its own planning)."""
    scope, since = b.meta.get("scope") or [], str(b.meta.get("created") or "")
    if not scope or not since or (c.age_days(since) or 0) < 1 / 24 or not c.git_root(p.root):
        return ""
    files = c._git(p.root, "log", f"--since={since}", "--name-only", "--pretty=format:", timeout=10).splitlines()
    moved = sorted({f for f in files if f and any(c.glob_match(f, s) for s in scope)})
    return (f"Changed in scope since this was planned ({since[:10]}): {c.fit(', '.join(moved), 200)}; re-ground the "
            f"plan against them before editing") if moved else ""


def cmd_checkpoint(args):
    p = resolve(args)
    with c.lock(p.dir):
        b = c.checkpoint(p, note=args.note, auto=args.auto, session=session())
    notes = b.section("Notes").strip() if b else ""
    out(args, {"task": b.id if b else None}, f"Checkpoint saved{' for ' + b.id if b else ' (no active task)'}."
        + (f"\nNotes:\n{notes}" if notes else ""))


def cmd_resume(args):
    p = resolve(args)
    r = c.resume_info(p)
    if not r["id"]:
        nxt = ", ".join(q["id"] for q in c.state_dict(p)["queue"][:3]) or "none"
        return out(args, r, f"No active task. Next in queue: {nxt}")
    step = f"step {r['step']['n']}/{r['step']['of']}: {r['step']['text']}" if r["step"] else f"{r['steps_done']}/{r['steps_total']} steps done"
    stale = (f"\nStale since it started (gone from the repo now): {', '.join(r['stale'])} — re-check the brief before "
             f"relying on it." if r.get("stale") else "")
    b = c.find_brief(p, r["id"])
    notes = b.section("Notes").strip()  # T-0630
    n, tried = _tried(b)
    extra = (f"\nTried on step {n}: " + "; ".join(f"{x} ×{k}" for x, k in tried)) if tried else ""
    green = None if getattr(args, "no_check", False) else _last_green(b)
    if green:  # T-0649: did anything drift since the last green check?
        guard_stored(p, b, green)  # T-0901 review: a brief's [ran] line can come from another clone
        code, output = c.run_command(p.root, green, 120)
        extra += (f"\nLast green check `{green}` still passes." if code == 0 else
                  f"\nLast green check `{green}` now fails ({c.run_result(code, output)}): something drifted since it "
                  f"passed — look before going on.")
    out(args, r, f"Resume {r['id']} [{r['type']} {r['tier']}] {r['title']} — {step}\n{r['resume']}{stale}"
        + (f"\nNotes:\n{notes}" if notes else "") + extra + f"\nBrief: {r['path']}")


def _queue_preview(p, args, order, briefs):
    """T-0114: the queue and the ranked inbox with this project's usual minutes for each type and size, and what each
    will need from the user under the current autonomy (a plan yes, an open fm ask, a core yes its scope implies),
    gathered first so they can be answered together before a long run."""
    import fmguard
    import fmwatch
    meta = c.read_meta(p)
    autonomy, pending, standing = c.effective_autonomy(p, meta), c.pending_tasks(meta), set(meta.get("standing") or {})
    usual = fmwatch.typical(c.ledger_tail(p, 5000))
    ctx = fmguard.Ctx(cwd=p.root, project_root=p.root, home=os.path.expanduser("~"), foreman_home=c.foreman_home(),
                      state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks())
    act = c.active_brief(briefs, p.lane)
    items = []
    for b in [x for x in order if x is not act] + c.rank_inbox(briefs):
        needs = [w for w in [c.waits_on_user(b, pending, autonomy)] if w]
        core = any("core" in fmguard.classify_write(os.path.join(p.root, re.split(r"[*?\[]", g)[0]), ctx)
                   for g in b.meta.get("scope") or [])
        if core and "core" not in standing:
            needs.append("core yes")
        items.append({"id": b.id, "type": b.type, "tier": b.tier, "title": b.title, "status": b.status,
                      "minutes": usual.get(f"{b.type}/{b.tier}"), "needs": needs})
    known = [i["minutes"] for i in items if i["minutes"] is not None]
    asks = [i for i in items if i["needs"]]
    lines = [f"Queue preview ({autonomy} autonomy): {len(items)} item(s), about {sum(known)} min for the {len(known)} "
             f"with history here; {len(asks)} need you" + (" — answer these together:" if asks else ".")]
    lines += [f"  ✋ {i['id']} {i['type']} {i['tier']} {c.fit(i['title'], 60)} — {', '.join(i['needs'])}" for i in asks]
    lines += [f"{n}. {i['id']} {i['type']} {i['tier']} [{i['status']}] "
              f"{'~' + str(i['minutes']) + ' min' if i['minutes'] is not None else '~? min'} — {c.fit(i['title'], 70)}"
              for n, i in enumerate(items, 1)]
    return out(args, {"autonomy": autonomy, "items": items, "minutes_known": sum(known)}, "\n".join(lines))


def cmd_queue(args):
    p = resolve(args)
    briefs = c.lane_view(c.load_briefs(p), p.lane)  # T-0134: another lane's work isn't this side's queue
    order, cycles, dangling = c.order_queue(briefs)
    if args.preview:
        return _queue_preview(p, args, order, briefs)
    if args.replan:
        with c.lock(p.dir):
            c.log_event(p, "replan", data={"order": [b.id for b in order]}, session=session())
            c.regen_views(p, briefs)
    data = {"order": [c.brief_summary(b) for b in order], "cycles": cycles, "dangling": [list(d) for d in dangling]}
    lines = []
    for i, b in enumerate(order, 1):
        lines.append(f"{i}. {b.id} {b.type} {b.tier} [{b.status}]{' !' if b.priority == 'urgent' else ''} — {b.title}")
        why = [x for x in (b.meta.get("inferred_why") and f"after {b.meta['inferred_why']}",
                           b.meta.get("group") and f"group: {b.meta['group']}") if x]
        if why:  # T-0383: what fm relate inferred, and why
            lines.append("   ↳ " + " · ".join(why))
    lines = lines or ["Queue empty."]
    if cycles:
        lines.append("Cycles: " + "; ".join(" ↔ ".join(x) for x in cycles))
    if dangling:
        lines.append("Dangling: " + ", ".join(f"{a}→{b}" for a, b in dangling))
    out(args, data, "\n".join(lines))


def cmd_log(args):
    p = resolve(args)
    try:
        data = json.loads(args.data) if args.data else {}
    except ValueError as e:
        raise UsageError(f"data must be JSON: {e}")
    if not isinstance(data, dict):
        data = {"value": data}
    rec = c.log_event(p, args.event, task=args.task, data=data, session=session())
    out(args, rec, None)


_SENSITIVE_PATH = re.compile(r"(^|/)(\.env(?!.*\.(example|sample|template)$)[^/]*|[^/]*\.pem)$"
                             r"|(^|[/._-])(secrets?|prod(uction)?)([/._-]|$)", re.I)
_SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".tox", "dist", "build"}


def sensitive_signals(root, cap=20000):
    """T-0960: paths under root that suggest it's sensitive: .env* (not .example/.sample/.template), *.pem, or a
    secret(s)/prod(uction) path part. Read-only; ignored files count (a .env is usually ignored)."""
    hits, seen = [], 0
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in _SKIP_DIRS)
        for f in sorted(files):
            seen += 1
            rel = os.path.relpath(os.path.join(d, f), root)
            if _SENSITIVE_PATH.search(rel):
                hits.append(rel)
        if seen > cap:  # ponytail: a capped walk, a git ls-files pass if huge repos miss signals
            break
    return hits


def cmd_sensitive(args):
    if args.state == "suggest":  # T-0960: the signals, never a setting
        root = c.git_root(args.path or os.getcwd()) or os.path.abspath(args.path or ".")
        hits = sensitive_signals(root)
        return out(args, {"root": root, "signals": hits},
                   "\n".join([f"Signals that {root} is sensitive:"] + [f"  {c.plain(h)}" for h in hits[:40]]
                             + ["fm sensitive on would mark it; nothing was changed."]) if hits else
                   f"No signals in {root} (.env*, *.pem, secret or prod in a path); nothing was changed.")
    if args.path:
        root = c.git_root(args.path) or os.path.abspath(args.path)
        p = c.find_project(root) or c.init_project(root)
    else:
        p = resolve(args)
    path = os.path.join(p.root, ".claude", "settings.local.json")
    data = {}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    perms = data.setdefault("permissions", {})
    if args.state == "on":
        perms["defaultMode"] = "default"
    else:
        perms.pop("defaultMode", None)
        if not perms:
            data.pop("permissions")
    c.write_atomic(path, json.dumps(data, indent=2) + "\n")
    _git_exclude(p.root, ".claude/settings.local.json")
    c.update_meta(p, sensitive=args.state == "on")
    with c.lock(p.dir):
        c.log_event(p, "sensitive", data={"on": args.state == "on"}, session=session())
        c.regen_views(p)
    what = "new sessions here start in manual permission mode" if args.state == "on" else "user default mode applies again"
    out(args, {"sensitive": args.state == "on"}, f"{p.slug}: sensitive {args.state} ({what}).")


def _git_exclude(root, rel):
    """Keep a machine-local settings file out of commits without touching the repo's .gitignore."""
    excl = os.path.join(root, ".git", "info", "exclude")
    if not os.path.isdir(os.path.dirname(excl)):
        return
    try:
        cur = open(excl).read() if os.path.exists(excl) else ""
        if rel not in cur.split("\n"):
            with open(excl, "a") as f:
                f.write(("" if cur.endswith("\n") or not cur else "\n") + rel + "\n")
    except OSError:
        pass


def _take_seen_ask(p, tid, cats):
    """The record the PreToolUse hook made for this exact `fm ask` (consumed): session, and whether a dialog was
    raised for it. None when the hook didn't see it."""
    import time
    path = os.path.join(p.dir, "asks.json")
    try:
        with open(path) as f:
            seen = json.load(f)
    except (OSError, ValueError):
        return None
    match = next((a for a in reversed(seen) if isinstance(a, dict) and a.get("task") == tid
                  and sorted(set(a.get("allow") or [])) == sorted(set(cats))
                  and time.time() - a.get("at", 0) < c.ASK_TTL), None)
    if match:
        seen.remove(match)
        c.write_atomic(path, json.dumps(seen))
    return match


def _prompted(p, tid, cats):
    """A permission dialog was shown for this exact request (this command only runs once it was approved)."""
    try:
        with open(os.path.join(p.dir, "prompts.json")) as f:
            seen = json.load(f)
    except (OSError, ValueError):
        return False
    import time
    return any(isinstance(a, dict) and a.get("task") == tid and a.get("allow") == sorted(set(cats))
               and time.time() - a.get("at", 0) < c.APPROVAL_TTL for a in seen)


def cmd_ask(args):
    """Record a request only. The grant happens in the UserPromptSubmit hook, on the user's own reply."""
    import fmguard
    p = resolve(args)
    cats = list(dict.fromkeys(args.categories))
    bad = [x for x in cats if x not in fmguard.CATEGORIES or x in fmguard.NOT_AUTHORIZABLE]
    if bad:
        ok = [x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE]
        raise UsageError(f"can't ask for {', '.join(bad)}; askable: {', '.join(ok)}")
    why = c.redact(args.why)
    if args.standing and cats != ["core"]:
        raise UsageError("--standing is for core alone: fm ask ID core --standing --why \"…\"")
    if args.pin:
        import fmplugins
        if "plugin" not in cats or fmplugins.content_hash(args.pin) is None:
            raise UsageError(f"--pin names a plugin to install or enable with the plugin category; {args.pin!r} "
                             f"isn't in the known marketplaces or installed (fm plugins find <need>)")
    with c.lock(p.dir):
        b = need_brief(p, args.id)
        if b.status in c.CLOSED and not args.standing:  # T-0302: a yes on a closed task would grant nothing
            raise UsageError(f"{b.id} is closed ({b.status}): a grant works only while its task is active; ask on "
                             f"an open task")
        if _prompted(p, b.id, cats):
            return out(args, {"task": b.id, "allow": cats, "via": "prompt"},
                       f"Approved in Claude Code's permission prompt: the hook records the grant of {', '.join(cats)} "
                       f"for {b.id}.")
        seen = _take_seen_ask(p, b.id, cats)
        sid = seen and seen.get("session")
        if not sid:
            raise UsageError("fm ask must run as its own Bash command in the Claude Code session that asks: the hook "
                             "ties the request to that session (it saw no matching call, so nothing was recorded). "
                             "If it was its own command, state was busy: run the same fm ask again")
        meta = c.read_meta(p)
        pend = [a for a in meta.get("pending_approvals") or [] if a.get("task") != b.id]
        pend.append(dict({"task": b.id, "allow": cats, "why": why, "session": sid, "at": c.now()},
                         **({"pin": args.pin} if args.pin else {})))
        meta["pending_approvals"] = pend
        c.write_meta(p, meta)
        c.log_event(p, "approval_requested", task=b.id, data={"allow": cats, "why": why}, session=sid)
        c.regen_views(p)  # the statusline shows what a yes would grant
    reload = (" The user approved Claude Code's permission dialog, but this session hasn't loaded Foreman's "
              "PermissionRequest hook, so the dialog can't grant it: they should run /reload-plugins.") \
        if seen.get("dialog") else ""
    out(args, {"task": b.id, "allow": cats, "why": why},
        f"Pending: {b.id} {', '.join(cats)} ({why}).{reload} Ask the user one yes/no question for it now; their next "
        f"message decides: a reply starting with yes grants it, anything else cancels it.")


def cmd_trust(args):
    """T-0120: whether Claude may edit the guard and Claude Code settings. Only the foreman-ui mod's /fm-trust on,
    typed by the user (its command.run checks the origin), turns it on, by writing the trust record into Foreman state
    itself; no tool call may write there, and fm has no "on". Off removes it, from anywhere. Status records each new
    trust in the ledger (the mod asks right after writing it)."""
    p = resolve(args)
    rec = c.trusted()
    if args.state == "off" and rec:
        os.remove(c.trust_path())
        c.log_event(p, "trust_off", session=session())
        rec = None
    elif rec:
        with c.lock(p.dir):
            meta = c.read_meta(p)
            if meta.get("trust_seen") != rec.get("at"):
                meta["trust_seen"] = rec.get("at")
                c.write_meta(p, meta)
                c.log_event(p, "trust_on", data={"at": rec.get("at")}, session=session())
    return out(args, {"trust": bool(rec)},
               "Trust on: Claude may edit the guard and Claude Code settings (Foreman state only through fm); "
               "/fm-trust off or fm trust off ends it." if rec else
               "Trust off: the guard and Claude Code settings need your yes per task (/fm-trust on, typed by you).")


def cmd_standing(args):
    """T-0119: show the project's standing yeses, or turn them off. Turning on happens only through the user's answer
    to `fm ask ID core --standing` in Claude Code's permission prompt."""
    p = resolve(args)
    with c.lock(p.dir):
        meta = c.read_meta(p)
        had = dict(meta.get("standing") or {})
        if args.state == "off" and had:
            meta.pop("standing", None)
            c.write_meta(p, meta)
            c.log_event(p, "standing_off", data={"was": sorted(had)}, session=session())
    if args.state == "off":
        return out(args, {"standing": {}}, "Standing yeses off: Foreman's core asks per task again." if had
                   else "No standing yes to turn off.")
    return out(args, {"standing": had}, "\n".join(f"Standing yes: {k} since {v.get('at')} ({v.get('why') or 'no reason'}); "
                                                 f"fm standing off revokes it" for k, v in had.items())
               or "No standing yes: Foreman's core asks per task.")


def _decision_row(line):
    """T-0341: one decisions.md row as fields (the desktop app's Decisions tab): date, kind (costly|outward|None),
    text, why, and whether a later decision reversed it."""
    body = line.removesuffix("  ← reversed later").strip().removeprefix("|").removesuffix("|")
    cells = [x.strip().replace("\\|", "|") for x in re.split(r"(?<!\\)\|", body)]  # cell() escapes a | as \|
    kind = re.match(r"\[(costly|outward)\]\s*", cells[1] if len(cells) > 1 else "")
    return {"date": cells[0], "kind": kind and kind.group(1), "text": (cells[1] if len(cells) > 1 else "")[
        kind.end() if kind else 0:], "why": cells[2] if len(cells) > 2 else "", "reversed": line.endswith("← reversed later"),
        "rejected": cells[3] if len(cells) > 3 else ""}


def _export_adr(p, args, rows):
    """T-0958: one ADR (Nygard: title, status, context, decision, consequences) per decisions.md row, numbered in
    order, so a re-export rewrites the same files."""
    top = os.path.abspath(args.export_adr)
    os.makedirs(top, exist_ok=True)
    written = []
    for n, r in ((n, _decision_row(row)) for n, row in rows):
        text = re.sub(r"^(\[[^\]]*\]\s*)*", "", r["text"]).strip() or "untitled"
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "decision"
        path = os.path.join(top, f"{n:04d}-{slug}.md")
        c.write_atomic(path, f"# {n}. {text}\n\nDate: {r['date']}\n\n## Status\n\n"
                       f"{'Superseded (reversed by a later decision)' if r['reversed'] else 'Accepted'}"
                       + (f" ({r['kind']})" if r["kind"] else "") + f"\n\n## Context\n\n{r['why'] or '(not recorded)'}"
                       f"\n\n## Decision\n\n{r['text']}\n\n## Consequences\n\nAlternatives rejected: "
                       f"{r['rejected'] or '(none recorded)'}\n")
        written.append(path)
    return out(args, {"dir": top, "files": written}, f"{len(written)} ADR(s) → {top}" if written else
               "No decisions recorded.")


def cmd_decide(args):
    """Record a decision; T-0057: --kind costly|outward marks one the user should review in the final report,
    --reverses names the earlier decision it undoes; --list shows them (--review: only those to review)."""
    p = resolve(args)
    path = os.path.join(p.dir, "decisions.md")
    sunset = None
    if getattr(args, "sunset", None) and (not args.decision or args.list or args.review or getattr(args, "ask", None) is not None
                                          or getattr(args, "digest", False) or getattr(args, "answer", None) is not None
                                          or getattr(args, "export_adr", None)):
        raise UsageError("--sunset goes with a decision text being recorded, not --list, --review, --ask, --digest, "
                         "--answer or --export-adr")
    applied = _apply_due_asks(p)  # any fm decide applies a passed deadline first
    if getattr(args, "ask", None) is not None:
        return _decide_ask(p, args)
    if getattr(args, "digest", False):
        return _digest(p, args, applied)
    if getattr(args, "answer", None) is not None:
        return _answer(p, args)
    if args.decision and getattr(args, "export_adr", None):
        raise UsageError("--export-adr exports the recorded decisions: run it without a decision text")
    if args.list or args.review or not args.decision:
        rows = [l.rstrip("\n") for l in (open(path, encoding="utf-8").readlines() if os.path.exists(path) else [])
                if l.startswith("| 2")]
        text = "\n".join(rows)
        reversed_ = re.findall(r"\[reverses: ([^\]]+)\]", text)
        nums = [n for n, r in enumerate(rows, 1) if not args.review or re.search(r"\| \[(costly|outward)\]", r)]
        pick = [rows[n - 1] + ("  ← reversed later" if any(x.lower() in rows[n - 1].lower() for x in reversed_
                                                          if "[reverses:" not in rows[n - 1]) else "") for n in nums]
        if getattr(args, "export_adr", None):  # numbered as in the full list, so a --review export never collides
            return _export_adr(p, args, list(zip(nums, pick)))
        return out(args, {"decisions": pick, "rows": [_decision_row(r) for r in pick]},
                   "\n".join(pick[-args.n:]) or "No decisions recorded.")
    try:
        revisit = c.revisit_tag(p.root, args.revisit) + " " if getattr(args, "revisit", None) else ""  # callers build
    except ValueError as e:                                                                          # their own args
        raise UsageError(str(e))
    if getattr(args, "sunset", None):  # T-1084: the decision lapses on this date; fm tidy lists it as expired
        try:  # fromisoformat takes 20200101 and 2020-W01-1 too; the reader needs YYYY-MM-DD
            if not re.fullmatch(r"\d{4}-\d\d-\d\d", args.sunset):
                raise ValueError
            sunset = c.datetime.date.fromisoformat(args.sunset).isoformat()
        except ValueError:
            raise UsageError("--sunset takes YYYY-MM-DD")
        revisit += f"[sunset: {sunset}] "
    _write_decision(p, args.decision, args.why, args.rejected, args.kind, args.reverses, args.task,
                    getattr(args, "revisited", None), revisit, cites=getattr(args, "cites", None))
    out(args, {"decision": args.decision},
        f"Decision recorded in {path}." + (" Its sunset is already expired." if sunset and sunset <= c.now()[:10] else ""))


def _write_decision(p, decision, why="", rejected="", kind="reversible", reverses=None, task=None, settles=None,
                    revisit="", locked=False, cites=None):
    def cell(v):
        return c.redact((v or "").replace("|", "\\|").replace("\n", " ").strip())
    words = lambda v: cell(v).replace("]", ")")  # a tag's words can't close the tag early
    tags = ("" if kind == "reversible" else f"[{kind}] ") + (
        f"[reverses: {words(reverses)}] " if reverses else "") + (
        f"[revisited: {words(settles)}] " if settles else "") + (
        f"[cites: {words(cites)}] " if cites else "") + revisit  # T-0654: what the decision rests on
    text = re.sub(r"^\[", "(", cell(decision))  # review: free text can't open with a tag fm would read
    row = f"| {c.now()[:10]} | {tags}{text} | {cell(why)} | {cell(rejected)} |\n"
    path = os.path.join(p.dir, "decisions.md")
    import contextlib
    with contextlib.nullcontext() if locked else c.lock(p.dir):
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else \
            "# Decisions\n\n| Date | Decision | Why | Alternatives rejected |\n|---|---|---|---|\n"
        c.write_atomic(path, cur + row)
        c.log_event(p, "decision", task=task, data={"decision": decision, "why": why, "rejected": rejected,
                                                     "kind": kind, "reverses": reverses}, session=session())


def _guard_named(text):
    """T-0439: the guard categories (or fm ask) an ask names: those are the user's to grant, never pre-answered."""
    import fmguard
    words = set(re.findall(r"[a-z][a-z-]*", text.lower()))
    words |= {w.rstrip("s") for w in words} | {p for w in words for p in w.split("-")}  # plugins, force-push
    named = [x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE and x in words]
    named += [cat for cat, syn in _GUARD_WORDS.items() if words & syn and cat not in named]  # T-0671 review
    return named + (["fm ask"] if re.search(r"(?i)\bfm\s+ask\b", text) else [])


# ponytail: words, not meaning ("Remove the alias?" isn't one, "Delete …" is); a miss is still refused by the guard
_GUARD_WORDS = {"git-destructive": {"push", "rebase", "force"}, "remote": {"origin", "upstream"},
                "credentials": {"credential", "secret", "password"}, "rm-outside": {"delete", "rm", "wipe", "purge"},
                "system": {"sudo", "systemctl"}, "publish": {"publish", "deploy", "upload"},
                "plugin": {"plugin", "marketplace"}, "core": {"guard"}}


def _decide_ask(p, args):
    """T-0439/T-0461: a question Claude would put to the user, with its default (given, or the taste record's pick of
    --options). Urgent: ask now. Full autonomy: decided now. Standard: it waits in the ask digest until its deadline."""
    q, options = c.plain(args.ask).strip(), [c.plain(o).strip() for o in args.options or [] if o.strip()]
    named = _guard_named(" ".join([q, *options, args.default or ""]))
    if named:
        raise UsageError(f"this ask names {', '.join(named)}: guard categories are the user's alone (fm ask ID "
                         f"<category> --why \"…\"); the taste record and the ask digest never pre-answer them")
    if not q or not (args.default or options):
        raise UsageError("fm decide --ask \"<question>\" needs --default ANSWER or --options A B … (the taste record picks)")
    if args.default:
        answer, why = c.plain(args.default).strip(), "the given default"
    else:
        import fmideas
        answer, why = fmideas.taste_default(p, options)
    rejected = ", ".join(o for o in options if o != answer)
    autonomy = "standard" if c.panicked() else c.effective_autonomy(p)  # T-1080 review: a spent risk budget asks
    data = {"q": q, "default": answer, "why": why, "options": options}
    if args.urgent:
        return out(args, dict(data, urgent=True), f"Urgent: ask the user now, one AskUserQuestion with \"{answer}\" "
                   f"first ({why}); record the answer: fm decide \"{q} → <answer>\".")
    if autonomy == "full":
        _write_decision(p, f"{q} → {answer}", f"full autonomy: the default ({why})", rejected, task=args.task)
        return out(args, dict(data, answer=answer, applied=True), f"Decided (full autonomy): {q} → {answer} ({why}).")
    import fmideas
    prec = fmideas.precedent(p, q, options)  # T-1064: the user's own earlier answers stand in, labelled, and can be overruled
    if prec:
        answer, why = prec[0], f"Proxy answer (from {prec[1]} earlier answers)"
        data = dict(data, default=answer, why=why)
    with c.lock(p.dir):
        meta = c.read_meta(p)
        d = meta.get("ask_digest") or {"asks": []}
        if not c.parse_ts(d.get("deadline")):
            d["deadline"] = c.iso(time.time() + DIGEST_HOURS * 3600)
        n = max((a.get("n", 0) for a in d["asks"]), default=0) + 1
        d["asks"].append(dict(data, n=n, task=args.task, at=c.now(), **({"proxy": True} if prec else {})))
        meta["ask_digest"] = d
        c.write_meta(p, meta)
        c.log_event(p, "ask_queued", task=args.task, data={"n": n, "q": q, "default": answer}, session=session())
        if prec:
            _write_decision(p, f"{q} → {answer}", why, rejected, task=args.task, locked=True)
            c.log_event(p, "proxy_answer", task=args.task, data={"n": n, "q": q, "a": answer}, session=session())
    if prec:
        return out(args, dict(data, answer=answer, proxy=True, queued=n, deadline=d["deadline"]),
                   f"{why}: {q} → {answer}. It stays in the digest as ask {n}; the user's answer there overrules it.")
    return out(args, dict(data, queued=n, deadline=d["deadline"]),
               f"Ask {n} waits in the digest ({len(d['asks'])}; unanswered, each takes its default at {d['deadline']}). "
               f"Keep working; before you end the turn put the digest to the user (fm decide --digest).")


DIGEST_HOURS = 8  # T-0461: how long a non-urgent ask waits for the user before its default applies


def _apply_due_asks(p):
    """T-0461: past the digest's deadline every unanswered ask takes its default, each a decision in decisions.md."""
    if not c.digest_due(c.read_meta(p).get("ask_digest")):
        return []
    with c.lock(p.dir):
        meta = c.read_meta(p)
        d = meta.get("ask_digest")
        if not c.digest_due(d):
            return []
        for a in d["asks"]:  # rows first: a crash between the two repeats a row rather than losing an ask
            if a.get("proxy"):
                continue  # its row was written when it was proxied
            _write_decision(p, f"{a['q']} → {a['default']}", f"ask digest deadline passed unanswered: the default "
                            f"({a.get('why')})", ", ".join(o for o in a.get("options") or [] if o != a["default"]),
                            task=a.get("task"), locked=True)
        meta.pop("ask_digest")
        c.write_meta(p, meta)
    return [dict(a, answer=a["default"]) for a in d["asks"]]


def _digest(p, args, applied):
    d = c.read_meta(p).get("ask_digest") or {}
    asks = d.get("asks") or []
    lines = [f"Default applied at the deadline: {a['q']} → {a['answer']}" for a in applied]
    if asks:
        lines += [f"Ask digest ({len(asks)}; unanswered, each takes its default at {d.get('deadline')}):"]
        lines += [f"  {a['n']}. {a['q']} — default: {a['default']}"
                  + (f" (of: {', '.join(a['options'])})" if a.get("options") else "") for a in asks]
        lines += ["Put them to the user in one AskUserQuestion, each default first; record each answer: "
                  "fm decide \"<answer>\" --answer N."]
    return out(args, {"asks": asks, "applied": applied, "deadline": d.get("deadline")},
               "\n".join(lines) or "The ask digest is empty.")


def _answer(p, args):
    if not args.decision:
        raise UsageError("fm decide \"<the user's answer>\" --answer N (N from fm decide --digest)")
    with c.lock(p.dir):
        meta = c.read_meta(p)
        d = meta.get("ask_digest") or {}
        a = next((x for x in d.get("asks") or [] if x.get("n") == args.answer), None)
        if not a:
            raise UsageError(f"no ask {args.answer} waits in the digest; fm decide --digest lists them")
        _write_decision(p, f"{a['q']} → {args.decision}", args.why or "the user's answer (ask digest)",
                        args.rejected or ", ".join(o for o in a.get("options") or [] if o != args.decision),
                        task=a.get("task") or args.task, locked=True)
        import fmideas
        c.log_event(p, "ask_answered", task=a.get("task"), data={"q": fmideas.ask_key(a["q"], a.get("options")), "a": args.decision},
                    session=session())
        if a.get("proxy") and a.get("default") != args.decision:
            c.log_event(p, "proxy_overruled", task=a.get("task"), data={"n": args.answer, "q": a["q"]}, session=session())
        d["asks"].remove(a)
        if not d["asks"]:
            meta.pop("ask_digest")
        c.write_meta(p, meta)
    return out(args, {"n": args.answer, "q": a["q"], "answer": args.decision}, f"Ask {args.answer}: {a['q']} → "
               f"{args.decision} (decisions.md).")


def _agent_report(path):
    """The final report from a subagent's output file (a JSONL transcript: its last assistant text), or the file's text
    when it isn't a transcript."""
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    report = None
    for line in raw.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        m = e.get("message") if isinstance(e, dict) else None
        if isinstance(m, dict) and m.get("role") == "assistant" and isinstance(m.get("content"), list):
            text = "\n".join(x.get("text", "") for x in m["content"] if isinstance(x, dict) and x.get("type") == "text")
            report = text.strip() or report
    return (report or raw).rstrip("\n") + "\n"


def cmd_research(args):
    p = resolve(args)
    name = args.name[:-3] if args.name.endswith(".md") else args.name
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", name):
        raise UsageError(f"research name must be a plain file name, got {args.name!r}")
    src = args.from_agent or args.file
    if src and not os.path.isfile(src):  # a FIFO or device would hang the read, a directory would crash it
        raise UsageError(f"{src} is not a regular file")
    text = (_agent_report(args.from_agent) if args.from_agent else
            open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read())
    path = os.path.join(p.dir, "research", name + ".md")
    # T-0629: what an agent noticed outside its brief becomes a discovered capture, not a line lost in a report
    noticed = [c.fit(c.plain(c.redact(m.group(1))).strip(" .`*"), 200)
               for m in re.finditer(r"(?mi)^\W*noticed:?\**\s*(.+)$", text)] if args.from_agent else []
    noticed = [x for x in dict.fromkeys(noticed) if x and x.lower() not in ("none", "nothing", "n/a")][:10]
    with c.lock(p.dir):
        c.write_atomic(path, c.defang(c.redact(text)))
        made = []
        for x in noticed:
            type_ = "FIX" if re.search(r"(?i)\b(bug|broken|drops?|crash|fails?|wrong|leak)\b", x) else "FEATURE"
            b = _create(p, _title(x), type_, c.guess_tier(type_, x), "captured", raw=f"{x}\n(noticed by an agent; "
                        f"research {name})", source="discovered")
            made.append(b.id)
            c.log_event(p, "capture", task=b.id, data={"source": "discovered", "type": type_, "from": name},
                        session=session())
        c.log_event(p, "research", task=args.task, data={"name": name, "chars": len(text), "noticed": made},
                    session=session())
        c.regen_views(p)  # (and fm sync's mirror)
    out(args, {"path": path, "noticed": made}, f"Saved {path}" + (f"; {len(made)} noticed item(s) captured: "
                                                                  f"{', '.join(made)}" if made else ""))


_PROMISE = re.compile(r"(?i)\bI(?:['’]ll| will)\s+(?:also|later|follow up (?:on|with)|come back to|circle back to)"
                      r"\s+(?!(?:note|mention|say|point out|add that)\b)[^.\n!?]{4,140}")
_OFFER = re.compile(r"(?i)\b(?:if|want|would|could|happy|can|shall|like)\b")  # T-0908: "If you want, I'll also…" offers


def capture_promises(p, text, sid=None):
    """T-0899: what a reply that ends the turn promises for later ("I'll also…", "I'll follow up on…") becomes an inbox
    item, once (an open one of the same title is enough); code blocks don't count. Returns the new ids."""
    said = re.sub(r"```.*?(?:```|$)", " ", text or "", flags=re.S)
    found = list(dict.fromkeys(c.fit(c.plain(c.redact(m.group(0))).strip(), 160) for m in _PROMISE.finditer(said)
                               if not _OFFER.search(re.split(r"[.!?\n]", said[:m.start()])[-1])
                               and not re.search(r"(?i)\bif you\b", m.group(0))))[:3]
    if not found:
        return []
    made = []
    with c.lock(p.dir, timeout=1):  # the Stop hook: a promise lost to a busy lock beats a stalled stop
        have = {b.title.lower() for b in c.load_briefs(p) if b.status not in c.CLOSED}
        for x in found:
            title = _title(f"Promised: {x}")
            if title.lower() in have:
                continue
            b = _create(p, title, "FEATURE", "S", "captured", raw=f"{x}\n(promised in Claude's reply; captured so it "
                                                                  f"isn't lost)", source="followup")
            c.log_event(p, "capture", task=b.id, data={"source": "promise"}, session=sid)
            made.append(b.id)
        if made:
            c.regen_views(p)
    return made


def _research_items(p):
    """(name, path of the file to read, mtime) for each note and brainstorm folder, newest first (T-0802)."""
    folder = os.path.join(p.dir, "research")
    items = []
    for n in os.listdir(folder) if os.path.isdir(folder) else []:
        path = os.path.join(folder, n)
        if os.path.islink(path):
            continue
        if os.path.isdir(path):
            path = os.path.join(path, "ideas.md")
        elif n.endswith(".md"):
            n = n[:-3]
        else:
            continue
        if os.path.isfile(path) and not os.path.islink(path):
            items.append((n, path, os.path.getmtime(path)))
    return sorted(items, key=lambda i: i[2], reverse=True)


def cmd_research_list(args):
    p = resolve(args)
    rows = []
    for n, path, mt in _research_items(p):
        with open(path, encoding="utf-8", errors="replace") as f:
            first = next((ln.strip("# \t\r\n") for ln in f if ln.strip()), "")
        rows.append({"name": n, "date": time.strftime("%Y-%m-%d", time.localtime(mt)), "title": c.fit(first, 80),
                     "bytes": os.path.getsize(path)})
    out(args, rows, "\n".join(f"{r['name']}  {r['date']}  {r['bytes']}B  {r['title']}" for r in rows)
        or "(no research saved)")


def cmd_research_show(args):
    p = resolve(args)
    name = args.name[:-3] if args.name.endswith(".md") else args.name
    items = {n: path for n, path, _ in _research_items(p)}
    if name not in items:
        import difflib
        near = difflib.get_close_matches(name, list(items), n=1)
        raise UsageError(f"no research named {name!r}" + (f"; closest: {near[0]}" if near else ""))
    with open(items[name], encoding="utf-8", errors="replace") as f:
        print(f.read(), end="")


def cmd_drive(args):
    p = resolve(args)
    c.update_meta(p, drive=args.state == "on")
    with c.lock(p.dir):
        c.log_event(p, "drive", data={"on": args.state == "on"}, session=session())
        c.regen_views(p)
    out(args, {"drive": args.state == "on"}, f"{p.slug}: drive {args.state}.")


def cmd_posture(args):
    """T-0963: lite runs only the guard's hook here (no injections, no bookkeeping); full is every hook."""
    p = resolve(args)
    if not args.state:
        posture = c.read_meta(p).get("posture") or "full"
        return out(args, {"posture": posture}, f"{p.slug}: posture {posture}.")
    c.update_meta(p, posture=args.state)
    with c.lock(p.dir):
        c.log_event(p, "posture", data={"posture": args.state}, session=session())
    what = "only the guard's hook runs here" if args.state == "lite" else "every hook runs"
    out(args, {"posture": args.state}, f"{p.slug}: posture {args.state} ({what}).")


def cmd_approve_reads(args):
    """T-0974: Foreman answers Claude Code's permission dialog for a command that only reads (fmguard.read_only); on is
    the user's to type (the guard refuses it from Claude), off is anyone's."""
    p = resolve(args)
    if args.state:
        c.update_meta(p, approve_reads=args.state == "on")
        with c.lock(p.dir):
            c.log_event(p, "approve_reads", data={"on": args.state == "on"}, session=session())
    on = bool(c.read_meta(p).get("approve_reads"))
    out(args, {"approve_reads": on}, f"{p.slug}: " + (
        "Foreman approves commands that only read (ls, cat, grep, git status …); anything else still asks." if on
        else "every permission dialog is yours, as Claude Code shows it."))


def cmd_pause(args):
    """T-0436: one flag for every project. It grants nothing, and lifting it only lets back what ran before, so
    either way it's no consent to guard."""
    on = args.state == "on"
    c.set_panic(on)
    out(args, {"paused": on}, "Paused everywhere: no drive, fm run, serve, night or lane launches, and autonomy reads "
        "standard; a session already running finishes its turn. fm pause off lifts it." if on else
        "Pause lifted: the drive and the launchers run again, under each project's own autonomy.")


def cmd_check(args):
    """The project's gate commands (tests, lint, doctor…), run together; any failure exits 1, so a pipe can't mask it."""
    p = resolve(args)
    if args.action in ("add", "rm"):
        with c.lock(p.dir):  # one read-modify-write, so concurrent adds can't drop each other
            meta = c.read_meta(p)
            checks = list(meta.get("checks") or [])
            if args.action == "add":
                if not args.words:
                    raise UsageError("fm check add needs a command")
                checks.append(" ".join(args.words))
            else:
                try:
                    gone = checks.pop(int(args.words[0]) - 1)
                except (IndexError, ValueError):
                    raise UsageError(f"no check {' '.join(args.words)!r}; fm check list numbers them")
                (meta.get("check_paths") or {}).pop(gone, None)
            meta["checks"] = checks
            c.write_meta(p, meta)
            c.log_event(p, "checks", data={"checks": checks}, session=session())
        return out(args, {"checks": checks}, f"{p.slug}: {len(checks)} check(s).")
    if getattr(args, "repeat", 0):  # T-0475: an intermittent failure's rate, gate by gate (nothing recorded or cached)
        n, rows = max(1, args.repeat), []
        for cmd in c.read_meta(p).get("checks") or []:
            guard_stored(p, c.active_brief(c.load_briefs(p), p.lane), cmd)  # T-0901 review
            passed = sum(1 for _ in range(n) if not c.run_command(p.root, cmd, args.timeout)[0])
            rows.append({"cmd": cmd, "passed": passed, "runs": n})
        out(args, {"repeat": rows}, "\n".join(f"{'✓' if r['passed'] == n else '✗'} {r['passed']}/{n}  {r['cmd']}"
                                              for r in rows) or "no checks (fm check add '<cmd>')")
        return 0 if all(r["passed"] == n for r in rows) else 1
    if args.action == "ambient":  # T-0705
        if args.words[:1] == ["run"]:  # the detached run an edit starts
            import fmambient
            return fmambient.run(p) or 0
        if args.words[:1] not in (["on"], ["off"]):
            raise UsageError("fm check ambient on|off")
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["ambient"] = args.words[0] == "on"
            c.write_meta(p, meta)
        return out(args, {"ambient": meta["ambient"]},
                   "Ambient tests on: after each edit the affected tests run in the background; you hear only when "
                   "they flip." if meta["ambient"] else "Ambient tests off.")
    if args.action == "onwrite":  # T-0947: a validator the write hook runs on matching files; a failure blocks
        glob_, cmd = (args.words[:1] or [None])[0], " ".join(args.words[1:])
        if cmd and "{file}" not in cmd:
            raise UsageError("fm check onwrite GLOB 'CMD {file}': the command needs {file}, the path just written")
        if cmd:
            guard_stored(p, c.active_brief(c.load_briefs(p), p.lane), cmd.replace("{file}", "file"))
        with c.lock(p.dir):
            meta = c.read_meta(p)
            rules = dict(meta.get("onwrite") or {})
            if glob_:
                rules.pop(glob_, None) if not cmd else rules.update({glob_: cmd})
                meta["onwrite"] = rules
                c.write_meta(p, meta)
        return out(args, {"onwrite": rules}, "\n".join(f"{g}: {x}" for g, x in rules.items())
                   or "No onwrite validators: fm check onwrite GLOB 'CMD {file}'.")
    if args.action == "affected":
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["affected"] = " ".join(args.words)
            c.write_meta(p, meta)
        return out(args, {"affected": meta["affected"]}, f"fm check --affected runs: {meta['affected'] or '(unset)'}")
    if args.action == "paths":  # T-0126: the files a gate covers; it is skipped while none of them changed
        with c.lock(p.dir):
            meta = c.read_meta(p)
            checks = list(meta.get("checks") or [])
            try:
                cmd = checks[int(args.words[0]) - 1]
            except (IndexError, ValueError):
                raise UsageError("fm check paths N GLOB…: N as fm check list numbers it (no globs: it runs every time)")
            paths, globs = dict(meta.get("check_paths") or {}), args.words[1:]
            paths.pop(cmd, None) if not globs else paths.update({cmd: globs})
            meta["check_paths"] = paths
            c.write_meta(p, meta)
        return out(args, {"cmd": cmd, "paths": globs},
                   f"{cmd}: " + (f"runs when {', '.join(globs)} changed (fm check --fresh runs it anyway)" if globs
                                 else "runs every time"))
    if args.affected:
        return _check_affected(p, args)
    checks = list(c.read_meta(p).get("checks") or [])
    check_paths = c.read_meta(p).get("check_paths") or {}
    if args.action == "list":
        return out(args, {"checks": checks, "paths": check_paths},
                   "\n".join(f"{i}. {x}" + (f"  [paths: {', '.join(check_paths[x])}]" if x in check_paths else "")
                             for i, x in enumerate(checks, 1)) or "No checks yet: fm check add '<cmd>'.")
    if not checks:
        hint = ""
        try:  # R3 bootstrap: what the project itself says it runs
            import fmmap
            m = fmmap.load(p) if c.git_root(p.root) else {}
            found = (m.get("gates") or []) + (m.get("ci") or [])[:4]
            hint = (f"; this project's tests look like: fm check add '{found[0]}'"  # T-0850: the line, ready to run
                    + (f" (also found: {'; '.join(found[1:])})" if found[1:] else "")) if found else ""
        except Exception:
            pass
        raise UsageError(f"no checks configured for this project: fm check add '<cmd>' (tests, lint, fm doctor…){hint}")
    import time
    act = c.active_brief(c.load_briefs(p), p.lane)
    tree = c.worktree_id(p.root)
    skip = red_first_tests(p, act, checks)  # T-1101
    env, left_out = _skip_env(skip), _left_out(skip)
    cached = None if args.fresh else _cached_pass(p, checks, tree, skip)
    if cached:  # the same gates already passed on this exact tree: rerunning them only costs time
        results, notes = [(cmd, 0, f"cached pass ({cached})", 0.0) for cmd in checks], {}
        if args.evidence:
            mutate(p, args.evidence, lambda b: b.add_evidence(
                "fm check: " + "; ".join(checks),
                f"exit 0 · {len(checks)} passed on this tree ({cached}){'; ' + left_out if left_out else ''}"[:600],
                step=args.step, ac=args.ac, tree=tree, ran=True),
                "evidence", {"step": args.step, "ac": args.ac, "cmd": "fm check", "result": "cached pass"})
        out(args, {"results": [{"cmd": x, "exit": 0, "cached": cached} for x in checks], "failed": 0,
                   "skipped_tests": skip},
            f"✓ all {len(checks)} gates passed on this exact tree already ({cached}); cached (fm check --fresh reruns)"
            + (f"\n! {left_out}" if left_out else ""))
        return 0
    before = _last_check_results(p, act.id if act else None)
    results, notes, skipped, reruns = [], {}, {}, []
    for cmd in _gate_order(p, checks):  # T-0047: timed; a failure is rerun once (flaky) and compared with the last run before the task
        gate_skip = None if args.fresh else _paths_unchanged(p, cmd, check_paths.get(cmd), tree)
        if gate_skip:  # T-0126: recorded as a pass carrying its real run's time and tree
            results.append((cmd, 0, gate_skip[0], 0.0))
            skipped[cmd] = {"since": gate_skip[1], "tree": gate_skip[2]}
            continue
        guard_stored(p, act, cmd)  # T-0901 review: a stored gate (fm smoke set cmd adds one too)
        t0 = time.monotonic()
        code, output = c.run_command(p.root, cmd, args.timeout if args.timeout > 0 else None, env=env)
        if code and time.monotonic() - t0 <= 120:  # a slow gate isn't rerun: its failure costs enough already
            code2, output2 = c.run_command(p.root, cmd, args.timeout if args.timeout > 0 else None, env=env)
            if not code2 and _flaky_count(p, cmd) >= 2:  # a racy bug passes half the time: not "flaky" forever
                notes[cmd] = "flaky again (failed first in 3+ recent runs): treated as a failure; find the race"
            elif not code2:
                reruns.append((cmd, code, output))  # T-0274 review: the names from the failing first run
                code, output, notes[cmd] = 0, output2, "flaky: failed, then passed on a rerun"
            elif before.get(cmd):
                notes[cmd] = "pre-existing: it also failed before this task"
        env = failure_class(output) if code else None
        if env:  # R4: say when a failure is the environment's, not a regression in the code
            notes[cmd] = "; ".join(filter(None, [notes.get(cmd), env]))
        results.append((cmd, code, output, time.monotonic() - t0))
        slow = None if code else _slower(p, cmd, results[-1][3])
        if slow:
            notes[cmd] = slow
        if code and args.fail_fast and len(results) < len(checks):  # the red loop: the first failure is enough
            notes[cmd] = "; ".join(filter(None, [notes.get(cmd), f"--fail-fast: {len(checks) - len(results)} "
                                                                 f"later gate(s) not run"]))
            break
    results.sort(key=lambda r: checks.index(r[0]))  # T-0467: listed (and cached, _cached_pass) in configured order
    after = c.worktree_id(p.root) if tree else None
    wrote = bool(tree) and after != tree  # R2: a check should only read; one of these wrote (formatter, codegen…)
    tree = after or tree
    failed = sum(1 for _, code, _, _ in results if code)
    if failed:
        c.hints_reset(p)  # T-0250: a quieted hint gets its detail back when a gate fails
    try:  # T-0272: which tests failed, and which failed then passed on this same tree (a note; the verdict stands)
        flaky = c.note_flakes(p, reruns + [(cmd, code, output) for cmd, code, output, _ in results if cmd not in skipped],
                              tree, commands=checks)
    except Exception:
        flaky = []
    try:  # T-0613: a failing gate is fingerprinted into failure memory, as a failing Bash run is
        import fmrecall
        for cmd, code, output, _ in results:
            if code and cmd not in skipped:
                fmrecall.note_failure(p, act.id if act else None, output)
    except Exception:
        pass  # failure memory is a hint; the gate's verdict stands either way
    c.log_event(p, "check_run", task=act.id if act else None, session=session(),
                data={"tree": tree, "env": c.env_id(), "results": [{"cmd": cmd, "exit": code, "s": round(s, 1), "note": notes.get(cmd),
                                                                     **({"failing": c.failing_tests(out_)[:50]} if code else {}),
                                                                     **skipped.get(cmd, {})} for cmd, code, out_, s in results],
                      **({"skip_tests": sorted(skip)} if skip else {}),
                      **({"sentinel": True} if os.environ.get("FOREMAN_SENTINEL_RUN") else {})})
    try:  # T-1117: a red gate is someone's task without anyone deciding so
        sentinel = os.environ.get("FOREMAN_SENTINEL_RUN") and os.environ.get("FOREMAN_SENTINEL_TREE") == tree
        sure = not wrote and (not act or bool(sentinel))  # mid-task red may be its own; a sentinel only on its tree
        base_lines = _baseline(p, [r for r in results if r[0] not in skipped and  # red-first work: only a failure fm
                                   (sure or str(notes.get(r[0]) or "").startswith("pre-existing"))])  # check knows predates it
    except Exception as e:  # the verdict stands; the capture is a convenience
        base_lines = [f"baseline capture failed: {e}"]
    if args.evidence:  # one run, one verdict: a later passing gate can't hide an earlier failing one
        shown = [r for r in results if r[1]] or results
        result = (f"✗ exit 1 · {failed} of {len(results)} failed: " if failed else
                  f"exit 0 · {len(results)} passed: ") + (f"({left_out}) " if left_out else "") + "; ".join(
            f"{cmd} → {c.run_result(code, output)}" + (f" ({notes[cmd]})" if cmd in notes else "")
            for cmd, code, output, _ in shown)
        mutate(p, args.evidence, lambda b: b.add_evidence("fm check: " + "; ".join(checks), result[:600],
                                                          step=args.step, ac=args.ac, tree=tree, ran=True),
               "evidence", {"step": args.step, "ac": args.ac, "cmd": "fm check", "result": result[:300]})
    lines = []
    for cmd, code, output, secs in results:
        lines.append(f"{'✗' if code else '✓'} {cmd} → {c.run_result(code, output)} ({secs:.1f} s)"
                     + (f" — {notes[cmd]}" if cmd in notes else ""))
        lines += ["    " + l for l in output.rstrip().splitlines()[-10:]] if code else []
    lines += [f"! {x}" for x in flaky + ([left_out] if left_out else []) + base_lines]
    if wrote:
        lines.append("! the gates changed the working tree: one of them writes files (a check should only read)")
    out(args, {"results": [{"cmd": cmd, "exit": code, "seconds": round(s, 1), "note": notes.get(cmd)}
                           for cmd, code, _, s in results], "failed": failed, "wrote": wrote, "skipped_tests": skip},
        "\n".join(lines))
    return 1 if failed else 0


def _baseline(p, results):
    """T-1117: a full-gate run that is red captures one urgent FIX naming the failing tests (one open task per gate and
    failing set; an environment failure isn't the code's, and a gate that names no failing test, a linter or fm doctor,
    says what's wrong itself); a green gate names an open baseline task it turned green. The caller passes only the
    runs it can vouch for: an unchanged tree, and no task mid-work unless the failure predates it."""
    import fmeco
    lines, open_ = [], [b for b in c.load_briefs(p) if b.meta.get("baseline") and b.status not in c.CLOSED]
    for cmd, code, output, _ in results:
        if not code:
            lines += [f"baseline is green again: {b.id} (fm task finish {b.id} once its criterion runs green)"
                      for b in open_ if f"`{cmd}`" in b.section("Raw request")]
            continue
        names = c.failing_tests(output)
        if not names or failure_class(output) or set(names) <= _known_flaky(p):  # a flake under load isn't a baseline
            continue
        head = f"Baseline red: `{cmd}` fails {', '.join(names[:6])}{' …' if len(names) > 6 else ''}."
        text = head + " Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing)."
        same = next((b for b in open_ if head in b.section("Raw request")), None)
        b, new = (same, False) if same else fmeco.capture_once(p, text, "FIX", "baseline")
        if new:
            mutate(p, b.id, lambda x: x.meta.update(priority="urgent", baseline=True), "baseline_red",
                   {"cmd": c.fit(cmd, 200), "failing": names[:20]})
            lines.append(f"baseline red: captured {b.id} (urgent): {c.fit(text, 160)}")
        else:
            lines.append(f"baseline still red: {b.id}")
    return lines


# ponytail: a denylist over declared checks only (criteria's verify commands); an allowlist if one ever slips through
_SIDE_EFFECTS = re.compile(r"\b(push|deploy|publish|release|install|uninstall|merge|commit|tag|rm|mv|cp|curl|wget|ssh|"
                           r"scp|rsync|docker|kubectl|terraform|fm|chmod|chown|dd|truncate|tee|kill|pkill|reset|"
                           r"checkout|migrate|seed|drop)\b|\s-i\b|--(fix|write|in-place|apply)\b|>|\b(python3?|node|ruby|"
                           r"perl|bash|sh) -[ce]\b")


def cmd_sentinel(args):
    """Re-run the checks that passed for the last N finished tasks (their [ran] evidence) and report any that fail
    now: a later change broke what an earlier task proved. Commands with side effects are skipped."""
    p = resolve(args)
    done = sorted((b for b in c.load_briefs(p, include_archive=True) if b.status == "done"),
                  key=lambda b: str(b.meta.get("updated", "")), reverse=True)[:args.last]
    cmds, skipped = {}, 0
    for b in done:
        for line in b.evidence():  # criteria checks only: steps record work (pushes, migrations) as well as checks
            if line.startswith("- (ac ") and c._RAN_MARK in line and "` → exit 0" in line:
                cmd = line.split("`", 2)[1]
                if _SIDE_EFFECTS.search(cmd):
                    skipped += 1
                elif cmd not in cmds:
                    cmds[cmd] = b.id
    checks = {}  # T-0489: assumptions a finished task rested on, with a command that stays true while they hold
    for b in done:
        for line in b.section(b.ASSUMPTIONS).splitlines():
            m = re.match(r"- \[\w+\] (.+?) — check: `(.+)`\s*$", line)
            if m and not _SIDE_EFFECTS.search(m.group(2)):
                checks.setdefault(m.group(2), (b.id, m.group(1)))
    results = []
    refused = []
    for cmd in list(cmds) + list(checks):  # T-0901: a stored check the guard refuses isn't rerun (all, before --max)
        try:
            guard_stored(p, None, cmd)
        except c.PolicyError:
            refused.append(cmd)
            cmds.pop(cmd, None)
            checks.pop(cmd, None)
    if refused:
        print(f"fm: warning: {len(refused)} stored check(s) the guard refuses weren't rerun: "
              + "; ".join(c.fit(x, 60) for x in refused[:3]), file=sys.stderr)
    for cmd, tid in list(cmds.items())[:args.max]:
        code, output = c.run_command(p.root, cmd, args.timeout)
        results.append({"cmd": cmd, "task": tid, "exit": code, "result": c.run_result(code, output)})
    for cmd, (tid, fact) in list(checks.items())[:args.max]:
        code, output = c.run_command(p.root, cmd, args.timeout)
        results.append({"cmd": cmd, "task": tid, "exit": code, "result": c.run_result(code, output), "assumption": fact})
        if code:
            title = _title(f"Assumption broke for {tid}: {fact}")
            if not any(x.title == title for x in c.load_briefs(p) if x.status not in c.CLOSED):
                with c.lock(p.dir):
                    nb = _create(p, title, "FIX", "S", "captured", raw=f"{title} (its check `{cmd}` now fails)",
                                 source="discovered", depends=[tid])
                    c.log_event(p, "capture", task=nb.id, data={"source": "sentinel", "assumption_of": tid})
                    c.regen_views(p)
    failed = [r for r in results if r["exit"]]
    c.log_event(p, "sentinel", data={"ran": len(results), "failed": [(r["task"], r["cmd"][:120]) for r in failed]},
                session=session())
    culprits = [_bisect(p, r, args.timeout) for r in failed if not r.get("assumption")] if \
        getattr(args, "bisect", False) else []  # T-0458
    out(args, {"results": results, "failed": len(failed), "skipped": skipped, "culprits": [x for x in culprits if x]},
        f"Sentinel: {len(results)} past check(s) from {len(done)} finished task(s); {len(failed)} failing now"
        + (f"; {skipped} with side effects skipped" if skipped else "") + "".join(
            f"\n  ✗ {r['task']}: " + (f"assumption \"{r['assumption']}\": " if r.get("assumption") else "")
            + f"{r['cmd']} → {r['result']}" for r in failed)
        + "".join(f"\n  ↳ broke at {x['sha'][:10]} {x['subject']}" + (f" ({x['task']})" if x["task"] else "")
                  + f": {x['captured']}" for x in culprits if x))
    return 1 if failed else 0


def first_bad(p, cmd, good, bad, timeout):
    """The first commit between good and bad where cmd fails (git bisect run in a throwaway worktree), or None."""
    import subprocess
    import tempfile
    if not good or not bad or good == bad:
        return None
    with tempfile.TemporaryDirectory(prefix="fm-bisect-") as t:
        wt = os.path.join(t, "wt")
        c._git(p.root, "worktree", "add", "--detach", "-q", wt, bad, timeout=120)
        if not os.path.isdir(wt):
            return None
        try:
            c._git(wt, "bisect", "start", bad, good, timeout=60)
            run = subprocess.run(["git", "-C", wt, "bisect", "run", "sh", "-c", cmd], capture_output=True,
                                 text=True, timeout=max(60, timeout * 20))
            m = re.search(r"^([0-9a-f]{40}) is the first '?bad'? commit", run.stdout, re.M)  # newer git quotes it
            c._git(wt, "bisect", "reset", timeout=60)
        finally:
            c._git(p.root, "worktree", "remove", "--force", wt, timeout=60)
            c._git(p.root, "worktree", "prune", timeout=30)
    return m.group(1) if m else None


def cmd_snapshots(args):
    """T-0884: the working files Foreman saved before a command discarded uncommitted work, newest first, each with
    the command that brings it back (it restores the saved files and leaves newer ones alone)."""
    rows = _snapshot_rows(resolve(args))
    text = "\n".join(f"{r['at']}  {r['sha']}  {'stash: ' if r['kind'] == 'stash' else 'before: '}{r['before']}\n"
                     f"  restore: {r['restore']}" for r in rows)
    return out(args, {"snapshots": rows}, text or _NO_SNAPSHOTS)


_NO_SNAPSHOTS = ("No snapshots: Foreman saves one before a command discards uncommitted work (git reset --hard, "
                 "checkout --, clean -f…).")


def _snapshot_rows(p):
    top = c.git_root(p.root)
    rows = []
    for ln in (c._git(top, "for-each-ref", "--sort=-refname", "--format=%(refname)%09%(objectname)%09%(subject)",
                      c.SNAPSHOTS, timeout=30) if top else "").splitlines():
        ref, sha, subject = (ln.split("\t", 2) + ["", ""])[:3]
        stash = ref.endswith("-stash")
        rows.append({"ref": ref, "sha": sha[:12], "at": ref[len(c.SNAPSHOTS):].split("-", 1)[0],
                     "before": c.plain(subject.removeprefix("Foreman snapshot before: ")),
                     "kind": "stash" if stash else "tree", "top": top,
                     "restore": c.restore_line(top, sha[:12], "stash" if stash else "tree")})
    return rows


def cmd_oops(args):
    """T-0960: the newest work snapshot and the command that brings it back; --apply runs it, after saving the files
    as they are now (that save is a snapshot too, so the restore can itself be undone)."""
    import shlex
    import subprocess
    rows = _snapshot_rows(resolve(args))
    if not rows:
        return out(args, {"snapshot": None}, _NO_SNAPSHOTS)
    r = rows[0]
    head = f"Newest snapshot {r['sha']} ({r['at']}), {'a stash' if r['kind'] == 'stash' else 'before: ' + r['before']}"
    if not args.apply:
        return out(args, {"snapshot": r, "applied": False},
                   f"{head}\n  restore: {r['restore']}\nfm oops --apply runs it: files in the snapshot are overwritten (the "
                   f"current ones are saved as a snapshot first, so a second fm oops --apply undoes it); files it "
                   f"doesn't have are left alone.")
    try:
        saved = c.snapshot(r["top"], f"fm oops --apply {r['sha']}", timeout=30)
    except RuntimeError as e:  # fail closed: nothing is restored over files that couldn't be saved first
        raise UsageError(f"couldn't save the current files first, so nothing was restored: {e}")
    run = c._git(r["top"], *shlex.split(r["restore"])[3:], timeout=120, proc=True)  # git -C TOP …: fmcore's runner
    if run.returncode:
        raise UsageError(f"{r['restore']} failed: {(run.stderr or run.stdout).strip()[-300:]}")
    return out(args, {"snapshot": r, "applied": True, "saved_first": saved},
               f"{head}: restored." + (f" The files as they were are snapshot {saved[0]} (fm snapshots)." if saved else ""))


def cmd_round(args):
    """T-0960: fm round close tags HEAD round-N and lists the finished tasks its commits name (a subject or a
    Foreman-Task trailer) since the previous round tag."""
    p = resolve(args)
    top = c.git_root(p.root)
    if not top or not c.git_head(top):
        raise UsageError("fm round close needs a git repo with a commit")
    nums = [int(t[6:]) for t in c._git(top, "tag", "--list", "round-*", timeout=10).split() if t[6:].isdigit()]
    prev = f"round-{max(nums)}" if nums else None
    tag = f"round-{max(nums, default=0) + 1}"
    got = c._git(top, "log", "--format=%s%x1f%b%x1e", f"{prev}..HEAD" if prev else "HEAD", timeout=60, proc=True)
    if got.returncode:
        raise UsageError(f"git log failed, so no round was tagged: {got.stderr.strip()[:200]}")
    log = got.stdout
    named = set()
    for rec in log.split("\x1e"):
        subj, _, body = rec.strip().partition("\x1f")
        if subj and not subj.startswith("Revert "):
            named |= set(re.findall(r"\bT-\d{4,}\b", subj)) | set(re.findall(r"Foreman-Task: (T-\d{4,})", body))
    done = [b for b in c.load_briefs(p, include_archive=True) if b.id in named and b.status == "done"]
    if c._git(top, "tag", tag, "HEAD", timeout=10, fail=None) is None:
        raise UsageError(f"git couldn't tag HEAD {tag}")
    lines = [f"Tagged HEAD {tag}: {len(done)} task(s) closed since {prev or 'the first commit'}."]
    lines += [f"  {b.id} {c.fit(b.title, 90)}" for b in done]
    return out(args, {"tag": tag, "since": prev, "tasks": [b.id for b in done]}, "\n".join(lines))


def cmd_show(args):
    """T-0960: one verb for "show me X": a task id → fm task show, an existing FILE[:LINE] → fm why, other words →
    fm recall."""
    first = args.words[0]
    if re.fullmatch(r"T-\d+(\.\d+)?", first, re.I):
        argv = ["task", "show", first.upper()]
    elif len(args.words) == 1 and os.path.isfile(re.sub(r":\d+$", "", first)):  # a folder or more words: recall
        argv = ["why", first]
    else:
        argv = ["recall", *args.words]
    return main(argv + (["--json"] if args.json else []) + (["-p", args.project] if getattr(args, "project", None) else []))


def cmd_bisect(args):
    """T-0612: the first commit where a check started failing, between --good (default: the active task's start
    commit) and HEAD, with the files it changed."""
    p = resolve(args)
    act = c.active_brief(c.load_briefs(p), p.lane)
    good = args.good or (act.meta.get("base") if act else None)
    if not good:
        raise UsageError("fm bisect --run CMD --good REF (no active task with a start commit to default to)")
    good = c._git(p.root, "rev-parse", "--verify", "-q", f"{good}^{{commit}}", timeout=10).strip()
    head = c._git(p.root, "rev-parse", "HEAD", timeout=10).strip()
    if not good:
        raise UsageError(f"{args.good} isn't a commit here")
    sha = first_bad(p, args.run, good, head, args.timeout)
    if not sha:
        return out(args, {"sha": None}, f"No first bad commit between {good[:10]} and HEAD for `{args.run}`: it fails "
                                        f"at the good end too, passes at HEAD, or bisect couldn't run.")
    subject = c.plain(c._git(p.root, "log", "-1", "--format=%s", sha, timeout=10).strip())[:120]
    files = c._git(p.root, "show", "--name-only", "--format=", sha, timeout=10).split()
    return out(args, {"sha": sha, "subject": subject, "files": files},
               f"First bad commit: {sha[:10]} {subject}\n  files: {', '.join(files[:12]) or '(none)'}\n  "
               f"git show {sha[:10]} for the diff")


def _bisect(p, r, timeout):
    """T-0458: git bisect, in a throwaway worktree, between the commit of the task that proved r's check (good) and
    HEAD (bad); the first bad commit is captured as a FIX naming it and its task. None when it can't run."""
    good = c._git(p.root, "log", "-1", "--format=%H", f"--grep=Foreman-Task: {r['task']}", timeout=30).strip()
    head = c._git(p.root, "rev-parse", "HEAD", timeout=10).strip()
    sha = first_bad(p, r["cmd"], good, head, timeout)
    if not sha:
        return None
    subject = c.plain(c._git(p.root, "log", "-1", "--format=%s", sha, timeout=10).strip())[:100]
    task = (re.findall(r"Foreman-Task: (T-\d+)", c._git(p.root, "log", "-1", "--format=%B", sha, timeout=10))
            or [None])[0]
    title = _title(f"Regression: {r['cmd'][:60]} broke at {sha[:10]} ({subject})")
    if not any(x.title == title for x in c.load_briefs(p) if x.status not in c.CLOSED):
        with c.lock(p.dir):
            nb = _create(p, title, "FIX", "S", "captured", raw=f"{title}; the check passed for {r['task']}"
                         + (f"; the commit is {task}'s" if task else ""), source="discovered",
                         depends=[x for x in [task] if x])
            c.log_event(p, "capture", task=nb.id, data={"source": "sentinel bisect", "sha": sha})
            c.regen_views(p)
        captured = nb.id
    else:
        captured = "already captured"
    return {"cmd": r["cmd"], "sha": sha, "subject": subject, "task": task, "captured": captured}


def _slower(p, cmd, secs, runs=5):
    """A gate that passed but took well over its usual time (median of its last passing runs): a perf regression or a
    test that started waiting on something."""
    past = []
    for e in reversed(c.ledger_tail(p, 2000)):
        for r in (e.get("data") or {}).get("results") or [] if e.get("event") == "check_run" else []:
            if r.get("cmd") == cmd and not r.get("exit") and r.get("s"):
                past.append(r["s"])
        if len(past) >= runs:
            break
    if len(past) < 3:
        return None
    med = sorted(past)[len(past) // 2]
    return f"slower: {secs:.1f} s vs a usual {med:.1f} s" if secs > 1.5 * med and secs - med > 2 else None


def _gate_order(p, checks, runs=20):
    """T-0467: the gates by failure odds per second of median runtime over their last `runs` real runs (skipped ones
    left out; a flaky first failure counts), so fail-fast stops sooner. Odds are (fails+1)/(runs+2): a gate that never
    failed still ranks by speed. A gate with no history runs first (unknown, may fail); none with any: as configured."""
    hist = {cmd: [] for cmd in checks}
    for e in reversed(c.ledger_tail(p, 2000)):
        for r in (e.get("data") or {}).get("results") or [] if e.get("event") == "check_run" else []:
            h = hist.get(r.get("cmd"))
            if h is not None and len(h) < runs and not r.get("since") and isinstance(r.get("s"), (int, float)):
                h.append((bool(r.get("exit")) or str(r.get("note") or "").startswith("flaky"), max(r["s"], 0.1)))

    def score(cmd):
        h = hist[cmd]
        if not h:
            return float("inf")
        med = sorted(s for _, s in h)[len(h) // 2]
        return (sum(f for f, _ in h) + 1) / (len(h) + 2) / med
    return sorted(checks, key=score, reverse=True)  # stable: equal scores keep the configured order


def _flaky_count(p, cmd, runs=20):
    """How many of the last `runs` fm check runs labelled this gate flaky."""
    seen = n = 0
    for e in reversed(c.ledger_tail(p, 2000)):
        if e.get("event") == "check_run":
            seen += 1
            n += any(r.get("cmd") == cmd and str(r.get("note") or "").startswith("flaky")
                     for r in (e.get("data") or {}).get("results") or [])
            if seen >= runs:
                break
    return n


_ENV_FAILURES = [
    (re.compile(r"ModuleNotFoundError|No module named|Cannot find module|command not found|error while loading shared "
                r"libraries|ImportError: cannot import name"), "environment: a module or tool is missing"),
    (re.compile(r"Connection refused|ECONNREFUSED|Could not resolve host|Temporary failure in name resolution|"
                r"Network is unreachable"), "environment: a network or service call failed"),
    (re.compile(r"Permission denied|EACCES"), "environment: permission denied"),
    (re.compile(r"No space left on device|ENOSPC"), "environment: disk full"),
]


def failure_class(output):
    """An environment cause visible in a failed run's output (missing tool, network, permissions, disk), or None."""
    tail = "\n".join((output or "").splitlines()[-60:])
    return next((why for rx, why in _ENV_FAILURES if rx.search(tail)), None)


CACHE_DAYS = 0.5  # a cached pass older than this reruns: time, caches and services outside the tree drift too


def _paths_unchanged(p, cmd, globs, tree):
    """T-0126: why a gate with declared paths can be skipped (its newest run passed, recently, in this environment, and
    nothing under its paths changed since), or None to run it.
    Returns (why, the real run's time, its tree): a skip records them, so a chain of skips still ages from, and diffs
    against, the run that really passed (review: re-stamping let a gate skip forever, past writes by other gates)."""
    if not globs or not tree:
        return None
    for e in reversed(c.ledger_tail(p, 2000)):
        d = e.get("data") or {} if e.get("event") == "check_run" else {}
        r = next((r for r in d.get("results") or [] if r.get("cmd") == cmd), None)
        if r is None:
            continue
        since, base = r.get("since") or e.get("ts"), r.get("tree") or d.get("tree")
        if r.get("exit") or d.get("env") != c.env_id() or not base or (c.age_days(since) or 0) >= CACHE_DAYS:
            return None
        top = c.git_root(p.root)  # --no-renames: a file moved out of the paths counts under its old name too
        names = c._git(top, "diff", "--name-only", "--no-renames", base, tree, timeout=60, fail=None)
        if names is None:
            return None  # its tree is gone: run it
        rel = [os.path.relpath(os.path.join(top, n), p.root) for n in names.splitlines() if n]
        if any(c.glob_match(n, g) for n in rel for g in globs):
            return None
        return (f"skipped: nothing under {', '.join(globs)} changed since its pass at {str(since)[11:16]} UTC",
                since, base)
    return None


def _run_py_names(cmd):
    """(tests folder, the test module names) of a `…tests/run.py NAME…` command, or None for any other command."""
    m = re.search(r"(\S*tests)/run\.py\b(.*)", cmd)
    return (m.group(1), re.findall(r"(?:^|[\s/'\"])(test_\w+)", m.group(2))) if m else None


def red_first_tests(p, act, gates):
    """T-1101: {module: task id} for the test files that are only another open task's red-first tests: its step-1
    run of a gate's own `tests/run.py NAME` (the same folder, inside the repo) failed, no run naming NAME passed since,
    the file is new (not at HEAD), and this task's scope and evidence don't name it. fm check leaves them out of
    run.py (FOREMAN_SKIP_TESTS) and says so."""
    # ponytail: one skip list for every run.py gate; per-gate lists if two suites ever share module names
    folder = lambda h: os.path.relpath(os.path.join(p.root, h[0]), p.root)  # noqa: E731
    folders = {f for g in gates if (h := _run_py_names(g)) and not (f := folder(h)).startswith("..")}
    if not folders:
        return {}
    cmd = lambda l: l.split("`", 2)[1] if l.count("`") >= 2 else ""  # noqa: E731
    mine = " ".join((act.meta.get("scope") or []) + [cmd(l) for l in act.evidence()]) if act else ""
    found = {}
    for b in c.load_briefs(p):
        if b.status not in c.OPEN or (act and b.id == act.id):
            continue
        red, green = {}, set()
        for line in b.evidence():
            hit = _run_py_names(cmd(line))
            if hit and "` → ✗ exit" not in line:
                green.update(hit[1])
            elif hit and folder(hit) in folders and (m := c._EV_RE.match(line)) and m.groups() == ("step", "1"):
                red.update({n: os.path.join(folder(hit), n + ".py") for n in hit[1]})
        for n, path in red.items():
            if n not in green and n not in mine and os.path.isfile(os.path.join(p.root, path)):
                found.setdefault(n, (b.id, path))
    if not found:
        return {}
    tracked = c._git(p.root, "ls-tree", "-r", "--name-only", "HEAD", "--", *{x for _, x in found.values()}, fail=None)
    if tracked is None:  # no git, or no commit yet: no telling a new file from a shared one, so nothing is left out
        return {}
    tracked = set(tracked.splitlines())
    return {n: tid for n, (tid, path) in found.items() if path not in tracked}


def _skip_env(skip):
    """The environment for a gate: FOREMAN_SKIP_TESTS only as fm check sets it, never inherited (a user's export, or
    an outer fm check's while the suite runs fm check)."""
    env = {k: v for k, v in os.environ.items() if k != "FOREMAN_SKIP_TESTS"}
    return dict(env, FOREMAN_SKIP_TESTS=",".join(sorted(skip))) if skip else env


def _left_out(skip):
    """The line fm check prints for what red_first_tests left out."""
    by = {}
    for n, tid in sorted(skip.items()):
        by.setdefault(tid, []).append(n)
    return "; ".join(f"skipped {len(ns)} test file(s) that are only task {tid}'s red-first tests: {', '.join(ns)}"
                     for tid, ns in by.items())


def _cached_pass(p, checks, tree, skip=()):
    """When the newest full fm check run was on this exact tree, with these gates, and all passed: its time."""
    if not tree:
        return None
    for e in reversed(c.ledger_tail(p, 2000)):
        if e.get("event") == "check_run":
            d = e.get("data") or {}
            rs = d.get("results") or []
            if d.get("tree") == tree and d.get("env") == c.env_id() and [r.get("cmd") for r in rs] == checks \
                    and (d.get("skip_tests") or []) == sorted(skip) \
                    and not any(r.get("exit") for r in rs) and (c.age_days(e.get("ts")) or 0) < CACHE_DAYS:
                return f"run at {str(e.get('ts', ''))[11:16]} UTC"
            return None
    return None


# T-0994: the test files a runner can run, by the words in its command; an unknown runner takes them all
_RUNNERS = (
    (re.compile(r"\b(?:python3?|pytest|unittest|tox|nox)\b|\.py\b"), (".py",)),
    (re.compile(r"\b(?:npm|npx|yarn|pnpm|bun|jest|vitest|mocha|node|deno)\b"),
     (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts")),
    (re.compile(r"\bgo\s+test\b"), (".go",)),
    (re.compile(r"\bcargo\b"), (".rs",)),
)


def _runnable(template, tests):
    """The tests `template` can run (a .tsx test handed to a Python runner ran nothing and read as a pass)."""
    for rx, exts in _RUNNERS:
        if rx.search(template):
            return [t for t in tests if t.endswith(exts)]
    return tests


def affected(p, b=None):
    """(command, tests, changed files) for the tests linked (fm map) to files changed since the task started, with the
    project's template; command None when no test is linked. fm check --affected and the ambient runner (T-0705)."""
    import fmmap
    import shlex
    act = b or c.active_brief(c.load_briefs(p), p.lane)  # T-1117 review: the closing task's base, active or not
    base = (c.task_base(p.root, act) if act else None) or "HEAD"
    changed = set(fmmap.changed(p.root, base))
    m = fmmap.load(p)
    # T-0875: a changed test file always runs, linked or not (a new one isn't in the map until it's committed); by its
    # name, so a helper under tests/ isn't run alone (pytest exits 5 when it collects nothing)
    own = {f for f in changed if c.TESTISH.search(os.path.basename(f)) and c.CODE.search(f)}
    # T-0952: a test that historically changes with a changed file (the map's co-change pairs, either way round):
    # hooks.json has no test named after it, but the wiring tests change with it
    istest = lambda f: c.TESTISH.search(os.path.basename(f)) and c.CODE.search(f)  # noqa: E731
    pairs = m.get("pairs") or {}
    paired = {t for f in changed for t in pairs.get(f, []) if istest(t)} | {
        a for a, bs in pairs.items() if istest(a) and any(b in changed for b in bs)}
    template = c.read_meta(p).get("affected") or ("python3 -m pytest -q {tests}" if any("pytest" in g for g in m["gates"]) else "")
    if not template:
        raise UsageError("no affected-tests command: fm check affected '<cmd with {tests} or {names}>'")
    tests = _runnable(template, sorted(set(fmmap.tests_for(m, sorted(changed))) | own | paired))
    cmd = template.replace("{tests}", " ".join(shlex.quote(t) for t in tests)).replace(
        "{names}", " ".join(shlex.quote(os.path.basename(t).rsplit(".", 1)[0]) for t in tests)) if tests else None
    return cmd, tests, changed


def _check_affected(p, args):
    """Only the tests linked (fm map) to files changed since the task started, with the project's template."""
    cmd, tests, changed = affected(p)
    act = c.active_brief(c.load_briefs(p), p.lane)
    if cmd:
        guard_stored(p, act, cmd)  # T-0901: the template is a stored command
    if not tests:
        return out(args, {"tests": [], "changed": sorted(changed)},
                   f"No tests linked to the {len(changed)} changed file(s); run the full gates: fm check") or 0
    skip = red_first_tests(p, act, [cmd])  # T-1101: as the full gates do
    code, output = c.run_command(p.root, cmd, args.timeout if args.timeout > 0 else None, env=_skip_env(skip))
    out(args, {"tests": tests, "exit": code, "changed": sorted(changed), "skipped_tests": skip},
        f"{'✗' if code else '✓'} affected tests only ({len(tests)}): {cmd} → {c.run_result(code, output)}"
        + (f"\n! {_left_out(skip)}" if skip else "")
        + "\n(the full gates still decide before commit and done: fm check)")
    return 1 if code else 0


def _last_check_results(p, task):
    """{gate: failed?} from the newest fm check run recorded before `task` (another task's, or none's)."""
    for e in reversed(c.ledger_tail(p, 2000)):
        if e.get("event") == "check_run" and e.get("task") != task:
            return {r.get("cmd"): bool(r.get("exit")) for r in (e.get("data") or {}).get("results") or []}
    return {}


_LENS_TPL = re.compile(r"^\*\*(\w+)\*\* — context: (.+?)\n> (.+?)$", re.M)
_REVIEW_OUT = ("Verify each finding by reading the code (cite file:line). Output one section per lens, \"## <lens>: ok | "
               "changes needed\", each with its findings ranked HIGH/MEDIUM/LOW with file:line, the concrete scenario, "
               "a reproducer (the command, input or test that shows it; without one it's a lead, not a finding: "
               "T-0651) and a fix; then \"## Not checked\". Only verified findings. Keep each finding on one "
               "HIGH/MEDIUM/LOW line, then give ReportFindings' fields under it: file (repo-relative), line, summary "
               "(one sentence), short_summary (<=60 chars), failure_scenario (concrete inputs/state -> wrong output), "
               "category (kebab-case), verdict (CONFIRMED|PLAUSIBLE, optional); most severe first.")


_FINDING = re.compile(r"(?m)^[ \t]*(?:[-*]|\d+[.)]?)?[ \t]*(?:\*\*|#+[ \t]*)?\[?(?:CRIT(?:ICAL)?|HIGH|MED(?:IUM)?)\b[\s*:—–\]-]*(.+)$")
PAST_FINDINGS = 6  # per lens, newest reviews first


def _past_findings(p, lens):
    """Headlines of the CRITICAL/HIGH/MEDIUM findings earlier reviews of this project saved for this lens (research
    files named with it, e.g. t0018-r4-adversary), newest first: the weak spots a new review should check again."""
    folder = os.path.join(p.dir, "research")
    try:
        names = [n for n in os.listdir(folder) if n.endswith(".md") and ({lens, "review"} & set(n[:-3].split("-")))
                 and not os.path.islink(os.path.join(folder, n)) and os.path.isfile(os.path.join(folder, n))]
        names.sort(key=lambda n: os.path.getmtime(os.path.join(folder, n)), reverse=True)
    except OSError:
        return []
    seen = []
    for n in names:
        try:
            report = _agent_report(os.path.join(folder, n))
        except OSError:
            continue
        if lens not in n[:-3].split("-"):  # a combined review: only its section for this lens
            m = re.search(rf"(?ms)^## {re.escape(lens)}\b.*?(?=^## |\Z)", report)
            report = m.group(0) if m else ""
        for m in _FINDING.finditer(report):
            text = m.group(1).replace("**", "").replace("`", "").replace(p.root + os.sep, "")
            line = c.fit(c.plain(text).strip(), 200)
            if line and line not in seen:
                seen.append(line)
            if len(seen) >= PAST_FINDINGS:
                return seen
    return seen


def _audit_scan(p, args):
    """fm audit scan [--base REV] (R4): the mechanical pre-audit over any diff (a branch, a PR checkout), no task
    needed; base defaults to where the branch left main. Exit 1 when it finds something."""
    import fmmap
    if not c.git_root(p.root):
        raise UsageError("fm audit scan needs a git repository")
    base = args.base or next((b for ref in ("origin/HEAD", "origin/main", "main", "origin/master", "master")
                              if (b := c._git(p.root, "merge-base", "HEAD", ref, timeout=10).strip())), "HEAD")
    diff = c._git(p.root, "diff", base, timeout=120)
    files = sorted(set(re.findall(r"(?m)^diff --git a/.+? b/(.+)$", diff)))
    try:
        m = fmmap.load(p)
    except Exception:
        m = None
    found = fmmap.pre_audit(p.root, diff, files, m)
    out(args, {"base": base, "files": files, "findings": found},
        f"Pre-audit of {len(files)} file(s) since {base[:12]}: " + (
            "\n".join(["", *(f"- {x}" for x in found)]) if found else "nothing mechanical found"))
    return 1 if found else 0


# T-0216: --split's reviewers, from skills/routing.json (T-0252); lenses in no group share one more reviewer
SPLIT_GROUPS = tuple(tuple(g) for g in c.routing().get("review_groups") or ())
READ_PARTS = 1500  # T-0983: diff lines past which the reviewer is told to read the diff in parts
SPLIT_SUGGEST = 800  # diff lines past which an L review suggests --split


_BULK = re.compile(r"(^|/)(fixtures?|testdata|__snapshots__)/|(^|/)(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|"
                   r"Cargo\.lock|poetry\.lock|go\.sum|uv\.lock)$|\.lock$|\.min\.(js|css)$")
CONTEXT_MAX = 200


def _compact_diff(diff):
    """T-0723 (reviewers read 3.2M tokens of diffs in 30 days): a file whose hunks repeat another's (synced copies)
    becomes one line naming the first, context lines are cut at CONTEXT_MAX characters, and fixtures and lockfiles
    are listed with their +/- counts. Changed lines always stay whole."""
    out, seen = [], {}
    for blk in re.split(r"(?m)^(?=diff --git )", diff):
        m = re.match(r"diff --git a/(.+?) b/(.+)\n", blk)
        hunks = blk[blk.find("\n@@") + 1:] if m and "\n@@" in blk else ""
        if not m or not hunks:
            out.append(blk)
            continue
        path = m.group(2)
        lines = hunks.splitlines()
        if _BULK.search(path):
            plus = sum(1 for x in lines if x.startswith("+"))
            minus = sum(1 for x in lines if x.startswith("-"))
            out.append(f"diff --git a/{path} b/{path}\n{path}: a fixture or lockfile, +{plus} −{minus} lines, left out\n")
            continue
        if hunks in seen:
            out.append(f"diff --git a/{path} b/{path}\n{path}: the same change as {seen[hunks]}\n")
            continue
        seen[hunks] = path
        cut = [x[:CONTEXT_MAX] + "…" if x.startswith(" ") and len(x) > CONTEXT_MAX else x for x in lines]
        out.append(blk[:blk.find("\n@@") + 1] + "\n".join(cut) + ("\n" if blk.endswith("\n") else ""))
    return "".join(out)


def _without_secrets(root, diff):
    """T-0413: the frozen diff a reviewer reads holds no secret: a credential file (the guard's names: .env*, *.pem …)
    keeps its header lines, not its contents, and key=value secrets elsewhere are redacted."""
    import types
    import fmguard
    ctx = types.SimpleNamespace(home=os.path.expanduser("~"), scratch=())
    out = []
    for block in re.split(r"(?m)^(?=diff --git )", diff):
        names = re.findall(r'(?m)^(?:diff --git "?a/.+? "?b/|--- "?a/|\+\+\+ "?b/|(?:rename|copy) (?:from|to) "?)(.+?)"?\t?$',
                           block)  # git quotes a name with unusual characters
        if any(fmguard._is_credential(os.path.join(root, n), ctx) for n in names):
            lines = block.splitlines(keepends=True)
            cut = next((i for i, x in enumerate(lines) if x.startswith(("@@", "Binary files", "GIT binary patch"))),
                       len(lines))
            block = "".join(lines[:cut]) + ("(contents left out: a credential file)\n" if cut < len(lines) else "")
        out.append(c.redact(block))
    return "".join(out)


def cmd_audit(args):
    """fm audit prep ID: freeze the diff since the task started and print one reviewer brief per lens."""
    import subprocess
    p = resolve(args)
    if args.action == "scan":
        return _audit_scan(p, args)
    if not args.id:
        raise UsageError("fm audit prep needs a task id")
    b = need_brief(p, args.id)
    if getattr(args, "forge", False):  # T-0652: try to break the checks before trusting them
        return _forge_brief(p, b, args)
    base = args.base or c.task_base(p.root, b)
    if not base:
        raise UsageError(f"{b.id} has no start commit on record (focused before fm kept one): "
                         f"fm audit prep {b.id} --base <rev>")
    tree = c.worktree_tree(p.root)
    if not tree:
        raise UsageError("fm audit prep needs a git repository")
    branch, upto = b.meta.get("lane_branch"), "working tree, untracked files included"
    if branch and not args.base and c._git(p.root, "rev-parse", "--verify", "-q", f"refs/heads/{branch}", fail=None):
        # T-0718: a builder's work is on its branch: from where it left main, not main's own commits since
        base, tree, upto = c._git(p.root, "merge-base", "HEAD", branch).strip() or base, branch, f"branch {branch}"
    try:
        r = subprocess.run(["git", "-C", p.root, "diff", base, tree], capture_output=True, text=True, errors="replace",
                           timeout=300)
    except subprocess.TimeoutExpired:
        raise UsageError(f"git diff {base[:12]} took over 5 minutes; narrow it with --base <a later rev>")
    if r.returncode:
        raise UsageError(f"git diff {base} failed: {r.stderr.strip()[:200]}")
    path = os.path.join(p.dir, "audits", f"{b.id}.diff")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    shown = _compact_diff(_without_secrets(p.root, r.stdout))  # the pre-audit reads the raw diff (T-0723)
    c.write_atomic(path, shown)
    shown_lines = shown.count("\n")  # T-0983: what the reviewer reads, not the raw diff
    with open(os.path.join(c.PLUGIN_ROOT, "skills", "intake", "references", "audit.md"), encoding="utf-8") as f:
        ref = f.read()
    templates = {m.group(1): (m.group(2), m.group(3)) for m in _LENS_TPL.finditer(ref)}
    import fmmap
    files = sorted(set(re.findall(r"(?m)^diff --git a/.+? b/(.+)$", r.stdout)))
    try:
        m = fmmap.load(p)
    except Exception:  # the map is a hint: it never stops an audit
        m = None
    found = fmmap.pre_audit(p.root, r.stdout, files, m)
    risky = ["adversary"] if c.sensitive(files, r.stdout) else []
    lenses = args.lens or (["self"] + risky if b.tier == "S" else [x for x in c.AUDIT_LENSES if x != "self"])
    missing = [x for x in lenses if x != "self" and x not in templates]
    if missing:
        raise UsageError(f"references/audit.md has no template for {', '.join(missing)} (its lens format changed?)")
    head = (f"Read-only audit of task {b.id} \"{b.title}\" ({b.type} {b.tier}) in {p.root}.\n"
            f"Diff to review: {path} (git diff {base[:12]} → {upto}; "
            f"{shown_lines} lines).")
    if shown_lines > READ_PARTS:  # T-0983: one Read returns ~2000 lines; leave room for the line prefixes
        head += (f"\nThe diff is over {READ_PARTS} lines, too long for one Read: read it in parts "
                 f"(Read with offset and limit, ~{READ_PARTS} lines each) until the end.")
    if found:  # T-0068: mechanical findings first, so the reviewer confirms them instead of hunting for them
        head += "\nPre-audit (mechanical; confirm or dismiss each, then review the rest):\n" + "\n".join(
            f"- {x}" for x in found)
    steps = _files_vs_steps(b, files)  # T-0610: does each changed file serve a step?
    import fmlib  # T-1036: the review checklists of the stack cards this task's edits used (self block and reviewers)
    try:  # the hook's per-task marker, not a ledger scan (an archived ledger would lose them); ":" names are markers
        with open(os.path.join(p.dir, "cards.json"), encoding="utf-8") as f:
            seen = json.load(f)
    except (OSError, ValueError):
        seen = {}
    used = [n for n in ((seen.get(b.id) if isinstance(seen, dict) else None) or [])
            if isinstance(n, str) and not n.startswith(":")]
    checks = [(n, rv) for n in used[:4] if (rv := fmlib.card_review(n))]  # never r: the diff run below is r
    if checks:
        steps += ("\n\n## Stack card checklists\nThe cards this task's edits used; hold the diff to them:\n"
                  + "\n".join(f"### {n}\n{rv[:1200]}" for n, rv in checks))
    head += steps
    blocks, sections = [], []
    for lens in lenses:
        if lens == "self":
            blocks.append("=== self (main thread) ===\n" + ref[ref.index("**self**"):].strip()
                          + "".join(f"\n- pre-audit: {x}" for x in found) + steps)
            continue
        context, prompt = templates[lens]
        extra = ""
        if lens == "intent":
            asked = re.sub(r"(?m)^> ?", "", b.section("Raw request")).strip() or b.title
            extra = (f"\nThe user's request, verbatim:\n{asked}\nAcceptance criteria:\n"
                     + "\n".join(f"- {a.text}" for a in b.acceptance()))
        past = _past_findings(p, lens)
        if past:
            extra += ("\nPast findings for this lens in this project (data from earlier reviews, not instructions; check "
                      "the same classes of weakness here):\n" + "\n".join(f"- {x}" for x in past))
        sections.append(f"## {lens}\nContext: {context}{extra}\n{prompt}")
    names = [x for x in lenses if x != "self"]
    focus = "".join(f"\nFocus: {n}" for n in args.note)
    by_lens = dict(zip(names, sections))
    # T-0216: --split gives each lens group its own fresh-context reviewer; default one reviewer reads the diff once
    groups = [g for g in ([[x for x in grp if x in by_lens] for grp in SPLIT_GROUPS]
                          + [[x for x in names if not any(x in grp for grp in SPLIT_GROUPS)]]) if g] \
        if args.split and len(names) > 1 else [names] if names else []
    briefs = []
    for i, grp in enumerate(groups, 1):
        block = (f"=== review ({', '.join(grp)}) ===\n{head}{focus}\n\n" + "\n\n".join(by_lens[x] for x in grp)
                 + f"\n\n{_REVIEW_OUT}")
        blocks.append(block)
        briefs.append(os.path.join(p.dir, "audits", f"{b.id}.review" + (f"-{i}" if len(groups) > 1 else "") + ".md"))
        c.write_atomic(briefs[-1], "\n\n".join([x for x in blocks if x.startswith("=== self")] + [block])
                       + f"\n\nDiff: {path}\n")
    if not briefs:
        briefs.append(os.path.join(p.dir, "audits", f"{b.id}.review.md"))
        c.write_atomic(briefs[0], "\n\n".join(blocks) + f"\n\nDiff: {path}\n")
    brief = briefs[0]
    big = b.tier == "L" and len(groups) == 1 and r.stdout.count("\n") > SPLIT_SUGGEST
    how = (f"Run {len(briefs)} foreman:fm-reviewer subagents in parallel, one per brief, each with the prompt \"Read "
           f"<brief> and do the review it describes.\": {', '.join(briefs)}; save each reply with fm research add "
           f"{b.id}-review-N --from-agent <its output file>; record each lens with fm task audit {b.id} <lens> …"
           if len(briefs) > 1 else
           f"Run one foreman:fm-reviewer subagent with the prompt \"Read {brief} and do the review it describes.\"; "
           f"save its reply with fm research add {b.id}-review --from-agent <its output file>; record each lens with "
           f"fm task audit {b.id} <lens> …" + (f" (a {r.stdout.count(chr(10))}-line L diff: fm audit prep {b.id} --split "
                                               f"gives each lens group a fresh reviewer, in parallel)" if big else "")
           if sections else f"Record it with fm task audit {b.id} self …")
    if sections:  # T-0780: verified findings reach the host's review UI before they become lenses
        how += "\nReport the verified findings with ReportFindings (empty list if none) before recording lenses."
    try:  # T-0276: installed review skills that fit a lens; their findings count as that lens
        import fmplugins
        fit = fmplugins.lens_skills(p, [x for x in lenses if x != "self"])
    except Exception:
        fit = {}
    if fit and not args.print:
        how += ("\nInstalled review skills that fit a lens (run one on the diff and record what it finds as that lens):"
                + "".join(f"\n  {lens}: {', '.join(names)} — fm task audit {b.id} {lens} \"{names[0]}\" \"<result>\""
                          for lens, names in fit.items()))
    # the brief goes to a file: printed, it would be paid for twice (here and in the reviewer's prompt)
    out(args, {"diff": path, "base": base, "lenses": lenses, "brief": brief, "briefs": briefs, "pre_audit": found,
               "lens_skills": fit},
        ("\n\n".join(blocks) + f"\n\nDiff: {path}\n" if args.print else
         f"Review brief ({', '.join(lenses)}; {sum(map(len, blocks))} chars): {brief}\nDiff: {path}\n"
         + "".join(f"Pre-audit: {x}\n" for x in found)) + how)


def _sync_in(args):
    """fm sync: a pull or merge changed .foreman/, so take it in before this command works on the old copy (cheap when
    nothing came in: a hash per mirrored file). Never in the way of the command itself."""
    if getattr(args, "cmd", None) == "sync":
        return
    try:
        p = resolve(args, create=False)
        if not c.read_meta(p).get("sync"):
            return
        import fmsync
        if fmsync.incoming(p):
            with c.lock(p.dir):
                fmsync.import_(p)
                c.regen_views(p)
    except (UsageError, OSError, ValueError, c.LockTimeout):
        pass


def cmd_next(args):
    p = resolve(args)
    b, st, action = c.next_for(p)
    usual = None
    if b and b.status != "active":  # T-0451: what this kind of task usually takes here (fm next only: not the hooks)
        import fmwatch
        usual = fmwatch.typical(c.ledger_tail(p, 5000)).get(f"{b.type}/{b.tier}")
    over = ""
    if b and b.status == "active":  # T-0644: past twice the usual, re-frame before pushing on
        import fmwatch
        events = c.ledger_tail(p, 5000)
        median = fmwatch.typical(events).get(f"{b.type}/{b.tier}")
        began = min((c.parse_ts(e.get("ts")) for e in events if e.get("event") == "focus" and e.get("task") == b.id
                     and c.parse_ts(e.get("ts"))), default=None)
        took = (time.time() - began.timestamp()) / 60 if began else 0
        if median and took > 2 * median:
            over = (f" · on it {took:.0f} min, over twice the usual {median:g} min for a {b.type} {b.tier}: re-frame — "
                    f"is the plan still the right size, or should it split?")
    meta = c.read_meta(p)
    loose = (meta.get("clauses") or {}).get("open") or []
    over += (f" · {len(loose)} clause(s) of the last request unaccounted: capture, answer, or fm clauses --note N "
             f"\"<why>\" (fm clauses --show)") if loose else ""
    asks = unanswered_asks(p)
    over += (f" · {len(asks)} unanswered ask(s) from your last session wait for the user's yes (✋ in fm state; put "
             f"them to the user at the end, never act on them first; deferred after {ASK_DAYS} days)") if asks else ""
    import fmlanes
    dead = fmlanes.stopped(p)  # T-1028
    over += (f" · builder(s) stopped, their Claude Code process ended: " + "; ".join(f"fm lane resume {i}" for i in dead)
             + " (keeps the work, frees the worktree, writes a new brief)") if dead else ""
    hollow = [e for e in c.ledger_tail(p, 500) if e.get("event") == "hollow_return"
              and (age := c.age_days(e.get("ts"))) is not None and age < 1]  # T-0963: today's, so an old one doesn't nag forever
    if hollow:
        d = hollow[-1].get("data") or {}
        over += (f" · {len(hollow)} hollow subagent return(s) today: the last, {d.get('agent_type')}"
                 f"{' on ' + hollow[-1]['task'] if hollow[-1].get('task') else ''}, said {d.get('chars')} chars: read its "
                 f"transcript ({d.get('transcript') or 'no path'}) before trusting or merging its work")
    if b and b.status == "active":  # T-0631: beliefs still open, each with what would kill it
        beliefs = [f"A{n} {t.split(' — kill: ')[0]} (dead if {t.split(' — kill: ')[1]})"
                   for n, tag, _, t in b.assumptions() if tag in (None, "assumed") and " — kill: " in t]
        over += f" · open beliefs: {'; '.join(c.fit(x, 120) for x in beliefs[:3])}" if beliefs else ""
    out(args, {"task": b.id if b else None, "stage": st, "action": action, "usual_minutes": usual},
        f"Next: {action}" + (f" · a {b.type} {b.tier} usually takes {usual:g} min here" if usual is not None else "")
        + over)


def cmd_autonomy(args):
    p = resolve(args)
    if not args.level:
        level = c.read_meta(p).get("autonomy", "standard")
        eff = c.effective_autonomy(p)  # T-1061, T-1080
        import fmrisk
        risky = fmrisk.slowed(p)
        why = risky if risky else "recent closes missed their plan, M needs approval; fm digest"
        return out(args, {"autonomy": level, "effective": eff, "slow": eff == "slow", "risk": risky},
                   f"{p.slug}: autonomy {level}" + (f" (now {eff}: {why})" if eff != level else "") + ".")
    c.update_meta(p, autonomy=args.level)
    with c.lock(p.dir):
        c.log_event(p, "autonomy", data={"level": args.level}, session=session())
        c.regen_views(p)
    out(args, {"autonomy": args.level}, f"{p.slug}: autonomy {args.level}.")


def lazy(module, func):
    def run(args):
        return getattr(__import__(module), func)(args)
    return run


# ---------------------------------------------------------------- parser

_ARGV = []  # the arguments main() is parsing


def _no_ids(text):
    """T-0873: help without the ticket ids its source keeps for provenance ("(T-0594)", ", T-0375)", "T-0368: ")."""
    text = re.sub(r"\s*\((?:T-\d{3,4}(?:,\s*|\s*\+\s*)?)+\)", "", text)
    text = re.sub(r"[,;]\s*T-\d{3,4}(?=\))", "", text)
    text = re.sub(r"\bT-\d{3,4}\b:?\s*", "", text)
    return re.sub(r"\(\s*\)|\(\s+", lambda m: "" if m.group(0).strip() == "()" else "(", text)


class _Parser(argparse.ArgumentParser):
    """No abbreviated long options (subparsers inherit the class): `--allo core` must not slip past the guard."""

    def __init__(self, *args, **kw):
        kw["allow_abbrev"] = False
        super().__init__(*args, **kw)

    def format_help(self):
        return _no_ids(super().format_help())

    def error(self, message):
        """T-0273: an unknown command or flag names the nearest real one (a wrong guess costs a retry otherwise)."""
        import difflib
        flags = sorted({o for prs in _all_parsers(build_parser()) for o in prs._option_string_actions})  # every
        # command's and the root's (-p); sorted, so the nearest match doesn't depend on set order
        unknown = [t.partition("=")[0] for t in _ARGV if re.match(r"--?[A-Za-z]", t) and t.partition("=")[0] not in flags]
        near = [m for t in unknown for m in difflib.get_close_matches(t, flags, n=1)][:1]  # a mistyped flag shifts the
        bad = re.search(r"invalid choice: '([^']*)' \(choose from (.+)\)", message)    # positionals: name it first
        if bad and not near:
            near = difflib.get_close_matches(bad.group(1), re.findall(r"'?([\w-]+)'?", bad.group(2)), n=1)
        super().error(message + (f" — did you mean {near[0]}?" if near else ""))


def _all_parsers(parser):
    """The parser and every subparser under it (for the nearest flag to an unrecognized one)."""
    out = [parser]
    for a in parser._actions:
        if isinstance(a, argparse._SubParsersAction):
            for sub in dict.fromkeys(a.choices.values()):
                out += _all_parsers(sub)
    return out


# T-0094: fm help's tiers, everyday first; every command is in exactly one (test_help holds that)
HELP_TIERS = [
    ("Every task", "next capture clauses intake batch task focus check smoke gates checkpoint resume queue relate state status log "
                   "ask decide"),
    ("Finding your way", "help demo show recall fix explain edit sub surprise vetoes rule why snapshots oops at outline impact map lib tour secrets quiet audit second research mission ideas "
                         "landscape deps oracle pr export instruments sym fail logs data trace suspects whyred bisect "
                         "record graph spec rewrite"),
    ("Project and settings", "init adopt inbox autonomy drive loop posture pause sensitive trust standing approve-reads budget risk sync share notify compact-output complete wiring "
                             "plugins docs doctor verify-ledger outbound sandbox release-check canary ci-watch tidy rollback round"),
    ("Reports", "digest outcomes cost burden dream usage repeats friction taste evals replay backtest bench evolve trial"),
    ("Running elsewhere", "lane page serve run session claude agents night draft scout orders mcp ui projects sweep machine watch "
                          "bus lease conductor"),
    ("Internal (hooks and installer)", "sentinel install-user uninstall-user"),
]


def cmd_help(args):
    sub = next(a for a in build_parser()._actions if isinstance(a, argparse._SubParsersAction))
    helps = {a.dest: _no_ids(" ".join((a.help or "").split())) for a in sub._choices_actions}
    lines = []
    for title, names in HELP_TIERS:
        lines += [title] + [f"  {n:<15}{c.fit(helps.get(n, ''), 100)}" for n in names.split()] + [""]
    out(args, {"tiers": [{"title": t, "commands": n.split()} for t, n in HELP_TIERS]},
        "\n".join(lines) + "fm <command> -h for its options.")


# T-0845: fm --help is where a newcomer starts: the everyday commands, not argparse's 100-verb blob
START_HERE = """usage: fm [-p PROJECT] <command> [options]

Foreman state CLI (the only writer of Foreman state). Start here:
  fm demo                  watch Foreman fix a seeded bug in a throwaway repo (no model calls)
  fm init                  register this repo (once; most commands do it for you)
  fm capture "<request>"   put a request in the inbox
  fm task new "<title>" --type FIX --tier S --ac "<done when> :: <cmd>" --step "<step>" --focus
                           plan a task (or a capture of the same title) and work on it
  fm next                  the one next required action
  fm status                where things stand
  fm focus ID              work on a planned task
  fm check                 run the gates (tests, lint)
  fm task finish ID --run "<cmd>" --audit "<how>"
                           close a task in one call
  fm queue                 what's planned, in order
  fm inbox                 captured requests waiting
  fm doctor                is Foreman healthy here?

fm help --all lists every command; fm <command> -h for its options; -p SLUG picks a project from elsewhere.
"""


_BASH_HOOK = """_fm() {
  local IFS=$'\\n'
  COMPREPLY=($(fm complete -- "${COMP_WORDS[@]:1:COMP_CWORD}" 2>/dev/null))
}
complete -F _fm fm
"""


def cmd_complete(args):
    """T-0924: what can come next, from the real parser (verbs, a verb's subcommands, its options) and the live
    briefs (open task ids where an id goes); --shell prints the hook: eval "$(fm complete --shell bash)"."""
    if args.shell:
        return print(("autoload -U +X bashcompinit && bashcompinit\n" if args.shell == "zsh" else "") + _BASH_HOOK, end="")
    words = list(args.words) or [""]
    cur, node = words[-1], build_parser()
    for w in words[:-1]:  # walk down the subcommands typed so far
        sub = next((a for a in node._actions if isinstance(a, argparse._SubParsersAction)), None)
        if sub and w in sub.choices:
            node = sub.choices[w]
    sub = next((a for a in node._actions if isinstance(a, argparse._SubParsersAction)), None)
    if cur.startswith("-"):
        found = sorted({o for a in node._actions for o in a.option_strings if o.startswith(cur)})
    elif sub:
        found = sorted(n for n in sub.choices if n.startswith(cur))
    else:
        p = c.find_project(os.getcwd())
        found = sorted(b.id for b in c.load_briefs(p) if b.status not in c.CLOSED and b.id.startswith(cur)) if p else []
    print("\n".join(found))


def build_parser():
    ap = _Parser(prog="fm", usage="fm [-p PROJECT] <command> [options]",
                 description="Foreman state CLI (the only writer of Foreman state).")
    ap.format_help = lambda: START_HERE  # only the root: subparsers keep argparse's own help
    ap.add_argument("-p", "--project", help="project slug (default: from cwd, then $FOREMAN_PROJECT)")
    sp = ap.add_subparsers(dest="cmd", required=True, metavar="<command>")

    def add(name, fn, **kw):
        s = sp.add_parser(name, **kw)
        s.set_defaults(fn=fn)
        s.add_argument("--json", action="store_true", help="machine-readable output")
        s.add_argument("-p", "--project", default=argparse.SUPPRESS)
        return s

    s = add("help", cmd_help, help="every command, in tiers: the everyday ones first")
    s.add_argument("--all", action="store_true", help="the same: every command (fm --help: the everyday ones)")
    s = add("init", cmd_init, help="register a project")
    s.add_argument("path", nargs="?")
    s.add_argument("--sensitive", action="store_true")

    s = add("state", cmd_state, help="print STATE (also fm status: the word /foreman:status uses, T-0393)",
            aliases=["status"])
    s.add_argument("--brief", action="store_true")
    s.add_argument("--line", action="store_true")

    s = add("intake", cmd_intake, help="parse an intake block into captured briefs")
    s.add_argument("text", nargs="?")
    s.add_argument("--file")

    s = add("capture", cmd_capture, help="capture a request to the inbox")
    s.add_argument("text", nargs="?")
    s.add_argument("--from-file", metavar="PATH", help="attach a log, transcript or screenshot (- : a paste on stdin): "
                                                       "its path and an excerpt; the request may be left out")
    s.add_argument("--source", default="user", choices=["user", "discovered", "followup", "self", "cross-project"],
                   help="cross-project: a request from another project (fm -p SLUG capture … asks that project)")
    s.add_argument("--type")
    s.add_argument("--tier", choices=["S", "M", "L"])
    s.add_argument("--scope", action="append")
    s.add_argument("--urgent", action="store_true")
    s.add_argument("--self", dest="self_", action="store_true", help="capture into Foreman's own project (self-improvement)")

    s = add("ask", cmd_ask, help="ask the user to authorize guard categories for a task; their next message decides")
    s.add_argument("id")
    s.add_argument("categories", nargs="+")
    s.add_argument("--why", default="")
    s.add_argument("--pin", help="plugin id: the plugin yes holds only for installing or enabling it, as it is now")
    s.add_argument("--standing", action="store_true",
                   help="core only: the yes covers every later task in this project until fm standing off")

    s = add("trust", cmd_trust, help="whether Claude may edit the guard and Claude Code settings (on: /fm-trust, typed)")
    s.add_argument("state", nargs="?", choices=["off"])

    s = add("standing", cmd_standing, help="the project's standing yeses (fm ask … core --standing); off revokes them")
    s.add_argument("state", nargs="?", choices=["off"])

    s = add("decide", cmd_decide, help="record a decision in decisions.md")
    s.add_argument("decision", nargs="?")
    s.add_argument("--why", default="")
    s.add_argument("--rejected", default="")
    s.add_argument("--task")
    s.add_argument("--kind", choices=["reversible", "costly", "outward"], default="reversible",
                   help="costly/outward: listed for the user's review (fm decide --review)")
    s.add_argument("--reverses", help="words from the earlier decision this one undoes")
    s.add_argument("--cites", metavar="REF", help="what it rests on: the user's message, a veto or a decision (T-0654)")
    s.add_argument("--revisit", metavar="TRIGGER",
                   help='"after YYYY-MM-DD" or "when PATH changes": fm next brings the decision back then')
    s.add_argument("--sunset", metavar="YYYY-MM-DD", help="the decision expires then: fm tidy lists it as expired (T-1084)")
    s.add_argument("--revisited", metavar="WORDS", help="words from an earlier decision whose trigger fired: it still holds")
    s.add_argument("--ask", metavar="QUESTION", help="a question for the user, with --default or --options (the taste "
                                                     "record picks): urgent → ask now; full autonomy → decided now; "
                                                     "standard → the ask digest, default applied at its deadline")
    s.add_argument("--default", metavar="ANSWER")
    s.add_argument("--options", nargs="+", metavar="OPTION")
    s.add_argument("--urgent", action="store_true", help="with --ask: it can't wait for the digest")
    s.add_argument("--digest", action="store_true", help="the asks waiting for the user (past the deadline: defaults "
                                                         "applied)")
    s.add_argument("--answer", type=int, metavar="N", help="the decision is the user's answer to digest ask N")
    s.add_argument("--list", action="store_true")
    s.add_argument("--review", action="store_true", help="only costly/outward decisions")
    s.add_argument("--export-adr", metavar="DIR", help="one ADR markdown file per decision in DIR (with --review: "
                                                       "only those) (T-0958)")
    s.add_argument("-n", type=int, default=30)

    s = add("research", cmd_research, help="save a research/recon summary into the project's research/")
    rsp = s.add_subparsers(dest="research_cmd", required=True)
    r = rsp.add_parser("add")
    r.add_argument("name")
    r.add_argument("--file")
    r.add_argument("--from-agent", metavar="FILE", help="a subagent's output file: keeps its final report, not the "
                                                           "transcript")
    r.add_argument("--task")
    r.add_argument("--json", action="store_true")
    r = rsp.add_parser("list", help="saved research, newest first (T-0802)")
    r.set_defaults(fn=cmd_research_list)
    r.add_argument("--json", action="store_true")
    r = rsp.add_parser("show", help="print one saved research note or brainstorm's ideas.md (T-0802)")
    r.set_defaults(fn=cmd_research_show)
    r.add_argument("name")
    r = rsp.add_parser("ask", help="recall first, then parallel web researchers per sub-question; every quoted claim "
                                   "is checked against the page it cites; one note saved (T-0206)")
    r.set_defaults(fn=lazy("fmresearch", "cmd_ask"))
    r.add_argument("question", nargs="?")
    r.add_argument("--file", help="a file of questions, one per line: one note each (T-0239)")
    r.add_argument("--quorum", metavar="MODEL", help="research each sub-question on this second model too; claims both "
                                                      "models make are marked (T-0229)")
    r.add_argument("--sub", action="append", help="a sub-question (repeatable); default: a planner child splits it")
    r.add_argument("--fanout", type=int, default=3, help="most sub-questions researched at once")
    r.add_argument("--model", default="sonnet")
    r.add_argument("--name", help="the note's file name (default: ask-<question>-<time>)")
    r.add_argument("--no-verify", action="store_true", help="don't fetch the cited pages")
    r.add_argument("--timeout", type=int, default=600, help="seconds for all researchers")
    r.add_argument("--task")
    r.add_argument("--json", action="store_true")
    r.add_argument("-p", "--project", default=argparse.SUPPRESS)

    s = add("task", cmd_task, help="task operations")
    tsp = s.add_subparsers(dest="task_cmd", required=True)

    def tadd(name):
        t = tsp.add_parser(name)
        t.add_argument("--json", action="store_true")
        return t

    t = tadd("dissent")  # T-0642
    t.add_argument("id")
    t.add_argument("words", nargs="*", help="add \"<objection>\" | resolve N \"<how it was answered>\"")
    t = tadd("split")  # T-0709
    t.add_argument("id")
    t.add_argument("--parts", type=int, help="how many children (default: about 4 files each, 2–4)")
    t.add_argument("--files", nargs="+", help="the files to split (default: its scope, else fm graph pack's read-set)")
    t.add_argument("--dry-run", action="store_true", help="show the partition only")
    t = tadd("capsule")  # T-0709
    t.add_argument("id")
    t = tadd("finding")  # T-0743
    t.add_argument("id")
    t.add_argument("lens", help=", ".join(c.AUDIT_LENSES))
    t.add_argument("verdict", choices=["confirmed", "rejected"])
    t.add_argument("text", nargs="+")
    t = tadd("revert")  # T-0732
    t.add_argument("id")
    t = tadd("packet")  # T-0466
    t.add_argument("id")
    t.add_argument("--out", help="where to write it (default: the project's handoffs/ID.md)")
    t.add_argument("--check", action="store_true",
                   help="rerun the failing command the packet hands over: accepted while it still fails (T-0704)")
    t.add_argument("--timeout", type=int, default=300)
    t = tadd("new")  # T-0846: its values and one worked example in -h
    t.epilog = ('example:\n  fm task new "Add login timeout" --type FIX --tier S --ac "times out after 30s :: pytest -k '
                'timeout" --step "failing test" --focus')
    t.formatter_class = argparse.RawDescriptionHelpFormatter
    t.add_argument("title")
    t.add_argument("--type", required=True, metavar="{" + ",".join(c.TYPES) + "}",
                   help="what kind of work (aliases such as BUG, PERF, FEAT and lowercase work too)")
    t.add_argument("--tier", required=True, choices=["S", "M", "L"],
                   help="S: ≤~30 lines, 1–2 files · M: several files or a design choice · L: cross-cutting or uncertain")
    t.add_argument("--scope", action="append")
    t.add_argument("--depends", action="append")
    t.add_argument("--raw")
    t.add_argument("--source", default="user", choices=["user", "discovered", "followup", "self"])
    t.add_argument("--from", dest="from_id")
    t.add_argument("--redo", metavar="ID", help="recreate a dropped task: keep its start point and edited files")
    t.add_argument("--ac", action="append", help="acceptance criterion (repeatable): name its observable, what the "
                                                 "user will see, and give its check as 'TEXT :: CMD'")
    t.add_argument("--step", action="append", help="step (repeatable)")
    t.add_argument("--interpretation", help="what the request means (M/L plan gate)")
    t.add_argument("--approach", help="options → choice → why (M/L plan gate)")
    t.add_argument("--focus", action="store_true", help="focus it right away (the plan gate still applies)")
    t = tadd("show")
    t.add_argument("id")
    t.add_argument("--story", action="store_true", help="the ledger as chapters (plan, steps, evidence, reviews, "
                                                        "close) with their times")
    t = tadd("set")
    t.add_argument("id")
    t.add_argument("assignments", nargs="*")
    t.add_argument("--allow", action="append")
    t.add_argument("--section", action="append", help="repeatable: each --section takes the --text (or --file) "
                                                       "given after it (T-1124)")
    t.add_argument("--text", action="append")
    t.add_argument("--file")
    t = tadd("step")
    t.add_argument("id")
    t.add_argument("action", choices=["add", "current", "done"])
    t.add_argument("arg")
    t.add_argument("--evidence", nargs=2, metavar=("CMD", "RESULT"))
    t = tadd("ac")
    t.add_argument("id")
    t.add_argument("action", choices=["add", "check", "edit"])
    t.add_argument("arg")
    t.add_argument("--verify")
    t.add_argument("--text", help="edit: the criterion's new text (its verify command stays unless --verify)")
    t.add_argument("--evidence", nargs=2, metavar=("CMD", "RESULT"))
    t = tadd("evidence")
    t.add_argument("id")
    t.add_argument("cmd", nargs="?", help="what was run (with RESULT), when --run can't run it")
    t.add_argument("result", nargs="?")
    t.add_argument("--run", metavar="CMD", help="run CMD (bash, repo root) and record its real exit code and output")
    t.add_argument("--timeout", type=float, default=600, help="--run limit in seconds")
    t.add_argument("--inconclusive", action="store_true",
                   help="the check neither proves nor disproves: recorded, never counted as passing (exits with the run's code)")
    g = t.add_mutually_exclusive_group()
    g.add_argument("--step", type=int)
    g.add_argument("--ac", type=int)
    t = tadd("audit")
    t.add_argument("id")
    t.add_argument("lens", help=", ".join(c.AUDIT_LENSES))
    t.add_argument("how")
    t.add_argument("result")
    t = tadd("finish")  # one-call close-out: run the checks, mark them, audits, docs, done
    t.add_argument("id")
    t.add_argument("--run", help="check for steps (and criteria without their own verify command)")
    t.add_argument("--audit", help="how the audits were done (the self checklist, a review pass…); not needed to retry a done task's --commit")
    t.add_argument("--result", default="no findings", help="the self audit's result (S)")
    t.add_argument("--lens", action="append", help="M/L: '<lens>: <result>' per audit lens (repeatable)")
    t.add_argument("--docs", help="Docs impact: the docs updated, or none: why")
    t.add_argument("--skip-affected", metavar="WHY", help="T-1117: close without the linked tests' verdict (a runner "
                                                         "fm can't read, a known-red suite), logged with WHY")
    t.add_argument("--lesson")
    t.add_argument("--ablate", action="store_true", help="T-1067: revert each hunk alone against the linked tests and "
                                                         "report the ones no test notices (slow)")
    t.add_argument("--timeout", type=float, default=600)
    t.add_argument("--commit", metavar="MESSAGE", help="then commit the task's own files with this message")
    t.add_argument("--followups", nargs="+", metavar="'Q => A'", help="the likely follow-up questions, answered (T-0639)")
    t.add_argument("--insight", help="one line: what this task taught that wasn't obvious (the digest lists them)")
    t.add_argument("--differently", metavar="TEXT", help="one line: what you would do differently next time (T-0641)")
    t.add_argument("--claim", action="append", metavar="'TAG: CLAIM [:: EVIDENCE]'",
                   help="a typed claim for the close and fm pr; TAG is checked, inferred or unchecked (T-0614)")
    t.add_argument("--why-not-caught", metavar="TEXT", help="FIX: the test, gate or guard that would have caught it "
                                                             "earlier (captured as a follow-up), or 'none: why' (T-0598)")
    t.add_argument("--stack", action="store_true", help="with --commit: one commit per step (per member of a batch), "
                                                        "each checked alone; a red one folds into the next (T-0710)")
    t.add_argument("--stack-check", metavar="CMD", help="the check each stacked commit runs alone (default: its "
                                                        "member's verify commands)")
    t = tadd("prove")  # red→green: fails on the start tree with only this task's tests, passes now
    t.add_argument("id")
    t.add_argument("--run", help="the test command")
    t.add_argument("--vacuous", action="store_true",
                   help="name the criteria whose checks pass on the start tree too (they don't test the change; T-0457)")
    t.add_argument("--same", metavar="CMD", help="CLEAN work: CMD's exit and output must match before and after "
                                                 "(a behaviour lock; T-0501)")
    t.add_argument("--hunks", action="store_true",
                   help="revert each code hunk of the task's diff alone: name the ones the check doesn't notice")
    t.add_argument("--max", type=int, default=20, help="--hunks: at most this many hunks (one check run each)")
    g = t.add_mutually_exclusive_group()
    g.add_argument("--step", type=int)
    g.add_argument("--ac", type=int)
    t.add_argument("--timeout", type=float, default=600)
    t = tadd("log")
    t.add_argument("id")
    t.add_argument("text", help="a steer, scope change, decision or note; appended to the brief's Log")
    t = tadd("hypo")
    t.add_argument("id")
    t.add_argument("action", choices=["add", "mark", "ruled"])
    t.add_argument("args", nargs="*", help="add: CLAIM · mark: N ruled-out|confirmed|open · ruled: none (what this "
                                           "task and tasks on its scope ruled out, and why)")
    t.add_argument("--probe", help="add: the command that would tell (recorded, not run)")
    t.add_argument("--run", metavar="CMD", help="mark: run the probe now and record its exit code and output")
    t.add_argument("--why", metavar="REASON", help="mark: why it was ruled out (or confirmed), kept beside the claim")
    t.add_argument("--write", action="store_true", help="ruled: also write handoffs/ID-ruled-out.md for fm-debugger")
    t.add_argument("--timeout", type=float, default=600)
    t = tadd("note")
    t.add_argument("id")
    t.add_argument("kind", choices=["fact", "question"])
    t.add_argument("text", nargs="+")
    t = tadd("assume")
    t.add_argument("id")
    t.add_argument("action", choices=["add", "verify"])
    t.add_argument("args", nargs="+", help="add: FACT · verify: N (its number in the Assumptions section)")
    g = t.add_mutually_exclusive_group()
    g.add_argument("--run", metavar="CMD", help="verify: run CMD; exit 0 marks it verified, anything else false")
    g.add_argument("--evidence", metavar="HOW", help="verify: how it was checked, when it can't run (file:line read…)")
    t.add_argument("--kill", metavar="TEXT", help="add: what would show it false (fm next lists it until verified)")
    t.add_argument("--check", metavar="CMD", help="add: a command that stays true while the assumption holds; fm "
                                                  "sentinel re-runs it after the task is done (T-0489)")
    t.add_argument("--timeout", type=float, default=600)
    t = tadd("done")
    t.add_argument("id")
    t.add_argument("--lesson", help="what the next similar task should know (M/L: required; 'none: why' allowed)")
    t = tadd("block")
    t.add_argument("id")
    t.add_argument("reason")
    t = tadd("drop")
    t.add_argument("id")
    t.add_argument("reason", nargs="?")
    t.add_argument("--done-in", metavar="ID", help="it was done as part of this other task (closed as done there)")
    t = tadd("defer")
    t.add_argument("id")
    t.add_argument("reason", nargs="?")
    t.add_argument("--until", help="YYYY-MM-DD: fm next names it again from that day (T-0450); \"when PATH changes\": "
                                   "once that file changes (T-0958)")

    s = add("map", lazy("fmmap", "cmd_map"), help="project map: gates, layout, entry points, hot files, test links")
    s.add_argument("--rebuild", action="store_true", help="rebuild even though HEAD hasn't moved")
    s.add_argument("--cold", action="store_true", help="the most-changed files no session has read (T-0660)")
    s.add_argument("--capture", action="store_true", help="with --cold: file one inbox item to read them (one open at a time)")
    s = add("lib", lazy("fmlib", "cmd_lib"), help="stack library: cards per language, framework, service and tool, "
            "plus installed plugins' skills (suggest, search, show, list, check; inject on|off: the edit-time card; "
            "stats: which cards fired)")
    s.add_argument("action", nargs="?", default="suggest", choices=["suggest", "search", "show", "list", "check", "source",
                                                                    "inject", "stats"])
    s.add_argument("words", nargs="*", help="search: topic words; show: a card name or plugin:skill")
    s.add_argument("--area", help="list: one area's cards")
    s.add_argument("-n", type=int, default=12, help="suggest: at most this many cards")
    s.add_argument("--days", type=int, help="stats: only injections of the last N days (default: all)")
    s.add_argument("--section", action="append", help="show: only these sections (verify, test, do, avoid, review); "
                                                     "repeatable")
    s.add_argument("--name", help="source add: the source's short name (default: the repo's)")
    s = add("scout", lazy("fmscout", "cmd_scout"), help="find work nobody asked for yet: a newer Claude Code, stack cards "
            "your projects lack, doctor failures, stale skill sources, a brainstorm when the queue is dry (T-0950)")
    s.add_argument("--slow", action="store_true", help="every probe, with the network and project scans (fm night's)")
    s.add_argument("--dry", action="store_true", help="list what it would capture; capture nothing")
    s = add("impact", lazy("fmmap", "cmd_impact"), help="likely tests and dependents of a path")
    s.add_argument("path")
    s = add("share", lazy("fmrecall", "cmd_share"), help="opt in: share this project's lessons and recall other projects' "
                                                         "(paths, URLs, emails, file names, task ids and the project "
                                                         "name are removed; other names in the prose are not)")
    s.add_argument("state", nargs="?", choices=["on", "off"])
    s = add("digest", lazy("fmcost", "cmd_digest"), help="the week in one screen: tasks, grades, lessons, decisions, cost")
    s.add_argument("--days", type=float, default=7)
    s = add("outcomes", lazy("fmoutcomes", "cmd_outcomes"), help="what became of finished tasks: reverted, fixed later "
                                                                 "by a task naming them, or held; track record (T-0616)")
    s.add_argument("--atlas", action="store_true", help="by file and language: where work didn't hold (T-0620)")
    s.add_argument("--readme", action="store_true", help="one sentence for a README: held, closed and ungraded "
                                                         "counts (T-0960)")
    for flag, why in (("settle", "log one outcome event per task whose 30-day window closed (survived or lost)"),
                      ("claims", "survival by the grade each finish recorded: did strong closes hold more often"),
                      ("regret", "lost tasks with the approach they took, and reversed decisions"),
                      ("graveyard", "lost and dropped tasks"),
                      ("seen", "survival of tasks the user corrected mid-task against the rest")):  # T-1060
        s.add_argument("--" + flag, action="store_true", help=why)
    s = add("verify-ledger", lazy("fmledger", "cmd_verify_ledger"), help="prove no ledger line was edited or removed: "
                                                                         "each carries the hash of the one before (T-1065)")
    s.add_argument("--head", help="also prove this head (a finish receipt's) is still in the chain: the tail wasn't cut")
    s = add("outbound", lazy("fmledger", "cmd_outbound"), help="every outbound request a task's sessions made: "
                                                              "WebFetch/WebSearch/MCP/curl hosts (T-1086)")
    s.add_argument("id", nargs="?", help="task (default: the focused one)")
    s = add("evals", lazy("fmcost", "cmd_evals"), help="turn a blocked or failed task into a plugin eval case; inbox: "
                                                        "what could become one (T-0734)")
    s.add_argument("action", choices=["add", "inbox"])
    s.add_argument("id", nargs="?")
    s.add_argument("--out", help="folder for the case (default: the project's state evals/)")
    s = add("bus", lazy("fmbus", "cmd_bus"), help="messages between sessions on this machine: send to one or all, read "
                                                  "yours (T-0708)")
    s.add_argument("action", choices=["send", "read", "watch"],
                   help="watch: the plugin monitor's stream of this session's new mail (T-0777)")
    s.add_argument("words", nargs="*")
    s.add_argument("--type", default="note", choices=["note", "steer", "stop"])
    s.add_argument("--wake", action="store_true",
                   help="wake an idle session: its watcher prints the mail, else one line typed into its tmux pane")
    s = add("lease", lazy("fmbus", "cmd_lease"), help="function-level edit leases between sessions (T-0708)")
    s.add_argument("action", nargs="?", default="list", choices=["list", "take", "drop"])
    s.add_argument("target", nargs="*", help="FILE[::SYMBOL]...")
    s.add_argument("--minutes", type=float, default=20)
    s.add_argument("--warn", action="store_true", help="take a claim that overlaps another session's, with a warning")
    s = add("conductor", lazy("fmbus", "cmd_conductor"), help="live sessions with their task, context, mail and leases; "
                                                              "steer them all (T-0708)")
    s.add_argument("action", nargs="?", default="list", choices=["list", "steer", "remote", "refresh"])
    s.add_argument("words", nargs="*")
    s.add_argument("--wake", action="store_true")
    s = add("spec", lazy("fmchange", "cmd_spec"), help="a one-line wish as a red unittest: a tool-less child's "
                                                        "assertions, only safe ones kept (T-0713)")
    s.add_argument("wish")
    s.add_argument("--module", required=True, help="the Python module the wish is about")
    s.add_argument("--out", help="the test file (default: tests/test_spec_<wish>.py)")
    s.add_argument("--model", default="haiku")
    s.add_argument("--timeout", type=int, default=180)
    s = add("rewrite", lazy("fmchange", "cmd_rewrite"), help="one rename rule across the repo; residual sites named; "
                                                              "--convert clears them with a cheap child (T-0713)")
    s.add_argument("old")
    s.add_argument("new")
    s.add_argument("--glob", help="only files matching this pattern")
    s.add_argument("--apply", action="store_true", help="write the changes (default: a dry run)")
    s.add_argument("--convert", action="store_true", help="with --apply: rewrite the residual lines with a cheap child")
    s.add_argument("--model", default="haiku")
    s.add_argument("--timeout", type=int, default=180)
    s = add("bisect", cmd_bisect, help="the first commit where a check started failing, and its files (T-0612)")
    s.add_argument("--run", required=True, metavar="CMD")
    s.add_argument("--good", metavar="REF", help="a commit where it passed (default: the active task's start)")
    s.add_argument("--timeout", type=int, default=120, help="seconds per run")
    s = add("fix", lazy("fmfixes", "cmd_fix"), help="known fixes: what got past an obstacle, offered the next time any "
                                                     "session meets it (list, add, rm)")
    s.add_argument("action", nargs="?", default="list", choices=["list", "add", "rm", "trust"])
    s.add_argument("text", nargs="?", help="add: the error text; rm/trust: the number fm fix list shows (trust: adopt "
                                          "a fix that came with the repo, so it is offered as one, not as a hint)")
    s.add_argument("--do", help="add: what gets past it")
    s.add_argument("--run", help="add: the command that does")

    s = add("dream", lazy("fmrecall", "cmd_dream"), help="the day's repeated failures as tripwire candidates with their "
                                                          "counterfactual (T-0665)")
    s.add_argument("--day", help="YYYY-MM-DD (default: today)")
    s = add("graph", lazy("fmgraph", "cmd_graph"), help="the work graph: blast radius of a change, a task's ranked "
                                                        "read-set, as of any moment (T-0707)")
    s.add_argument("action", choices=["blast", "pack", "build"])
    s.add_argument("words", nargs="*")
    s.add_argument("--as-of", help="only what was known by this ISO time (backtests)")
    s.add_argument("--top", type=int, default=15)
    s = add("suspects", lazy("fmdebug", "cmd_suspects"), help="files ranked for a failure: stack, task change, test "
                                                               "links, recency (T-0706)")
    s.add_argument("file", nargs="?", help="the failing run's output (default: stdin)")
    s.add_argument("--top", type=int, default=5)
    s = add("whyred", lazy("fmdebug", "cmd_whyred"), help="the minimal hunks of this task's change that turn a command "
                                                           "red (delta debugging, T-0706)")
    s.add_argument("cmd")
    s.add_argument("--timeout", type=int, default=300)
    s = add("record", lazy("fmdebug", "cmd_record"), help="rerun a Python command and show the locals where its "
                                                           "exceptions unwound (T-0706)")
    s.add_argument("cmd")
    s.add_argument("--top", type=int, default=4)
    s.add_argument("--timeout", type=int, default=600)
    s = add("cost", lazy("fmcost", "cmd_cost"), help="tokens by task, session and tool, from the transcripts")
    s.add_argument("--days", type=float, default=7)
    s.add_argument("--by-model", action="store_true", help="tasks finished per model and type/tier, with their grades")
    s.add_argument("--forecast", action="store_true", help="when the 5-hour and weekly usage windows fill at the "
                   "pace so far (T-0973)")
    s.add_argument("--task", metavar="ID", help="one task: spent, its cap and the forecast from similar tasks (T-1083)")
    s.add_argument("--refresh-cache", action="store_true", help=argparse.SUPPRESS)  # the Stop hook's detached refresh
    s.add_argument("--sessions", action="store_true",
                   help="per session: turns, context per turn, the cache read/write/output split and cache busts")
    s = add("burden", lazy("fmcost", "cmd_burden"), help="Foreman's own cost on real sessions per version: bookkeeping "
                                                          "turns, refusals, injected context (T-0712)")
    s.add_argument("--days", type=float, default=14)
    s.add_argument("--by-verb", action="store_true", help="the fm verbs no session called in the window (T-0959)")
    s = add("usage", lazy("fmcost", "cmd_usage"), help="skills, playbooks and fm commands used (and never used)")
    s.add_argument("--days", type=float, default=30)
    s.add_argument("--prune", action="store_true",
                   help="fm commands no session ran in the window, in any project (T-0468; nothing is removed)")
    s.add_argument("--agents", action="store_true", help="a scorecard per agent type: spawns, tokens, lanes kept (T-0647)")
    s.add_argument("--lesions", action="store_true", help="what each fm evolve --drop ablation found (T-0664)")
    s = add("at", cmd_at, help="run a command as of a task's start or a commit, in a throwaway worktree")
    s.add_argument("target", help="a task id (its start) or a commit, branch or tag")
    s.add_argument("--timeout", type=float, default=600)
    s.add_argument("words", nargs=argparse.REMAINDER)
    s = add("complete", cmd_complete, help="tab completion: candidates for the words typed so far; --shell bash|zsh "
                                           "prints the hook to source")
    s.add_argument("--shell", choices=["bash", "zsh"])
    s.add_argument("words", nargs="*")
    s = add("quiet", cmd_quiet, help="run a noisy command: one line on success, the tail on failure")
    s.add_argument("--tail", type=int, default=40)
    s.add_argument("--timeout", type=float, default=1800)
    s.add_argument("words", nargs=argparse.REMAINDER)
    s = add("gates", cmd_gates, help="what fm task done will require for a type and tier (default: the active task)")
    s.add_argument("type", nargs="?", type=str.upper, choices=c.TYPES)
    s.add_argument("tier", nargs="?", type=str.upper, choices=["S", "M", "L"])
    s = add("pr", lazy("fmcost", "cmd_pr"), help="a pull-request description from a task's brief, with its proof "
                                                  "(red→green, lens verdicts, assumptions, bench replays; printed only); "
                                                  "fm pr threads ID: review comments to steps; fm pr train: merge in order")
    s.add_argument("id", help="a task id, or threads / train")
    s.add_argument("more", nargs="*", help="threads: the task id")
    s.add_argument("--pr", type=int, help="threads: the PR number (default: the PR of branch foreman/ID)")
    s.add_argument("--task", help="train: the task whose publish grant covers the merges (default: the active one)")
    s = add("second", lazy("fmsecond", "cmd_second"),
            help="an independent second read: plan (another model), debate (rebut a review), session (what was missed)")
    s.add_argument("what", choices=["plan", "cheapest", "debate", "session"])
    s.add_argument("id", nargs="?", help="plan, debate: the task")
    s.add_argument("--review", help="debate: the research note holding the earlier review")
    s.add_argument("--model", help="plan, session: the child's model, another than the main one (default sonnet)")
    s.add_argument("--if-due", action="store_true", help="session: only once a day")
    s.add_argument("--exclude", help="session: the current session's id (its transcript isn't the previous one)")
    s.add_argument("--force", action="store_true", help="plan: run it on a tier protocols.json gives no panel")
    s.add_argument("--role", choices=["pre-mortem", "naive", "prosecutor", "defender", "devil"],
                   help="plan: read it from a stress-test stance, saved as its own Plan review section (T-0604)")
    s.add_argument("--timeout", type=float, default=300)
    s = add("relate", lazy("fmrelate", "cmd_relate"),
            help="order and group the queue and inbox by which open tasks build on others: ids they mention, and a "
                 "tool-less child's reading (runs on its own once a day when 3+ tasks are new); --clear undoes")
    s.add_argument("--clear", action="store_true", help="drop every inferred dependency and group, and turn the "
                                                         "automatic runs off")
    s.add_argument("--on", action="store_true", help="turn the automatic runs back on after --clear")
    s.add_argument("--drop", nargs=2, metavar=("T-B", "T-A"), help="veto one inferred edge (T-B after T-A), for good")
    s.add_argument("--no-child", action="store_true", help="only the ids tasks mention: no model call")
    s.add_argument("--if-due", action="store_true", help="only once a day, when 3+ open tasks are new since the last run")
    s.add_argument("--model", default="haiku", help="the child's model (default haiku)")
    s.add_argument("--timeout", type=float, default=300)
    s = add("mcp", lazy("fmmcp", "cmd_mcp"), help="serve Foreman's state, next action, recall, research, briefs, stack "
                                                 "library and instruments as read-only MCP tools over stdio; new: "
                                                 "scaffold a tested MCP server wrapping any CLI; register: the "
                                                 "harness's add line (T-0946)")
    s.add_argument("action", nargs="?", default="serve", choices=["serve", "new", "register"])
    s.add_argument("words", nargs="*", help="new: NAME · register: claude|codex|gemini [DIR]")
    s.add_argument("--wrap", metavar="'CMD'", help="new: the command the server runs, as argv (no shell)")
    s.add_argument("--sub", metavar="a,b", help="new: the subcommands a caller may pick (an enum)")
    s.add_argument("--dir", help="new: the folder to write (default: ./NAME)")
    s.add_argument("--force", action="store_true", help="new: write into a folder that isn't empty")
    add("wiring", lazy("fmdoctor", "cmd_wiring"), help="one screen of what is wired: version, hooks, flags, standing "
                                                        "yeses, trust, pause, budget, plugins (T-0469)")
    s = add("orders", lazy("fmorders", "cmd_orders"), help="standing orders: requests that capture themselves on a "
                                                             "schedule or when a file changes (T-0452)")
    s.add_argument("action", nargs="?", default="list", choices=["list", "add", "rm", "run"])
    s.add_argument("text", nargs="*", help="add: what to capture · rm: N")
    s.add_argument("--every", help="add: a period, e.g. 30m, 6h, 1d, 1w")
    s.add_argument("--on-change", dest="on_change", help="add: a file in the project; captures when its content changes")
    s.add_argument("--type", help="add: the captured task's type (default FEATURE)")
    s = add("night", lazy("fmnight", "cmd_night"),
            help="budgeted background work while you're away (landscape when due, the daily second read, the court); "
                 "refused at high usage; fm digest reports it")
    s.add_argument("--dry-run", action="store_true", help="list tonight's jobs and estimates; run nothing")
    s.add_argument("--print-timer", action="store_true",
                   help="print a systemd user timer + service and a crontab line for fm night here; install nothing")
    s.add_argument("--max-usd", type=float, default=2.0, help="the night's spend at most (and today's budget left)")
    s.add_argument("--only", action="append", metavar="JOB", help="only this job (repeatable): landscape, "
                                                                  "second session, court")
    s = add("draft", lazy("fmdraft", "cmd_draft"),
            help="draft the top queued S task with a headless claude in a throwaway worktree (branch draft/T-x); "
                 "swept when the queue's top changes; never merged")
    s.add_argument("--status", action="store_true", help="sweep a stale draft and say what is waiting; draft nothing")
    s = add("landscape", lazy("fmoutside", "cmd_landscape"),
            help="research what people want from coding-agent harnesses now: what's new since the last scan, what "
                 "Foreman lacks")
    s.add_argument("--if-due", action="store_true", help="only when the last scan is 30+ days old")
    s.add_argument("--fanout", type=int, default=3)
    s.add_argument("--model", default="sonnet")
    s.add_argument("--no-verify", action="store_true", help="don't fetch the cited pages")
    s.add_argument("--timeout", type=int, default=600)
    s = add("deps", lazy("fmoutside", "cmd_deps"),
            help="dependencies a major version behind their registry's latest, with the migration question to research")
    s.add_argument("words", nargs="*", help='"check <install command>": age, typosquat and registry look at the '
                                            "packages an npm/pip/cargo install names (T-1049)")
    s.add_argument("--research", type=int, nargs="?", const=3, default=0, metavar="N",
                   help="research the first N migrations now (default 3; each budget-checked)")
    s.add_argument("--calls", action="store_true", help="each dependency's installed version and import sites with "
                                                        "the names used, read locally, no network (T-0594)")
    s.add_argument("--model", default="sonnet")
    s.add_argument("--timeout", type=int, default=600)
    s = add("tour", lazy("fmmap", "cmd_tour"), help="a task's (or, --since REF, a range's) changed files in reading "
                                                   "order with sizes and a review-risk verdict: what to review first")
    s.add_argument("id", nargs="?")
    s.add_argument("--since", metavar="REF", help="everything since REF's merge base with HEAD, uncommitted included")
    s = add("export", lazy("fmcost", "cmd_export"),
            help="AGENTS.md for other harnesses: working rules, corrections, map, lessons, decisions, playbooks")
    s.add_argument("what", choices=["agents", "cursor", "gemini"])
    s.add_argument("--out", metavar="PATH",
                   help="where to write it (default: AGENTS.md, .cursor/rules/foreman.mdc or GEMINI.md at the project root)")
    s.add_argument("--force", action="store_true", help="replace a file fm export didn't write")
    s = add("why", lazy("fmmap", "cmd_why"), help="the commits and Foreman tasks behind FILE[:LINE], with their lessons")
    s.add_argument("target")
    add("snapshots", cmd_snapshots, help="uncommitted work Foreman saved before a command discarded it, and how to "
                                         "bring it back")
    s = add("oops", cmd_oops, help="the newest work snapshot and its restore command; --apply restores it (T-0960)")
    s.add_argument("--apply", action="store_true", help="restore it (the files as they are now are saved first)")
    s = add("show", cmd_show, help="a task id → task show, FILE[:LINE] → why, other words → recall (T-0960)")
    s.add_argument("words", nargs="+")
    s = add("round", cmd_round, help="close a round: tag HEAD round-N, list the tasks closed since the last (T-0960)")
    s.add_argument("action", choices=["close"])
    add("release-check", lazy("fmdemo", "cmd_release_check"),
        help="fm doctor and fm demo in a temporary HOME: a clean checkout passes before a release (T-0960)")
    s = add("secrets", lazy("fmsecrets", "cmd_secrets"), help="credentials in the working tree, Claude config and "
                                                             "(--history) git history, by place and kind, never printed")
    s.add_argument("--history", action="store_true", help="also every commit on every branch")
    s = add("replay", lazy("fmreplay", "cmd_replay"), help="the guard on the real shell commands of recent sessions: what "
                                                           "it now blocks or lets through compared with the accepted run")
    s.add_argument("--days", type=int, default=14, help="how far back the session logs are read (default 14)")
    s.add_argument("--accept", action="store_true", help="take this run's verdicts as the baseline")
    s.add_argument("--cmd", metavar="TEXT", help="only this command: the guard's default verdict, never run it")
    s.add_argument("--cwd", metavar="DIR", help="with --cmd: the folder it would run in (default: here)")
    s.add_argument("--candidate", metavar="REF|FILE", help="score another guard (a git ref of Foreman's repo, or a "
                                                          "fmguard.py file) against the working one (T-0712)")
    s = add("backtest", lazy("fmbacktest", "cmd_backtest"), help="where a changed rule, known fix or card would have "
                                                                 "fired on recent real sessions, read-only (T-1058)")
    s.add_argument("--rule", metavar="REGEX", help="calls (command, path, pattern) the regex matches")
    s.add_argument("--fix", metavar="SIG", help="failed calls whose output contains this error signature")
    s.add_argument("--card", metavar="NAME", help="calls that mention this library card by name")
    s.add_argument("--days", type=int, default=14, help="how far back the session logs are read (default 14)")
    s = add("outline", lazy("fmmap", "cmd_outline"), help="a file's definitions with line ranges (read a range, not all)")
    s.add_argument("path")
    import fminstr  # T-0701: the instruments, their help and arguments come from one registry
    add("instruments", lazy("fminstr", "cmd_instruments"),
        help="the zero-token instruments: typed tools with input schemas and line caps (sym, fail, logs, data, trace)")
    for name in fminstr.TOOLS:
        fminstr.arguments(add(name, lazy("fminstr", "cmd_" + name), help=fminstr.TOOLS[name][1]), name)

    s = add("vetoes", cmd_vetoes, help="what the user said never to do, checked before matching commands and edits")
    s.add_argument("action", nargs="?", choices=["list", "rm"], default="list")
    s.add_argument("n", nargs="?", type=int)
    s = add("rule", cmd_rule, help="the user's regex rules on Bash commands or edited paths that warn or block")
    s.add_argument("action", nargs="?", choices=["list", "add", "rm"], default="list")
    s.add_argument("arg", nargs="?", help="add: the pattern (a Python regex, searched for); rm: N from fm rule list")
    s.add_argument("--on", choices=["bash", "path"], default="bash", help="a Bash command, or an edited file's path")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--block", action="store_true", help="deny a matching call with the why (the default)")
    g.add_argument("--warn", action="store_true", help="a note on a matching call, which still runs")
    s.add_argument("--why", help="what the refusal or note says")
    s.add_argument("--from-veto", type=int, metavar="N", help="the rule from veto N (fm vetoes): its key words")
    s.add_argument("--moves", metavar="METRIC", help="the ledger metric this should lower (e.g. corrections): a trial fm digest grades")
    s.add_argument("--by", type=int, default=30, metavar="DAYS", help="days until the trial is graded (default 30)")
    s = add("trial", lazy("fmtrials", "cmd_trial"), help="self-changes registered with --moves, graded once due (T-1059)")
    s = add("surprise", cmd_surprise, help="log where the model of the code was wrong: \"<expected> → <observed>\"")
    s.add_argument("text", nargs="+")
    s.add_argument("--task", help="the task it came up in (default: the active one)")

    s = add("recall", lazy("fmrecall", "cmd_recall"), help="related past work: briefs, decisions, research")
    s.add_argument("text", nargs="*")
    s.add_argument("--task", help="recall for this task's title, request and scope")
    s.add_argument("-n", type=int, default=4)
    s.add_argument("--corrections", action="store_true", help="the user's recent corrections (for /foreman:reflect)")
    s.add_argument("--magnets", action="store_true", help="files the most FIX tasks touched (T-0613)")
    s.add_argument("--lessons", action="store_true", help="lessons by id: times shown, never recalled, recurred (T-0617)")
    s.add_argument("--retire", metavar="LESSON", help="with --lessons: leave this lesson (T-0123.1) out of recall and "
                                                      "tripwires (T-0743)")
    s.add_argument("--why", help="with --retire: why it no longer helps")
    s.add_argument("--consolidate", action="store_true", help="with --lessons: group near-duplicate lessons and "
                                                              "propose one each; retires nothing (T-1071)")
    s.add_argument("--from-night", action="store_true", help=argparse.SUPPRESS)
    s.add_argument("--capture", action="store_true", help="with --consolidate: file the proposal as a captured task")
    s.add_argument("--export-rules", action="store_true", help="write the live lessons to .claude/rules/"
                                                               "foreman-lessons/, one file per task, paths: its files (T-0958)")
    s.add_argument("--repos", action="store_true", help="prior art: the text's identifiers in other projects that opted "
                                                        "in with fm share on (never sensitive ones), file:line (T-0618)")
    s.add_argument("--others", action="store_true", help="a similar fixed failure or lesson in other projects that opted "
                                                         "in with fm share on; text is a failure, or use --task (T-1073)")
    s.add_argument("--explain", metavar="QUESTION", help="where the identifiers a question names are defined and used, "
                                                         "cited file:line (T-0659)")
    s.add_argument("--ask", metavar="QUESTION", help="answer from briefs, ledger, decisions and research (SQLite FTS5 "
                                                     "BM25), each passage citing its task ids")
    s = add("explain", lazy("fmrecall", "cmd_explain"), help="why Foreman did it: the rule, inputs and ledger events "
                                                             "behind the last guard block or drive/Stop decision")
    s.add_argument("what", nargs="?", choices=["block", "drive"], help="only guard blocks, or only drive/Stop decisions")

    s = add("focus", cmd_focus, help="make a task the single active task")
    s.add_argument("id")

    s = add("checkpoint", cmd_checkpoint, help="flush the resume point into the brief and STATE")
    s.add_argument("--note")
    s.add_argument("--auto", action="store_true")

    s = add("clauses", lazy("fmrecall", "cmd_clauses"), help="split a multi-part request into clauses and match each to "
                                                              "a task; fm next names the unaccounted ones (T-0595)")
    s.add_argument("text", nargs="*", help="the user's message (or, with --note, why the clause needs no task)")
    s.add_argument("--note", type=int, metavar="N", help="mark unaccounted clause N as handled (answered, or no task)")
    s.add_argument("--show", action="store_true", help="the unaccounted clauses of the last request")
    s = add("resume", cmd_resume, help="print the resume point, and re-run the last green check for drift")
    s.add_argument("--no-check", action="store_true", help="don't re-run the last green check (T-0649)")

    s = add("queue", cmd_queue, help="ordered queue")
    s.add_argument("--replan", action="store_true")
    s.add_argument("--preview", action="store_true", help="usual time per item here, and what each will need from you")

    s = add("log", cmd_log, help="append a ledger event")
    s.add_argument("event")
    s.add_argument("data", nargs="?")
    s.add_argument("--task")

    s = add("sensitive", cmd_sensitive, help="mark a repo sensitive (manual permission mode there); suggest: the "
                                             "signals that it is, nothing set")
    s.add_argument("state", choices=["on", "off", "suggest"])
    s.add_argument("path", nargs="?")

    s = add("drive", cmd_drive, help="keep Claude working while the queue has unblocked work")
    s.add_argument("state", choices=["on", "off"])

    s = add("edit", lazy("fmedit", "cmd_edit"), help="a batch of exact replacements across files from stdin (JSON or "
            "@@ file / <<< old / === new / >>> blocks), all or none, inside the task's scope (T-1089)")
    s.add_argument("--dry-run", action="store_true", help="say what would change; write nothing")
    s.add_argument("--file", help="read the batch from this file instead of stdin (a builder writes it with Write)")
    s = add("sub", lazy("fmedit", "cmd_sub"), help="a regex codemod: per-file counts first, --apply writes (T-1089)")
    s.add_argument("pattern")
    s.add_argument("repl", help="the replacement (re.sub syntax: \\g<1> for a group)")
    s.add_argument("--glob", action="append", help="files to search, relative to the project (repeatable; ** works)")
    s.add_argument("--apply", action="store_true", help="write the changes (inside the task's scope)")
    s.add_argument("--max", type=int, default=50, help="refuse to write more files than this")

    s = add("loop", lazy("fmloop", "cmd_loop"), help="the forever loop (T-1057): on, an empty queue starts the next "
            "improvement round (review, brainstorm past every earlier run, queue, build) until two dry rounds")
    s.add_argument("action", nargs="?", choices=["status", "on", "off", "round", "yield"])
    s.add_argument("n", nargs="?", type=int, help="yield: how many grounded ideas this round queued")

    s = add("posture", cmd_posture, help="lite: only the guard's hook runs in this project; full: every hook (T-0963)")
    s.add_argument("state", nargs="?", choices=["lite", "full"])

    s = add("approve-reads", cmd_approve_reads, help="on: Foreman answers Claude Code's permission dialog for commands "
                                                       "that only read (yours to turn on; T-0974)")
    s.add_argument("state", nargs="?", choices=["on", "off"])

    s = add("pause", cmd_pause, help="stop everything Foreman runs unattended, in every project (fm pause off lifts it)")
    s.add_argument("state", nargs="?", choices=["on", "off"], default="on")

    add("next", cmd_next, help="the one next required action (derived from the briefs)")

    s = add("sentinel", cmd_sentinel, help="re-run the checks recent finished tasks passed; report what fails now")
    s.add_argument("--last", type=int, default=10, help="finished tasks to cover")
    s.add_argument("--max", type=int, default=20, help="commands to run at most")
    s.add_argument("--timeout", type=float, default=120)
    s.add_argument("--bisect", action="store_true", help="find the commit that broke each failing check (git bisect in "
                                                        "a throwaway worktree) and capture it as a FIX (T-0458)")
    s = add("check", cmd_check, help="run the project's gate commands together (tests, lint…); exit 1 on any failure")
    s.add_argument("action", nargs="?", default="run", choices=["run", "add", "rm", "list", "paths", "affected",
                                                                          "ambient", "onwrite"])
    s.add_argument("words", nargs="*", help="add: the command; rm: its number (fm check list); paths: its number, then "
                                            "the globs it covers (none: always run); affected: a command with {tests} "
                                            "(paths) or {names} (file names without extension); onwrite: GLOB and a "
                                            "command with {file}, run on each matching write (5 s; a failure blocks; "
                                            "GLOB alone removes it; nothing lists them)")
    s.add_argument("--timeout", type=float, default=600, help="seconds per command")
    s.add_argument("--fresh", action="store_true", help="run even if the gates passed on this exact tree already")
    s.add_argument("--repeat", type=int, default=0, help="run each gate N times and report its pass rate (an "
                                                       "intermittent failure; nothing is recorded; T-0475)")
    s.add_argument("--fail-fast", action="store_true", help="stop at the first failing gate (while iterating)")
    s.add_argument("--affected", action="store_true", help="only the tests linked to files changed since the task "
                                                           "started (fm map); the full gates still decide at the end")
    s.add_argument("--evidence", metavar="ID", help="record each result as evidence on this task")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--step", type=int)
    g.add_argument("--ac", type=int)

    s = add("friction", lazy("fmfriction", "cmd_friction"),
            help="Foreman's own friction since the last self-improvement pass: a digest, or a brief for one subagent")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--brief", action="store_true", help="write a self-contained brief for one read-only subagent")
    g.add_argument("--mark", action="store_true", help="record a finished pass: the next digest starts after it")
    g.add_argument("--every", type=int, help="fm next calls for a pass every N closed tasks (0: off)")
    g.add_argument("--reject", metavar="TEXT", help="a dead end: later digests skip lines with TEXT (T-0471)")
    g.add_argument("--minutes", action="store_true", help="minutes lost in the last week, by kind (T-0959)")
    s.add_argument("--why", help="--reject: why it's a dead end")

    s = add("repeats", lazy("fmrepeats", "cmd_repeats"),
            help="commands and procedures this project keeps repeating, and what project tool each could become")
    s.add_argument("action", nargs="?", default="list", choices=["list", "dismiss"])
    s.add_argument("words", nargs="*", help="dismiss: the shape or step as fm repeats prints it")
    s.add_argument("--forge", action="store_true", help="draft a script or skill for each repeat in research/ and "
                                                        "capture a task to adopt it (T-1070)")
    s.add_argument("--draft", action="store_true", help="write a playbook draft from steps 3+ finished tasks took in "
                                                        "the same order (T-0734; adopting it is asked first)")

    s = add("sync", lazy("fmsync", "cmd_sync"),
            help="opt-in mirror of this project's briefs, decisions and research in the repo (.foreman/)")
    s.add_argument("action", nargs="?", default="status", choices=["status", "on", "off", "import", "export"])
    s.add_argument("--remove", action="store_true", help="off: also delete .foreman/")

    s = add("audit", cmd_audit, help="prep audits: freeze the task's diff and write one review brief for one reviewer")
    s.add_argument("action", choices=["prep", "scan"], help="prep ID: review brief for a task; scan: mechanical "
                                                             "pre-audit of any diff (--base, default: the main branch)")
    s.add_argument("id", nargs="?")
    s.add_argument("--print", action="store_true", help="print the brief instead of only its path")
    s.add_argument("--forge", action="store_true", help="prep: a brief asking for a change that keeps each check "
                                                        "green yet breaks its criterion (T-0652)")
    s.add_argument("--split", action="store_true", help="one brief per lens group (up to 3) for parallel fresh-context "
                                                        "reviewers instead of one reviewer for every lens (T-0216)")
    s.add_argument("--lens", action="append", choices=list(c.AUDIT_LENSES), help="only this lens (repeatable)")
    s.add_argument("--base", help="diff from this revision (default: the commit the task was focused at)")
    s.add_argument("--note", action="append", default=[], help="focus for every lens brief: this round's change, "
                                                               "threat model, what to ignore (repeatable)")

    s = add("autonomy", cmd_autonomy, help="standard (asks for L plans, ? items, approvals) or full (never asks mid-run)")
    s.add_argument("level", nargs="?", choices=["standard", "full"])

    s = add("tidy", lazy("fmtidy", "cmd_tidy"), help="hygiene (dry-run by default)")
    s.add_argument("--apply", action="store_true")
    s.add_argument("--all", action="store_true")
    s.add_argument("--lanes-only", action="store_true", help="only worktrees and branches of closed tasks (what fm night runs)")
    s.add_argument("--plugins", action="store_true", help="also report plugin footprint (slow: runs claude plugin details)")

    s = add("rollback", lazy("fmrollback", "cmd_rollback"), help="restore the state as the snapshot taken at the last "
                                                             "Foreman upgrade had it (T-1085)", allow_abbrev=False)
    s.add_argument("--list", action="store_true")
    s.add_argument("--snapshot", metavar="OLD", help=argparse.SUPPRESS)  # the upgrade hook's detached child
    s.add_argument("--to", metavar="NAME", help="a snapshot from --list (default: the newest upgrade snapshot)")
    s.add_argument("--yes", action="store_true")

    s = add("doctor", lazy("fmdoctor", "cmd_doctor"), help="self-check")
    s.add_argument("--full", action="store_true")
    s.add_argument("-v", "--verbose", action="store_true", help="list the passing checks too")
    s.add_argument("--restore-state", action="store_true", help="move fallback state back to the default dir")
    s.add_argument("--repair", action="store_true", help="move empty (crash-truncated) git objects into the quarantine")
    s.add_argument("--accept-supply", action="store_true",
                   help="take the current plugins and MCP servers as the supply-chain baseline (T-0672)")

    s = add("sweep", lazy("fmeco", "cmd_sweep"), help="ask every other project about a fix: where a pattern is (or what "
                                                       "recall relates), a brief in its inbox; edits nothing there")
    s.add_argument("fix", help="the fix, as the brief's first line")
    s.add_argument("--grep", metavar="TEXT", help="the sibling pattern (a fixed string, git grep in each project)")
    s.add_argument("--type", default="FIX")
    s.add_argument("--dry-run", action="store_true", help="say where it would ask; capture nothing")
    s = add("adopt", lazy("fmeco", "cmd_adopt"), help="take in an existing repo: map, gates (a flake rerun), secrets, "
                                                       "dependencies once; a baseline note and CLEAN/RESEARCH work queued")
    s.add_argument("--history", action="store_true", help="only mine git history (reverts, fix: commits) into a lesson "
                                                          "note and known fixes")
    s = add("inbox", lazy("fmeco", "cmd_inbox"), help="captured requests waiting; fm inbox gh reads the repo's open "
                                                       "issues (read-only) into briefs, their text kept as untrusted data")
    s.add_argument("source", nargs="?", choices=["gh"], help="a tracker to capture from; none lists the inbox")
    s.add_argument("--repo", metavar="OWNER/REPO", help="default: the repo gh finds here")
    s.add_argument("--limit", type=int, default=30)
    s = add("ci-watch", lazy("fmci", "cmd_ci_watch"), help="after a push, poll the branch's latest CI run through gh; a "
                                                           "failure's log tail becomes a FIX brief (data), up to --max-retries; it can run "
                                                           "max-polls x interval: use run_in_background, or let fm next or a Monitor wake you")
    s.add_argument("--branch", help="default: the branch gh finds here")
    s.add_argument("--commit", metavar="SHA", help="the commit to watch (default: git HEAD, followed as fixes are pushed)")
    s.add_argument("--max-retries", type=int, default=3)
    s.add_argument("--interval", type=float, default=30, help="seconds between polls")
    s.add_argument("--max-polls", type=int, default=120)
    s = add("risk", lazy("fmrisk", "cmd_risk"), help="today's risk budget: destructive guard blocks, failed closes and "
                                                      "reverts spend points; past the cap autonomy steps down a notch")
    s.add_argument("action", nargs="?", choices=["show", "set"], default="show")
    s.add_argument("--day", type=float, help="set: the daily cap in points (the user's to set)")
    s.add_argument("--because", help="set: why (logged)")
    s = add("canary", lazy("fmeco", "cmd_canary"), help="Claude Code's version against the last seen; on a change the "
                                                         "hook fixtures, a hook smoke and fm replay run, a failure is a brief")
    s.add_argument("--if-changed", action="store_true", help="only when the version changed (each session start)")
    s = add("machine", lazy("fmeco", "cmd_machine"), help="this machine's identity: a stable id and a name (shown in "
                                                           "fm projects and, once named, in brief logs fm sync carries)")
    s.add_argument("--name", help="name this machine")

    s = add("bench", lazy("fmbench", "cmd_bench"), help="Foreman's benchmark from finished tasks: build cases, replay "
                                                         "them with a candidate plugin, compare runs (T-0212)")
    bsp = s.add_subparsers(dest="bench_cmd", required=True)
    b = bsp.add_parser("seed-review", help="bench a reviewer on planted one-line bugs (T-0646)")
    b.add_argument("--json", action="store_true")
    b.add_argument("-p", "--project", default=argparse.SUPPRESS)
    b.add_argument("--cases", type=int, default=5)
    b.add_argument("--reviewer", metavar="CMD", help="a reviewer that reads the diff on stdin (default: fm-reviewer)")
    b.add_argument("--model", default="sonnet")
    b.add_argument("--seed", type=int, default=0)
    b = bsp.add_parser("guard", help="mutation-test the guard: which rules no command notices (T-1066)")
    b.add_argument("--json", action="store_true")
    b.add_argument("-p", "--project", default=argparse.SUPPRESS)
    b.add_argument("--coverage", action="store_true", help="which rules a command corpus is blocked by")
    b.add_argument("--mutate", action="store_true", help="drop one rule site at a time and run the guard's tests on each")
    b.add_argument("--weaken", action="store_true", help="with --mutate: negate the guarding if instead of dropping")
    b.add_argument("--flip", action="store_true", help="with --mutate: flip one operator or constant inside a check "
                                                       "function per mutant instead (T-1121)")
    b.add_argument("--days", type=int, default=14, help="--coverage: session-log days to read (default 14)")
    b.add_argument("--cmds", metavar="FILE", help="--coverage: one command per line instead of the session logs")
    b.add_argument("--tests", metavar="CMD", help="--mutate: the test command (default: run.py -p 'test_guard*.py')")
    b.add_argument("--module", metavar="FILE", help="--mutate: the module to mutate (default fmguard.py)")
    b.add_argument("--max", type=int, default=40, help="--mutate: mutants run, sampled evenly (default 40)")
    b.add_argument("--only", metavar="CATEGORY", help="--mutate: only this category's sites")
    b.add_argument("--timeout", type=int, default=300, help="--mutate: seconds per mutant (default 300)")
    b = bsp.add_parser("scorecard", help="each saved run's pass rate on the train and holdout splits (T-0734)")
    b.add_argument("--json", action="store_true")
    b.add_argument("-p", "--project", default=argparse.SUPPRESS)
    b = bsp.add_parser("hygiene", help="cases that pass or fail the same in every saved run: they tell no version "
                                        "from another (T-0656)")
    b.add_argument("--json", action="store_true")
    b.add_argument("-p", "--project", default=argparse.SUPPRESS)
    for name in ("build", "list", "run", "show", "compare", "gate", "models"):
        b = bsp.add_parser(name)
        b.add_argument("--json", action="store_true")
        b.add_argument("-p", "--project", default=argparse.SUPPRESS)
        if name in ("build", "run", "models"):
            b.add_argument("--ids", nargs="+", help="only these task ids")
        if name in ("list", "run"):
            b.add_argument("--split", choices=["train", "holdout"], help="only that split (a stable 1 in 5 is "
                                                                          "held out from fm evolve; T-0734)")
        if name == "models":
            b.add_argument("--models", default="haiku,sonnet", help="comma-separated models to compare")
            b.add_argument("--max", type=int, default=3)
            b.add_argument("--runs", type=int, default=1)
            b.add_argument("--budget", type=float, default=3.0)
            b.add_argument("--timeout", type=int, default=30)
            b.add_argument("--save", action="store_true", help="keep the recommendation for fm run --models")
        if name == "build":
            b.add_argument("--last", type=int, default=30, help="finished tasks to consider, newest first")
            b.add_argument("--commits", metavar="RANGE", help="cases from this git range's commits instead of briefs "
                                                                "(any repo; needs --verify)")
            b.add_argument("--verify", metavar="CMD", help="with --commits: the command that grades a case; {tests} "
                                                            "becomes its test files")
            b.add_argument("--judged", action="store_true", help="work whose commit has no tests (docs, UI, prose) "
                                                                 "becomes a case a judge grades against its criteria")
        if name == "run":
            b.add_argument("--plugin", help="the plugin folder to test (default: this Foreman)")
            b.add_argument("--max", type=int, default=3, help="cases to run")
            b.add_argument("--model")
            b.add_argument("--budget", type=float, default=3.0, help="USD per case (claude --max-budget-usd)")
            b.add_argument("--timeout", type=int, default=30, help="minutes per case")
            b.add_argument("--label", help="name for these results (default: the time)")
            b.add_argument("--runs", type=int, default=1, help="attempts per case: a pass rate instead of one sample")
        if name == "show":
            b.add_argument("label")
        if name == "gate":
            b.add_argument("a", help="the reference results (live)")
            b.add_argument("b", help="the candidate's results")
            b.add_argument("--cost-tolerance", type=float, default=0.15, help="allowed rise in mean cost per case")
        if name == "compare":
            b.add_argument("a")
            b.add_argument("b")
    contests = {"duel": "replay cases with Foreman alone and with another plugin beside it, and gate the two (T-0240)",
                "versions": "replay cases on Foreman at an earlier git revision and on this one, and gate the two (T-0241)",
                "court": "turn the user's steers and corrections into judged cases and replay them (T-0242)",
                "soak": "replay a case as a conversation with a child playing the user; report what they had to repeat "
                        "(T-0243)",
                "stranger": "a newcomer session in a toy repo with only the README: its stumbles become self items "
                            "(T-0244)"}
    for name, text in contests.items():
        b = bsp.add_parser(name, help=text, description=text)
        b.add_argument("--json", action="store_true")
        b.add_argument("-p", "--project", default=argparse.SUPPRESS)
        if name == "duel":
            b.add_argument("plugin", nargs="?", help="a plugin folder, or an installed plugin's id")
            b.add_argument("--vs", choices=["none"], help="none: Foreman against Claude with no plugins (only the "
                                                          "guard, as a settings hook) instead of a rival (T-0963)")
        if name == "versions":
            b.add_argument("rev", help="the earlier Foreman revision (a commit, tag or HEAD~N)")
            b.add_argument("--source", help="the Foreman checkout REV is in (default: the running one's repo)")
        if name in ("court", "soak", "stranger"):
            b.add_argument("--plugin", dest="plugin_dir", help="the plugin folder to test (default: this Foreman)")
        if name not in ("court", "stranger"):
            b.add_argument("--ids", nargs="+", help="only these case ids")
        if name == "soak":
            b.add_argument("--turns", type=int, default=3, help="the user's replies at most")
        b.add_argument("--max", type=int, default=1 if name == "soak" else 3 if name != "court" else 8,
                       help="cases to run")
        b.add_argument("--model")
        b.add_argument("--budget", type=float, default=3.0, help="USD per session (claude --max-budget-usd)")
        b.add_argument("--timeout", type=int, default=30, help="minutes per session")
        if name in ("duel", "versions"):
            b.add_argument("--cost-tolerance", type=float, default=0.15, help="allowed rise in mean cost per case")
        if name == "court":
            b.add_argument("--label", help="name for these results (default: court-<time>)")

    s = add("batch", cmd_batch, help="work several not-yet-started requests as one task: one plan, gate run, review and "
                                     "commit; each closes done in it (T-0257)")
    s.add_argument("ids", nargs="*")
    s.add_argument("--title")
    s.add_argument("--suggest", action="store_true", help="list related items worth one batch each (T-0670)")
    s.add_argument("--apply", action="store_true", help="with --suggest: make those batches")

    s = add("budget", lazy("fmbudget", "cmd_budget"), help="spend on child runs and subagents today, and the caps that "
                                                            "bound it (T-0227)")
    s.add_argument("action", nargs="?", default="show", choices=["show", "set"])
    s.add_argument("--day", type=float, help="set: USD per day for everything fm spawns")
    s.add_argument("--run", type=float, help="set: USD per command")
    s.add_argument("--because", help="set: why a cap goes up (recorded as a costly decision)")
    s.add_argument("--days", type=int, default=1, help="show: spend over this many days")

    s = add("evolve", lazy("fmevolve", "cmd_evolve"), help="one bench-gated generation: revise (or --drop) one Foreman "
                                                            "instruction file on an evolve branch, bench both, gate (T-0224)")
    s.add_argument("--target", required=True, help="the file to revise, relative to the repo (e.g. plugin/skills/x/SKILL.md)")
    s.add_argument("--drop", action="store_true", help="empty the file instead (ablation)")
    s.add_argument("--repo", help="Foreman's repo (default: the one holding this plugin)")
    s.add_argument("--plugin-dir", default="plugin", help="the plugin folder inside the repo")
    s.add_argument("--ids", nargs="+", help="only these bench cases")
    s.add_argument("--max", type=int, default=3)
    s.add_argument("--runs", type=int, default=1)
    s.add_argument("--model", help="the model the replays run on")
    s.add_argument("--mutate-model", default="sonnet")
    s.add_argument("--live", help="reuse these earlier live results instead of replaying live again")
    s.add_argument("--budget", type=float, default=3.0)
    s.add_argument("--timeout", type=int, default=30)
    s.add_argument("--moves", metavar="METRIC", help="the ledger metric a kept change should lower: a trial fm digest grades (T-1059)")
    s.add_argument("--by", type=int, default=30, metavar="DAYS", help="days until the trial is graded (default 30)")

    s = add("oracle", lazy("fmideas", "cmd_oracle"), help="behaviour examples and ambiguities from the task's spec alone, "
                                                           "before the code is read (T-0226)")
    s.add_argument("id")
    s.add_argument("--model", default="sonnet")
    s.add_argument("--timeout", type=int, default=300)

    s = add("mission", lazy("fmmission", "cmd_mission"), help="the mission and brainstorm seeds for an open-ended "
                                                               "request, composed from the project (T-0375)")
    s.add_argument("--request", help="the user's words, verbatim")
    s = add("demo", lazy("fmdemo", "cmd_demo"), help="see Foreman work on a seeded bug in a throwaway repo, with no "
                                                      "model calls and nothing left behind (T-0870)")
    s.add_argument("--pace", type=float, default=0, metavar="SECONDS",
                   help="pause per stage and type the commands out, for watching or recording (try 1)")
    s = add("smoke", lazy("fmsmoke", "cmd_smoke"), help="check the product the way its user uses it: the web UI in a "
                                                         "headless browser at desktop and phone width (T-0417)")
    s.add_argument("action", nargs="?", choices=["run", "set"], default="run")
    s.add_argument("words", nargs="*", help="set: web <url> | http <url> | cmd \"<command>\"")
    s.add_argument("--expect", help="set cmd: a regex its output must match")
    s.add_argument("--status", type=int, default=200, help="set http: the status it must return")
    s.add_argument("--json-key", dest="json_key", help="set http: a key its JSON body must have")
    s = add("ideas", lazy("fmideas", "cmd_ideas"), help="tool-less brainstorm children, one per lens, in parallel")
    s.add_argument("--pack", required=True, help="context pack file (- for stdin)")
    s.add_argument("--lens", action="append", help="repeatable; default: user value, unspoken needs, delight, reliability, "
                                                    "simplicity, bold bets")
    s.add_argument("--model", default="sonnet")
    s.add_argument("--rounds", type=int, default=1, help="super brainstorm: each round builds on every idea so far")
    s.add_argument("--dry", type=int, default=3, help="stop when a later round adds fewer new ideas than this")
    s.add_argument("--seen", action="append", help="an earlier ideas.md whose ideas this run must go past (repeatable)")
    s.add_argument("--deepen", type=int, default=0, help="then a yes-and round for each of the K biggest idea categories")
    s.add_argument("--falsify", action="store_true", help="one more child: the quickest kill test for each idea (T-0606)")
    s.add_argument("--crossbreed", action="store_true", help="one more child: the top ideas combined (T-0628)")
    s.add_argument("--timeout", type=int, default=300)

    s = add("page", lazy("fmpage", "cmd_page"),
            help="now (active task, queue, counts) and optionally a research catalogue as one HTML page for a claude.ai "
                 "Artifact; prints the publish line and how to read the Build/Veto picks back (T-0786)")
    s.add_argument("--catalogue", metavar="NAME", help="research/NAME.json or research/NAME/catalogue.json: clusters")
    s.add_argument("--url", help="record the Artifact link from a first publish, printed on later runs")
    s.add_argument("--out", metavar="PATH", help="write here instead of the project's page.html")
    s.add_argument("--picks", metavar="FILE", help="store the page's picks ({cluster id: add|veto} JSON, - for stdin) "
                                                   "in state picks.json; needs --catalogue (T-0962)")
    s = add("serve", lazy("fmserve", "cmd_serve"),
            help="run Claude Code Remote Control here in the background (systemd user unit): [start|status|stop] [PATH]")
    s.add_argument("args", nargs="*", metavar="[ACTION] [PATH]")
    s.add_argument("--permission-mode", choices=c.PERMISSION_MODES)
    s.add_argument("--all", action="store_true", help="with stop: every fm serve unit")

    s = add("taste", lazy("fmideas", "cmd_taste"), help="what your choices say you want: kept, dropped (and why), "
                                                         "steered, corrected, vetoes to propose; brainstorms use it")
    s.add_argument("action", nargs="?", choices=["adopt", "decline", "compile"],
                   help="the user's yes or no to the proposed vetoes (all, or N); compile N: a proposal as a rule (T-1063)")
    s.add_argument("which", nargs="?", type=int, metavar="N")
    s.add_argument("-n", type=int, default=8)
    s.add_argument("--block", action="store_true", help="compile N as a block rule, not a warn: the user's to type (T-1063)")
    s.add_argument("--overwrites", action="store_true", help="files the user's own commits reworked soon after an "
                                                            "agent's (T-0655)")
    s = add("lane", lazy("fmlanes", "cmd_lane"), help="a git worktree beside the repo with its own active task: "
                                                       "new <id>, list, rm <id> (never discards uncommitted work); "
                                                       "brief <id>: an S/M task for a foreman:fm-builder subagent; "
                                                       "resume <id>: take back a stopped builder's work")
    s.add_argument("action", choices=["new", "list", "rm", "brief", "merge", "max", "resume"])
    s.add_argument("id", nargs="?", help="the task id; max: how many builders may be out at once (1-6)")
    s.add_argument("--spike", action="store_true", help="new: a throwaway lane fm lane merge refuses (T-0732)")
    s.add_argument("--force", metavar="REASON", help="resume: although the builder isn't known to be stopped or ignored "
                                                     "files would go (T-1028); the reason is logged")
    s.add_argument("--unverified", metavar="REASON", help="merge: merge although the criteria's re-run is red, with the "
                                                          "reason on the ledger (main thread only, T-0948)")
    s = add("session", lazy("fmsession", "cmd_session"), help="agent sessions on this device (claude, codex, gemini, "
                                                                "opencode), detached: start MESSAGE, list, tail ID, "
                                                                "send ID MESSAGE, stop ID, rm ID, agents")
    s.add_argument("action", nargs="?", default="list",
                   choices=["start", "list", "tail", "send", "stop", "rm", "agents", "_run"])
    s.add_argument("rest", nargs="*", help="the session id and/or the message")
    s.add_argument("--agent", default="claude", help="start: which agent CLI runs it")
    s.add_argument("--cwd", help="start: the folder it works in (default: here)")
    s.add_argument("--model", help="start: the agent's model name")
    s.add_argument("--title", help="start: a name for the list (default: the first line of the message)")
    s.add_argument("--arg", action="append", default=[], help="start: an extra argument for the agent CLI, every turn "
                                                              "(repeat; --arg=--yolo)")
    s.add_argument("--from", dest="from_line", type=int, default=0, help="tail: start at this event line")
    s.add_argument("--follow", action="store_true", help="tail: keep printing new events; list: a new list whenever a session changes")
    s.add_argument("--interval", type=float, default=0.3, help="tail --follow: seconds between checks")
    s = add("agents", lazy("fmagents", "cmd_agents"), help="Foreman's guard, context, MCP server and rules in Codex, "
                                                             "Gemini CLI and opencode: list, install AGENT, uninstall "
                                                             "AGENT")
    s.add_argument("action", choices=["list", "install", "uninstall"])
    s.add_argument("agent", nargs="?", choices=["codex", "gemini", "opencode"])
    s = add("claude", lazy("fmclaude", "cmd_claude"), help="every Claude Code session on this device (terminal, remote, "
                                                             "headless): list, show ID, agents ID, image ID REF, files "
                                                             "ID, file ID PATH, send ID MESSAGE")
    s.add_argument("action", choices=["list", "show", "agents", "image", "files", "file", "send"])
    s.add_argument("rest", nargs="*", help="the session id, then a ref, path or message")
    s.add_argument("--all", action="store_true", help="list: headless (SDK, claude -p) sessions too")
    s.add_argument("--limit", type=int, default=150, help="list --all: at most this many headless ones, newest first")
    s.add_argument("--agent", help="show/image: a subagent's transcript (its id from fm claude agents)")
    s.add_argument("--from", dest="from_line", type=int, default=0, help="show: from this transcript line")
    s.add_argument("--follow", action="store_true", help="list/show: keep printing as sessions change")
    s.add_argument("--interval", type=float, default=0.5, help="--follow: seconds between checks")
    s.add_argument("--model", help="send: the model for the continuation")
    s = add("run", lazy("fmserve", "cmd_run"), help="work the queue in fresh claude -p sessions, one task each")
    s.add_argument("--max", type=int, default=10, help="tasks to finish before stopping")
    s.add_argument("--parallel", type=int, default=1, help="independent S/M tasks with disjoint scopes at once, each in "
                                                           "its own lane, merged back when gated and clean (max 3)")
    s.add_argument("--timeout", type=float, default=60, help="minutes per session")
    s.add_argument("--max-usd", type=float, help="stop starting tasks once this run's measured spend reaches it "
                                                 "(one at a time; T-1046)")
    s.add_argument("--stall", type=float, default=20, help="minutes a session's transcript may sit still before fm "
                                                          "run stops it and goes on (0: never; T-0447)")
    s.add_argument("--fit", action="store_true", help="small tasks first (S, M, then L), so more finish before a usage "
                                                      "limit; on by itself while usage runs ahead of pace (T-0732)")
    s.add_argument("--failover", choices=["codex", "gemini", "opencode"],
                   help="opt-in for this run: when a usage limit outlasts --wait, hand the task's packet to this agent "
                        "(it leaves for that provider; T-0731)")
    s.add_argument("--wait", type=float, default=6, help="hours to wait out usage limits in total (0: stop at one)")
    s.add_argument("--permission-mode", choices=c.PERMISSION_MODES)
    s.add_argument("--sandbox", action="store_true", help="each session under Claude Code's sandbox: Bash writes only "
                                                          "its checkout, fm's state and the git dir; no sandbox, no "
                                                          "session (T-0975); or fm sandbox on")
    s.add_argument("--no-sandbox", action="store_true", help="run sessions without Claude Code's sandbox")
    s.add_argument("--models", help="model per tier, e.g. S=sonnet,M=sonnet,L=opus (default: Claude Code's)")
    s.add_argument("--save", action="store_true", help="keep --models for later runs")
    s = add("sandbox", lazy("fmserve", "cmd_sandbox"), help="fm run's sandbox as a project setting: on, off, allow "
                                                           "DOMAIN, show (T-1086)")
    s.add_argument("action", nargs="?", default="show", choices=["on", "off", "allow", "show"])
    s.add_argument("domains", nargs="*")
    s = add("notify", lazy("fmserve", "cmd_notify"), help="command fm run uses to tell you a task finished or blocked")
    s.add_argument("command", nargs="*", help="gets the message as $1, e.g. notify-send Foreman \"$1\"")
    s.add_argument("--off", action="store_true")
    s.add_argument("--test", action="store_true")

    s = add("plugins", lazy("fmplugins", "cmd_plugins"),
            help="find plugins in the known marketplaces, check enabled ones for conflicts, install after approval")
    s.add_argument("action", choices=["find", "check", "install", "enable", "disable", "add-marketplace", "forget"])
    s.add_argument("words", nargs="*", help="find: what you need; check: one plugin id (default: all enabled); "
                                            "install/enable: one id (either installs it if missing, else enables "
                                            "it); add-marketplace: owner/repo, git URL or path; forget: an id to keep")

    s = add("docs", lazy("fmdocs", "cmd_docs"), help="report markdown that drifted from the repo")
    s.add_argument("path", nargs="?")
    s.add_argument("--strict", action="store_true", help="exit 1 when anything drifted")

    s = add("ui", lazy("fmwatch", "cmd_ui"), help="view model for UI surfaces (the foreman-ui mod): --json")
    s.add_argument("--follow", action="store_true", help="print a new view line whenever the project changes")
    s.add_argument("--interval", type=float, default=0.5, help="--follow: seconds between checks")
    s.add_argument("--demo", action="store_true", help="print a canned view (every key a real one has) as JSON")
    s = add("projects", lazy("fmwatch", "cmd_projects"), help="every Foreman project on this device (the desktop "
                                                                "app's list): --json, --follow, --next")
    s.add_argument("--follow", action="store_true", help="print a new list whenever a project changes")
    s.add_argument("--next", action="store_true", help="one ranked list of every project's next action")
    s.add_argument("--interval", type=float, default=0.5, help="--follow: seconds between checks")
    s = add("watch", lazy("fmwatch", "cmd_watch"), help="live dashboard")
    s.add_argument("--once", action="store_true")
    s.add_argument("--interval", type=float, default=1.0)

    s = add("install-user", lazy("fmsetup", "cmd_install"), help="wire Foreman into ~/.claude (used by install.sh)")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--record-disabled", action="append", metavar="PLUGIN_ID",
                   help="record a plugin Foreman disabled (listed by uninstall.sh for re-enabling)")
    s = add("compact-output", lazy("fmsetup", "cmd_compact_output"),
            help="shorten big Bash outputs for the model (head, failure lines, tail; full text in a file)")
    s.add_argument("state", nargs="?", choices=["on", "off", "shadow", "status"],
                   help="shadow: record what it would cut (fm compact-output shows the total), never shorten")
    s = add("uninstall-user", lazy("fmsetup", "cmd_uninstall"), help="undo install-user from the manifest")
    s.add_argument("--dry-run", action="store_true")
    return ap


def _options_first(parser, argv):
    """T-0332: argparse reads a command's positionals in one run, so in `fm session send ID --json -- MSG` the option
    ends that run and MSG is left over. For the commands taking ID then words (session, claude), known options (with
    their values) standing right before `--` move in front of the positionals; anything else is left as typed, so a
    flag inside an unprotected message is still an error (its review)."""
    k = 2 if argv[:1] in (["-p"], ["--project"]) else 0
    if argv[k:k + 1] not in (["session"], ["claude"]) or "--" not in argv[k + 1:]:
        return argv
    sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction)).choices[argv[k]]
    head = argv[k + 1:argv.index("--", k + 1)]
    first = next((i for i, t in enumerate(head) if t in sub._option_string_actions), len(head))
    i = first
    while i < len(head):
        act = sub._option_string_actions.get(head[i])
        if act is None:
            return argv
        i += 1 + (1 if act.nargs is None else act.nargs if isinstance(act.nargs, int) else 1)
    if i != len(head):
        return argv
    return argv[:k + 1] + head[first:] + head[:first] + argv[k + 1 + len(head):]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    global _ARGV
    _ARGV = list(argv)  # T-0273: what _Parser.error reads for a mistyped flag
    parser = build_parser()
    if not argv and c.find_project(os.getcwd()):  # T-0917: bare fm in a project answers "what now?"
        main(["state", "--line"])
        print("fm help: every command")
        return main(["next"])
    args = parser.parse_args(_options_first(parser, argv) or ["help"])  # bare fm elsewhere: the tiers, not a usage error
    if args.cmd != "complete":  # a TAB press reads the briefs, never syncs or locks (round-7 review)
        _sync_in(args)
    try:
        rc = args.fn(args)
        return rc if isinstance(rc, int) else 0  # evidence --run / check pass on the command's exit code
    except c.PolicyError as e:
        print(f"fm: refused: {e}", file=sys.stderr)
        return 2
    except c.LockTimeout as e:
        print(f"fm: {e} (another fm or hook is writing; retry)", file=sys.stderr)
        return 3
    except (UsageError, KeyError) as e:
        print(f"fm: {e.args[0] if e.args else e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"fm: state looks corrupt: {e} (run fm doctor)", file=sys.stderr)
        return 4
