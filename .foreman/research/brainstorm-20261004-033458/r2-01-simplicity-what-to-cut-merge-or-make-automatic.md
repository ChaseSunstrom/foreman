# Brainstorm — lens: simplicity: what to cut, merge or make automatic

- **Make the reviewer wait a background task by default** — FIX — value 5 — effort M — risk med — category: drive
  Why: 31+ drive stops on a background reviewer, ~1–2 min idle per batch. Fold "park the reviewer", "bounded wait" and "zero-turn waits" into one rule: review starts at step close, the next queued task begins, and the verdict is checked at the next gate. Nothing in the user's flow ever says "waiting".
  Done when: a drive over a 3-task queue records zero turn-ends whose only reason is a pending reviewer, and each task's close still lists its review verdict.

- **Make `fm guard check '<cmd>'` the only way to probe the guard, and have hooks call it** — CLEAN — value 4 — effort S — risk low — category: guard
  Why: the ad-hoc hook probe took several tries because the event name is argv[1]. One verdict function shared by the hook and the CLI means one code path, so there is no divergence between "what I tested" and "what ran". This merges the `fm guard try`, dry-run and receipt ideas into one verb.
  Done when: `fm guard check 'git -c core.fsmonitor=x status'` prints the same verdict and reason code the hook gives for that command, and a test asserts both call the same function.

- **Move pre-audit and guard patterns into one data file, excluded from self-matching by its extension** — FIX — value 4 — effort S — risk low — category: patterns
  Why: the pre-audit flags the file that defines its own regexes as network code. A `patterns.json` that the scanner skips by path ends the false positive, and it also lets `fm evolve` tune the patterns, as it already does with routing.json.
  Done when: running the pre-audit on a diff that only edits patterns.json raises no network or ingest flag, and a diff adding a real `urllib` call elsewhere still does.

- **Fold `fm second`, `audit`, `bench court` and `bench duel|versions|soak` under `fm review` and `fm bench --vs`** — CLEAN — value 4 — effort M — risk med — category: verbs
  Why: Pass 3 added many sibling verbs, and the inbox plus the idea list already ask for collapse. Keep old names as aliases that print the new spelling once, so nothing breaks.
  Done when: `fm --help` lists one review verb and one bench verb, every old invocation still works and notes its replacement, and the suite passes unchanged.

- **Require every new verb to name what it replaces, or auto-expire it after N sessions unused** — CLEAN — value 4 — effort M — risk low — category: lifecycle
  Why: the verb count grew by about 15 in a day (budget, oracle, bench, evolve, models, batch, tour, proof, landscape, deps, second…). `fm cost` already counts use, so the data exists. Unused verbs get demoted from `--help` first, never deleted without a yes.
  Done when: a verb unused across 20 sessions disappears from `--help`, still runs, and appears under `fm help --all` with its last-used date.

- **Cut the open inbox to three named pipelines with reasons recorded** — CLEAN — value 3 — effort S — risk low — category: planning
  Why: the inbox holds 7 items that overlap with shipped work. Night shift, sentinel scheduling and the morning report are one idea. Lesson confidence, claims half-life and planted defects are one "measure what the memory is worth" pipeline. The Foreman MCP server and the stranger test belong to the "works without Foreman's own session" pipeline.
  Done when: the inbox lists three pipelines, each old item links to its pipeline or to a recorded cut reason, and no item is silently dropped.

- **Wild: Run Foreman in "one verb" mode where plain `fm` infers the next action** — FEATURE — value 4 — effort L — risk med — category: interface
  Why: `fm next` already exists and "make fm with no arguments the whole interface" was proposed. The deeper step is to have it execute the unambiguous action (open the brief, run the gate, request the review), asking only when two options are close. wild
  Done when: in a fixture repo with a half-done task, bare `fm` runs the next gate and prints what it ran, and when two options tie it asks one question.

- **Wild: Make every feature a named module that can be switched off, with `fm ablate` measuring what each one earns** — FEATURE — value 4 — effort L — risk high — category: ablation
  Why: the user wants quality without cost growth, and nothing currently tests whether a feature earns its tokens. Combine the module switches with `fm bench` to run the same cases with and without a module, then propose the cut when it makes no difference. wild
  Done when: `fm ablate recall` runs a fixed bench with recall disabled and prints a pass-rate and token delta.

- **Wild: Hold a monthly "delete-only" pass that proposes removals and may not add code** — CLEAN — value 3 — effort M — risk low — category: pruning
  Why: pass after pass has added features, and the rules file is capped at 120 lines to hold it back. A pass mode with a net-negative line count rule, driven by the usage and ablation data, gives subtraction an owner. wild
  Done when: `fm pass --delete-only` produces a brief whose acceptance criteria include a net negative line count and a green suite.

- **Auto-tier from the diff footprint, with the user confirming only on a disagreement** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: S tasks spreading past two files already get re-tiered by hand. Deriving the tier from the map's impact set at brief time removes a question asked on every task, and a mid-task footprint jump bumps the tier on its own.
  Done when: a request touching three modules is briefed as M without being asked, and an S task that grows past two files is bumped with a one-line note.
