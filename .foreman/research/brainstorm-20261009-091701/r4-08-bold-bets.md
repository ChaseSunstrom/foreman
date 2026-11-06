# Brainstorm — lens: bold bets

- **Merge by re-deriving, not by diffing** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: JARVIS hit a refused lane merge (T-0280 couldn't land during T-0278), and the merge-train idea only sequences textual merges. Assumption: the brief plus acceptance criteria carry enough intent to replay.
  Done when: for two lanes that conflict semantically, `fm lane merge` re-runs the second brief on the first lane's result, and the merged tree passes both lanes' original gates with no hand-resolved conflict markers.

- **Resolve every symbol in a diff against reality** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: hallucinated APIs, flags and import paths are a top agent failure that tests miss when code paths are unexercised. `fm outline` and `fm impact` already index definitions, so this extends them.
  Done when: a diff calling a nonexistent method on an installed library, or an `fm` subcommand that doesn't exist, fails `fm task done`, naming the symbol and the version checked.

- **Optimise a metric with a lane-per-experiment loop (`fm tune`)** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: the user asks for "super recursive" improvement, but the pack shows only task-shaped work. Metric goals (p95 latency, hook time via `bench_hooks.py`, bundle size, flake rate) are open-ended hill-climbs that don't fit a brief.
  Done when: `fm tune --metric "<cmd>" --budget N` runs N lane experiments, keeps only measured improvements, and stops with a table of kept and rejected attempts and the final delta.

- **Reproduce time- and race-dependent bugs in a deterministic simulator** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: the pack shows a slow-gate signal and wait-loop bugs, and the existing ideas cover statistical reruns and environment perturbation. Controlling the clock, RNG, scheduling order and recorded network gives a bit-exact failing run, and optionally `rr` for backward debugging.
  Done when: a seeded flaky test fails identically on 10 of 10 reruns under `fm sim --seed S`, and the fix is accepted only if the same seed passes.

- **Keep a living threat model and data-flow map for the user's product** — SECURITY — value 4 — effort M — risk low — category: security
  Why: the existing security ideas protect Foreman's own sessions. Assumption: users shipping apps (JARVIS and others) have no map of where personal data or trust boundaries live.
  Done when: a diff that adds a new outbound network call or a new store of user data fails the done gate until the map and threat entry are updated, and `fm threats` lists the change.

- **Check diffs for licence and provenance contamination** — SECURITY — value 3 — effort M — risk low — category: compliance
  Why: assumption: generated code can reproduce copyleft snippets verbatim, and dependency changes are the only licence check proposed so far.
  Done when: a fixture diff containing a verbatim GPL function is flagged with its likely source, and a clean diff passes with no network access.

- **Run long-lived investigations that probe on a schedule** — FEATURE — value 4 — effort M — risk med — category: research
  Why: T-0316 and T-0336 are blocked on waiting for external state, and the drive's rule is "never idle". Assumption: some RESEARCH and FIX work (an intermittent production issue, a post-update check) needs a probe at intervals over days with hypotheses accumulating.
  Done when: an investigation brief with `--probe "<cmd>" --every 6h` appends dated observations and closes itself with a conclusion when a stated condition holds, surviving reboots.

- **Watch upstream contracts and turn drift into briefs** — FEATURE — value 4 — effort M — risk low — category: maintenance
  Why: `fm deps` only reports major-version lag. Breaking behaviour comes from API schemas, changelogs and Claude Code hook-surface changes (T-0316 exists because of one).
  Done when: a change in a pinned OpenAPI file, or a changelog line mentioning a symbol the repo uses, produces a captured brief naming the call sites.

- **Admit lanes by machine load** — PERFORMANCE — value 3 — effort S — risk low — category: scheduling
  Why: assumption: parallel lanes plus gates plus a headless browser from `fm smoke` thrash a laptop, and the JARVIS runs already used many lanes.
  Done when: with CPU or RAM over a threshold, `fm lane new` queues instead of starting, and `fm watch` shows the reason.

- **Wild: Run an architecture flex test** — FEATURE — value 4 — effort L — risk med — category: refactoring
  Why: wild. Generate about 10 plausible future requests from the roadmap and `fm landscape`, build each in a throwaway spike lane, and score each by diff size and files touched. The rigid hotspots become the CLEAN queue's priorities.
  Done when: `fm flex` outputs a ranked list of files that every spike had to change, with spike diffs discarded and nothing merged.

- **Wild: Send upstream fixes for bugs that bite the user's dependencies** — FEATURE — value 3 — effort L — risk high — category: ecosystem
  Why: wild. When a task works around a dependency bug (the surprise log records the wrong model of the code), an idle-time lane reproduces it upstream and drafts a minimal patch and issue. Nothing is sent without explicit per-item approval.
  Done when: for a recorded workaround, Foreman produces a tested upstream patch and issue draft in a local folder and posts nothing until `fm ask` is granted.

- **Wild: Resurface forgotten decisions by spaced repetition** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: wild. The user keeps re-asking and steering on settled topics (budget at 75%, cleanup never done). Show a decision or veto just before the user is likely to contradict it, with growing intervals if they confirm it.
  Done when: a decision older than N days that touches the active task's files appears once in the session start card, and is silenced for a longer interval after the user confirms it.

- **Wild: Scale autonomy from a signed mandate** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: wild. The user wants unattended runs (night, drive, JARVIS sessions never idle) but with limits that are only partly spoken. One typed document covers scope, spend, allowed irreversible actions, stop conditions and success definition, and every unattended action is checked against it.
  Done when: `fm night` refuses to start without a mandate, and an out-of-mandate action halts the run and appears in the morning report with the clause it broke.
