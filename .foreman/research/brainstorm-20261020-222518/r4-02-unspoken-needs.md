# Brainstorm — lens: unspoken needs

- **Trust the cwd before the first call** — FEATURE — value 5 — effort S — risk low — category: first-run
  Why: the nixie run "just isn't doing anything" and the pack's ideas list has "warn when the cwd isn't the project you meant" only as a title. Assumption: the user ran it from a subfolder or an unregistered directory without noticing which project root Foreman resolved.
  Done when: `fm code "x"` in a subdirectory or a non-Foreman folder prints the resolved project root and its queue count before any model call, and a test asserts the line appears first.

- **Make the first-sign-of-life deadline a failing test** — FIX — value 5 — effort M — risk low — category: liveness
  Why: the planner ran for minutes with 66k–133k input tokens and no visible output. Many ideas propose heartbeats, but none turns "something visible within N seconds" into a gate that fails the build.
  Done when: a bench case with a fake CLI that stays silent for 60 s fails unless Activity shows a named "waiting on <runner>, N s" line within 10 s.

- **Convert "it just isn't doing anything" into a stall record automatically** — FEATURE — value 5 — effort M — risk med — category: self-notice
  Why: the user said Foreman should figure this out without being asked. The watchdog ideas diagnose, but none persists the evidence (child tree, last bytes read, token count, env marker) as a task with a repro. Assumption: friction phrases are already detected by the T-1330 follow-up.
  Done when: a run with no child output for the stall threshold writes `stall-<run>.json` and opens a task whose body quotes the user's phrase and the diagnosis.

- **Keep the user's standing permissions as a ledger Foreman reads** — FEATURE — value 4 — effort S — risk med — category: autonomy
  Why: the user said three times to stop asking about releases, to keep going, and that they give full permission. Each was a fresh steer. Foreman should store these as durable grants, scoped and revocable, and show them.
  Done when: `fm grants` lists "release: always (said 2026-10-20)" and a release task proceeds without any `fm ask`; revoking one restores the prompt.

- **Rank "what needs you" across projects by age and blocking** — FEATURE — value 4 — effort M — risk low — category: home screen
  Why: T-0325, T-0335, T-0336, T-0352 and T-0418 sit blocked for unnamed reasons. Assumption: the home screen from T-1330 lists them by project but not by how long they have waited or what each unblocks.
  Done when: the home screen's first row is the single oldest blocked item that gates other tasks, with the one command that would clear it.

- **Show the startup tax before launching a worker, and offer the lean profile** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: the 66k–133k tokens per planner call come from loading every plugin and Foreman's hooks. T-1327 strips context but the user never sees the cost or the saving.
  Done when: before a nested claude starts, one line shows "loads ~N tokens; lean profile ~M", measured by a probe, and a test checks the lean figure is lower.

- **Write the release notes the user reads from their own requests** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: seven of the user's recent requests are "Release 1.2.4x: <list>", each hand-composed. Assumption: the task titles that closed since the last tag already hold that list.
  Done when: `fm release --draft` prints a tag line and summary built from closed task titles, matching the format of the last three release requests.

- **Pin the rule that `fm` must be on PATH as a doctor failure** — FIX — value 4 — effort S — risk low — category: setup
  Why: `fm` wasn't a command in the user's shell and needed a manual ~/.local/bin link. Assumption: `fm doctor` only checks inside Claude Code.
  Done when: `fm doctor` run from a bare login shell without the plugin on PATH reports a red line with the exact link command, and passes after it.

- **Let a complaint become a check, and show which check it became (wild)** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: the user's complaints, such as "looked like crap with all the text" and "isn't doing anything", are the real acceptance criteria and get lost between rounds.
  Done when: the phrase "it just isn't doing anything" creates a named regression case in the bench and `fm code bench` runs it.

- **Offer a one-key "take it from here" when Claude Code itself stalls (wild)** — FEATURE — value 3 — effort L — risk high — category: handoff
  Why: the user moves between Claude Code and fm code and is annoyed by gaps between them. Assumption: the session transcript file is readable.
  Done when: in a project with a recent Claude Code transcript, `fm code --adopt` opens a run whose request and plan are seeded from that transcript's last user turn.

- **Leave a morning digest of what the unattended runs did (wild)** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: "dont' stop until complete, full auto" shows the user runs long sessions unattended. Assumption: the digest will be read on the next `fm code` open, not pushed anywhere.
  Done when: opening the home screen after a night of runs shows a first card listing closed, failed and waiting tasks per project with their costs.

- **Name the duplicate-Foreman fact on screen (wild)** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: the user asked to prevent a second Foreman when Claude Code runs as a worker, and T-1327 does so silently. A silent fix is invisible, so the user can't trust it.
  Done when: a worker's Activity shows "nested Claude: Foreman context off (depth 1)" once per run, and a test asserts it.
