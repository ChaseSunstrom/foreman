# Brainstorm — lens: speed and cost

- **Cache check results by content hash of touched inputs** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: Gates rerun the 704-test suite (~30 s) per brief and per batch even when the files the criteria depend on are unchanged; the friction list shows load-induced flake on reruns. Prior ideas covered "cache gate results by input hash" only as a title; this one specifies keying on the impact-map closure plus the verify command plus the interpreter version, and storing it as ledger evidence flagged `cached`, never counted as fresh proof for the final done check.
  Done when: running `fm check` twice with no file change in a criterion's impact closure executes its verify command once, and the second run prints `cached (run T-xxxx#n)`. Touching one file in the closure forces a rerun.

- **Show a per-task token and wall-clock bill at close** — FEATURE — value 4 — effort S — risk low — category: cost visibility
  Why: fm budget caps spend but the user's worry is subagents "eating a crap ton of tokens"; there is a cap but no per-task breakdown tying spend to stage (plan, review, research, brainstorm, gates). Assumption: fmcost already has per-child usage records to join against the ledger.
  Done when: `fm task done` prints a table of tokens, dollars and seconds by stage and child, and `fm cost` totals match it within rounding.

- **Make drive wait-states zero-turn** — PERFORMANCE — value 4 — effort M — risk med — category: drive
  Why: 18 drive turns ended only to await a reviewer subagent. Each ended turn replays context. Rather than just a "waiting" state, run the independent work (next brief's intake, map refresh, recall prefetch) during the wait, so the wait is productive and the turn count drops.
  Done when: in a replayed drive with a pending reviewer, the count of turn-ends caused by waiting falls to 0 for runs where independent queued work exists, and the replay shows that work done before the verdict lands.

- **Cut review cost with a diff-risk pre-score** — PERFORMANCE — value 4 — effort M — risk med — category: review
  Why: Every batch gets a full fm-reviewer, which finds 3–7 real issues, so don't drop it. Instead, score the diff mechanically (new parsers, exported text, guard or state code, no tests added) and pick a lens subset and model tier. Low-risk docs or rename diffs get one lens. Assumption: lens-level cost is roughly linear in lenses run.
  Done when: a docs-only diff runs one lens and a diff touching a parser or export runs all five. Bench cases that previously caught issues still catch them.

- **Share one prefix across sibling children** — PERFORMANCE — value 4 — effort M — risk low — category: prompt caching
  Why: Brainstorm lenses, research recon agents and review lenses each get a freshly built context pack. Build one byte-stable pack prefix, with lens-specific text last, so the provider's prompt cache hits across siblings. Assumption: fmideas and fmresearch currently interleave per-child text early in the prompt.
  Done when: two lens children for one pack have an identical first N KB, and `fm cost` reports a cache-read share above a set threshold in a sample run.

- **Auto-pick the cheapest sufficient child model per call** — FEATURE — value 4 — effort M — risk med — category: model routing
  Why: `fm models` and the bench exist, but routing from their data isn't wired into spawn time. A router reads cheapest-passing results and escalates a model tier only on a failed quote check or a failed verify.
  Done when: a child spawn for a mechanical task picks the cheaper tier per the models table, and a forced failure escalates once and records why in the ledger.

- **Wild: Speculative step pre-execution in a throwaway lane** — FEATURE — value 4 — effort L — risk high — category: latency
  Why: Steps with known verify commands could be speculatively attempted by a cheap child in a lane worktree while the main thread reviews the previous step. A patch is accepted only if it passes verify, so unused work wastes budget but never corrupts. It must be capped by `fm budget`.
  Done when: in a two-step brief, step 2's patch is ready before step 1's review ends, is applied only after its verify passes, and a discarded patch leaves the main tree untouched.

- **Wild: Spend-per-lesson dashboard that retires expensive no-ops** — FEATURE — value 3 — effort M — risk low — category: always-on cost
  Why: The rules file is capped at 6000 chars, and every always-on line costs tokens in every turn. Join each rule line's token cost to bench ablation lift and show it in the UI, with a one-key proposal to demote lines that never earned their cost.
  Done when: the UI lists the rules lines ranked by cost against measured lift, and the demote action produces a diff of the rules file that the bench gate evaluates.

- **Wild: Quote the machine's load before running gates** — FIX — value 3 — effort S — risk low — category: gates
  Why: A gate class flaked once under heavy machine load. Read load average before a gate run and either delay briefly or run serially, recording the reason as a note rather than a retry that hides a real failure.
  Done when: with a simulated high load, a gate run records a load note and uses reduced parallelism. A real failing test still fails on the first run.

- **Batch research queries into one fetch plan with a page cache** — PERFORMANCE — value 3 — effort M — risk low — category: research
  Why: The inbox lists research batching and a page cache separately. Merge them: collect all open questions in a brief, dedupe the URLs they will want, fetch once, and have each question read from the shared cache with its own quote check. Cut the standalone cache item and keep this one.
  Done when: two questions needing the same page cause one fetch in the ledger, and each question still has its own quote-verified claims.

- **Add a fast-lane auto-detector with an escape hatch** — FEATURE — value 3 — effort S — risk med — category: intake
  Why: S-tier briefs still pay full intake, gate and review overhead. Detect trivial changes (one file, under N lines, existing test covers it) and use a shortened path with a mandatory evidence run. Escalate to the full path if the diff grows.
  Done when: a one-line fix completes with one criterion, one gate run and no reviewer spawn, and adding a second file mid-task switches the brief to the full path.
