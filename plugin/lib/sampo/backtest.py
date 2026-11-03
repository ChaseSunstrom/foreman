"""T-1058: fm backtest: where a changed rule, known fix or card would have fired on recorded sessions, and how those
calls went. Read-only; it reads the session logs fm replay reads and writes nothing."""
import re

from sampo import replay


def cmd_backtest(args):
    from sampo import cli
    from sampo import lib
    if sum(bool(x) for x in (args.rule, args.fix, args.card)) != 1:
        raise cli.UsageError("fm backtest takes one of --rule REGEX, --fix SIGNATURE, --card NAME")
    if args.rule:
        try:
            rx = re.compile(args.rule)
        except re.error as e:
            raise cli.UsageError(f"--rule is not a regex: {e}")
        hit, what = (lambda ev: bool(rx.search(ev["text"]))), f"rule /{args.rule}/"
    elif args.fix:
        sig = args.fix.lower()  # a fix fires on the failure text, so only on calls that failed
        hit, what = (lambda ev: ev["errored"] and sig in ev["result"].lower()), f"fix `{args.fix}`"
    else:
        if not any(x["stem"] == args.card for x in lib.cards()):
            raise cli.UsageError(f"no card named {args.card!r} (fm lib list)")
        rx = re.compile(r"(?<![\w-])" + r"[-\s]".join(map(re.escape, args.card.split("-"))) + r"(?![\w-])", re.I)
        hit, what = (lambda ev: bool(rx.search(ev["text"]))), f"card {args.card}"
    events = list(replay.events(args.days))
    fired = [e for e in events if hit(e)]
    d = {"fires": len(fired), "sessions": len({e["session"] for e in fired}), "errored": sum(e["errored"] for e in fired),
         "calls": len(events), "scanned_sessions": len({e["session"] for e in events})}
    if not events:
        text = f"no recent session logs in the last {args.days} days: nothing to backtest {what} on"
    else:
        text = (f"{what} would have fired {d['fires']} times in {d['sessions']} session(s) "
                f"of {d['scanned_sessions']} scanned ({d['calls']} calls); {d['errored']} followed by an error")
    return cli.out(args, d, text)
