<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Characterisation tests: pin behaviour before a refactor

Use when you must change code that has thin or no tests and nobody can say exactly what it does: a refactor,
a port to another language or library, a performance rewrite, or a cleanup that should change nothing.
The tests record what the code does today, right or wrong; they are a safety net, not a specification.

Built on library cards: `fm lib show characterization-tests` (the technique), `fm lib show golden-files` and
`fm lib show approval-tests` (storing large outputs), `fm lib show legacy-code` (seams for untestable code),
`fm lib show refactoring` (small behaviour-preserving steps).

## The procedure

1. **Mark the blast radius.** List the functions, endpoints or commands the change will touch, and their callers.
   Pass: the brief names each entry point the pins must cover.
2. **Pick inputs from reality,** not from imagination: production samples, logged requests, existing fixtures,
   plus the edges (empty, zero, negative, huge, non-ASCII, malformed). Include inputs that raise: an error is
   behaviour too. Pin files get committed: scrub production samples first (replace secrets, tokens, emails,
   names, addresses and account numbers with synthetic values of the same shape), and grep the pin files for
   them before the commit. Pass: you name the grep and it finds nothing.
3. **Find a seam** where you can call the code and read the result without the network, the clock or random
   numbers. Freeze or inject those; if the code reads them directly, add the smallest seam first (a parameter
   with the old default) and commit that alone.
4. **Pin on the unchanged code** (snippet below). The first run writes the recorded outputs and fails; review
   the file, commit it, rerun. Pass: the pins are committed before the first refactor commit.
5. **Check the pins reach the code.** Branch coverage on the touched module, or deliberately break one line and
   watch a pin fail. Pass: you name the line you broke and the pin that caught it.
6. **Refactor in small steps,** running the pins after each. A refactor commit never edits the recorded
   outputs. Pass: `git diff --stat` on the pin files is empty for every refactor commit.
7. **Bugs found on the way stay pinned.** If a pin records a wrong answer, keep it, capture the bug as its own
   task, and fix it after the refactor in a commit that changes that one expected value.
8. **Decide the pins' fate.** Replace them with intention-revealing tests, or keep them and say why.

## A pin harness in twenty lines

Runs as is (Python, stdlib only); keep one JSON file per entry point under `tests/pins/`.

```python
import json, os

def pin(path, fn, cases):
    got = {}
    for args in cases:
        key = repr(args)  # before the call: fn may mutate its arguments
        try:
            got[key] = repr(fn(*args))
        except Exception as e:  # errors are behaviour too
            got[key] = f"raises {type(e).__name__}: {e}"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(got, f, indent=1, sort_keys=True)
        raise AssertionError(f"pinned {len(got)} cases to {path}: review it, commit it, rerun")
    with open(path, encoding="utf-8") as f:
        assert got == json.load(f)
```

`repr` must be stable: sort sets and dict keys, and strip addresses and timestamps from the output before
pinning, or the pin fails on every run.
