# Brainstorm — lens: performance

- **Budget every hook's import time and lazy-load the rest** — PERFORMANCE — value 4 — effort M — risk low — category: latency
  Why: `plugin/lib` has 35 modules and `bench_hooks.py` already exists, but nothing says how much of each hook's time is Python import. Assumption: most hooks pay for modules they never use (guard pulls in the cost and UI code, for example).
  Done when: `bench_hooks.py` reports import time per hook, `fm doctor` fails if any hook's import time exceeds its budget, and a lazy-import pass cuts the median PreToolUse time by a measured amount.

- **Count wasted round trips per task** — FEATURE — value 5 — effort M — risk low — category: turns
  Why: the user's repeated complaints are all extra turns: the focus-in-the-line refusal twice in a row, the "no active task" refusal that offered the wrong command, and `fm task new --focus && edit` costing "one tool call". Nothing measures this. Assumption: the transcripts already show the retry sequences.
  Done when: `fm friction` and `fm digest` show, per task, the count of refusals, retries and serial independent calls with the top three causes, and the number falls after one fix lands.

- **Learn the file-to-test map from coverage** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: `fm map` links tests to source by name (`test_budget.py` → `fmbudget.py`). Name matching misses tests that cover files indirectly, which limits "run only the gates a diff can affect" and the edit-time sentinel (T-0214). Assumption: the gates can run under a coverage tool that records which test touched which file.
  Done when: a coverage-derived link table exists, `fm impact` uses it, and on 10 replayed diffs it picks a superset of the tests that actually failed.

- **Cache gate results per test file by input hash** — PERFORMANCE — value 4 — effort L — risk med — category: gates
  Why: tree-hash reuse is all-or-nothing, so one changed file reruns everything. Per-test caching keyed on the test file plus the hashes of the files it covers (from the coverage map) would let a small diff skip most of the suite. The T-0424 friction fix already shows slow gates are a tracked signal.
  Done when: a one-line change reruns only the affected test files, a deliberately broken dependency still makes the right test fail, and the cache is shared across lanes.

- **Cancel reviewer fan-out on the first blocker** — PERFORMANCE — value 3 — effort S — risk low — category: orchestration
  Why: reviewer lenses run in parallel and each costs tokens and time. Once one lens returns a blocking finding, the diff must change and the rest of the round is wasted. Assumption: lens runs are separate processes that can be stopped.
  Done when: a seeded blocker in one lens stops the others within seconds, the survivors' partial output is kept, and the ledger records tokens saved.

- **Index the project map incrementally from git object hashes** — PERFORMANCE — value 3 — effort M — risk low — category: indexing
  Why: the map note says "262 files, as of an older HEAD", so the map goes stale and is rebuilt wholesale. Re-parsing only files whose blob hash changed would keep `fm map`, `outline`, `impact` and `why` current at near-zero cost.
  Done when: after a one-file edit, `fm map` refreshes in under 50 ms and matches a full rebuild exactly (tested by diff).

- **Cache guard verdicts by parsed command shape** — PERFORMANCE — value 3 — effort M — risk med — category: guard
  Why: the guard replays 5000 real commands, and most real sessions repeat the same shapes (`git status`, `pytest -x`). Caching verdicts keyed on the normalized AST plus the policy hash would skip re-parsing, but only for commands whose verdict depends on the shape alone.
  Done when: replay shows a hit rate, verdicts with and without the cache are identical across the 5000-command corpus, and the guard's cached p95 drops measurably.

- **Build a precomputed session image** — PERFORMANCE — value 3 — effort M — risk low — category: startup
  Why: SessionStart, resume and the statusline each read briefs, STATE and the map. Writing one prebuilt image on checkpoint and commit would turn all of them into a single file read. Assumption: those reads are a visible share of startup.
  Done when: SessionStart does one read plus a freshness check, and its output matches the slow path byte for byte in a test.

- **Set reasoning effort per step type** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: model routing is already proposed, but effort is a separate dial. Mechanical steps (rename, changelog, merge) don't need deep reasoning, while planning and the guard do. Assumption: the harness exposes an effort setting for the headless runs `fm run` and the builder lanes start.
  Done when: `fm bench` compares fixed against per-step effort on replayed tasks, with equal pass rate and lower tokens and wall time.

- **Wild: keep a warm browser daemon for `fm smoke`** — PERFORMANCE — value 3 — effort M — risk low — category: verification
  Why: `fm smoke` launches a headless browser at desktop and phone sizes, and a cold launch per check is probably most of its time. A reusable browser kept alive per project, reset between runs, would make the product check cheap enough to run after every task and in the drive's idle moments. Wild.
  Done when: the second `fm smoke` in a session starts in under a second, and a test confirms cookies and storage are cleared between runs.

- **Wild: pack lanes by predicted file overlap** — FEATURE — value 4 — effort L — risk med — category: scheduling
  Why: the user hit `fm lane merge` refusing beside dirty main (T-0403). The deeper cost is lanes that touch the same files and serialize at merge. Predict each task's file set from the brief and past `why` data, then dispatch only disjoint sets together. Wild.
  Done when: on a 10-task queue the packer picks lane sets with zero predicted overlap, and measured merge conflicts fall against naive dispatch.

- **Wild: compile Foreman's hot path to a stripped self-checking "fast kernel"** — PERFORMANCE — value 3 — effort L — risk high — category: latency
  Why: the hooks fire on every tool call, so milliseconds multiply across a session. A small kernel (guard parse, active-task lookup, focus check) falls back to the full Python path whenever its inputs are unfamiliar. Wild, and assumption: the kernel can be a single small file with a differential test against the full guard.
  Done when: the kernel agrees with the full guard on the whole replay corpus, falls back on anything unknown, and runs in under a third of the median hook time.

- **Wild: let idle drive time shorten the next task's critical path** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: the drive now offers queued work during background jobs (T-0401). It could instead spend those idle minutes on read-only prep for the next task: a warmed gate cache, recon summaries, a prebuilt `fm tour`. Wild.
  Done when: the next focused task starts with its gate cache warm and recon already written, and the time from `fm focus` to first edit falls in a measured A/B run.
