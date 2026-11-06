# Brainstorm — lens: approaches

- **Fail a task over to another agent when usage runs out** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: the pace/budget work (T-0320) and the codex/gemini/opencode adapters exist, but nothing joins them. Resume points are already portable via `fm resume`, so the pieces are there. Assumption: the checkpoint can be rendered as the other harness's context file with `fm export`.
  Done when: with Claude usage mocked at 100%, `fm run` hands the active task to a codex session, which resumes at the recorded step and finishes it, and the ledger shows the handoff.

- **Record a baseline of known-red gates** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: `fm check` exits 1 on any failure, so a project that arrives with pre-existing red tests makes every task look like it broke something. Quarantining flaky gates is a different problem. Assumption: new projects often arrive partly red.
  Done when: `fm init` stores a baseline of failing checks, and `fm task done` fails only on failures not in the baseline. It reports "N pre-existing, 0 new" and flags a baseline entry that has gone green.

- **Test the adapters with a scripted fake model and cassettes** — FEATURE — value 4 — effort M — risk low — category: adapters
  Why: T-0335, T-0336 and T-0337 are blocked on live codex, gemini and opencode accounts. Assumption: a scripted agent that emits fixed tool calls through each harness's hook protocol is enough to exercise the guard, drive and resume paths.
  Done when: `fm agents verify codex` runs a scripted scenario (an allowed edit, a refused `rm`, a resume after compaction) with no network. The run fails if a hook output deviates from the recorded cassette.

- **Spend the user's attention as a budget and batch asks** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: `fm ask` and standing yeses exist, and the user keeps removing blocks and idle time (75% pace, "never leave idle"). But asks still interrupt one by one. This is distinct from predicting approvals: it changes when asks are delivered, not whether they are asked. Assumption: most asks can wait for the next natural pause.
  Done when: non-urgent asks queue into one digest shown at session start or via `fm next`, work on unblocked tasks continues meanwhile, and the ledger counts interruptions per day.

- **Add an objectives layer above tasks** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: the user's asks are outcomes ("Foreman checks the product the way its user uses it", "never idle"), yet the queue holds 20+ flat tasks and `fm relate` only groups by mentions. Assumption: an objective can carry a measurable check, such as an `fm smoke` journey or a replay metric.
  Done when: `fm objective new` links tasks to a measurable check, and `fm state` shows each objective as met, moving or stalled, with the tasks serving it.

- **Detect re-asks of things already dropped** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: the pack shows YAGNI decisions and "working as intended" drops (the guard `&&` focus case, the `python -c` case). Those requests will come back in new words. Assumption: `fm recall` over decisions.md can match them.
  Done when: capturing a request similar to a recorded drop prints the decision and its reason. The user can override with `--again`, and that override is logged.

- **Mine invariants from the repo and propose them as gates** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: gates come only from `fm map` discovery. Assumption: running the test suite under tracing can surface stable properties, such as call-count bounds, schema keys and exit-code contracts, that no test asserts.
  Done when: `fm gates --mine` lists at least one candidate invariant with its evidence. Accepting it adds a gate that fails on a seeded violation.

- **Park and resume tasks with a task stack** — FEATURE — value 3 — effort M — risk med — category: workflow
  Why: JARVIS hit refusals when switching between lane tasks and T-0278, which shows context switches are costly. Capture-only handles new asks but not urgent preemption. Assumption: a parked task needs its dirty files and resume point saved together.
  Done when: `fm focus --push T-X` parks the current task's step and dirty-file list. Finishing T-X pops back to the exact step, and the guard never reports "no active task" during the switch.

- **Rank review packets by risk and the reader's time** — FEATURE — value 3 — effort M — risk low — category: review
  Why: `fm tour` orders files for reading but treats all hunks as equal. Assumption: risk can be scored from hot files, guard-adjacent paths, test coverage links and diff size.
  Done when: `fm tour --minutes 5` shows only the hunks that fit that time, highest risk first. It states what was skipped, and a seeded risky hunk always appears.

- **Express guard rules as data in a policy engine** — FEATURE — value 3 — effort L — risk high — category: guard
  Why: the guard is hand-coded bash parsing with repeated patch tasks (T-0275, T-0414, T-0421, T-0422), and each fix touches code. Trade-off: more rules become auditable and testable, but it adds an engine dependency and a migration risk. Assumption: the parsed command tree can feed a Cedar/OPA-style evaluator.
  Done when: at least the symlink-`rm` and confine rules live in a declarative file. The 5000-command replay gives identical verdicts, and a rule change needs no Python edit.

- **Triage the public repo's issues into briefs** — FEATURE — value 3 — effort M — risk med — category: community
  Why: T-0352 plans publishing the Desktop app on GitHub, and the Foreman repo is public. Assumption: issue text is untrusted and must go through intake without executing anything from it. wild
  Done when: `fm intake --github` turns a new issue into a captured brief with a link back. The issue text is quoted as data, and the guard refuses an injected instruction in a test issue.

- **Rebuild Foreman from its own prompt and diff the result** — FEATURE — value 3 — effort L — risk med — category: self-hosting
  Why: `--build` and `BUILD_PROMPT.md` already exist, and `fm bench` can replay cases. Nothing checks that the prompt still produces a working Foreman. Assumption: a rebuild in a clean directory is affordable overnight. wild
  Done when: a nightly job builds a fresh Foreman from `BUILD_PROMPT.md` and runs `fm bench` on it. It reports the score gap against the shipped version and lists the features the prompt no longer reproduces.

- **Give rules a half-life and require reaffirmation** — FEATURE — value 3 — effort M — risk low — category: governance
  Why: the user has flagged cleanup that "never got done", while rules, vetoes and standing yeses only accumulate. Auto-retiring stale lessons is a different idea, since this applies to the user's own commands. Assumption: the user prefers a quick keep-or-drop prompt to silent expiry. wild
  Done when: each veto and standing yes carries a last-used date. After N idle days it appears once in `fm next` as keep, drop or snooze, and a dropped rule stops being enforced.

- **Let two lanes duel a risky guard change in public** — FEATURE — value 2 — effort M — risk med — category: guard
  Why: guard fixes land after incidents, and the false-positive history lives in JARVIS reports. Assumption: pairing a loosening lane against a tightening lane, with the 5000-command replay as referee, would expose regressions before release. wild
  Done when: `fm guard duel` runs both candidate patches through the replay and prints which commands each flips. A patch that blocks a previously allowed safe command, or allows a previously blocked dangerous one, is flagged.
