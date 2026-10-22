"""T-1551: Foreman for other tools, stdlib only and read-only (no network, no state written).
fm timeline: a task's run (its ledger events) as Perfetto / Chrome trace JSON (ui.perfetto.dev, chrome://tracing) or, with
--otlp, OTLP JSON for an OpenTelemetry collector. fm glance: the status as one JSON line for shells and status bars.
fm lsp: a Language Server stub over stdio that publishes a brief's proof gaps as diagnostics."""
import hashlib
import json
import math
import os
import re
import sys

import fmcore as c

# ---------------------------------------------------------------- fm timeline


def _clean(o):
    """Redacted the way the ledger is (an older Foreman's line may predate it); a non-finite number would be invalid JSON."""
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, list):
        return [_clean(x) for x in o]
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    return c.redact(o)


def _secs(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0 else 0.0


def run_of(p, tid):
    """The brief (None once archived) and the task's ledger events as [(POSIX time, event)], in ledger order."""
    b = c.find_brief(p, tid)
    since = (b.meta.get("created") if b else None) or ""  # nothing before the task was made concerns it
    run = []
    for e in c.ledger_events(p, since=since if isinstance(since, str) else ""):
        t = c.parse_ts(e.get("ts"))
        if e.get("task") == tid and t:
            run.append((t.timestamp(), e))
    return b, run


def model(tid, title, run, private):
    """spans [{name, start, end, track, args, error}] and marks [{name, at, track, args}]: the task (track None) with
    its steps laid end to end inside it, each check of a check_run (on its session's track, laid end to end and
    ending at the event), and every event as a mark. private (a sensitive project): timings and kinds, no words."""
    t0, t1 = run[0][0], run[-1][0]
    spans = [{"name": tid if private or not title else f"{tid} {c.redact(title)}", "start": t0, "end": t1,
              "track": None, "args": {"task": tid}, "error": False}]
    ends, marks, floor = {}, [], {}
    for t, e in run:
        d = e.get("data") if isinstance(e.get("data"), dict) else {}
        track = c.redact(str(e.get("session_id") or "no session"))
        if e.get("event") in ("evidence", "step_done") and isinstance(d.get("step"), int):
            ends[d["step"]] = t
        if e.get("event") == "check_run" and isinstance(d.get("results"), list):
            end = t  # gates run one after another; ts is cut to the second, so a run never starts before the last one
            for r in reversed([r for r in d["results"] if isinstance(r, dict)]):  # ended (Perfetto drops overlaps)
                s, code = _secs(r.get("s")), r.get("exit")
                start = max(end - s, min(floor.get(track, end - s), end))
                spans.append({"name": "check" if private else c.redact(str(r.get("cmd")))[:200], "start": start,
                              "end": end, "track": track, "error": bool(code),
                              "args": {"exit": code if isinstance(code, int) else None, "s": s}})
                end = start
            floor[track] = t
        marks.append({"name": str(e.get("event")), "at": t, "track": track, "args": {} if private else _clean(d)})
    prev = t0
    for n, end in sorted(ends.items(), key=lambda kv: kv[1]):
        spans.append({"name": f"step {n}", "start": prev, "end": end, "track": None, "args": {"step": n},
                      "error": False})
        prev = end
    return spans, marks


def perfetto(slug, spans, marks):
    """Chrome trace JSON (the Object Format Perfetto imports): a thread per session, the task's own track first."""
    tracks = {None: 1}
    for x in spans + marks:
        tracks.setdefault(x["track"], len(tracks) + 1)
    us = lambda t: int(round(t * 1e6))  # noqa: E731
    evs = [{"name": "process_name", "ph": "M", "pid": 1, "tid": 1, "args": {"name": f"foreman {slug}"}}]
    evs += [{"name": "thread_name", "ph": "M", "pid": 1, "tid": n, "args": {"name": "task" if k is None else k}}
            for k, n in tracks.items()]
    evs += [{"name": s["name"], "cat": "foreman", "ph": "X", "ts": us(s["start"]),
             "dur": max(0, us(s["end"]) - us(s["start"])), "pid": 1, "tid": tracks[s["track"]], "args": s["args"]}
            for s in spans]
    evs += [{"name": m["name"], "cat": "ledger", "ph": "i", "s": "t", "ts": us(m["at"]), "pid": 1,
             "tid": tracks[m["track"]], "args": m["args"]} for m in marks]
    return {"traceEvents": evs, "displayTimeUnit": "ms"}


def _any(v):
    if isinstance(v, bool):
        return {"boolValue": v}
    if isinstance(v, int):
        return {"intValue": str(v)}
    if isinstance(v, float):
        return {"doubleValue": v}
    return {"stringValue": v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}


def otlp(slug, tid, spans, marks):
    """OTLP JSON (ExportTraceServiceRequest): the task is the root span, steps and checks its children, the events
    its span events. Ids are hashes of the project and task, so a second export of the same run matches the first."""
    trace = hashlib.sha256(f"{slug} {tid}".encode()).hexdigest()[:32]
    sid = lambda i: hashlib.sha256(f"{trace} {i}".encode()).hexdigest()[:16]  # noqa: E731
    ns = lambda t: str(int(round(t * 1e9)))  # noqa: E731
    attrs = lambda d: [{"key": str(k), "value": _any(v)} for k, v in d.items()]  # noqa: E731
    out = []
    for i, s in enumerate(spans):
        span = {"traceId": trace, "spanId": sid(i), "name": s["name"], "kind": 1, "startTimeUnixNano": ns(s["start"]),
                "endTimeUnixNano": ns(max(s["start"], s["end"])),
                "attributes": attrs(dict(s["args"], **({"foreman.session": s["track"]} if s["track"] else {})))}
        if i:
            span["parentSpanId"] = sid(0)
        if s["error"]:
            span["status"] = {"code": 2}  # STATUS_CODE_ERROR
        out.append(span)
    out[0]["events"] = [{"timeUnixNano": ns(m["at"]), "name": m["name"],
                         "attributes": attrs(dict(m["args"], **{"foreman.session": m["track"]}))} for m in marks]
    return {"resourceSpans": [{"resource": {"attributes": attrs({"service.name": "foreman", "foreman.project": slug})},
                               "scopeSpans": [{"scope": {"name": "foreman"}, "spans": out}]}]}


def cmd_timeline(args):
    import fmcli
    p = fmcli.resolve(args, create=False)
    tid = (args.id or "").upper() or getattr(c.active_brief(c.load_briefs(p), p.lane), "id", "")
    if not tid:
        raise fmcli.UsageError("no active task here: name one (fm timeline T-0042)")
    if not re.fullmatch(r"T-\d+", tid):
        raise fmcli.UsageError(f"{args.id!r} isn't a task id (T-0042)")
    b, run = run_of(p, tid)
    if not run:
        raise fmcli.UsageError(f"no ledger events for {tid} in {p.slug}")
    spans, marks = model(tid, b.title if b else "", run, bool(c.read_meta(p).get("sensitive")))
    doc = otlp(p.slug, tid, spans, marks) if args.otlp else perfetto(p.slug, spans, marks)
    text = json.dumps(doc, ensure_ascii=False)
    if not args.out:
        return print(text)
    path = os.path.realpath(args.out)  # through a symlink, not over it
    c.write_atomic(path, text + "\n")
    print(f"{path}: {tid}, {len(spans)} spans and {len(marks)} events; "
          + ("POST it to a collector's /v1/traces" if args.otlp else "open it at https://ui.perfetto.dev"))


# ---------------------------------------------------------------- fm glance


def glance(p):
    """One status for any shell or bar: the counts, and waybar's text, tooltip and class (paused, active, blocked, idle)."""
    sd = c.state_dict(p)
    a = sd["active"]
    step = (f"{a['step']['n']}/{a['step']['of']}" if a["step"] else f"{a['steps_done']}/{a['steps_total']}") if a else None
    paused = bool(sd["paused"] or sd["panic"])
    title = c.redact(a["title"]) if a else None
    return {"v": 1, "project": p.slug, "task": a and a["id"], "type": a and a["type"], "tier": a and a["tier"],
            "title": title, "step": step, "queue": len(sd["queue"]), "inbox": len(sd["inbox"]),
            "blocked": len(sd["blocked"]), "lanes": len(sd["lanes"]), "paused": paused, "drive": bool(sd["drive"]),
            "autonomy": sd["autonomy"], "text": c.state_line(sd),
            "tooltip": f"{p.slug}: " + (f"{a['id']} {title}" if a else "no active task"),
            "class": "paused" if paused else "active" if a else "blocked" if sd["blocked"] else "idle"}


def cmd_glance(args):
    import fmcli
    try:
        p = fmcli.resolve(args, create=False)  # a bar polling outside a project never makes one
    except fmcli.UsageError:
        if getattr(args, "project", None):
            raise
        return print(json.dumps({"v": 1, "project": None, "text": "", "tooltip": "not in a Foreman project",
                                 "class": "none"}))
    print(json.dumps(glance(p), ensure_ascii=True))  # escaped: no U+2028 a line reader could split on


# ---------------------------------------------------------------- fm lsp

MAX_BODY = 32 << 20  # a frame bigger than this ends the session (no client sends a 32 MB brief)
WARNING, INFO = 2, 3


def _u16(text):
    return len(text.encode("utf-16-le")) // 2  # LSP columns count UTF-16 code units


def gaps(text):
    """A brief's proof gaps as LSP diagnostics: a criterion with no verify command or no evidence, a step with no
    evidence (no test run recorded). Text that isn't a brief has none."""
    if not isinstance(text, str):
        return []
    text = text.replace("\r\n", "\n")
    try:
        b = c.Brief.parse(text)
    except ValueError:
        return []
    tid, out, section, ac = b.id or "ID", [], None, 0
    proven = {(m.group(1), int(m.group(2))) for x in b.evidence() if (m := c._EV_RE.match(x))}  # has_evidence, once
    lines = text.split("\n")
    for i in range(text[:text.find("\n---\n", 4) + 5].count("\n"), len(lines)):
        line, hit = lines[i], None
        if line.startswith("## "):
            section = line[3:].strip()
        elif section == "Acceptance criteria" and (m := c._AC_RE.match(line)):
            ac += 1
            if not c.verify_of(m.group(2)):
                hit = WARNING, f"criterion {ac} has no verify command, so nothing can prove it"
            elif ("ac", ac) not in proven:
                hit = (WARNING if m.group(1) in "xX" else INFO,
                       f"criterion {ac} has no evidence yet: fm task evidence {tid} --ac {ac} --run \"<cmd>\"")
        elif section == "Steps" and (m := c._STEP_RE.match(line)) and ("step", int(m.group(1))) not in proven:
            n = int(m.group(1))
            hit = (WARNING, f"step {n} is ticked but has no evidence: no test run recorded for it") if m.group(2) in "xX" \
                else (INFO, f"step {n} has no evidence yet: fm task evidence {tid} --step {n} --run \"<test>\"")
        if hit:
            out.append({"range": {"start": {"line": i, "character": 0}, "end": {"line": i, "character": _u16(line)}},
                        "severity": hit[0], "source": "foreman", "message": hit[1]})
    return out


def _frames(inp):
    """Each message body in turn (None for a frame without a usable Content-Length); ends at EOF or an oversized frame."""
    while True:
        n, seen = None, False
        while True:
            line = inp.readline(65536)
            if not line:
                return
            if not line.strip():
                if seen:
                    break
                continue  # blank lines between frames
            seen = True
            k, _, v = line.partition(b":")
            if k.strip().lower() == b"content-length" and v.strip().isdigit():
                n = int(v)
        if n is None:
            yield None
            continue
        if n > MAX_BODY:
            return
        body = inp.read(n)
        if len(body) < n:
            return
        yield body


def serve(inp, out):
    """The stub: initialize, shutdown and exit; didOpen, didChange, didSave (with text) and didClose publish the
    document's proof gaps. Full sync, so no document is kept. Exit code 0 only after a shutdown."""
    def send(msg):
        body = json.dumps(dict(msg, jsonrpc="2.0"), ensure_ascii=False).encode("utf-8")
        out.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
        out.flush()

    def publish(uri, text):
        if isinstance(uri, str):
            try:
                found = gaps(text)
            except Exception:  # a diagnostic is a hint: odd text must not end the editor's session
                found = []
            send({"method": "textDocument/publishDiagnostics", "params": {"uri": uri, "diagnostics": found}})

    down = False
    for body in _frames(inp):
        try:
            msg = json.loads(body) if body is not None else None
        except (ValueError, RecursionError):  # bad JSON or UTF-8, or nesting deeper than Python recurses
            msg = None
        if not isinstance(msg, dict):
            send({"id": None, "error": {"code": -32700, "message": "parse error"}})
            continue
        method, params = msg.get("method"), msg.get("params") if isinstance(msg.get("params"), dict) else {}
        doc = params.get("textDocument") if isinstance(params.get("textDocument"), dict) else {}
        changes = params.get("contentChanges")
        if method == "initialize":
            send({"id": msg.get("id"), "result": {
                "capabilities": {"textDocumentSync": {"openClose": True, "change": 1, "save": {"includeText": True}}},
                "serverInfo": {"name": "foreman"}}})
        elif method == "shutdown":
            down = True
            send({"id": msg.get("id"), "result": None})
        elif method == "exit":
            return 0 if down else 1
        elif method == "textDocument/didOpen":
            publish(doc.get("uri"), doc.get("text"))
        elif method == "textDocument/didChange" and isinstance(changes, list) and changes \
                and isinstance(changes[-1], dict):
            publish(doc.get("uri"), changes[-1].get("text"))
        elif method == "textDocument/didSave" and "text" in params:
            publish(doc.get("uri"), params["text"])
        elif method == "textDocument/didClose":
            publish(doc.get("uri"), None)
        elif "id" in msg and isinstance(method, str):
            send({"id": msg["id"], "error": {"code": -32601, "message": f"method not found: {method}"[:200]}})
    return 0 if down else 1


def cmd_lsp(args):
    return serve(sys.stdin.buffer, sys.stdout.buffer)
