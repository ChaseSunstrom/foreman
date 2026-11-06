# Brainstorm — lens: simplicity

- **Delete the 14 backlog zombies in one sweep** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: Open work lists T-0034, T-0035, T-0166, T-0214, T-0217, T-0275, T-0317, T-0325, T-0335–T-0337, T-0352, T-0365, T-0418, T-0431 as deferred or blocked, some for months (Release 1.2.16 is stale since 1.2.27 shipped). Every session reads them; none will move.
  Done when: `fm task list --open` shows none of these without a dated, one-line reason to stay, and the rest are closed as dropped with a recorded reason.

- **Merge the duplicate native-integration ideas into one tracked epic** — CLEAN — value 4 — effort S — risk low — category: planning
  Why: the "ideas so far" list repeats the same five or six moves (ScheduleWakeup/Monitor wake, PushNotification, ReportFindings, model ladder, step sync, Artifact cockpit) under 4–5 titles each. Left alone, they become 25 tasks.
  Done when: exactly one task per distinct native feature exists, and `fm task list` has no two titles describing the same change.

- **Make fm doctor print a single "CC-native overlap" table** — FEATURE — value 4 — effort M — risk low — category: doctor
  Why: assumption: Foreman reimplements things Claude Code now does (tmux bus, notify shell command, findings format, lane worktrees, delta reads already dropped for this reason, T-0034 audit vs /code-review). The user's own measured drop shows the pattern: duplicating a built-in costs a hook process for nothing.
  Done when: `fm doctor` lists each Foreman mechanism next to its native equivalent with "keep / replace / delete" and a cited reason, and a test fails if a listed mechanism has no row.

- **Fold the 73 skills into a measured core and a lazy rest** — CLEAN — value 4 — effort M — risk med — category: skills
  Why: plugin/skills holds 73 entries; only some are likely invoked. Skill descriptions load into every session's context. assumption: usage data exists in transcripts.
  Done when: a report shows invocation counts for all 73 over 30 days, skills with zero uses are archived or merged, and the session-start skill listing is smaller by a stated token count.

- **Retire the tmux send-keys bus behind a single wake interface** — CLEAN — value 4 — effort M — risk med — category: wake
  Why: user said "make sure it doesnt sit idle" (T-0758); wakeups by typing into a tmux pane break outside tmux and are a fragile surface. One `wake(session)` function with ScheduleWakeup as the only path removes a branch in every launcher.
  Done when: `grep -r send-keys plugin/lib` returns nothing and an idle-session test wakes via the new path.

- **Make the active step a derived value, never a stored one** — FIX — value 5 — effort M — risk med — category: state
  Why: T-0759: "it will start working on different steps without updating the step". Storing step state that the model must update invites drift. Compute it from evidence (which step's files and tests were last touched or passed).
  Done when: a replay of a transcript where edits precede `fm step` calls shows the displayed step equal to the step owning the edited files, with no model-side call.

- **Collapse the 14 hook events to the ones with a measured decision** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: hooks are latency-gated by bench_hooks.py; MessageDisplay, Notification and SessionEnd probably only log. assumption: some hooks never change an outcome.
  Done when: each registered hook has a counted "changed a decision" figure over 30 days, zero-impact ones are removed, and bench_hooks p95 improves or holds.

- **Write one page, "what Foreman adds over stock Claude Code"** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: MASTER.md documents every file, but with built-in /code-review, /simplify, worktrees, Monitor and Workflow now native, the user and Foreman itself need a short answer to what is left to own. Also guides every deletion above.
  Done when: a ≤1-page section lists only capabilities with no native equivalent, each linked to the test that proves it.

- **Wild: Make Foreman a thin default and the rest opt-in packs** — FEATURE — value 4 — effort L — risk high — category: packaging
  Why: the install has 341 files and flags like --security, --docs, --no-mod; wild because it reverses growth. Core is guard, task store, resume, and verify; lanes, night, ideas, desktop become packs.
  Done when: `install.sh --core` yields a working install under a stated file count, and the e2e roundtrip passes with only core.

- **Wild: Add a "deletion budget" to each release** — CLEAN — value 3 — effort S — risk low — category: release
  Why: the last eight releases (1.2.17–1.2.27) each added milestones; none recorded removals. release.py could require net lines or skill count not to rise.
  Done when: `release.py` prints added versus removed files and lines, and fails when both are zero removed for three releases in a row.

- **Wild: Let Foreman answer "can I just ask Claude instead?" per task** — FEATURE — value 3 — effort M — risk med — category: triage
  Why: user wrote terse requests and asked for less friction; assumption: many tasks (S, FIX of one line) cost more in classify/plan/verify ceremony than the work. A tiny-task fast path skips plan review and full gates.
  Done when: S-tier tasks touching one file run with no plan step and one targeted test, and the bench shows fewer tool calls on a fixture set, with the guard unchanged.

- **Make fm batch the default for same-session captures** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: T-0757 asked to group related things into one task; dropped as "already built" because the user still had to know it. Auto-group captures that share files or words in the same session.
  Done when: three captured requests touching the same module appear as one batched task with three steps.

- **Prune the user's-words steers into a three-line preference file** — CLEAN — value 3 — effort S — risk low — category: memory
  Why: steered/dropped entries repeat one message: no duplicated built-ins, measured claims, fewer tokens, bigger orchestration. A short preferences file read by ideation avoids re-proposing dropped ideas.
  Done when: `fm ideas` input includes the file, and a rerun does not propose delta reads or a context firewall.
