# Brainstorm — lens: reliability

Lens: reliability, mission #12 "Staying lean and safe". Measured: hook p95 278 ms, 387k context per reply, 42 guard blocks of `interpreter-code-driving-foreman`, 2 brief-guard false positives, 5 of 1219 cards used, SessionStart note ~2k chars × 89.

- **Hook latency budget per event, enforced in CI** — PERFORMANCE — value 5 — effort M — risk low — category: hooks
  Why: p95 is 278 ms across 13533 runs, and gen-0 says hook p95 may not grow; `bench_hooks.py` exists but is only a gate listed in the map, not a per-event ratchet.
  Done when: `bench_hooks.py --runs 20` fails a test if any single event's p95 exceeds its stored budget, and the budget file shrinks only by a recorded commit.

- **Brief-guard false-positive corpus as regression tests** — FIX — value 4 — effort S — risk low — category: guard
  Why: 2 false positives read a dict key and a `.join(` call as written paths.
  Done when: both strings sit in a test file, pass the guard, while 20 known-bad path writes still block.

- **Guard mutation night: delete each rule in a copy, see a test fail** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: "keeps the guard intact" has no measure; a rule with no failing test when removed is unprotected. assumption: rules are enumerable from the guard's table.
  Done when: `fm guard drill` reports every rule with the test that caught its removal, and lists zero uncaught rules.

- **SessionStart note dedupe by hash** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: the ~2k-char note was injected 89 times; unchanged text on resume or compaction repeats.
  Done when: a second SessionStart with an identical note injects a one-line "unchanged (hash)" and the injected bytes drop ≥70% in the test.

- **Context-per-reply budget with named top contributors** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: 387k average per reply is mostly the host's, but Foreman's share is unmeasured. assumption: injected blocks can be tagged by source.
  Done when: `fm cost --by-source` prints Foreman's bytes per injection source, and a ratchet test fails on growth.

- **Withhold-one-block A/B to prove each injection earns its bytes** — PERFORMANCE — value 4 — effort M — risk med — category: lean
  Why: the lean steer says growth with no measurement waits; injected blocks themselves have no outcome measure.
  Done when: one block is withheld on 1 session in 10 and `fm outcomes` shows pass-rate with vs without, per block.

- **Fail-open vs fail-closed table for every hook, tested by crashing it** — FIX — value 5 — effort M — risk med — category: hooks
  Why: hooks run 13533 times; an exception or timeout must not silently drop the guard. assumption: no such table exists today.
  Done when: a test forces each hook to raise and to hang, and asserts the guard hook fails closed, the cosmetic ones open, and the doctor names which.

- **Dead-weight ratchet: unused verbs and cards listed, retired softly** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: 5 of 1219 cards used; gen-0 §6 requires subtracting as adding, but unmeasured library growth only waits.
  Done when: `fm burden --dead` lists cards unused in 90 days, `--retire` moves them to a restorable shelf, and the card count falls with no test red.

- **Guard-block explainer with the safe alternative** — FIX — value 3 — effort S — risk low — category: guard
  Why: `interpreter-code-driving-foreman` blocked 42× in 7 days, so the agent repeatedly hits it; each repeat wastes a turn.
  Done when: the block message names the equivalent `fm` verb and a test shows the repeat count of that rule per session drops on replay.

- **Wild: Hostile-session replay — feed the guard a week of real hook inputs plus child-written evasions** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: wild; only inputs Foreman didn't author find real holes. assumption: hook inputs are logged enough to replay.
  Done when: a nightly replay reports blocks, false positives and evasions that passed, and a new evasion files a red-first task.

- **Wild: Lean twin — run the same task with Foreman's hooks off and compare cost and time** — PERFORMANCE — value 4 — effort L — risk med — category: lean
  Why: wild; the only honest measure of "staying lean" is Foreman's overhead per session.
  Done when: `fm overhead` prints seconds and tokens added per session over 20 paired runs.

- **Wild: Hook black-box recorder with one-command replay** — FIX — value 3 — effort M — risk low — category: observability
  Why: wild; p95 spikes and guard false positives can't be reproduced without the exact input.
  Done when: `fm hooks replay N` re-runs the Nth recorded hook input and shows the same decision and timing within 20%.

- **Warm-daemon hooks with cold fallback, guard stays in-process** — PERFORMANCE — value 3 — effort L — risk high — category: hooks
  Why: python startup likely dominates 278 ms. assumption: no daemon exists.
  Done when: p95 of non-guard hooks drops below 100 ms and killing the daemon changes nothing but speed.

Next question: Which of Foreman's injected blocks has the user ever acted on, and can that be read from the transcript rather than guessed?
Next question: If hook p95 is dominated by interpreter startup, would a measured fast path in a non-Python shim beat any amount of Python tuning?
