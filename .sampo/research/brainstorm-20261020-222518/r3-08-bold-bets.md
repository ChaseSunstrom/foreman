# Brainstorm — lens: bold bets

- **Make `fm code` a launch-time contract: a 10-second "first sign of life" SLA** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the nixie run sat for minutes with no sign of work (66k–133k input tokens per nested call, then orphaned on quit). Existing ideas diagnose silence after the fact; none make a visible deadline part of the product.
  Done when: a test with a fake runner that stays silent shows a named diagnosis ("runner loading 118k tokens of plugins", with the kill/slim/wait choice) in the Activity lane within 10 s, and a runner that streams passes without it.

- **Adopt a "lineage" env marker so any Foreman-in-Foreman collapses to one owner** — FIX — value 5 — effort S — risk low — category: nesting
  Why: the user asked to "prevent duplicate things when FM is installed as a claude plugin"; T-1327 strips context for nested Claude, but nothing covers other CLIs (codex, gemini, aider) that load their own hooks or call `fm` from a worker.
  Done when: running `fm code` with a worker that itself invokes `fm task new` and `fm code` creates no second queue entry, prints "owned by run R-…", and the nested guard still refuses a destructive command.

- **Compile every complaint into a standing regression check ("friction → check")** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: the user said "I shouldn't even need to ask"; the pack lists friction phrases ("just isn't doing anything", "why can't I…") but only as notes. Existing ideas file tickets; none turn the phrase into an executable check that stays in CI.
  Done when: feeding the phrase "it just isn't doing anything" to the intake creates a task whose verify command is a silent-runner test, and that test fails on a build without the watchdog and passes with it.

- **Add a `fm code` portable runner "audition" that writes the routing table from the user's own repos** — FEATURE — value 4 — effort L — risk med — category: runners
  Why: the user wants to manage ANY CLI/model; the bench grades on seeded tasks, but the choice of default is still manual. Past-run history across projects is real evidence for routing.
  Done when: `fm code audition` runs a 3-task sample on each detected runner in a scratch worktree, then `fm code config show` lists a per-request-kind default with the grade and cost that justified it.

- **Make a project's "resume point" a first-class object across app launches** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: closed lids, closed terminals and kill left an orphan in the nixie case; the home screen (T-1330) lists past runs but nothing says "this one was interrupted at step 3 of 5, resume?".
  Done when: killing a run with SIGKILL mid-step and launching bare `fm code` shows that run at the top of home with a one-key resume that continues from the recorded step and not from the plan.

- **Ship `fm code` as a Claude-style bare launcher with a shell integration installer** — FIX — value 4 — effort S — risk low — category: setup
  Why: `fm` wasn't on the user's PATH outside Claude Code; the fix was a manual link. Setup is still hand-run.
  Done when: on a fresh HOME, `python3 plugin/bin/fm setup` creates the PATH link (or prints the one exact line for the shell rc), and `fm code` then opens the home screen with no further configuration.

- **Give each worker CLI a measured "startup tax" that gates the launch** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: 66k–133k tokens per call came from nested plugin and rule loading; nobody sees this before the spend.
  Done when: `fm code runners` prints input tokens at first call per runner (measured by a one-word probe), and a runner over a configurable threshold prompts for the lean profile before starting.

- **Cross-project "what needs me" ranking that reads only existing task state** — FEATURE — value 4 — effort M — risk low — category: home screen
  Why: the user wants multiple projects managed; blocked/deferred items sit in many tasks (e.g. T-0325, T-0335, T-0352 blocked on external actions). Nothing ranks them across projects by who can act.
  Done when: the home screen's top strip lists blocked items from at least two fixture projects, each with the action needed (grant, install, answer), sorted by age, and selecting one jumps to its fix command.

- **Wild: Let Foreman write its own next brainstorm brief at the end of every release** — FEATURE — value 4 — effort M — risk med — category: autonomy — wild
  Why: the user keeps releasing and said "I shouldn't even need to say anything"; deferred "Later from…" tasks pile up (T-0788…T-0799) with no trigger to revisit them.
  Done when: after `fm release`, a dated brief appears listing the three deferred tasks whose triggers (evidence, bench result, user friction) now hold, and none whose triggers do not.

- **Wild: Adopt a running interactive Claude Code session as a lane through its transcript file** — FEATURE — value 3 — effort L — risk high — category: interop — wild
  Why: users work in Claude Code and fm code side by side; the dock pane already exists. Assumption: the session transcript is readable and tail-able without injecting input.
  Done when: with a Claude Code session running in another terminal, `fm code --watch` shows that session's steps, guard verdicts and changed files in a lane, read-only, without altering the session.

- **Wild: Rehearse a request against a "ghost" runner that returns canned plan shapes before spending anything** — FEATURE — value 3 — effort M — risk low — category: cost — wild
  Why: users hit cost and wait surprises on first calls; a dry-run showing the task, criteria and verify commands before any model spend lets them correct a misread request cheaply.
  Done when: `fm code --rehearse "request"` prints the intended project, runner, task title and criteria with a cost estimate and writes nothing, and the same request without the flag produces a task matching it.

- **Wild: Pasteable setup code that carries runners, theme and defaults, never secrets** — FEATURE — value 3 — effort S — risk low — category: setup — wild
  Why: "better config/setup" plus the user's habit of working on several machines (Linux, macOS CI). Assumption: the user has more than one machine.
  Done when: `fm code config export` prints one line, `fm code config import <line>` on a clean HOME reproduces the defaults, and the output contains no API key or token (checked by a secret-pattern test).

- **Hold a per-project lock so two app instances cannot run the same task** — FIX — value 3 — effort S — risk low — category: safety
  Why: the home screen (T-1330) lets any queued task run from any instance; with a tray, a TUI and a Claude Code worker all alive, double starts are likely. Existing leases cover workers, not app launches.
  Done when: starting `fm code --task T-X` in two terminals leaves one running and the second printing "T-X is running in pid N, attach?" with exit code non-zero.
