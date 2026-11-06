# Brainstorm — lens: bold bets

- **Run a mutation test on every ledger** — FEATURE — value 5 — effort M — risk low — category: integrity
  Why: the pack asks which reader gives a wrong answer, not an error, when a record class is missing. Nobody has tested this. Foreman reads many self-written ledgers (bets, outcomes, receipts, ticks).
  Done when: `fm doctor --ledgers` copies each ledger, deletes one record class at a time, and lists every reader whose output changed without raising an error. Each such reader has a failing test or a loud-failure fix.

- **Add an "unproven" receipt state that overrides can't turn into "proven"** — FIX — value 5 — effort M — risk low — category: proof
  Why: the pack asks how a receipt says "unproven" when a UI check can't run, and who records that an override isn't proof. Assumption: today a skipped check can read as a pass.
  Done when: a finish run with no display records `unproven:no-display`. A manual override adds `overridden-by-user` and never changes the status to proven. `fm outcomes` counts the two separately.

- **Audit past "proven" labels for reversals** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the pack asks which proven labels were reversed later and what share had no run record. Reopened tasks, reverts and failed bets are the signal.
  Done when: `fm outcomes --reversals` prints the reversal rate per proof kind and the share with no run record. Running it on the existing history gives a nonempty table.

- **Log hand-typed verification commands from the Claude Code bash-input channel** — FEATURE — value 4 — effort S — risk low — category: user model
  Why: the pack asks what the user types by hand to check verdicts. Dropped asks show `fm night --print-timer` came in as bash-input, so the harness already carries it. This needs no shell history.
  Done when: a hook records the user's `!`-prefixed commands against the open task. `fm intake` shows the three most common as candidate proof kinds.

- **Run a restore drill on a scratch host** — FEATURE — value 4 — effort M — risk low — category: ops
  Why: the pack asks what must be rebuilt by hand if the host is wiped. Timers, steers, ledgers and the installed mod all live outside git.
  Done when: `fm restore --drill` rebuilds Foreman state into an empty directory or container from backups. It prints a diff of what did not come back, and `fm doctor` WARNs if no drill ran in 90 days.

- **Add an outside witness for ops gauges** — SECURITY — value 4 — effort M — risk med — category: ops trust
  Why: timer liveness, bet settlement and canary state are trusted only because Foreman wrote them. Assumption: the check can stay local.
  Done when: a separate systemd unit under a different identity re-derives each gauge from journald and git, and `fm doctor` flags any disagreement. A test that fakes a gauge file is caught.

- **Check that stored steer checks aren't vacuous** — FIX — value 5 — effort M — risk low — category: steers
  Why: every steer gets an automatic check via `fm decide --check`, but nothing shows a check can fail. A check that always passes gives false assurance.
  Done when: for each stored check, the sweep applies a planted violation in a scratch copy and the check must go red. Checks that stay green are listed as vacuous.

- **Fuzz the guard with an adversarial agent** (wild) — SECURITY — value 5 — effort L — risk med — category: guard
  Why: the guard is the safety claim for bypass mode, and the only evidence is hand-written cases. Assumption: a tool-less generator can write bypass attempts in a sandbox.
  Done when: `fm guard fuzz` generates N obfuscated destructive commands (encoding, quoting, indirection) and reports the escape rate. Every escape becomes a red-first test.

- **Replay a finished task from its recorded commands** (wild) — FEATURE — value 4 — effort L — risk med — category: reproducibility
  Why: a proof is stronger if a third party can reproduce it, and it supports the T-0867 scorecard. Assumption: recorded commands and the start commit are enough to re-run.
  Done when: `fm replay T-xxxx` checks out the start commit in a scratch directory and re-runs the proof commands. It reports reproduced, drifted or unreproducible.

- **Publish a signed duel scoreboard against plain Claude** (wild) — FEATURE — value 4 — effort L — risk med — category: credibility
  Why: T-1231, T-0866 and T-0867 are deferred because there are no cases. The proof-before-presentation rule already requires public claims to match exam lines.
  Done when: the site shows held-out duel results, each linked to a signed run record. A claim with no record fails the sweep.

- **Let the user bet against Foreman** (wild) — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: bets already carry harness and Brier scores. Adding the user's own predictions ("this passes first time", "this holds a week") gives a human baseline and a way to find where the user's judgment beats Foreman's.
  Done when: `fm bet --me` records a prediction on a task. `fm outcomes --judgment` shows user and Foreman Brier side by side once 20 are settled.

- **Pick ceremony by nightly ablation** — PERFORMANCE — value 4 — effort L — risk med — category: lean
  Why: T-1266 and T-2536 point at the same thing: the guard-only arm shows which injected rules earn their chars. Assumption: the bench is cheap enough to run one ablation per night.
  Done when: each night one feature is switched off on the duel set. A feature with no pass loss and a cost saving is queued as a subtraction task with the run attached.

- **Add a cross-vendor judge to the finish gate** — SECURITY — value 3 — effort M — risk med — category: verification
  Why: the steer says to use signals Foreman didn't author, and T-0335 and T-0336 show the other CLIs aren't live-verified yet. Assumption: a second CLI is installed.
  Done when: a task with a high-risk diff gets a cold verdict from a different-vendor CLI. A disagreement blocks the close until the user reviews it.

Next question: which Foreman claims (README, site, receipts) have never been checked by anything Foreman didn't write?
Next question: if the user stopped opening `fm` output for a month, which verdicts would they miss, and which would still reach them unprompted?
