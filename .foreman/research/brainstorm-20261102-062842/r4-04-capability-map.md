# Brainstorm — lens: capability map

- **Version the event envelope and test every migration** — FIX — value 4 — effort M — risk low — category: reliability
  Why: assumption: the pack has many envelope, replay and tape ideas but none says what happens when the envelope shape changes. A tape recorded last month would silently mis-replay after a schema change.
  Done when: a golden tape recorded on envelope v1 replays under v2 code through an explicit migration and produces identical outcomes, and an unknown version makes `fm doctor` WARN naming the version.

- **Lint trigger predicates statically** — FEATURE — value 4 — effort M — risk low — category: trigger table
  Why: assumption: the pack proposes a trigger table, `triggers.toml`, a cycle check and shadow mode, but nothing that checks a condition for always-true, never-true, shadowed or overlapping rules before it arms.
  Done when: `fm when --lint` flags a planted always-true rule, an unreachable rule and two rules that fire on the same event, and exits non-zero on each.

- **Separate "source unhealthy" from "no events"** — FIX — value 5 — effort M — risk low — category: watchers
  Why: the pack has blind-detectors and retry storms. It has no per-source circuit breaker that records "GitHub returned 5xx for 6h" as unknown rather than as a quiet night. Without that, "checked, nothing found" would be false.
  Done when: a fake forge returning 503 produces a ledger row of state `unknown` (not `quiet`), the morning note says the source was unreachable, and the breaker half-opens on a schedule.

- **Route notifications through a channel ladder** — FEATURE — value 4 — effort M — risk med — category: delivery
  Why: assumption: yes-cards and morning notes are proposed for many surfaces, but no escalation by unread age exists (terminal note, then desktop notify, then an opt-in ntfy or email). Without it, an unread note is indistinguishable from an ignored one.
  Done when: with a fixture clock, a card unread after the configured age escalates exactly one rung, each rung logs a row, and no network rung fires without an explicit setting.

- **Layer policy as user, repo and trigger with `fm why` showing each layer** — FEATURE — value 4 — effort M — risk med — category: policy
  Why: the pack has per-trigger budgets, quiet hours, consent files and overlap policy, but no stated precedence among them. Two layers disagreeing is the likely cause of a surprising fire or a surprising silence.
  Done when: `fm why TRIGGER` prints the effective value of each setting with the layer that won, and a test with conflicting user and repo values shows the stricter one winning.

- **Search the fire ledger like a table** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: fires are recorded in many ledgers (cause chain, lateness, outcome, receipt), but nothing joins them. The user's first-hour question after a bad fire is "what else did that trigger do this week?"
  Done when: `fm fires --trigger X --since 7d --outcome dropped --json` returns one joined row per fire, with cause, lane, task and outcome, from existing ledgers and no new store.

- **Cap the cost of any one trigger edit with a what-changed preview** — FEATURE — value 3 — effort M — risk low — category: trigger table
  Why: assumption: editing a threshold today means re-arming blind. A preview that replays the last 30 days of the tape under the old and new rule would show added and removed fires before the edit lands.
  Done when: `fm when edit` prints "+3 fires, -1 fire, est. cost delta" against the tape and applies only after the user confirms.

- **Send a fire-drill through the notification path** — FEATURE — value 3 — effort S — risk low — category: delivery
  Why: assumption: a delivery channel can be configured and silently dead, so the install yes would rest on a path nobody has seen work.
  Done when: `fm drill notify` sends a labelled test card through every configured rung and reports which delivered, each as `ok`, `failed` or `not configured`.

- **Wild: Fire on git-reflog frustration patterns** — FEATURE — value 3 — effort M — risk med — category: signals
  Why: wild; assumption: shell-history mining is proposed, but the reflog is a cheaper, local, repo-scoped signal. Repeated `reset --hard`, abandoned branches or revert-then-redo within minutes mark a stuck moment. It needs no install if read at the session edge.
  Done when: a fixture reflog with three resets in ten minutes yields one quiet offer ("stuck? want a cold look at the diff?"), and a normal reflog yields none.

- **Wild: Write an epitaph when a trigger is retired** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; retirement of unused triggers is proposed several times, but nothing records what was learned. A short stored note (fires, kept rate, last useful fire, why it died) makes a later re-proposal check history first.
  Done when: retiring a trigger writes one epitaph line with its stats, and proposing a similar trigger later prints that line beside the card.

- **Wild: Surf the user's lulls for heavy fires** — PERFORMANCE — value 3 — effort M — risk med — category: scheduling
  Why: wild; assumption: the pack pauses triggers while the user is present and gates on battery and load, but not the inverse. Opportunistically running the heaviest fires in observed idle lulls (from session gaps, no sensors) uses allowance that would otherwise expire unused.
  Done when: replaying a recorded week, heavy fires land only in gaps the tape marks idle, with zero overlap with a user-active interval.

- **Check that a quiet week is genuinely quiet** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: assumption: gen-2 graded ticks on what fired. A zero-event week is ambiguous (nothing happened, the watcher was down, or the rule was wrong). A sparse planted-event probe every week would separate those without any install.
  Done when: a weekly planted event in a fixture repo is detected end to end, and a deliberately broken watcher turns the week's grade from `quiet` to `blind`.

- **Export a trigger bundle for another machine, restore-checked** — FEATURE — value 2 — effort M — risk med — category: portability
  Why: assumption: multi-machine ideas cover leases and sharing signatures, not a plain export of the trigger table, consent and cursors with a restore check.
  Done when: export on machine A and import into an empty state dir on B yields an identical `fm why` output for every trigger, and a mismatched schema version refuses with the repair command.

Next question: which decisions in the self-triggering path would the user make differently if they could see a single unified fire record, and does the user already look at any of the existing ledgers?
Next question: what does Foreman do when two sources report the same underlying event differently (CI red on both a push and a PR), and who decides which is canonical?
