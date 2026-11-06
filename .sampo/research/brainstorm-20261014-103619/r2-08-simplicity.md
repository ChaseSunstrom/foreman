# Brainstorm — lens: simplicity

- **Make the installer a native plugin install with zero flags** — CLEAN — value 4 — effort M — risk med — category: install
  Why: install.sh has about 9 flags (`--security`, `--docs`, `--no-bypass`, `--no-mod`, `--no-wiring`, `--build`, `--desktop`, and others) plus Python bootstrapping. Assumption: Claude Code's plugin marketplace can carry hooks, agents and skills, so only wiring and bypass need a first-run `fm setup`.
  Done when: on a clean machine `claude plugin install foreman` plus one `fm setup` yields a passing `fm doctor`, and install.sh shrinks to a thin shim.

- **Retire the non-Claude harness adapters** — CLEAN — value 4 — effort M — risk med — category: scope
  Why: T-0335, T-0336 and T-0337 (Codex, Gemini, opencode) are blocked and never live-verified, and each costs conformance and guard-parity surface. Foreman is described as "a discipline layer for Claude Code".
  Done when: the adapter code and its tests are removed, the three tasks are closed as won't-do with a decision record, and `fm doctor` and the full suite are green with fewer files.

- **Store lessons and vetoes as native path-scoped rules** — CLEAN — value 4 — effort M — risk med — category: memory
  Why: SessionStart and UserPromptSubmit hooks inject lessons by custom code under a latency gate. Assumption: Claude Code loads `.claude/rules/*.md` with path globs lazily, which would make the injection hook unnecessary.
  Done when: lessons render into rule files, the injection code is deleted, and `bench_hooks.py` shows lower p95 with a bench lesson-recall case unchanged.

- **Move the declarative half of the guard into settings deny rules** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: most guard rules are fixed patterns such as `rm -rf ~` and force-push, while the heuristic parser is where false positives live (see the dropped heredoc and `python -c` cases). Assumption: deny rules still apply in bypass mode. Check that first.
  Done when: a generated `permissions.deny` block covers N static rules, the guard's parser handles only the remainder, and a differential corpus shows identical verdicts.

- **Make one skill the router and push the other 72 into references** — CLEAN — value 4 — effort M — risk low — category: skills
  Why: plugin/skills holds 73 files, and every description sits in context each session. Progressive disclosure through a single router with `references/` pays for only what is used.
  Done when: the session-start skill listing drops below a measured token count and the bench routing cases still pick the right procedure.

- **Use the native todo list as the step pointer** — FIX — value 5 — effort M — risk med — category: step tracking
  Why: T-0759 reports work starting on different steps without the step being updated, and Foreman keeps its own parallel pointer. Assumption: a hook can read the host's todo state, so the pointer can have one owner.
  Done when: the pointer is read from native todo state, the custom writer is deleted, and a test that works ahead of the pointer shows the pointer following.

- **Run a hook diet driven by measured effect** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: 14 hook events are registered and latency-gated, but nothing shows which ever changed an outcome. MessageDisplay, Notification and PermissionRequest are the likeliest to be redundant.
  Done when: a report lists per-event fire counts against behaviour changes over 30 days, and every event with zero effect is removed with `bench_hooks.py` improved.

- **Merge fragments of one message into one task** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-0755 to T-0760 are separate captures from one rambling message, one of them truncated ("also, the …"). T-0757 shows the user asking to "put them into one task/milestone".
  Done when: a multi-part message becomes one task with a checklist, and a test with the six captures above yields one parent task.

- **Make ListAgents the lane registry** — CLEAN — value 3 — effort M — risk med — category: fleet
  Why: Foreman keeps its own lane state and reconciles it on resume, while the host already tracks background agents. Assumption: ListAgents lists them with enough identity to map back to a task.
  Done when: lane state files are deleted, resume reconciles from ListAgents, and killing a lane mid-step is still detected.

- **Freeze the foreman-ui mod at its current version** — CLEAN — value 3 — effort S — risk low — category: ui
  Why: T-0418 (update to 0.6.1) is blocked and T-0166 (refactor) is deferred, and a patched bundle breaks on Claude Code updates. The statusline and output style already carry the essentials.
  Done when: the mod is marked maintenance-only in MASTER.md, the open tasks are closed, and `fm doctor` reports the mod as optional.

- **Wild: Ship a "Foreman Lite" that must tie the full build on bench** — FEATURE — value 4 — effort L — risk med — category: lite mode
  Why: wild. The discipline might fit in an output style, the guard, the done-gate and resume. Anything that loses to the full build on the bench is the only proof a subsystem earns its place.
  Done when: a lite profile runs the bench, and every subsystem it omits is either shown to lose or listed as proven value.

- **Wild: Put a 30-day fuse on every new feature** — CLEAN — value 4 — effort M — risk med — category: lifecycle
  Why: wild. The user asked for deletion-minded releases (outline-first reads, delta reads dropped as duplicating a built-in). A feature that isn't used within its fuse is removed unless the user renews it.
  Done when: each feature records a usage counter and an expiry, and `fm doctor` lists features about to expire.

- **Wild: Derive the ledger from Claude Code transcripts** — CLEAN — value 3 — effort L — risk high — category: state
  Why: wild. Foreman keeps a ledger, briefs, STATE and decisions beside transcripts that already hold the events. An index over the transcripts could replace most of the writers.
  Done when: `fm ledger` for one finished task is rebuilt from transcripts alone and matches the stored ledger on a replay test.
