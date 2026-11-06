# Brainstorm — lens: unspoken needs

- **Trust the first minute: show "alive" evidence before any model answers** — FEATURE — value 5 — effort M — risk low — category: first-run
  Why: "it just isn't doing anything" in nixie came from minutes of silent planner time (66k–133k input tokens per call). T-1329 covers streaming progress, but not the case where the CLI emits nothing; the user needs proof of life from the OS side.
  Done when: with a fake runner that sleeps 60s silently, `fm code` shows within 5s a line with the child's pid, CPU time delta and bytes of stdout, and it updates every 5s (checked in a pty test).

- **Warn when the cwd isn't the project you meant** — FIX — value 4 — effort S — risk low — category: safety
  Why: the failing run was "started in ~/projects/nixie"; assumption: some of the confusion was Foreman not recognising the folder (no `.foreman`, not a git root, or a parent project). Bare `fm code` needs a visible "working in X, branch Y, N dirty files" banner before the first call.
  Done when: running `fm code` in a subfolder, a non-git folder and an unregistered folder each prints a one-line banner naming the root it resolved to, with a test for the three cases.

- **Make Enter cancel-safe: Ctrl-C always returns a summary and leaves no processes** — FIX — value 5 — effort M — risk med — category: reliability
  Why: the planner "kept running orphaned" after quit. T-1326 kills children; the unspoken need is confidence afterwards, i.e. a post-quit receipt "stopped 3 processes, 0 left, tree clean/dirty".
  Done when: after killing the TUI mid-run, `ps` shows zero descendants and the next `fm code` start prints what was left half-done (dirty files, open task) with a resume/discard choice.

- **Show the money before it burns: a startup-tax estimate per runner, per project** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: 66k–133k input tokens per planner call is invisible to the user until it hurts; each plugin and hook adds to it. Estimate from the last measured call per (runner, project) and show it in the runner picker.
  Done when: the picker lists "~N tokens to start" for each runner from recorded history, and a runner with no history says "unmeasured" rather than a guess.

- **Turn the user's complaint into the next task automatically (friction receipt)** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: the user said twice "I shouldn't even need to ask". Their phrases ("just isn't doing anything", "why can't I…") are listed as triggers but nothing shows a receipt. Assumption: detection exists only as a captured task (not built).
  Done when: a prompt containing a friction phrase creates a task tagged `friction` with the quoted phrase and the area, a test feeds the three phrases from the pack, and `fm` lists the receipt at the next session start.

- **Keep a "standing permission" record so release and push never ask again** — FEATURE — value 4 — effort S — risk med — category: autonomy
  Why: the user pushed back three times ("stop asking me if you can release", "full permission", "full auto"). Assumption: this is remembered only in conversation, and the publish-grant message still points at a permission prompt.
  Done when: a durable `standing grants` entry (scoped to this repo, with expiry and a revoke command) makes `fm release --push` proceed without a prompt, and `fm grants` lists it; the guard's other refusals are unchanged.

- **Put a "did you mean this project?" resolver on the home screen** — FEATURE — value 3 — effort M — risk low — category: multi-project
  Why: multi-project is asked for; typing "fix nixie's login" should pick the project. Distinct from the listed cross-project ideas in that it ranks by name, recent activity and git remote, and asks only when two tie.
  Done when: typing a request naming a known project on the home screen preselects it, and an ambiguous name shows two candidates; tested with three fixture projects.

- **Export a one-paste bug report for Foreman's own failures** — FEATURE — value 4 — effort S — risk low — category: support
  Why: the user reports problems in prose ("why can't I launch…"); Foreman then has to rediscover context. A bundle (versions, runner probe, last 50 events, config provenance, secrets scrubbed) lets the friction round start informed.
  Done when: `fm code report` prints a scrubbed bundle under 200 lines, and a test plants a fake API key in config and proves it is absent.

- **Wild: Let Foreman say "I'm stuck" in your own notifications, with the fix attached** — FEATURE — value 3 — effort M — risk med — category: attention — wild
  Why: assumption: the user walks away during long runs; the nixie silence went unnoticed or unexplained. A desktop notification (off by default) says "nixie run quiet 4 min: planner is loading 120k tokens. [Lean profile] [Wait]".
  Done when: with the setting on, a simulated 4-minute silence triggers one `notify-send` call with the diagnosis text; with it off, none.

- **Wild: Adopt the Claude Code session you're already in** — FEATURE — value 4 — effort L — risk high — category: handoff — wild
  Why: the user lives in Claude Code and treats fm as a plugin and as an app; no path moves work between them. "take this to fm code" would pass the queue, task and transcript summary.
  Done when: a command run inside a Claude session creates an fm code run carrying that session's open task and last request, and the TUI shows it as "adopted".

- **Wild: A "second opinion" button that sends the stuck step to another runner** — FEATURE — value 3 — effort M — risk med — category: runners — wild
  Why: with any CLI manageable, a stuck or failing step could be retried on a different runner in one keypress without losing checks.
  Done when: pressing the key on a failed step re-runs only that step on the chosen runner, with the same guard verdicts, and records which runner passed.

- **Make duplicate-Foreman detection a visible fact, not just a silent fix** — FIX — value 4 — effort S — risk low — category: plugin hygiene
  Why: the user asked to "prevent duplicate things when FM is installed as a claude plugin". T-1327 strips context from nested sessions, but a user who installs the plugin and also runs the app will still ask which one is active.
  Done when: `fm doctor` and the TUI header print "Foreman: one owner (<path>, version)" or list two installs with versions and the one that wins, tested with two fake install paths.

- **Record each friction-free first run as a regression fixture** — CLEAN — value 3 — effort M — risk low — category: testing
  Why: the pack's complaints (fm not in PATH, bare `fm code` errors, no-model failure) were all first-five-minute failures found by the user, not CI. Replaying them in a clean HOME in CI stops a repeat.
  Done when: a CI job with an empty HOME and PATH lacking `fm` runs `fm code` in a pty, reaches the home screen and gets an answer to a question request using a fake runner.
