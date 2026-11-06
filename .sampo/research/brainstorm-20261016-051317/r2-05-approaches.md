# Brainstorm — lens: approaches

- **Merge shared registry lines with a union merge driver** — FIX — value 4 — effort S — risk low — category: simplicity
  Why: HELP_TIERS conflicts hit nearly every second merge (T-1059, T-1062 twice). This is the do-less answer to per-verb registry files: a `.gitattributes` `merge=union` rule or a tiny driver on the registry files. Trade-off: line order can shuffle, and a duplicate line is possible.
  Done when: a test repo where two branches each add a different HELP_TIERS line merges with no conflict and both lines present.

- **Add `fm check` as one pre-flight dispatcher** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: the review shows three separate gaps with the same shape, "would this be accepted before it costs a run": a guard decision (T-1125, T-1141), a verify command nobody checks when it is added, and a builder diff before "done". One verb with `fm check cmd|verify|diff` replaces three new verbs, which also keeps the help list short.
  Done when: `fm check verify "npm test"` in a repo without npm exits non-zero with a reason, and `fm check cmd "<heredoc to fm edit>"` prints allow with the matching rule.

- **Let the loop schedule its own next round** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: the user says "I shouldn't need to ask" and keeps re-issuing "forever loop round N". Each round would end by writing a wake time plus preconditions (gates green, no live human session, budget left, load low). A scheduler such as a cloud routine or timer would start the next round only when they hold. Assumption: a durable scheduler is available (T-0793). Trade-off: unattended spend, so it needs the budget envelope below.
  Done when: finishing a round writes `next_round.json`, and a simulated wake with a failing precondition does nothing and logs why.

- **Cache brainstorm output per lens so a rerun only fills the gaps** — PERFORMANCE — value 3 — effort S — risk low — category: reliability
  Why: capped `claude -p` children lose partial work (T-0831), and `fm ideas` runs 9 lenses × 4 rounds. Key each lens result by hash of pack plus lens plus round, and rerun only the missing ones. This is cheaper than the salvage approach.
  Done when: killing `fm ideas` mid-run, then rerunning it, spawns only the lenses with no cached result.

- **Check pane screenshots with a vision child** — FEATURE — value 4 — effort M — risk med — category: beautiful UI
  Why: the pane wasn't screenshot-verified last round, and the user's own complaints are visual (no separator between session and chat, inline chat in the tree). A small vision pass reads before/after frames against a short rubric (separators between regions, truncation, colour clashes). Trade-off: model judgment is noisy, so it files findings and does not block a release.
  Done when: a frame with the separator row removed yields a finding naming it, and a good frame yields none.

- **Reuse reviews by hunk hash** — PERFORMANCE — value 3 — effort M — risk med — category: agents
  Why: reviewers find real defects in almost every branch, so branches go through review, fix, re-review. Re-reviewing the whole diff each time is wasted spend. Cache findings by hunk hash and send only changed hunks plus their open findings. Trade-off: a changed callee can invalidate a hunk the cache calls unchanged.
  Done when: after fixing one hunk, the second review's prompt contains only that hunk and the earlier findings, with a test counting the lines sent.

- **Mark a guard decision wrong in one command** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: false positives cost the most debugging time, and the fix was a hand-written replay script both times. `fm guard wrong` would capture the last denied command, its cwd and the rule that fired into a regression fixture and open a FIX task.
  Done when: running it after a denial adds a fixture file that fails against the current guard, and the test suite picks it up.

- **Export the ledger as OpenTelemetry spans** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: `fm state` took over 120 s under load and nobody could see where the time went. The ledger already has task, stage and hook timing. Assumption: the user or a team has, or wants, a trace viewer. Trade-off: it only matters if someone looks at it.
  Done when: `fm trace export <task>` writes OTLP JSON where stages are child spans of the task, and a collector's validator accepts it.

- **Set a round-level dollar envelope** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: per-task caps exist, but a forever loop spends at the round level and this run has a `$25` budget line. The round splits its budget across lanes by expected value, returns unspent funds, and stops cleanly when the budget is gone. Assumption: spend per lane is readable from the spend log.
  Done when: a round with a $1 envelope halts after the cap with a report listing unfinished lanes.

- **Wild: Run a canary HOME that tracks main** — FEATURE — value 4 — effort L — risk med — category: reliability
  Why: marketplace users lag (installed foreman-ui 0.7.0 vs the repo's 0.17.0), and a self-edited Foreman can't be fully trusted by itself. A second HOME auto-pulls main and replays the user's real hook payloads and queue dry-run each night. A divergence from the stable install is reported before the user upgrades. Trade-off: it needs disk and an unattended schedule. wild
  Done when: a deliberately broken commit on main makes the canary report a divergence within one cycle while the stable HOME is untouched.

- **Wild: Treat silence as consent, with a receipt** — FEATURE — value 3 — effort M — risk high — category: user value
  Why: the user is often AFK and says "don't ask me anything", yet some decisions need them. Each pending question carries a default and a deadline. On expiry the default applies, a one-key revert is written, and the question is listed in the final report. This is stricter than parking assumptions because it has a deadline and an undo. wild
  Done when: a question with a 1-minute default applies the default after the deadline, and `fm undo <id>` restores the prior state.

- **Wild: Keep a kata gym of seeded bugs** — FEATURE — value 3 — effort L — risk low — category: developer experience
  Why: "Foreman got better" is hard to prove on real repos. A bundled toy repo with known seeded bugs and known fixes would be solved weekly by fresh headless sessions, under old and new Foreman. Time-to-green and interrupts would be the fitness score. Trade-off: the gym only measures the failure shapes someone thought to seed. wild
  Done when: `fm gym run` prints per-kata pass and time, and a Foreman variant that disables the red-first rule scores measurably worse on at least one kata.
