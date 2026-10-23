"""fm mandate (T-1400): a sweeping request kept as one standing record (its text, its clauses, an end date, a spend
bound) that fm scout and fm night read. While it stands, what scout captures says it was found under it; once it ends,
scout captures one decision (renew it or let it lapse) and nothing more under it until the user renews or clears it."""
import time

import fmcore as c


def get(p):
    """The project's mandate with `expired` worked out, or None."""
    m = c.read_meta(p).get("mandate")
    if not isinstance(m, dict) or not m.get("text"):
        return None
    until = c.parse_ts(m.get("until"))  # a datetime, or None for a missing or damaged one (never ends)
    return dict(m, expired=bool(until and until.timestamp() <= time.time()))


def put(p, text, until, usd=None):
    """Set the mandate: text, its clauses (fm clauses), until (epoch seconds), an optional USD bound."""
    import fmrecall
    m = {"text": c.plain(text).strip(), "clauses": fmrecall.clauses(text)[:20], "until": c.iso(until),
         "set_at": c.now(), **({"usd": usd} if usd is not None else {})}
    c.update_meta(p, mandate=m)
    c.log_event(p, "mandate", data={"text": c.fit(m["text"], 200), "until": m["until"]})
    return m


def clear(p):
    with c.lock(p.dir):
        meta = c.read_meta(p)
        had = meta.pop("mandate", None)
        c.write_meta(p, meta)
    return had


def lapse_finding(m):
    """The one decision an ended mandate leaves: a scout Finding keyed by when it was set, so it's captured once."""
    import fmscout
    return fmscout.Finding(f"mandate:{m.get('set_at')}", f"Mandate ended: {c.fit(m['text'], 90)}", "RESEARCH", "S",
                           f"the standing mandate set {str(m.get('set_at'))[:10]} ended {str(m.get('until'))[:10]}; "
                           "nothing more is captured under it. Decide: renew it (fm mandate set \"<text>\" --until "
                           "YYYY-MM-DD) or let it lapse (fm mandate off).")


def _until(day):
    import fmcli
    try:
        t = time.mktime(time.strptime(day, "%Y-%m-%d")) + 86400 - 1  # the end of that local day
    except (TypeError, ValueError):
        raise fmcli.UsageError(f"--until takes a date, YYYY-MM-DD, got {day!r}")
    if t <= time.time():
        raise fmcli.UsageError(f"--until {day} has already passed: give a later date")
    return t


def cmd_mandate(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "set":
        if not args.text or not args.until:
            raise fmcli.UsageError('fm mandate set "<the sweeping request>" --until YYYY-MM-DD [--usd N]')
        m = put(p, " ".join(args.text), _until(args.until), args.usd)
        return fmcli.out(args, m, f"Mandate set until {m['until'][:10]}: {c.fit(m['text'], 120)} "
                                  f"({len(m['clauses'])} clause(s)); fm scout and fm night read it.")
    if args.action == "off":
        had = clear(p)
        return fmcli.out(args, {"cleared": bool(had)}, "Mandate cleared." if had else "No mandate was set.")
    m = get(p)
    if not m:
        return fmcli.out(args, {"mandate": None}, 'No mandate. fm mandate set "<request>" --until YYYY-MM-DD sets one.')
    state = "ended" if m["expired"] else "stands"
    return fmcli.out(args, {"mandate": m}, "\n".join(
        [f"Mandate {state} (until {str(m.get('until'))[:10]}): {m['text']}"] + [f"  - {x}" for x in m["clauses"][:10]]))
