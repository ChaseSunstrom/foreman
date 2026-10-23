"""fm dojo (T-1608): a short drill, for people, of commands the guard refuses and why. Each round shows one command
from the guard's labelled corpus; you say allow or refuse, then see what the guard does (judged live, as the hook
would, with no grants) and why. Off a terminal, or with --json, it prints the drill as a study sheet with the answers.
"""
import os
import random
import re
import sys

import fmcore as c


def rounds(n=8, seed=None):
    """[{cmd, cwd, should, why, category}] for n labelled cases, about half refused; category is the guard's live
    verdict (the category it refuses with, or allow)."""
    import fmreplay
    shipped = os.path.join(fmreplay._plugin_here(), "tests", "fixtures", "guard_cases.jsonl")  # the curated corpus
    cases, seen = [], set()
    for path in dict.fromkeys([shipped, fmreplay.cases_path()]):  # and what fm guard wrong stored here
        for k in fmreplay.load_cases(path)[0]:
            if (k["cmd"], k.get("cwd")) not in seen:
                seen.add((k["cmd"], k.get("cwd")))
                cases.append(k)
    rng = random.Random(seed)
    block = [k for k in cases if k["should"] == "block"]
    allow = [k for k in cases if k["should"] == "allow"]
    pick = rng.sample(block, min(len(block), (n + 1) // 2)) + rng.sample(allow, min(len(allow), n // 2))
    rng.shuffle(pick)
    where = lambda k: fmreplay.resolve_cwd(k.get("cwd") or "")  # noqa: E731  as fm replay judges the corpus
    live = fmreplay.verdicts([(k["cmd"], where(k)) for k in pick])
    return [{"cmd": k["cmd"], "cwd": k.get("cwd") or "~", "should": k["should"], "why": k.get("why") or "",
             "category": live.get(fmreplay._key(k["cmd"], where(k)))} for k in pick]


def _answer(d):
    refused = d["should"] == "block"
    cat = d["category"] if refused and d["category"] not in (None, "allow") else ""
    why = re.sub(r"^T-\d+:?\s*", "", c.plain(d["why"])) or "no reason recorded"  # a person needs the reason, not the id
    return f"the guard {'refuses' if refused else 'allows'} it: {why}" + (f" ({cat})" if cat else "")


def cmd_dojo(args):
    import fmcli
    if not 1 <= args.rounds <= 40:
        raise fmcli.UsageError("--rounds is 1 to 40")
    drills = rounds(args.rounds, args.seed)
    if not drills:
        return fmcli.out(args, [], "No labelled guard cases here to drill (plugin/tests/fixtures/guard_cases.jsonl).")
    quiz = args.quiz or (sys.stdin.isatty() and sys.stdout.isatty())
    if args.json or not quiz:
        return fmcli.out(args, drills, "\n".join(
            ["Guard dojo, the answers (on a terminal, fm dojo asks first):"]
            + [f"  {'✗' if d['should'] == 'block' else '✓'} {c.plain(d['cmd'])}\n      {_answer(d)}" for d in drills]))
    right = asked = 0
    for i, d in enumerate(drills, 1):
        where = "" if d["cwd"] in (".", "~") else f"   (in {c.plain(d['cwd'])})"
        print(f"\n{i}/{len(drills)}  {c.plain(d['cmd'])}{where}\n  allow or refuse? [a/r] ", end="", flush=True)
        said = sys.stdin.readline().strip().lower()[:1]
        if said not in ("a", "r"):  # end of input, or no answer: stop here
            print()
            break
        asked += 1
        ok = (said == "r") == (d["should"] == "block")
        right += ok
        print(f"  {'✓ right' if ok else '✗ not quite'}: {_answer(d)}")
    tip = ' Try any command: fm guard try "CMD"; a verdict you think is wrong: fm guard wrong.'
    print(f"\n{right}/{asked} right." + (tip if asked else ""))
    return 0
