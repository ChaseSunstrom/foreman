# Brainstorm — lens: delight

- **Publish a living task Artifact** — FEATURE — value 5 — effort M — risk low — category: Artifact
  Why: Artifact is unused (0 references); the user keeps asking for a "Cockpit UI" (Frontier 11) and complains it "sits idle" (T-0758) with no visible state. A private claude.ai page showing queue, current step, evidence and ✗/✓ runs gives something shareable and phone-viewable without a new server.
  Done when: `fm task` in a session publishes one Artifact whose page shows the active task's steps and updates within 10s of `fm task step done`, verified by reading the artifact's data back.

- **Let the Artifact steer the queue** — FEATURE — value 4 — effort M — risk med — category: Artifact
  Why: assumption: ArtifactComments / "ask Claude" deliver page input to the session. Reorder, defer or capture-from-page lets the user steer from a phone; matches "reordering of operations" (T-0757) and the user's refusal to be handed commands.
  Done when: a comment "defer T-0034" on the page results in that task's status changing to deferred within one turn, with a recorded event.

- **Push when it matters, silence otherwise** — FEATURE — value 5 — effort S — risk low — category: Notifications
  Why: fm notify only runs a user shell command; PushNotification is unused. Long unattended runs (fm night, queue drains) should ping on "needs you", "queue done", "gate failed" — and never on routine progress.
  Done when: a blocked task triggers exactly one PushNotification with the task id and the question, and a normal step completion triggers none (test with a stubbed sender).

- **Replace the idle-nudge send-keys with Monitor and ScheduleWakeup** — FIX — value 5 — effort M — risk med — category: Idle handling
  Why: T-0758 "make sure it doesn't sit idle"; fm bus wakes sessions by typing into tmux panes, which breaks without tmux. Monitor streams background-test output as notifications, ScheduleWakeup self-paces. assumption: both are callable from inside a Foreman turn.
  Done when: with tmux absent, a session waiting on a background gate resumes by itself when the gate finishes, and no send-keys is invoked.

- **Show review findings natively via ReportFindings** — FEATURE — value 4 — effort S — risk low — category: Review UX
  Why: reviewer subagents already produce findings and Foreman has "reproducible findings" machinery (T-0697); typed findings rendered by the host UI beat prose in a transcript, and de-dupe across rounds.
  Done when: a reviewer run emits ReportFindings entries carrying file:line and severity, and the same findings are recorded in the task file.

- **Spend-aware model ladder per step** — FEATURE — value 5 — effort M — risk med — category: Model routing
  Why: T-0755 asks "can foreman spawn agents of lower models?". Agent takes per-call `model` and `effort`; today only S-tier lanes pass "sonnet". Route reads/greps to haiku, plans to opus at high effort, and record per-step which tier was tried and whether it passed, so the ladder tunes itself.
  Done when: a task with three steps of differing size spawns agents at different models, and `fm` reports tier and pass/fail per step.

- **Step tracker that can't drift** — FIX — value 4 — effort S — risk low — category: Step state
  Why: T-0759: "it will start working on different steps without updating the step". A PostToolUse check compares the files being edited against the current step's declared scope and nudges (or auto-advances) when they diverge.
  Done when: editing a file that belongs to step 3's scope while step 2 is current yields a one-line correction, covered by a test.

- **Weekly cloud routine for repo hygiene** — FEATURE — value 3 — effort M — risk med — category: Scheduling
  Why: RemoteTrigger and /schedule are unused; fm night already runs overnight but only on the user's machine. A cloud cron could run the dead-test, stale-lesson and dependency sweeps and open the result as an Artifact. assumption: the user's account allows routines.
  Done when: one routine is registered by Foreman and its first run produces a report the next session shows.

- **Wild: Foreman Radio** — FEATURE — value 3 — effort M — risk low — category: Delight — wild
  Why: assumption: Monitor can stream a log. A quiet one-line ticker ("T-0761 step 3/5 ✓ tests 212 pass") through Monitor makes unattended work feel alive, replacing the dead-air complaint.
  Done when: starting a task opens a Monitor stream that prints one line per step change and stops when the task closes.

- **Wild: Morning-after Artifact** — FEATURE — value 4 — effort M — risk low — category: Artifact — wild
  Why: fm night runs unattended; a single page with what shipped, what was blocked, diffs, evidence and a "revert this" per item turns a log dump into something people show others.
  Done when: after an `fm night` run, the Artifact exists and lists every closed task with its evidence and a link to its commit.

- **Wild: Fleet of sibling sessions that talk** — FEATURE — value 3 — effort L — risk high — category: Multi-session — wild
  Why: SendMessage and ListAgents are unused; fm bus types into tmux panes. Sessions on a laptop and a remote box could hand off tasks and stop each other from touching the same files.
  Done when: two sessions on different tasks exchange a "claiming path X" message and the second avoids X, shown in a test with stubs.

- **Wild: Replay a task as a scrubbable timeline** — FEATURE — value 3 — effort L — risk low — category: Artifact — wild
  Why: Foreman already records evidence, steps and tool results; an Artifact with a slider that scrubs through a finished task makes reviewing and teaching from it a pleasure, and feeds the flywheel (Frontier 12).
  Done when: a closed task's timeline page renders every step's evidence in order and the slider shows the state at each step.

- **Use LSP for plan-time blast radius** — FEATURE — value 4 — effort M — risk low — category: Planning
  Why: LSP references are unused; plans currently estimate scope from `fm map` and grep. Showing "this function has 14 callers in 6 files" in the plan makes sizing honest and ties tests to the right files (T-0214).
  Done when: a plan for renaming a function lists the referencing files from LSP, and the step list covers them.
