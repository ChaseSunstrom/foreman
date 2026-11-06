# Brainstorm — lens: user value

- **Fix the brief-guard path false positives** — FIX — value 4 — effort S — risk low — category: guard
  Why: the pack says two brief-guard false positives read a dict key and a `.join(` call as written paths. Each one blocks a legitimate brief, and a guard the user learns to distrust gets bypassed.
  Done when: a red-first test with a brief containing `d["a/b"]` and `",".join(x)` passes the guard, and a brief that really names a protected path is still blocked.

- **Split the SessionStart note into a hash and a delta** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: the pack measures a ~2k-char note injected 89 times. Assumption: most starts see unchanged state.
  Done when: a second session start with unchanged state injects under 200 chars, and a changed state injects only the changed lines (checked by a test on the hook output).

- **Break down the 387k context per reply by source** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: `fm cost` shows 387k per reply on average but not how much comes from Foreman's injections, the host's own prompt, tool output or the transcript. Without that split, "keep context small" can't be aimed at anything.
  Done when: `fm cost --by-source` prints bytes and tokens for each source, with Foreman's share as a percentage, and the sum matches the total within 2%.

- **Teach the model from its own guard blocks** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: `core:interpreter-code-driving-foreman` was blocked 42 times in 7 days. Each block is a wasted turn, and the same mistake repeats. Assumption: the repeats come from a few phrasings.
  Done when: the top repeated block gets a one-line avoid hint injected only in sessions where it fired before, and `fm friction` shows that block's weekly count falling over the next 7 days.

- **Stop shipping the 1214 unused stack cards** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: 5 of 1219 cards are used. Per §6, each generation must subtract as much as it adds.
  Done when: the installed footprint shrinks by a stated number of files, and `fm lib show NAME` still resolves any removed card on demand (fetched or generated) in a test.

- **Make `fm doctor` name the slowest hook and its cause** — FEATURE — value 3 — effort S — risk low — category: performance
  Why: p95 is 278 ms over 13533 runs, but the pack shows only the aggregate. The bench gate covers the synthetic path, not the user's real one.
  Done when: `fm doctor` lists the 3 slowest hooks by p95 with the event and the dominant step, and a test seeds a slow hook and sees it named first.

- **Require a retired-verb name for every new verb** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the §6 subtract rule is stated but enforced only by review. `fm burden --by-verb` already reports unused verbs.
  Done when: `fm task finish` refuses a diff that adds a verb with no matching removal, merge or `--waive` recorded with `fm decide`; a test covers both cases.

- **Re-run the guard corpus when the host CLI updates** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard depends on hook behaviour in Claude Code, Codex, Gemini CLI and opencode, which change under it. Assumption: no check currently fires on a host version change.
  Done when: a version change recorded at session start triggers the known-bad corpus through the real hook path, and a test with a stubbed host that stops sending the field turns `fm doctor` red.

- **Keep one lean-budget file that every coverage cell cites** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: the 61 empty cells in #12 would otherwise be 61 hand-written phrasings, which the "no templated cell" rule rejects. One budget file (hook ms, injected bytes, verbs per surface) gives each cell a concrete, checkable number.
  Done when: each filled #12 cell names a budget key and a measuring command, and a sweep check fails on a cell whose key doesn't exist.

- **Wild: Show Foreman's own cost on the status line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The user has to trust the "lean" claim, and this makes it visible per session, e.g. "Foreman: +0.3s, 1.2k tokens".
  Done when: the status line shows hook milliseconds and injected tokens for the current session, matching `fm cost` within 5%.

- **Wild: Prove "leave no trace" with an install-then-eject round trip** — SECURITY — value 3 — effort M — risk low — category: safety
  Why: wild. Someone wary of a hook-installing tool wants proof it can be removed. T-0794 mentions eject but doesn't prove byte-identical removal.
  Done when: a test installs into a scratch repo and home, runs `fm eject`, and finds no changed file or setting outside a listed allowlist.

- **Wild: Send a weekly "what the guard stopped" note in plain words** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. The 42 blocks are visible only in logs. A short note ("stopped 42 attempts to run Python that drives Foreman; 2 were wrong") shows the user what the guard earns.
  Done when: `fm night`'s digest includes the guard's count and its false-positive candidates, each with the command text and a one-word keep or loosen answer.

Next question: Which of the 61 empty cells are true n/a (for example the site's "operate") and which need a measured budget, and who decides?
Next question: Does any injected block (SessionStart note, lessons, steers) lose outcomes when withheld, and is that measured per host?
