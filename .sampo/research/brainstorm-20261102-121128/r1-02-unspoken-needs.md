# Brainstorm — lens: unspoken needs

- **Record every override of an unproven row as "not proof"** — FEATURE — value 5 — effort S — risk low — category: proof integrity
  Why: the pack's open question: "When the user overrides an unproven row by hand, who records that the override isn't proof?" The user keeps asking for "proof before presentation", so a manual override that later reads as a pass would break the thing they care about most.
  Done when: overriding an unproven proof row writes a ledger record of class `override`, and `fm prove`, finish receipts and the site claims check all show it as "overridden, unproven"; a test confirms no reader counts it as proven.

- **Label UI checks that couldn't run as "unproven (no display)"** — FIX — value 5 — effort S — risk low — category: receipts
  Why: open question about headless CI, no browser, no display. Foreman has a web UI and a foreman-ui mod, and T-0797 defers native browser verification. A skipped check that looks green is the worst failure for a "proves its work" product.
  Done when: a UI-kind task finished with no display produces a receipt line "UI: unproven, reason: no display", and `fm doctor` counts such receipts separately from passes.

- **Audit past "proven" labels against later reversals** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: open question about which "proven" labels were reversed later. The user already built bet calibration (T-2610, T-2611), but it covers bets, not proof labels.
  Done when: `fm outcomes --proof-reversals` lists each reopened or reverted task that had a "proven" label, with a column for whether a run record existed at the time, and prints the reversal rate.

- **Rehearse a host wipe with `fm restore --drill`** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: open question about replacing the host. Foreman keeps ledgers, timers (fm night), steers, the Genesis tower and mod installs. T-0798 (recovery) is deferred, and nothing proves they come back together. Assumption: most state lives under a few directories plus systemd units.
  Done when: the drill restores into an empty temp HOME, reinstalls the units, and reports which ledgers, steers, timers and grants came back and which need hand work. A test fails if a new state file is missing from the manifest.

- **Cross-check every ops gauge against a signal Foreman didn't write** — FEATURE — value 4 — effort M — risk low — category: ops trust
  Why: the user's steer says weakness-finding must use "signals Foreman didn't author"; T-2542 reads systemd for timers, and the other gauges (bet settlement, canary state) are self-reported. Assumption: git history, file mtimes and the CI API can contradict most of them.
  Done when: `fm doctor` shows, beside each gauge, an outside source (systemd, git log, GitHub Actions) and WARNs on disagreement; a test with a faked-stale gauge triggers the WARN.

- **Check each ledger reader against a missing record class** — FIX — value 4 — effort M — risk med — category: ledger safety
  Why: the first open question: which reader would answer wrongly, not error, if a record class vanished. Bet Brier, base rates and "10 settled" thresholds all count records and would silently shift.
  Done when: a test deletes each record class in turn from a fixture ledger and each reader either errors with "class X missing" or reports "insufficient data". No reader returns a confident number.

- **Log the commands the user types to check Foreman, via a `fm verify` alias** — FEATURE — value 3 — effort S — risk low — category: user habits
  Why: open question about what the user types by hand to check verdicts. Assumption: the user greps ledgers and reruns tests. Wrapping the common ones, without reading shell history, shows which verdicts they don't trust.
  Done when: `fm verify <task>` reruns a task's proof commands and records that the user asked; `fm doctor` shows the count per proof kind.

- **Record which proof artifacts get opened after a finish receipt** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: open question about whether a bigger proof bundle is supported by use. The receipt links artifacts, but nothing records opens.
  Done when: opening an artifact through `fm show` writes an open record, and `fm cost` or `fm doctor` shows the share of receipts whose artifacts were ever opened.

- **Wild: Chaos-month for the guard — replay your own near-misses** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: wild. The guard blocks commands you'd never want run, but nothing says what it let through. Replay each session's allowed Bash commands in a sandbox, mutated toward the dangerous variant, and report any that the guard would have missed.
  Done when: `fm guard fuzz` runs on recorded allowed commands in a sandbox with no side effects and lists mutated variants that pass the guard, with 0 unreviewed.

- **Wild: A "second opinion" button that has a different model re-judge any green receipt** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: wild. The user's steer wants cold reads by a different model, yet that is internal to Genesis. Putting it on any finished task lets the user doubt a verdict in one command and records the disagreement.
  Done when: `fm recheck <task>` runs a cold read with a different model on the diff and proof, stores the verdict, and `fm outcomes` shows the disagreement rate.

- **Wild: A weekly "what I would have told you" letter from the user model** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild. The user wrote the sealed next-three-steers prediction (fmforesight). Mailing it weekly, then scoring it against what they actually asked, would show whether the model reads them and surface needs they haven't voiced.
  Done when: a weekly note lists 3 predicted asks with reasons, and the next week's note scores each as hit, miss or partial, showing a running hit rate.

- **Wild: Dead-man's switch for the whole tower** — FEATURE — value 3 — effort S — risk low — category: ops
  Why: wild. Foreman runs unattended and "advances itself", but if the host or timer dies, only Foreman's own gauges would say so. Assumption: an external ping (a free heartbeat service or a git push) is acceptable only if set explicitly.
  Done when: with the setting on, each night tick sends a heartbeat to a user-configured URL, and with it off, nothing leaves the host; `fm doctor` states which mode is active.

- **Warn when a steer's automatic check has gone stale** — CLEAN — value 3 — effort S — risk low — category: steers
  Why: the user turned every steer into a stored check, and some, like the Haiku-vs-Sonnet cold-read rule, change across later steers. A check that still passes after its rule was superseded would give false comfort.
  Done when: `fm doctor` flags any check whose steer was later amended or contradicted without an update, and a test with a superseded steer produces that flag.

Next question: Which of Foreman's refusals or blocks has the user overridden by hand, and what did those overrides cost or save?
Next question: What would a new user need to see in their first hour to believe the "proves its work" claim without reading MASTER.md?
