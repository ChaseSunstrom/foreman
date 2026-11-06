# Brainstorm — lens: blind spots

Eight of the pack's missed asks (T-2499 to T-2505, T-2525) fall into five classes. For each class I ask what else in the project is still in it. The earlier brainstorms already cover session-bound loops, stale maps, form-only gauges and sibling premises, so I took different angles.

| Class | Question a brainstorm should have asked |
|---|---|
| Unseen dimension (T-2500) | What does every ledger row record, and what does it fail to say about where the row came from? |
| Self-measured numbers (T-2503, T-2504) | Which numbers does Foreman produce, time and judge itself, with nothing outside it checking? |
| No fresh look (T-2501, T-2502, T-2505) | What is only ever reviewed by the thing that built it? |
| Needs a session to advance (T-2499) | What stops moving when the user is away? |
| Fixed one place, not its siblings (T-2525) | Where else does the same premise live? |

- **Score each brainstorm by the asks it missed** — FEATURE — value 5 — effort M — risk low — category: meta-measure
  Why: eight asks in the pack were asks "no idea predicted", and nothing counts that rate.
  Done when: `fm ideas --report` prints, per lens, how many of the user's later asks it predicted, from the "asked" stream, and the next Seed opens with the weakest lens.

- **Time hooks from outside the harness** — PERFORMANCE — value 5 — effort M — risk low — category: lean
  Why: the 278 ms p95 comes from `fm friction`, which Foreman's own hooks log. That likely omits interpreter startup and host wait (assumption).
  Done when: `bench_hooks.py` records the host-side wall clock beside the self-reported time, and `fm doctor` flags a gap over 20%.

- **Make a lean hook-latency watchdog run in the night tick** — FEATURE — value 4 — effort S — risk low — category: lean
  Why: T-2499 showed that anything advancing only inside a session stalls while the user is away. Lean gauges are in that class (assumption).
  Done when: a tick with no session files one task when hook p95, injected context or verb count crosses its ratchet, and files nothing otherwise.

- **Measure each guard rule's precision from what happens after a block** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: 42 blocks of `core:interpreter-code-driving-foreman` and 2 brief-guard false positives are known, but nothing says which rules mostly block the wrong thing.
  Done when: each rule shows blocks, the user's overrides and same-intent retries, and a rule over 30% false positives is flagged. The guard is never auto-loosened.

- **Report the effective guard settings and name any typo'd key** — FIX — value 4 — effort S — risk low — category: guard
  Why: assumption: a misspelled settings key falls back to a default that could be fail-open. The pack shows many knobs (`--pace`, `--round-first`).
  Done when: `fm doctor` lists each guard-relevant key with its value and source, and a test with an unknown key fails loudly instead of silently running with defaults.

- **Fuzz the guard and brief-guard for pathological input** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the brief-guard already misreads `.join(` and dict keys as paths, so its parsing is fragile. A slow parse also blows the hook tail latency (assumption).
  Done when: a 1 MB adversarial command and a 10k-path brief each finish in under 50 ms, and a test pins that.

- **Find write-only ledger fields** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: assumption: T-2500 shows fields were added to ledgers without anyone reading them. The same cost-without-reader pattern fits the 1219 stack cards, of which 5 are used.
  Done when: a sweep lists every logged field with no reader in `plugin/lib`, and each is either read, dropped or recorded as a deliberate keep.

- **Quote the cost before a fan-out** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: this run is 10 lenses × 4 rounds × 3 deepens, and no cold read or brainstorm child shows its price up front (assumption).
  Done when: `fm ideas` and the cold reads print the child count and an estimated spend first, and refuse over `--max-cost` unless forced.

- **Garbage-collect state for repos that moved or vanished** — CLEAN — value 2 — effort S — risk med — category: lean
  Why: assumption: state sits under `state/projects/<name>-<hash>`, so a moved checkout orphans it.
  Done when: `fm doctor` lists orphaned project state with its size, and moving it is a user-confirmed verb (dry-run by default).

- **Count the attention the user is asked for** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: there are many "blocked on user" rows, digests, yes-bundles and cards, but no one budget across them.
  Done when: a daily count of items needing the user's eyes is shown with a ceiling, and surplus items roll into the one batched yes.

- **Wild: Backtest the brainstormer on its own missed asks** — FEATURE — value 4 — effort M — risk low — category: meta-measure — wild
  Why: the pack lists eight missed asks as ready-made held-out cases.
  Done when: replaying the Seed from before each missed ask through the current lenses reports how many it now predicts.

- **Wild: Corrupt a settings copy nightly and check the guard stays closed** — SECURITY — value 3 — effort M — risk low — category: guard — wild
  Why: assumption: configuration decay is a silent way for a guard to go open.
  Done when: a nightly job damages a copy of the settings in ten ways and each damage either blocks the unsafe command or is reported.

- **Wild: Show a "this week's blind spot" card** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: the user keeps having to ask for things no one anticipated, so the harness could point at its own likely blind spot first.
  Done when: Monday's digest names the one area with the most user asks and no coverage cell, with a one-word skip or build.

Next question: Which Foreman numbers or gates does only Foreman itself time, score or judge, and what outside signal could check each one?
Next question: Which loops, grants or digests wait on the user's presence, and what does each one cost per day of absence?
