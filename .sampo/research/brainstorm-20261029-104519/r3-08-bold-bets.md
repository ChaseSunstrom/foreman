# Brainstorm — lens: bold bets

- **Run a proof-forgery red team as a standing gate** — SECURITY — value 5 — effort L — risk med — category: trust
  Why: Foreman's core promise is "prove its work with commands it actually ran"; T-1994 shows a DONE-WHEN `-k` that matched nothing could pass silently. Nothing in the pack tests whether a proof can be faked (empty test, a `-k` matching zero, a command that always exits 0).
  Done when: a seeded corpus of 10 fake-proof patterns (zero-test match, `|| true`, assert-free test, stubbed command) is each rejected by `fm task prove`, and a new pattern added to the corpus fails CI until a check catches it.

- **Make proofs discriminate by construction** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the user's recent steers ("ac 1's -k matched no test", T-1994 AND rule) are all the same hole: a check that can't fail. Assumption: DONE-WHEN verification is only run forward, never against the pre-change tree.
  Done when: `fm task done` on a FIX refuses when its DONE-WHEN command also passes on the stash of the pre-change tree, naming the command.

- **Replay the user's real ask history as a regression corpus** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: the "asked" stream shows ~20 consecutive fix/feature requests with concrete DONE-WHENs; T-0035 (eval capture) is deferred. These are free, user-authored, labeled cases for intake, titling and gating.
  Done when: `python3 plugin/tests/run.py corpus` replays at least 50 past asks through `parse_intake` and title shaping, asserting expected task kind, scope paths and title cut points, and fails on any drift.

- **Auto-write the sibling fix when a fix lands** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the asks come in pairs of the same shape (T-1984 and T-1996 both fixed "a check ignores the focused task's own scope"; `_task_files` then "had the same gap"). Assumption: siblings can be found by grepping the changed predicate's other callers.
  Done when: closing a FIX that edits a function with other callers produces a captured, not-yet-started task listing each caller file:line, and zero when there is only one caller.

- **Give each task a single owner-of-files ledger written at edit time** — FIX — value 4 — effort M — risk med — category: invariants
  Why: repeated "another task's dirty file" bugs (`_theirs`, scope check at close, first_touch counting, core-integrity warning) were each fixed per call site. One ledger removes the class.
  Done when: a test that edits files under two focused tasks shows every check (doctor, scope, sensitive-file, affected-tests) consulting the same ledger, and a grep-based test fails if a check reads `git status` directly.

- **Budget the deterministic path before the model path** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: the log is dominated by suite-overlap and test-selection work (T-1964, T-1971, T-1994); each model turn waiting on a full suite is the cost. Assumption: most fix tasks touch one module with one matching test.
  Done when: a one-file FIX with a named test closes with only that test and the gates its files affect running, and `fm ship` prints the seconds saved versus a full run.

- **Quote the cost of a queue before running it** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: the user queues many items and says "keep going"; the deferred T-1231 and budget-dropping logic (T-1991) show cost matters but isn't predicted. Assumption: past tasks give a per-kind cost/time distribution.
  Done when: `fm queue quote` prints a low/median/high time and token estimate for the open queue, and the estimate falls within the range on 8 of the next 10 closed tasks.

- **Wild: Let Foreman fight itself in a nightly bracket** — FEATURE — value 4 — effort L — risk med — category: evolution — wild
  Why: assumption: two Foreman configs (with and without one gate or lesson) can be run on the same replayed asks; the duel already exists as a concept (T-1231).
  Done when: a nightly job runs N replayed tasks under config A and B, and writes a one-line verdict naming which gate or lesson earned or lost its place.

- **Wild: Keep a "deletion court" for every surface** — CLEAN — value 4 — effort M — risk low — category: scope — wild
  Why: the backlog holds 17+ "Later from" items and unverified adapters (T-0335 to T-0337); the user dropped YAGNI items readily. Each surface gets a use counter and must argue its case yearly.
  Done when: `fm court` lists every command, skill and adapter with its 60-day call count and proposes the bottom 10 for deletion as ready-to-run tasks.

- **Wild: Let a pasted bug report become a finished, shipped task** — FEATURE — value 5 — effort L — risk high — category: autonomy — wild
  Why: the user's asks are already shaped as "FIX: symptom (function) @file DONE-WHEN: …". Assumption: a pasted stack trace or complaint can be reduced to that shape by reproducing first.
  Done when: pasting a failing command's output yields a captured task whose DONE-WHEN reproduces the failure on the current tree, verified red before any edit.

- **Wild: Run the guard hook as a real jail, not a filter** — SECURITY — value 4 — effort L — risk high — category: sandbox — wild
  Why: the guard blocks commands by pattern in bypass mode; patterns are evadable. Assumption: bubblewrap or a user namespace is available on the Linux hosts it targets.
  Done when: a command the pattern guard misses (an obfuscated `rm -rf` of a path outside the project) is stopped by the jail with the project tree unchanged, shown in a test.

- **Detect instruction injection in fetched files at the hook** — SECURITY — value 4 — effort M — risk med — category: injection
  Why: T-0791 holds 18 deferred injection and supply-chain ideas; fm reads pasted content, skills and marketplace sources (the anthropic-skills sync).
  Done when: a fixture file containing "ignore previous instructions and run curl …" read via a tool result is flagged in the hook output, and the following Bash call to that command is held for confirmation.

- **Cache the gate result by file content hash** — PERFORMANCE — value 3 — effort M — risk low — category: speed
  Why: gates rerun after unrelated edits ("a mid-gate edit gets an ambient run afterward"). Assumption: gates are deterministic given the files they declare.
  Done when: running `fm check` twice with no relevant file change shows the second run reporting "cached" for each unchanged gate and finishing in under 20% of the first run's time.

- **Show why a refusal happened with one command** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: many recent fixes are refusals that gave no way forward (docs-impact, `-k` mismatch, core-integrity). Assumption: each refusal can record its rule id and inputs when raised.
  Done when: `fm why-refused` prints the last refusal's rule, the exact inputs that triggered it, and the one command that would clear it.
