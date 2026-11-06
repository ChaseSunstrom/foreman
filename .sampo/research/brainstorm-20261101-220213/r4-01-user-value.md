# Brainstorm — lens: user value

- **Add a user-owned protected-paths file the guard enforces for every agent** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: assumption: the guard blocks command shapes, but the user's own "never touch" list (`~/.ssh`, `prod.env`, `migrations/applied/`) has no one file. The 2 brief-guard false positives show path logic is the fragile part, so a plain deny/allow list is a safer base.
  Done when: a path listed in the file is refused by `fm code`, Claude Code, and a headless run, each with a test that names the line in the file.

- **Add a timed, scoped guard release valve** — FEATURE — value 5 — effort S — risk med — category: guard
  Why: the guard blocked `core:interpreter-code-driving-foreman` 42 times in 7 days. Without a sanctioned `fm guard allow RULE --for 10m --task T-…`, a user who hits one block is tempted to uninstall. The allowance re-arms itself and is logged for the final report.
  Done when: after the window the same command is blocked again, and the allowance is visible in `fm doctor` while active.

- **Treat an interrupt after an allowed call as a guard-miss signal** — FEATURE — value 4 — effort M — risk low — category: learn
  Why: the "learn" column has no signal the user authors for free. A user pressing Esc right after a command the guard allowed is a soft vote for a new rule. Foreman files only a candidate in shadow, never an auto-rule.
  Done when: a replayed transcript with an interrupt after an allowed `rm -r` produces one shadow candidate row, and nothing is enforced.

- **Add an untrusted-checkout mode** — SECURITY — value 5 — effort M — risk med — category: supply chain
  Why: assumption: a freshly cloned repo can carry its own `.claude` settings, CLAUDE.md, stack cards and `fm` config, and those load before the user has judged the repo. Until `fm trust` is run, Foreman ignores the repo-provided parts and says which it skipped.
  Done when: a fixture repo with a hostile hook file runs nothing on session start, and `fm trust` enables it.

- **Refuse any spawn that has no default cost ceiling** — SECURITY — value 4 — effort S — risk low — category: headless
  Why: the headless/server column is where nobody is watching. Audit every `claude -p` and `fm code` spawn path; one with no cap and no setting fails a test that lists the spawn sites.
  Done when: a test enumerates the spawn sites and fails if one has no resolved ceiling.

- **Warn on secrets pasted into a prompt, before they are sent** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: assumption: the diff-secret scan covers finished work, not the prompt. A UserPromptSubmit check for key-shaped strings could suggest putting it in an env var. This stays one cheap regex pass inside the hook budget.
  Done when: a prompt containing a fake `sk-…` key produces a one-line warning, and hook p95 is unchanged in `bench_hooks.py`.

- **Ship a minimal install profile for headless and server use** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: T-0794 (Lite mode) sits deferred while 61 cells are empty. A profile with only the guard, `fm doctor` and the task loop gives the server and CLI columns a real answer instead of an n/a. Context per reply averages 387k, so a smaller footprint matters.
  Done when: `fm install --profile minimal` leaves under N hooks and under N injected bytes, and `fm doctor` passes with no `claude` on PATH.

- **Print the guard state at session start in one line** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: bypass-mode users need to know the guard is armed on this surface now. The line reads "guard armed: 14 rules, last verified against host 2.1.301", or says "unguarded" for hookless agents.
  Done when: all four harnesses print a line, and a deliberately disarmed guard prints "unguarded".

- **Wild: Export a dated guard receipt bundle for a team lead** — FEATURE — value 3 — effort M — risk low — category: audit
  Why: wild. A user running agents in bypass mode at work may need to show what the guard stopped and what it let through. A redacted JSON plus a one-page summary, built from existing logs, is something nobody else ships.
  Done when: `fm guard receipt --since 30d` writes a file with no paths outside the repo.

- **Wild: Let a user's "that was dumb" word promote any past tool call into a rule draft** — FEATURE — value 3 — effort M — risk med — category: learn
  Why: wild. Users already tell agents off in chat. A short phrase after an action turns that action into a candidate rule with a replay against the last 30 days of calls. A user who wrote nothing never gets one.
  Done when: a scripted correction creates a draft that lists how many past calls it would have blocked.

- **Wild: Show a "weight versus saved" ticker on the status line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A running pair, "+0.3s/turn, 2 blocks this week", makes the lean-and-safe tradeoff visible. Users stop guessing whether Foreman is worth keeping.
  Done when: the status line shows both numbers from `fm friction` and `fm guard` logs, and appears only if the user opts in.

- **Add a "why is this cell n/a" page for the user, not the tower** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the 61 cells are written for Genesis. A user choosing between Desktop and headless wants "what is protected here" in one table, with each row linking to the probe command that proves it.
  Done when: the site's Genesis page renders the grid with a probe link per non-n/a cell.

- **Stamp the host version beside every guard claim** — FIX — value 3 — effort S — risk low — category: trust
  Why: assumption: guard claims age silently when Claude Code, Codex or Gemini update. Claims show "verified on 2.1.301, 9 days ago" and turn grey when the host differs.
  Done when: a stubbed newer host version turns the claim stale in `fm doctor`.

Next question: Which of the 61 cells would a user actually read, and which exist only so the sweep goes green?
Next question: What does a user do the first time the guard blocks something they truly wanted, and is every path from there something other than uninstalling?
