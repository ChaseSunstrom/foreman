# Brainstorm — lens: unspoken needs

- **Precompute the session-start note in the tick** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: assumption: the note is rebuilt in the hook path. T-2605 shows hook wait time is a gated metric, and `bench_hooks.py` already measures it. The tick (or the first Stop of a stale session) writes the note to a file and the hook only reads it. That gives self-triggering a benefit measured by the existing gate with no model call.
  Done when: `bench_hooks.py --runs 20` SessionStart p95 is lower with a fresh precomputed note than with none, and a stale note falls back to the old path.

- **Pulse the tower: measure idle hours with open work and restart a stalled drive** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: standing rules say "the tower advances itself" and "wait out real usage limits and resume". Both need a live session, and nothing measures the hours the tower sat idle with open Missions. The metric is tower-idle-hours per day, and a due tick or session edge relaunches `fm drive`.
  Done when: `fm genesis pulse` prints idle-hours for the last 7 days from the ledgers, and a killed drive with open work is relaunched at the next tick in a fixture.

- **Reject any self-triggering grade whose inputs are all Foreman-written** — CLEAN — value 4 — effort S — risk low — category: measurement integrity
  Why: the standing rule requires weakness-finding from signals Foreman didn't author. Tick grades built only from tick ledgers grade themselves. Each grade declares its inputs by origin (git remote times, CI conclusions, the user's commits, file mtimes), and `fm genesis check` goes red on a grade with no outside input.
  Done when: a grade fed only from `night`/tick ledgers fails the check, and the same grade with CI timestamps added passes.

- **Check a replay tape's realism against the real ledgers** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: assumption: replay and soak tapes are the main evidence while no timer exists. A tape that is too regular flatters the grade. Compare inter-event gaps, burstiness and absence lengths with the real event log, and print the distance next to every replay grade.
  Done when: a uniform-gap synthetic tape is flagged "unrealistic" and the grade line carries "tape distance: X".

- **Report the impact of the install when it finally happens** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the pack says the grade "waits on the user's install". Ticks carry a source tag (session, replay, timer). When the first timer tick lands, a change-point report compares lateness and kept-result rate before and after. Without it, the live week can't be tied to the session-borne baseline.
  Done when: a fixture ledger with session ticks followed by timer ticks prints a before/after lateness table, with "insufficient" under 10 ticks per side.

- **Scan the OS for every unattended start path, not just Foreman's registry** — SECURITY — value 3 — effort M — risk low — category: security
  Why: the registry lists what Foreman installed, not what exists. Read `systemctl --user list-timers`, crontab, `core.hooksPath` and repo git hooks, and rc-file snippets, then diff them against the registry. This finds orphaned units from older versions and anything planted by a cloned repo's hooks.
  Done when: a fixture with a stray `foreman-old.timer` and a repo `post-checkout` hook shows both under "unregistered" in `fm doctor`.

- **Remember a declined install and re-ask only when the evidence changes** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: the install card repeats. The user hasn't installed and has said they won't be blocked on it. A "no" or silence is stored with the numbers shown, and the card returns only when lateness or missed-fire counts move past a stated threshold.
  Done when: after a decline, ten sessions with flat numbers show no card, and one session after a threshold crossing shows it once.

- **Stage a ready fix for every `fm doctor` WARN that has one** — FEATURE — value 3 — effort M — risk med — category: developer experience
  Why: T-2597 warns when CHANGELOG's Unreleased passes 14 days, and T-2542 warns on dead timers. A WARN names a fix and nothing acts on it. The tick runs the fix in a scratch worktree and leaves a diff, so the user's yes applies a patch that already exists.
  Done when: an aged Unreleased in a fixture produces a staged release-notes diff, and `fm yes` applies it only after confirmation.

- **Skip the tick when hook headroom is low** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: assumption: lazy ticks ride session edges and add latency to hooks. Admission control reads the event's recent p95 against its budget and defers the tick when headroom is under a set margin. The deferral is counted as lateness, so it is visible.
  Done when: with a fixture p95 at 90% of budget the tick defers and logs it, and at 50% it runs.

- **Sweep unpushed commits for secrets and guard-class commands before a push** — SECURITY — value 3 — effort M — risk low — category: security
  Why: assumption: the finish-time secret scan covers only the task diff. Commits made by hand or by lanes while no session watched can carry credentials. A tick or session-edge job scans `@{u}..HEAD` and files a held item, never rewriting history.
  Done when: a fixture commit containing a fake key is reported by the next tick before any push, and a clean branch reports "checked, nothing found".

- **Show who calls each verb unattended in `fm help VERB`** — FEATURE — value 2 — effort S — risk low — category: docs
  Why: a standing rule says every capability must be called by a real session path, and `fm genesis check` has a "reach" check. The same reach data, shown as "called by: SessionStart, tick job X, drive" or "called by: nothing", gives docs that cannot go stale.
  Done when: `fm help ci-watch` lists its callers, and a verb with none prints "not called by any session path".

- **Wild: read triggers out of commit trailers** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: wild. A trailer like `fm-revisit: 2026-11-20` or `fm-after: ci-green` is parsed from history at session edges and gates, so the trigger travels with the commit through rebases and clones with no config file. Trailers are data, never commands, and they only file a capture.
  Done when: a commit with `fm-revisit` a day past produces one deferred-capture at the next session start, and a trailer containing a shell command is shown as text and never run.

- **Wild: fail the gate when a dated deferral comes due** — FEATURE — value 3 — effort S — risk low — category: triggers
  Why: wild. Many open items are deferred (T-0034 and others), and T-2603 already counts a dated deferral as carried. Make `fm check` and `fm ship` show a due deferral as a named red item, so any gate run is the clock and no timer is needed.
  Done when: a deferral dated yesterday fails `fm check` with its task id, and the same deferral dated tomorrow passes.

- **Wild: have a free local model grade each night's fires** — FEATURE — value 2 — effort M — risk med — category: privacy, measurement
  Why: wild; assumption: a local model such as ollama is installed. It reads the day's tick log and answers one fixed question, "did any fire look pointless or wrong?", at zero tokens. Its answers are labeled provisional. It stands in for the cold-child grade when the budget is thin.
  Done when: with a local model present, `fm night` appends one graded line per day, and with none present it prints "no local grader" and does nothing else.

Answer to "the first hour after something Foreman did goes wrong": the steps stop, find, explain, undo and prevent recurrence. Several are listed as new verbs above (`fm oops`, `fm why`, the stop file), so those verbs are the missing piece.

Next question: which self-triggering result does the user act on without checking, and what is the one-line outside check for it?
Next question: when the user finally installs the timer, which grade should change first, and who verifies that it did?
