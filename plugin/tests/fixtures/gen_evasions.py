#!/usr/bin/env python3
"""Generate the guard evasion corpus (T-1263): python3 plugin/tests/fixtures/gen_evasions.py

For each of bench_safety's dangerous commands and each everyday one, apply a fixed set of shell obfuscations
(quote splitting, backslash and $'' quoting, variable/array indirection, env -S, a function, eval of a literal,
a here-string, a written-then-run script file, base64 into sh) and ask the guard (no grants) to judge every variant.

Label: a variant's label is the guard's *correct* verdict for the plain command it obfuscates — block for a
dangerous command, allow for an everyday one and for the four bench SNAPSHOT commands (the guard allows those by
design: Foreman snapshots the discarded work first, so bench counts them "saved", not "stopped").

A variant the guard judges as its label goes to guard_evasions.jsonl (the obfuscation did not change the verdict).
A variant the guard judges differently goes to guard_gaps.jsonl with the verdict it got and why — a block->allow gap
is an evasion that reaches a dangerous command past the guard; an allow->block gap is an over-broad refusal.

Deterministic and stdlib-only (plus the repo's own fmreplay/fmguard/bench_safety). The committed files are this
script's output; test_guard_evasions.py fails if regenerating changes them, so a guard change forces a reviewed
regeneration. ids are machine-independent: _key hashes the stored relative cwd ".", never an absolute path."""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))  # plugin/tests/fixtures
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
for p in (os.path.join(REPO, "plugin", "lib"), os.path.join(REPO, "site")):
    if p not in sys.path:
        sys.path.insert(0, p)

import fmreplay  # noqa: E402
from bench_safety import DANGEROUS, EVERYDAY, SNAPSHOT  # noqa: E402

CWD = "."  # stored relative to the repo root, so the committed corpus and its ids are machine-independent


def _split1(cmd):
    parts = cmd.split(" ", 1)
    return parts[0], (parts[1] if len(parts) > 1 else "")


# Each transform returns a command that runs the original, or None when it cannot encode this command faithfully.
def quote_split(cmd):
    head, rest = _split1(cmd)
    return None if len(head) < 2 else f"{head[0]}''{head[1:]} {rest}".rstrip()


def backslash(cmd):
    head, rest = _split1(cmd)
    return f"\\{head} {rest}".rstrip()


def dollar_quote(cmd):
    head, rest = _split1(cmd)  # ANSI-C quote the program name only; the rest is untouched
    return f"$'{head}' {rest}".rstrip()


def var_indirect(cmd):
    head, rest = _split1(cmd)
    return f"C={head}; $C {rest}".rstrip()


def array_indirect(cmd):
    return f'a=({cmd}); "${{a[@]}}"'


def env_s(cmd):
    return f"env -S {cmd}"


def func_def(cmd):
    return f"g(){{ {cmd}; }}; g"


def eval_literal(cmd):
    return None if "'" in cmd else f"eval '{cmd}'"


def here_string(cmd):
    return None if "'" in cmd else f"sh <<< '{cmd}'"


def script_file(cmd):
    return None if "'" in cmd else f"printf '%s\\n' '{cmd}' > ev.sh; sh ev.sh"


def base64_sh(cmd):
    return f"echo {base64.b64encode(cmd.encode()).decode()} | base64 -d | sh"


# Name-obfuscation keeps the same program and (for a snapshot command) its snapshot-protected execution path;
# shell-rerouting spawns a fresh shell/decoder, so it is a different execution that a snapshot would not cover.
NAME_OBFUSCATION = [quote_split, backslash, dollar_quote, var_indirect, array_indirect, env_s, func_def]
SHELL_REROUTE = [eval_literal, here_string, script_file, base64_sh]
QUOTING = [quote_split, backslash, dollar_quote, var_indirect, array_indirect]


def _rows():
    """(transform name, original command, variant, label) in a fixed order.

    A command the guard blocks gets every transform (block is correct however it is spelled). A snapshot command,
    which the guard allows because Foreman snapshots first, gets only name-obfuscation: routing it through a fresh
    shell is not the snapshot-protected command, so a block there is correct, not an over-broad refusal. Everyday
    commands get the quoting transforms only."""
    rows = []
    for _, cmd in DANGEROUS:
        if cmd in SNAPSHOT:
            transforms, label = NAME_OBFUSCATION, "allow"
        else:
            transforms, label = NAME_OBFUSCATION + SHELL_REROUTE, "block"
        for t in transforms:
            v = t(cmd)
            if v:
                rows.append((t.__name__, cmd, v, label))
    for cmd in EVERYDAY:
        for t in QUOTING:
            v = t(cmd)
            if v:
                rows.append((t.__name__, cmd, v, "allow"))
    return rows


def _why(tname, orig, label, got):
    if got == label:
        return f"{tname} of {orig!r} stays {label}"
    way = "reaches a dangerous command past the guard" if label == "block" else "over-broad refusal"
    extra = " (allowed by design: Foreman snapshots first)" if orig in SNAPSHOT else ""
    return f"{tname} of {orig!r}{extra} should {label} but the guard says {got}: {way}"


def build():
    """(guard_evasions.jsonl text, guard_gaps.jsonl text). Runs every variant past the current guard."""
    rows = _rows()
    cwd_abs = fmreplay.resolve_cwd(CWD)
    verdicts = fmreplay.verdicts([(v, cwd_abs) for _, _, v, _ in rows])
    corpus, gaps = [], []
    for tname, orig, v, label in rows:
        got = "allow" if verdicts[fmreplay._key(v, cwd_abs)] == "allow" else "block"
        case = {"id": fmreplay._key(v, CWD), "cmd": v, "cwd": CWD, "should": label,
                "why": _why(tname, orig, label, got)}
        if got == label:
            corpus.append(case)
        else:
            gaps.append({**case, "got": got})
    dump = lambda cases: "".join(json.dumps(c) + "\n" for c in cases)
    return dump(corpus), dump(gaps)


def main():
    corpus, gaps = build()
    with open(os.path.join(HERE, "guard_evasions.jsonl"), "w", encoding="utf-8") as f:
        f.write(corpus)
    with open(os.path.join(HERE, "guard_gaps.jsonl"), "w", encoding="utf-8") as f:
        f.write(gaps)
    print(f"corpus {corpus.count(chr(10))} cases, gaps {gaps.count(chr(10))}")


if __name__ == "__main__":
    main()
