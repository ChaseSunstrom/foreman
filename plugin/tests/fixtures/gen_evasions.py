#!/usr/bin/env python3
"""Generate the guard evasion corpus (T-1263): python3 plugin/tests/fixtures/gen_evasions.py

For each of bench_safety's dangerous commands and each everyday one, apply a fixed set of shell obfuscations
(quote splitting, backslash and $'' quoting, variable/array indirection, env -S, a function, eval of a literal,
a here-string, a written-then-run script file, base64 into sh) and ask the guard (no grants) to judge every variant.

Label: a variant's label is the guard's *correct* verdict for the plain command it obfuscates — block for a
dangerous command, allow for an everyday one. The four bench SNAPSHOT commands are left out: the guard allows them in
a project's own tree (Foreman snapshots the discarded work first) but blocks them in Foreman's own checkout, which is
protected core, so their verdict depends on the tree the test runs in. The BASH_ENV one is left out too: the guard
judges the file it loads, so its verdict depends on whether payload.sh exists in the home folder (T-1480).

A variant the guard judges as its label goes to guard_evasions.jsonl (the obfuscation did not change the verdict).
A variant the guard judges differently goes to guard_gaps.jsonl with the verdict it got and why — a block->allow gap
is an evasion that reaches a dangerous command past the guard; an allow->block gap is an over-broad refusal.

Deterministic and stdlib-only (plus the repo's own fmreplay/fmguard/bench_safety). The committed files are this
script's output; test_guard_evasions.py fails if regenerating changes them, so a guard change forces a reviewed
regeneration. ids are machine-independent: _key hashes the stored cwd "" (the home folder), never an absolute path.
Run in the repo, a variant's verdict changed with the tree: Foreman's main checkout is protected core, a builder's
worktree is not."""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))  # plugin/tests/fixtures
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
for p in (os.path.join(REPO, "plugin", "lib"), os.path.join(REPO, "site")):
    if p not in sys.path:
        sys.path.insert(0, p)

import fmreplay  # noqa: E402
from bench_safety import DANGEROUS, EVERYDAY, SNAPSHOT  # noqa: E402

CWD = ""  # the home folder (the guard's default): outside Foreman's protected checkout and the same on every machine


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


_COMPOUND = re.compile(r"[|&;<>]")  # an array or env -S holds one simple command; a pipe or list stays outside it


def array_indirect(cmd):
    return None if _COMPOUND.search(cmd) else f'a=({cmd}); "${{a[@]}}"'


def env_s(cmd):
    return None if _COMPOUND.search(cmd) else f"env -S {cmd}"


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


QUOTING = [quote_split, backslash, dollar_quote, var_indirect, array_indirect]
EVERY = QUOTING + [env_s, func_def, eval_literal, here_string, script_file, base64_sh]
_ASSIGN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


def _rows():
    """(transform name, original command, variant, label) in a fixed order.

    A dangerous command gets every transform (block is correct however it is spelled); everyday commands get the
    quoting transforms only. A command led by NAME=value skips the quoting ones: bash runs a quoted, escaped or
    expanded assignment as a command name, so those variants are a harmless 'command not found', not the command."""
    rows = []
    for _, cmd in DANGEROUS:
        if cmd in SNAPSHOT or "BASH_ENV=" in cmd:  # T-1480: BASH_ENV's verdict hangs on payload.sh existing here
            continue
        for t in EVERY:
            v = None if t in QUOTING and _ASSIGN.match(cmd) else t(cmd)
            if v:
                rows.append((t.__name__, cmd, v, "block"))
    for cmd in EVERYDAY:
        for t in QUOTING:
            v = None if _ASSIGN.match(cmd) else t(cmd)
            if v:
                rows.append((t.__name__, cmd, v, "allow"))
    return rows


def _why(tname, orig, label, got):
    if got == label:
        return f"{tname} of {orig!r} stays {label}"
    way = "reaches a dangerous command past the guard" if label == "block" else "over-broad refusal"
    return f"{tname} of {orig!r} should {label} but the guard says {got}: {way}"


def home_in_a_repo():
    """The corpus runs from the home folder; one inside a git tree (a dotfiles repo) is a project to the guard."""
    import fmguard
    return fmguard.project_root_for(os.path.expanduser("~"), os.path.expanduser("~")) is not None


def build():
    """(guard_evasions.jsonl text, guard_gaps.jsonl text). Runs every variant past the current guard."""
    rows = _rows()
    cwd_abs = fmreplay.resolve_cwd(CWD)
    if home_in_a_repo():
        raise SystemExit(f"{cwd_abs} is inside a git tree, so the guard judges the corpus as a project: "
                         "regenerate on a machine whose home folder isn't")
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
