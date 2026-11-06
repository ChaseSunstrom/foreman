# Brainstorm — lens: bold bets

- **Build a feature manifest that runs Foreman's own plumbing** — CLEAN — value 5 — effort M — risk med — category: simplicity
  Why: Round 1 added about 10 features, each with its own doctor probe, "known gaps" prose and opt-in flag (compact output off, monitor unverified). Many catalogue ideas ask for fire counters, kill switches, ablation, a feature map and a generated FEATURES.md, and all of them need the same record. One manifest entry per feature would hold id, min Claude Code version, doctor probe, fire counter, shadow state, kill switch and doc line, and every one of those surfaces would be generated from it.
  Done when: adding a feature means adding one manifest entry, and `fm doctor`, FEATURES.md and `fm feature off <id>` all pick it up with no other edit; a test fails if a hook or monitor exists without an entry.

- **Add a generic shadow mode that promotes a feature after N agreeing runs** — FEATURE — value 5 — effort M — risk low — category: rollout
  Why: Compact output is off until the user says yes, the monitor's arming is unverified, and the user dropped features whose premise was never measured (delta reads, Read-hook scoping). Any manifest feature could instead compute what it would have done, log it beside what happened, and offer promotion once the counterfactuals hold. Each feature then proves itself rather than waiting for a yes.
  Done when: with compact output in shadow mode, the model sees full output, the ledger records the would-be stub and its saving, and `fm feature promote compact` appears only after N sessions with zero failure-line loss.

- **Run `fm whatif <setting>` against 30 days of real transcripts** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: The compact-output case rested on a one-off measurement (44.3M chars of Bash output over 30 days), and several dropped ideas died because their premise was never checked. A replay calculator would report tokens, hook time, the number of Reads touched, and how many outputs would have hidden a failure line, before the user is asked for a yes.
  Done when: `fm whatif compact=on` prints projected tokens saved and counts of lost failure lines from stored transcripts, and the numbers match a hand-checked sample.

- **Close each round automatically with `fm round close`** — FEATURE — value 5 — effort M — risk med — category: recursion
  Why: The user defined "recursively improve" as ship, review, brainstorm on top, and repeat, yet the board is unticked after round 1 and the review is manual. Combined with the manifest's fire counters, a close step would classify each shipped item as keep, tune or revert from observed use and open revert tasks. It would also write the next round's brief, including the user's "etc." steers.
  Done when: closing round 1 produces a per-item verdict table from counters, queues at least one tune or revert task for an item with zero fires, and the round-2 brainstorm pack contains no already-shipped item.

- **Run Foreman natively on Windows** — FEATURE — value 4 — effort L — risk high — category: devices
  Why: The README says "Linux, macOS or WSL (not native Windows)", and the tmux and bash assumptions in the bus, the wake path and the guard's shell parsing all depend on a POSIX shell. Assumption: users on native Windows exist and are lost at install. The plugin monitor and ScheduleWakeup could replace tmux, and the guard could parse PowerShell.
  Done when: the install and roundtrip e2e pass on a Windows runner in CI, with the guard blocking a destructive PowerShell command.

- **Give every wake path a delivery receipt, then stop trusting unreceipted ones** — FIX — value 4 — effort S — risk low — category: liveness
  Why: The monitor, tmux send-keys and Stop nudges all exist, but nothing records which delivered. If a session sits idle while the queue has work, the cause stays unknown. A per-wake id echoed by the next hook would feed an idle-incident record and let the bus drop paths that never receipt.
  Done when: `fm bus` shows per-path delivered and lost counts, and a simulated dead monitor falls back to the next path within one cycle and logs the failed path.

- **Cap every injected-context block with a CI-enforced byte budget per event** — PERFORMANCE — value 4 — effort S — risk low — category: performance
  Why: Hook p50 is 74–98 ms per Read and the savings are measured in tokens, but nothing stops the next round from re-growing the preamble. The budget would be a number per event in the manifest, with the bench failing a build that exceeds it.
  Done when: a test fails when an injected block grows more than 10% over its manifest budget, and the budget table prints in `fm doctor`.

- **Replay old incidents as drills against every release** — SECURITY — value 4 — effort M — risk low — category: security
  Why: The 2026-10-14 headless-drive incident was fixed by a point change, and the guard has a growing list of false-positive cases. A drill directory of incident to expected-verdict pairs, run in the release gate, would keep each fix from silently regressing.
  Done when: the release script runs all drills, and reverting the headless-never-drives fix makes one drill fail.

- **Wild: Have round 3 waiting at breakfast** — FEATURE — value 4 — effort L — risk med — category: recursion
  Why: Wild. The user said "etc. etc. etc." and keeps asking for repeated improvement. Overnight, `fm round` would do a bounded, budget-capped pass on deferred clusters whose unlock triggers fired. It would leave one reviewable branch and a one-screen delta card, and ship nothing unreviewed.
  Done when: after a night run the user finds a branch, a card with before and after metrics, and no change on main.

- **Wild: Offer ablation week as a one-key toggle** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: Wild. With every feature switchable through the manifest, the user could turn off a random third of features for a week. Fire counters and re-ask rates would then show which ones they actually miss, and the rest would become deletion candidates.
  Done when: `fm ablate start` disables the chosen features and, after the period, prints a missed-versus-unmissed table.

- **Wild: Launch a first-ten-minutes stranger test for installs** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: Wild. A fresh Claude with only the README tries a toy task and records where it stalls. The installer is a long curl pipeline with 8 flags, and the README is long enough that its first-run path is hard to see. That stall log would drive README and doctor fixes.
  Done when: a CI job runs the stranger test on a toy repo and fails if the child needs more than N tool calls to reach its first closed task.
