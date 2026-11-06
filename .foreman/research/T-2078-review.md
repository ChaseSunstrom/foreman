**Verdict:** approve with nits. The three acceptance criteria are met, and `put` refuses gen-0 and every path outside the tower shape. I found one race in `init` and one false-positive refusal. I did not run the tests.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:70 — `init` refuses any text that `c.redact` would change. The keyword pattern at fmcore.py:979 matches `token: [REDACTED] or `password: [REDACTED], because it only needs a keyword, `:` or `=`, and four or more characters. A request like "NEVER: log the token: [REDACTED]" cannot be saved as gen-0. The only advice is "take it out first", which makes gen-0 no longer verbatim. — Name the kinds with `c.secret_kinds(text)` in the message, and either narrow the check to the high-confidence patterns (private key, JWT, API key, URL password) or add an explicit `--allow-secret`. — confidence medium
- LOW — plugin/lib/fmgenesis.py:84 — `put` silently rewrites the same prose to `[REDACTED]` in gap-map, seed and mission docs, and the user is never told. — Print "redacted: <kinds>" when `c.redact(text) != text`. — confidence medium
- LOW — plugin/lib/fmgenesis.py:104 — The request says "status shows the tower". The criteria read that as `fm genesis` with no action. `fm status` and `/foreman:status` show nothing about the tower. — Confirm the reading, or add a one-line tower summary to `fm status`. Also, catalogue.md and report.md are accepted by `put` but never listed in status. — confidence low

## lens: adversary
- MEDIUM — plugin/lib/fmgenesis.py:67-74 — The `os.path.exists` check runs outside `c.lock`. Two concurrent `fm genesis init --file A` and `--file B` calls both pass it. The second then runs `write_atomic`, whose `os.replace` succeeds on a 0444 file because the directory is writable (fmcore.py:941). That overwrites gen-0, which is meant to be immutable. Between `write_atomic` and `chmod` the new file is also 0644 and writable. — Move the exists check inside the `with c.lock(...)` block. Write with `os.open(O_CREAT|O_EXCL, 0o444)`, or `chmod` the temp file before the replace. — confidence high (by reading the code; no reproducer was run)
- Dismissed: the `fullmatch` regex on `put` names is solid. `../`, `/etc/x`, a trailing newline and `gen-0/seed.md` are all refused, and the test covers them. A planted symlink at `research/genesis/gen-1` would redirect a `put`, but that needs write access to the state directory already.

## lens: edge
- LOW — plugin/lib/fmgenesis.py:72,83 — `c.LockTimeout` after 5 seconds is neither an `OSError` nor a `ValueError`. It escapes the `except` in `cmd_genesis` as an unformatted error. — Add `c.LockTimeout` to the except tuple, or confirm that the top-level handler formats it. — confidence low
- `init` reads `--file` as bytes, and non-UTF-8 input is stored unchanged, which is correct. `put` reads in text mode, so CRLF becomes LF, which is fine for tower docs but not byte-faithful.

## lens: operator
- OK. The status read is one `listdir` plus one small file read. `init` and `put` each add one ledger event. There is no hook, no loop and no always-on context. MASTER.md and CHANGELOG.md match the code, and no module registry needed updating.

## lens: maintainer
- LOW — plugin/tests/test_genesis.py — Three paths have no test: `init` refusing a secret-like text, `put` redacting, and a missing `--file` (the UsageError at fmgenesis.py:124-125). Python-checklist item: a failure-path test. — Add one assertion for each. — confidence high
- The public functions `init`, `put`, `status` and `home` have no type hints. This matches the neighbouring modules, so it is only a nit.

## Acceptance criteria
- `init` saves gen-0 byte-identical, read-only, and refuses a second init: met (the test checks bytes, the mode bits, and a second init that exits nonzero and says "already"). The race above is not covered.
- `put gen-1/seed.md` files it, and paths outside the shape or gen-0.md are refused: met (fmgenesis.py:79, test lines 187-194).
- Status lists gen-0, the gap map, each generation's seed, missions and critiques, and the exam line count: met (fmgenesis.py:88-117, test lines 196-215).

## Implicit decisions
- Overwriting an existing `put` target is allowed, with no history kept.
- The exam count is the non-blank lines of `exam.jsonl`.
- gen-0 is checked with `c.redact` as the secret detector.
- N in `gen-N` starts at 1 and has no upper bound.
- `put` and `init` log ledger events named `genesis_put` and `genesis_init`.

## Not checked
- The tests were not run.
- Behaviour on a case-insensitive filesystem.
- Whether the top-level handler formats `LockTimeout`.

Noticed: none
