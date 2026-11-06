# Brainstorm — lens: approaches

- **Ablate each gate in the duel** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: assumption: many gates were added after one-off failures, and the pack has no data on which of them change outcomes. T-1231 (duel) and T-1266 (ceremony profile) are both deferred for lack of evidence.
  Done when: `fm duel --without <gate>` runs the corpus with that gate off and prints pass-rate, cost and time deltas for each gate. Gates with zero delta over N runs are listed as retirement candidates.

- **Run Foreman on a foreign repo for a week** — FEATURE — value 5 — effort M — risk low — category: dogfood
  Why: all 21 recent asks are fixes to Foreman's own tooling (ambient, ship, doctor, run.py, intake). Friction on a codebase Foreman didn't grow up in is unseen. Assumption: a small external repo is available for this.
  Done when: a scripted session on a pinned external repo produces a friction report (blockers hit, dead-end refusals, wasted reruns), and at least 3 of its items are filed as tasks.

- **Mine transcripts for friction** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the steers ("a scratchpad write set it off while dogfooding", "-k matched no test") show friction only after the user notices it. Denied tool calls, immediate re-asks and retried commands in session logs are the objective signal. Assumption: transcripts are readable locally.
  Done when: `fm friction` reads local session logs and ranks the top 5 repeated denial or retry patterns, with a count and an example for each. It never leaves the machine.

- **Test each README promise with a black-box scenario** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the README makes five claims: plan before edit, prove with commands run, one task at a time, keep going, guard hook. Recent fixes (two suites at once, a dry streak miscounted) are violations of those claims found late.
  Done when: a `claims` suite has one scenario per README sentence, run in a temp repo through the real hooks. Removing the enforcement behind any claim turns exactly its scenario red.

- **Spike every idea with kill criteria before building** — FEATURE — value 4 — effort M — risk med — category: process
  Why: 30+ "Later from T-07xx/T-08xx" items sit deferred because they were scheduled without evidence, and the user dropped several built-out ideas as YAGNI or already handled.
  Done when: an idea marked M or L gets a time-boxed spike task that must end in a recorded keep or kill with one measured fact. A killed spike writes a dropped record the check-against-dropped step can see.

- **Budget the context weight Foreman injects** — PERFORMANCE — value 4 — effort M — risk low — category: simplicity
  Why: the map lists 1,248 files under `plugin/skills/` plus rules and hooks. Assumption: session-start and per-turn injected text costs real tokens and attention, and nothing caps it.
  Done when: `fm doctor` reports tokens injected at session start and per turn, and fails when they exceed a configured budget. A test fixes the number.

- **Give dropped ideas a resurrection trigger** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: a drop reads "YAGNI: only matters if more callers appear", which is a condition nobody is watching. Without a trigger, such ideas get re-proposed or are lost.
  Done when: a dropped item may carry `REVISIT-IF:` with a runnable check (a grep count or a metric). `fm` surfaces it once the check turns true, and not before.

- **Run every command in the docs** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the docs-impact blocker proves a doc exists, not that its examples work. Assumption: README and docs contain runnable `fm` snippets.
  Done when: fenced blocks marked `# runs` execute in a temp repo in CI. A renamed flag that a doc still uses fails the build.

- **Prove there is no undeclared network traffic** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the local-first stance is stated but not tested, and the platform is Linux with namespaces available.
  Done when: the e2e roundtrip runs under `unshare -n` and passes with no network. Any new outbound call needs an allowlist entry in the test.

- **Derive local gates from the CI workflow** — FEATURE — value 3 — effort S — risk low — category: reuse
  Why: `.github/workflows/test.yml` and the `fm doctor` / `roundtrip.py` / `bench_hooks.py` gates are maintained as two lists. Assumption: they can drift.
  Done when: a test fails if a CI test command is missing from the gate list, or the reverse.

- **Fork a task across ceremony profiles and keep the cheapest pass** — FEATURE — value 4 — effort L — risk med — category: cost — wild
  Why: assumption: ceremony cost varies by task kind, and T-1266 wants data to choose. Running one real task under 3 profiles in parallel worktrees generates it directly.
  Done when: `fm fork <task> --profiles lite,std,full` runs all three in isolated worktrees and reports pass, cost and time for each. The cheapest passing diff is offered for merge.

- **Simulate the user to fuzz intake and the loop** — FEATURE — value 3 — effort M — risk low — category: testing — wild
  Why: the user writes terse `FIX: … @path> DONE-WHEN: …` lines, and parse_intake broke on @path-only lines and on mid-sentence tokens. A synthetic user in that style would find the next such break before the user does.
  Done when: a generator emits 200 intake bursts in the user's recorded style, and a run asserts none is dropped, mis-scoped or mis-titled.

- **Replace scattered state with one append-only event journal** — CLEAN — value 4 — effort L — risk high — category: architecture — wild
  Why: assumption: the pane, web UI, receipts, ledgers and doctor each re-derive state, and bugs like "gate 1 never saw that write" come from views that disagree.
  Done when: task, gate and edit events go to one `events.jsonl`. The pane and `fm status` are rebuilt from it alone, and a replay test reproduces a recorded session's final state byte for byte.

- **Cap the loop by net deletion on alternating rounds** — CLEAN — value 3 — effort S — risk low — category: simplicity — wild
  Why: the recent history is all additions (new messages, new checks), and the pack's own idea list asks for a retiring gate ledger without a driver.
  Done when: every second loop round must merge a task with negative net lines or a retired item. The loop's stop line reports the running net.
