# Brainstorm — lens: delight

- **Show a "while you were away" return card** — FEATURE — value 5 — effort M — risk low — category: return-delight
  Why: user runs hours-long and multi-day sessions (5-day Volt session) and complains about slowness and rot; assumption: they step away often.
  Done when: after ≥10 min idle, the next prompt shows a one-card summary (tasks finished, gates failed, what needs the user, next queued) built from the ledger, and it disappears on first keypress.

- **Add a "plain-words" mode for every status string** — FEATURE — value 4 — effort S — risk low — category: copy/clarity
  Why: "L, T, M mean nothing as letters"; the user keeps hitting jargon (stages, tiers, gates, auditing). Assumption: other terms are equally opaque.
  Done when: a single glossary map drives the band, pane, `fm` output and toasts, and a test fails if any rendered surface contains a bare tier or stage letter or an unmapped internal term.

- **Show a "why is this slow" live waterfall for the current task** — FEATURE — value 4 — effort M — risk low — category: time transparency
  Why: measured gates 18.8 h, `cargo test` median 8 min, close-out 42 of 125 h; the user said "takes hours". Seeing where time goes right now makes waiting tolerable and prompts action.
  Done when: the pane has a stacked time bar per task (planning/executing/gates/audits/waiting-on-user) and a running gate shows elapsed vs. its own median with an ETA.

- **Celebrate finished tasks with a shareable receipt** — FEATURE — value 3 — effort S — risk low — category: reward
  Why: users show off the "nice animated foreman stuff"; assumption: a compact artifact is something they'd paste to others.
  Done when: `fm task finish` emits a one-screen receipt (title, size words, files +/−, gates passed, audits, wall time, tokens) and the mod plays a short mascot animation; `fm receipt T-xxxx` reprints it as text/markdown.

- **Run an ambient "idea of the day" from the inbox and history** — FEATURE — value 3 — effort M — risk low — category: brainstorm
  Why: user says brainstorming doesn't produce "things I want but don't know how to say". Assumption: idle moments and finished-task toasts are a cheap place for Haiku to surface one suggestion drawn from their repeated corrections.
  Done when: after a task closes, a dismissible toast offers one Haiku-generated follow-up grounded in that task's diff and the user's recent words, with a one-key "capture to inbox", capped at one per task and zero when usage mode is frugal.

- **Add a token and usage "fuel gauge" with per-playbook cost previews** — FEATURE — value 4 — effort M — risk low — category: usage-awareness
  Why: the user is usage-sensitive and wants more playbooks/subagents without burning usage. Showing the estimated cost before launching a playbook makes cheap options visible.
  Done when: the playbook picker lists each playbook with an estimated token range from past runs, and the footer shows a running session spend against a user-set budget.

- **Wild: Make the mascot react to the work** — FEATURE — value 3 — effort M — risk low — category: personality — wild
  Why: a pixel mascot exists but is decorative; assumption: users love small characterful touches.
  Done when: the mascot has at least five states (idle, thinking, running tests, gate failed, all green) driven by `fm ui --json`, and it can be turned off with the existing config.

- **Wild: Add a "Foreman radio" that narrates a long run as a spoken-style log** — FEATURE — value 2 — effort M — risk low — category: ambient — wild
  Why: runs last hours with the user away; assumption: a calm, scrollable one-line-per-milestone feed ("T-0176 tests green, starting audit") is nicer than a dashboard you must open.
  Done when: a Pane tab shows a timestamped plain-English feed generated from ledger events without model calls, and `fm radio --tail` prints the same lines.

- **Wild: Build a "task cinema" that replays a finished task in 20 seconds** — FEATURE — value 3 — effort L — risk med — category: replay — wild
  Why: ledger records steps, files, gates and tools; a fast-forward animation of the band, files filling in and gates ticking makes a satisfying review of what happened while away. Assumption: the ledger has enough timestamps.
  Done when: `/fm replay T-xxxx` plays the task's step bar, file +/− bars and gate results at 20× speed and can be paused and scrubbed.

- **Wild: Offer a "dream mode" that uses idle time to pre-warm the next task** — FEATURE — value 4 — effort L — risk med — category: speed — wild
  Why: the user hates slowness; assumption: while the user reviews, a read-only fork can pre-ground and draft the plan for the next queued task so it begins instantly.
  Done when: with a non-empty queue, the next task shows "plan pre-drafted" in the queue card, starting it skips grounding and planning calls, and the draft is discarded if the repo changed materially.

- **Add a "needs you" single-key inbox of blockers across projects** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: protected-core edits, plugin updates and plan approvals each need a user yes and stall autonomy; assumption: multiple projects run at once.
  Done when: one Pane section lists every pending yes (with the exact diff or command) across projects, and pressing Y approves a selected item or A approves a batch of same-kind items in one keystroke.
