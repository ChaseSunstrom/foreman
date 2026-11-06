# Brainstorm — lens: deepen: trust

- **Install as a transaction: `fm install --plan`, then apply with a journal** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: newcomer finding A2 (silent third-party plugins, bypass, outputStyle, statusline, 20 deny rules) and A10 (uninstall residue, "defaultMode = None"). Combines the plan, receipt, per-item opt-out and git-backed journal ideas into one mechanism.
  Done when: `install.sh --plan` prints every `~/.claude` change as an itemised list and writes nothing; applying records each change in a journal; `uninstall` replays it in reverse and a diff of `~/.claude` before and after is empty.

- **Default to a ask-first permission posture, with bypass as an explained opt-in** — FIX — value 5 — effort S — risk med — category: trust
  Why: A2 says bypass by default is a large trust ask, and the install output only says "Claude Code asks you to confirm once". Rivals (B) add commands and don't rewrite permissions.
  Done when: a fresh install leaves `permissions.defaultMode` untouched unless `--bypass` is passed or the user answers yes to an install question that states what bypass does and which guard rules replace the prompts.

- **Log "would have asked" decisions so bypass can be earned** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the guard already classifies commands in bypass mode; the ledger has 688 tasks. Recording which calls default mode would have prompted, and which of those the guard blocked, gives evidence rather than a leap of faith. Assumption: the guard can tell a prompting call from a silent one.
  Done when: `fm trust` shows, for the last N days, the count of calls default mode would have prompted, how many the guard blocked, and how many were harmless, and offers bypass only after a configurable clean streak.

- **Add `fm claude-undo`: snapshot `~/.claude` at session start and restore on request** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: Foreman edits settings, rules, statusline and plugins, and the user has no one-step revert (A10). A rolling snapshot covers Foreman's own bugs as well as install.
  Done when: after a test run that mutates settings, `fm claude-undo` restores the earlier bytes and prints the files it changed; snapshots are capped in count and size.

- **Add `fm try`: one session of Foreman that leaves no trace** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: A1 and A3 show a newcomer has to commit before seeing any value, while rivals install with one marketplace command. A temp config dir plus `claude --plugin-dir` would avoid touching the real HOME. Assumption: Claude Code honours a config-dir override.
  Done when: `fm try` starts a session with Foreman active, and `~/.claude` has an identical checksum before and after, including after a Ctrl-C.

- **Ship a marketplace-installable "Foreman Lite" that adds commands and hooks without rewriting `~/.claude`** — FEATURE — value 5 — effort L — risk med — category: trust
  Why: B says every popular rival installs through the marketplace and only adds commands, and Foreman lacks that path. Lite carries the guard, evidence gate and resume, and none of the settings wiring. The posture is chosen at install, and the full set is an upgrade.
  Done when: `/plugin install` alone gives a session that blocks a seeded dangerous command and records evidence, with a zero-line diff to user settings.

- **Make the guard core one auditable page with a published threat model** — SECURITY — value 4 — effort M — risk med — category: trust
  Why: users are asked to trust a guard inside a 28k-line codebase (D). A small core, with exhaustive tests that map to a written threat model, makes the trust ask checkable. Open task T-0275 (guard reads script files) belongs in it.
  Done when: the guard's decision core is under a fixed line budget in one file, every rule maps to a named test, and CI fails if either breaks.

- **Fail the release on install footprint and hook latency** — CLEAN — value 3 — effort S — risk low — category: trust
  Why: C and D show the footprint growing (rules loaded every session, 1.5k chars of SessionStart context), and `bench_hooks.py` is already a gate. Add budgets for files written to `~/.claude`, always-loaded words and hook milliseconds.
  Done when: a change that adds 500 words to the always-loaded rules, or writes a new file under `~/.claude`, fails the release check with the delta shown.

- **Make the held rate honest: a ledger-derived scorecard with ungraded work shown as ungraded** — FIX — value 4 — effort M — risk low — category: trust
  Why: C says 670 of 688 held, but 159 of last week's 370 are "ungraded", and the bench has 1 case and 0/3 court cases. A trust claim built on unspoken denominators erodes trust. Pairs with the README lint that makes every number cite a results file.
  Done when: `fm digest` and the README print held, fixed-later and ungraded counts with their denominators, and a lint fails on any README number that has no source file.

- **Wild: a day-7 "did Foreman earn its place" card with keep / lite / remove**
  Why: wild; assumption: the ledger has enough tasks by day 7 to show real catches, such as blocked commands, failed-then-fixed gates and resumed work. The card lists them in plain words, and "remove" runs the journaled uninstall in one keystroke.
  Done when: on day 7 the next session opens with the card; choosing each option performs and reports the matching change; declining stops it for 30 days.
  — FEATURE — value 4 — effort M — risk low — category: trust

- **Wild: a no-model hostile-repo drill at first install**
  Why: wild; the guard can be shown working before the user trusts it. A scratch repo contains a planted `rm -rf`, a curl-pipe-bash and a secret-exfil attempt, and Foreman runs them against its own guard and shows each refusal.
  Done when: `fm drill` prints a pass/fail line per seeded attack with no model calls and no writes outside its temp directory, and `fm doctor` runs it as a check.
  — SECURITY — value 4 — effort S — risk low — category: trust

- **Wild: let Foreman recommend its own uninstall when the bench shows no lift**
  Why: wild; a plugin that tells the owner when it isn't helping earns more trust than any badge. It needs the bench to have real cases first (C: 1 case today). Assumption: the bench can compare with and without Foreman on the user's own repo.
  Done when: after at least N paired bench runs on the user's repo with no measured improvement, `fm status` suggests Lite or removal, and no nag appears while results are positive.
  — FEATURE — value 3 — effort L — risk med — category: trust

- **Add `fm oops`: one word for "that was wrong", which reverts and teaches**
  Why: the ledger already stores diffs, evidence and lessons, and "fixed later" is only 2.6%. A one-word escape lowers the cost of trusting the agent: it reverts the last task's changes in the worktree, files the miss as a lesson and reopens the task.
  Done when: after a finished task, `fm oops` restores the pre-task tree, reopens the task with the reason attached, and writes a lesson that appears in the next related brief.
  — FEATURE — value 4 — effort M — risk med — category: trust

- **Publish `foreman/evidence` as a GitHub required status check**
  Why: the evidence gate is Foreman's core promise, but only the local session sees it. Posting the recorded evidence for a task's commits as a commit status lets reviewers and teammates trust the claim without trusting the author's machine; it also answers the missing GitHub sync (B).
  Done when: a PR from a Foreman task shows a `foreman/evidence` status linking the gate output, and a PR whose evidence is missing or stale shows it failing.
  — FEATURE — value 4 — effort M — risk med — category: trust
