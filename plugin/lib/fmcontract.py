"""fm contract (T-1158): how long and how much an unattended run may take. The Stop drive, the forever loop and fm run
consult over(p); past either bound they stop continuing and fm contract receipt says what ran. Spend is what fm budget's
ledger recorded since the contract began (fm run's sessions and subagents; an interactive session's own usage isn't in it)."""
import time

import fmbudget
import fmcore as c


def parse_until(hhmm, now=None):
    import fmcli  # lazy: the Stop hook imports this module and shouldn't pay for the CLI
    now = time.time() if now is None else now
    try:
        h, m = (int(x) for x in hhmm.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
    except ValueError:
        raise fmcli.UsageError(f"--until takes HH:MM (24-hour, local time), got {hhmm!r}")
    lt = time.localtime(now)
    t = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, h, m, 0, 0, 0, -1))
    return t if t > now else time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday + 1, h, m, 0, 0, 0, -1))


def _iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def spent(p, since, upto=None):
    lo, hi = _iso(since), _iso(upto) if upto else "9"
    return sum(e.get("usd") or 0 for e in fmbudget.ledger(days=3650)
               if e.get("project") in (p.slug, None) and lo <= str(e.get("ts", "")) <= hi)


def over(p, now=None):
    """'time' or 'spend' once a bound is reached (frozen at the first time it is seen), else None; no contract: None."""
    k = c.read_meta(p).get("contract")
    if not k:
        return None
    if k.get("ended"):
        return k["ended"]
    now = time.time() if now is None else now
    why = ("time" if k.get("until") and now >= k["until"]
           else "spend" if k.get("usd") is not None and spent(p, k["started"]) >= k["usd"] else None)
    if why:
        c.update_meta(p, contract={**k, "ended": why, "ended_at": now})
    return why


def receipt(p):
    over(p)  # notice a bound reached since anyone last looked
    k =c.read_meta(p).get("contract")
    if not k:
        return "no contract"
    end = k.get("ended_at")
    since = _iso(k["started"])
    done = [e["task"] for e in c.ledger_tail(p, 20000) if e.get("event") == "task_done" and e.get("task")
            and str(e.get("ts", "")) >= since and (not end or str(e["ts"]) <= _iso(end))]
    return (f"contract receipt: {len(done)} task(s) closed" + (": " + ", ".join(done) if done else "")
            + f" · spend ${spent(p, k['started'], end):.2f}" + (f" of ${k['usd']:g}" if k.get("usd") is not None else "")
            + f" · bound that ended it: {k.get('ended') or 'none yet'}")


def line(p):
    """The fm next suffix: the contract's state, empty with none."""
    k = c.read_meta(p).get("contract")
    if not k:
        return ""
    if over(p):
        return f" · contract ended ({c.read_meta(p)['contract']['ended']} bound): the drive stops; fm contract receipt"
    return ""


def cmd_contract(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "off":
        meta = c.read_meta(p)
        meta.pop("contract", None)
        c.write_meta(p, meta)
        return fmcli.out(args, {"contract": None}, f"{p.slug}: contract off.")
    if args.action == "receipt":
        return fmcli.out(args, {"receipt": receipt(p)}, receipt(p))
    if args.until or args.usd is not None:
        if args.usd is not None and not args.usd >= 0:
            raise fmcli.UsageError("--usd must be a number >= 0")
        now = time.time()
        k = {"started": now, "usd": args.usd, "until": parse_until(args.until, now) if args.until else None}
        c.update_meta(p, contract=k)
    k = c.read_meta(p).get("contract")
    if not k:
        return fmcli.out(args, {"contract": None}, f"{p.slug}: no contract (fm contract --until HH:MM --usd N).")
    why = over(p)
    bits = ([f"until {time.strftime('%a %H:%M', time.localtime(k['until']))}"] if k.get("until") else []) \
        + ([f"${k['usd']:g}"] if k.get("usd") is not None else [])
    fmcli.out(args, {"contract": k, "over": why}, f"{p.slug}: contract {' and '.join(bits)}"
              + (f" — ended by the {why} bound" if why else ", holding") + ".")
