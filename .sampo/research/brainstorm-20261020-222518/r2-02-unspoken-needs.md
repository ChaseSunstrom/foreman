# Brainstorm — lens: unspoken needs

- **Answer "did my words land?" with a request echo before any work starts** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: The nixie run "just isn't doing anything", and the user keeps restating asks ("again, I shouldn't even need to say anything"). Assumption: they can't tell whether a request was captured, interpreted as a question vs. task, or routed to a runner. Echo within 1s: kind (fix/question/new project), project, runner, estimated token tax, and the first checkable criterion.
  Done when: `fm code "<request>"` in a fake-runner test prints the kind, project, runner and one criterion before the first runner call, and the timing is asserted under 1s.

- **Make every silent minute self-explaining with a live "what it's waiting on" line** — FIX — value 5 — effort M — risk low — category: liveness
  Why: Planner ran for minutes at 66k–133k input tokens per call with no visible progress, then orphaned on quit. Distinct from T-1329 (streaming progress): this names the cause (runner loading plugins, model thinking, waiting on a lease, waiting on you) when no events arrive, and offers a key to act (cut, switch runner, kill).
  Done when: a scripted fake runner that stays silent 20s causes the Activity panel to show a named wait cause and a key hint, asserted in a golden frame.

- **Detect Foreman-inside-Foreman at process level and refuse the duplicate** — FIX — value 5 — effort S — risk low — category: nesting
  Why: The user asked to "prevent duplicate things when FM is installed as a claude plugin". T-1327 strips context for nested Claude, but a depth marker in the environment, checked by hooks, fm, and the guard, makes any CLI worker (codex, gemini, aider wrapping fm) safe too. Assumption: not all nested paths go through the one launcher T-1327 touches.
  Done when: with `FM_DEPTH=1` set, a Foreman hook and `fm code` each print one line "nested: outer Foreman is in charge" and do not capture requests or start a planner; the guard still blocks `git reset --hard`.

- **Turn friction phrases into a standing, self-filed diagnostic round** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: The user said Foreman should notice "it just isn't doing anything" and "why can't I…" itself, and it was already asked as a task. Round 2 angle: make the trigger a rule table with a receipt ("noticed friction in fm code, opened T-xxxx, brainstorm queued") and a per-area cooldown, so it can't spam rounds.
  Done when: feeding the phrase "why can't I launch X" to the request-capture hook files one task tagged with the area and a receipt line; a second identical phrase within the cooldown files none.

- **Adopt an existing Claude Code session or terminal run into fm code (wild)** — FEATURE — value 4 — effort L — risk high — category: continuity
  Why: assumption: the user starts in Claude Code (where fm works) and then wants fm code's TUI over the same work. Import the session transcript and open task as the run's starting state rather than restarting a 133k-token planner.
  Done when: `fm code --adopt <session>` opens a run whose first screen shows the session's open task and last 3 tool calls, with no planner call made.

- **Offer "what should I work on?" as the bare-`fm code` landing answer** — FEATURE — value 5 — effort M — risk low — category: home screen
  Why: T-1330 plans a home over queue/inbox/blocked. The unspoken need: the user doesn't want to read a list; they want one ranked recommendation across projects (blocked-but-unblockable, cheapest green win, oldest stalled) with a one-key start.
  Done when: with three seeded projects, the home screen's top line names one task with a reason, and Enter starts it with the suggested runner.

- **Make wrong-directory runs impossible to miss** — FIX — value 4 — effort S — risk low — category: projects
  Why: The nixie run happened in ~/projects/nixie, and multi-project is a stated goal. Assumption: users launch from odd directories, subfolders, or worktrees. Always show the resolved project root, branch and dirty state in the header, and ask once when cwd is a subfolder of a different registered project.
  Done when: running `fm code` from a nested subdirectory shows the repo root and branch in the first frame; a cwd inside two nested repos asks which.

- **Ship `fm code why`: one command that explains the last run or the current silence** — FEATURE — value 4 — effort S — risk low — category: diagnosis
  Why: The user's route to find out what happened was asking Claude. A deterministic command reading the event log and process registry answers: alive or not, last event age, token tax, orphaned children, runner used.
  Done when: against a recorded stalled-run fixture, `fm code why` prints the named cause and exits nonzero for a dead run.

- **Price and time the first call before it runs, with a one-key cheaper path** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: 66k–133k input tokens per planner call is a surprise cost nobody opted into. Preflight measures the runner's startup load (plugins, hooks, rules) and offers the lean profile if it exceeds a threshold. Distinct from the token meter ideas: this acts before the spend.
  Done when: a fake runner reporting a 100k start load triggers a prompt with the estimate and a lean-profile option, and choosing it drops the logged load below the threshold.

- **Let Foreman keep a "last session" so reopening resumes the thing you were doing** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: Quitting killed work and the user had to restart. With T-1326 killing children, the run state should be journaled so `fm code` offers "resume T-xxxx at step 3" first.
  Done when: killing a fake run mid-step then launching `fm code` shows a resume option that continues from the journaled step with no replanning.

- **Install check that fixes the shell itself (wild)** — FEATURE — value 4 — effort M — risk med — category: setup
  Why: `fm` wasn't a command in the user's shell; a link in ~/.local/bin fixed it by hand. Bare `fm` should detect that, say so, and offer the exact fix, including PATH order, shell rc, and a stale duplicate binary shadowing the plugin one.
  Done when: in a sandbox HOME with `fm` off PATH, running the plugin's `bin/fm` prints the detected gap and the one-line fix, and applying it makes `command -v fm` succeed.

- **Dock beside Claude Code as a live companion, not a separate app (wild)** — FEATURE — value 3 — effort M — risk med — category: surface
  Why: The user runs Claude Code with the foreman-ui pane today and also wants an app like it; assumption they'll use both. A `--dock` view shows only the "now" line, needs-you strip and queue for the same project, sharing the event log.
  Done when: with a run in progress, `fm code --dock` renders at 40 columns showing the current station and the queue, updating as events append.

- **Hand the user a morning digest across all projects when unattended runs end (wild)** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: "dont stop until complete, full auto" shows they run long. Assumption: they leave and return. A single page: what closed with proof, what is blocked on them, what it cost, per project, written as a file and opened by bare `fm code`.
  Done when: after a fake two-project unattended run, the home screen's first panel lists both projects' closed and blocked tasks with cost, and the same content exists as a file.
