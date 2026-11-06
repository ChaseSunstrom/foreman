## Verdict
Changes needed. The core change is correct, but the third-refusal advice still points to a grant that can't help, and one unread-program refusal is still liftable.

## lens: intent
- MEDIUM — plugin/lib/fmguard.py:4015 — The size-limit refusal ("{path} is N KB, over the 256 KB the guard reads: run its commands directly or split it") is also a system refusal for a script never read. It doesn't match `_unread` (no "can't read", not the parse-budget suffix). `bash big.sh` over 256 KB still runs unread under `--allow system`. The CHANGELOG line says "or one it can't open", but no refusal in the code says that. The size-limit one is the only other "script too long" refusal. — Add an `_unread` clause for it, with a test (a >256 KB file under `allow=("system",)`), or drop "can't open" from the CHANGELOG and capture the gap. — confidence: medium. I'm unsure whether the user meant only the parse-time one.

## lens: adversary
- No bypass found. Every `_unread` detail I traced (3510, 3541-3542, 776, 4060-4067, 4427) is matched by the new `check` clause. A user path or script line containing "can't read" can only over-refuse, never lift.

## lens: edge
- MEDIUM — plugin/lib/fmguard.py:3890, 3931 — `_unread` matches on "can't read", so "sed -f/--file runs a script file the guard can't read here" and "vim -S/-s/-u/-l/--cmd loads a script the guard can't read" are now unliftable too. `_hint` (174-214) has no case for them, so the message says "no grant lifts this" with no way through. `sed -f x.sed file` with a system grant used to run. Reproducer: `sed -f s.sed f` under `allow=("system",)`. Neither the AC nor the changelog mentions it. — Add a `_hint` line (for example "put the sed commands in -e, or run the script file as a script the guard reads") or narrow `_unread`; say so in the CHANGELOG. — confidence: high that the behaviour changed, medium that it's unwanted.

## lens: operator
- MEDIUM — plugin/lib/fmhooks.py:1782-1784 — The 3rd-repeat advice branches only on `guard.unanalysed(...)`. For an unread system refusal it still says "ask the user (fm ask ID system …)". That yes is now useless, so the agent is sent into a dead-end ask loop. T-1929 handled this for UNANALYSED but T-1932 didn't. Reproducer: 3 identical `echo x | sh` blocks in one session, then read the reason. — Export one predicate (for example `guard.unliftable(block)` = `unanalysed(d) or cat == "system" and _unread(d)`) and use it in `check`, `_message` and this site. — confidence: high.
- Cost at scale: one substring test per system finding, which is negligible.

## lens: maintainer
- LOW — plugin/lib/fmguard.py:137 — The "unliftable" rule is now spelled in three places: `unanalysed()`, the `check` clause and `_message`. The next refusal class will miss one, as fmhooks did. This is the same fix as the operator finding.
- Tests: the new assertions in plugin/tests/test_guard.py fail without the change. I saw no test for the sed/vim "can't read" cases or the 256 KB case.

## Acceptance criteria
- Every `_unread` system refusal stays refused under `--allow system`, and its message names no grant: met for the pipe, IFS, too-deep and parse-budget cases (test_guard.py:528, 538-539; fmguard.py:136-137, 263-264). The size-limit refusal is not covered (see intent).
- Other system refusals are still lifted: met (test_guard.py:541, crontab and the sudo commands).
- I didn't run `python3 plugin/tests/run.py test_guard` (read-only).

## Implicit decisions
- It reuses the existing `_unread` substring test and doesn't add a new category.
- Unliftability applies only to `system`.
- The message wording copies T-1929's "no grant lifts this."

## Not checked
- The test suite run.
- The wider guard walk.
- The CHANGELOG format against the checklist: the entry is in plain words and has no exploit detail.

Noticed: the `_unread` substring test on free text (the T-1929 pattern) remains. A path such as /etc/"can't read" makes an ordinary system-folder refusal unliftable.
