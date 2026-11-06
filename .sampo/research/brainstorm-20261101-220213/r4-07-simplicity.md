# Brainstorm — lens: simplicity

- **Fill cells from verb tags, not prose** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the 61 empty cells need real, untemplated content, and a hand-written grid is where templating creeps in. Assumption: each `fm` verb can carry `stage` and `surface` tags in its registry entry, so a cell is a query over those tags and a missing cell is a missing tag.
  Done when: `fm genesis sweep` counts empty cells by querying verb tags, and adding a tag to one verb moves exactly one cell from empty to filled with no `coverage.md` edit.

- **Freeze other-agent support at guard-only** — CLEAN — value 4 — effort S — risk med — category: surfaces
  Why: T-0335, T-0336 and T-0337 are blocked and no host adapter is live-verified. T-0794 already proposes retiring adapters. The honest cell for Codex, Gemini and opencode is "guard and AGENTS.md only; drive, done-gate and grants unsupported".
  Done when: the three blocked tasks close as decided-not-built with the reason recorded, `fm doctor` prints the supported tier per host, and the "other agents" column has no cell claiming more than that tier.

- **Make the brief-guard path check stat-based** — FIX — value 3 — effort S — risk low — category: guard
  Why: two false positives read a dict key and a `.join(` call as written paths. Instead of tuning the regex, only treat a token as a path if it sits under a Files heading or it exists on disk (or its parent does).
  Done when: a red-first test with both known false positives passes, a corpus of real briefs shows no newly allowed write outside the repo, and the regex heuristics are deleted.

- **Collapse overlapping standing steers into canonical rules** — CLEAN — value 3 — effort M — risk med — category: rules
  Why: the steer list has many near-duplicates (several 2026-10-31 and 2026-11-01 entries cover pausing the long-horizon exam, deferring the exam to the end, and testing cadence). Rules text is injected, and gen-0 says rules size may not grow. Each merged rule keeps its dates, the original wording and its automatic check.
  Done when: the injected steer block is at least 30% smaller by bytes, `fm decide --check` still passes for every original steer, and a cold read finds no meaning lost.

- **Merge all hooks of one event into a single process** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: hook p95 is 278 ms over 13.5k runs. Assumption: several hooks on the same event each pay Python start-up and import cost. One dispatcher per event pays it once, and a failing sub-hook must not stop the guard.
  Done when: `bench_hooks.py --runs 20` shows p95 per event dropping, the guard still blocks with another sub-hook crashed on purpose, and the number of registered hook commands per event is 1.

- **Ship a standalone single-file guard for headless/server** — FEATURE — value 4 — effort M — risk med — category: headless
  Why: the standing rule says Foreman works with no `claude` on PATH, but the guard currently imports from `plugin/lib`. A stdlib-only `guard.py` that imports nothing from fm is the smallest safe install on a server or another host.
  Done when: copying only that file into an empty directory and running it under `python3 -I` blocks the 12 corpus commands, and a test fails if the file ever gains a non-stdlib import.

- **Auto-shelve stack cards by last load** — CLEAN — value 3 — effort S — risk low — category: library
  Why: `fm lib stats` shows 5 of 1219 cards used, and "drop 8 unmeasured cards" was already a dropped task. A shelf rule is simpler than judging each card: unloaded for 90 days moves it to a cold directory, and `fm lib show` still finds it.
  Done when: after running the shelf command, the installed card count falls below 100, `fm lib show NAME` still resolves a shelved card, and the use counter is unchanged.

- **Let each verb declare its retirement trigger at creation** — CLEAN — value 3 — effort S — risk low — category: subtraction
  Why: gen-0 says to subtract as you add, but nothing says which verb pays. A one-line `retire_if:` (for example "zero calls in 60 days") in the verb registry makes the burden report actionable.
  Done when: `fm burden --by-verb` lists verbs past their trigger, and a new verb without the field fails `fm doctor`.

- **Wild: Keep a "negative space" file instead of the grid** — CLEAN — value 3 — effort S — risk low — category: coverage — wild
  Why: assumption: stating per surface what Foreman deliberately does not do is shorter and easier to check than 64 cells of what it does. Each negative is one line with a falsifier, such as "Desktop: no tray icon (T-0325 blocked)".
  Done when: every surface has at most 5 negative lines, each naming a task or a test that would fail if the opposite became true.

- **Wild: Make one append-only event log the only state** — CLEAN — value 4 — effort L — risk high — category: architecture — wild
  Why: assumption: much of the stale-state, baton and ledger-disagreement class (the "baton, ledger and repo disagree after a kill" item) comes from several stores. Keeping tasks, bets, grants and goals as views over one log removes the reconciliation code.
  Done when: a spike shows tasks and bets rebuilt from the log alone matching the current files on the repo's own history, and the spike names the number of reconcile functions it deletes.

- **Wild: Cap the guard at 50 lines for "mini mode"** — FEATURE — value 3 — effort S — risk med — category: guard — wild
  Why: assumption: for a stranger's VPS or a phone-sized Foreman, a 50-line denylist covering force-push, `rm -rf`, secret reads and interpreter-driven fm is the whole sellable safety story. The full guard is an upgrade, and a test checks the mini rules are a subset of the full ones.
  Done when: the file is ≤50 lines, blocks every deny class in the corpus marked "core", and `fm doctor` reports which tier is active.

- **Wild: Hold a monthly "delete the least-loved verb" vote the code tallies** — CLEAN — value 2 — effort S — risk low — category: subtraction — wild
  Why: assumption: with call counts per verb and a retire trigger, the tool can propose the single least-used verb each month with its callers, and the user answers with one word.
  Done when: the proposal prints the verb, the call count and the replacement, and a "yes" removes it with the docs and tests in the same commit.

- **Default `fm doctor` to one section per surface** — CLEAN — value 2 — effort S — risk low — category: legibility
  Why: assumption: the 61-cell grid is only useful if the user can read it. Eight surface rows, each saying proven, partly proven or not supported, are enough for the sweep and for the user.
  Done when: `fm doctor` prints exactly one line per surface, and every "proven" line cites a command that was run.

Next question: Which of the 61 cells would the user cut if each cost them one line to read, and does the event log show anyone ever using the surface in that cell?
Next question: Which of Foreman's own hooks or rules has never fired in the last 30 days, and what in the pack would show it was still needed?
