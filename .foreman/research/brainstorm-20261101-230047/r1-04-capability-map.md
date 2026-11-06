# Brainstorm — lens: capability map

- **Declare every trigger in one registry file** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: the pack shows `fm night` ticks, `fm triggers` (capture grouping) and `fm ci-watch` as three separate mechanisms. Assumption: no common envelope for event, condition, action, budget and reversibility class exists yet.
  Done when: `fm triggers list` shows the night tick and ci-watch as registry rows, each with its last fire, budget and action class.

- **Catch up missed schedules** — FEATURE — value 4 — effort S — risk low — category: schedules
  Why: the timers the user installed are the main schedule path. Assumption: nothing replays a run missed while the laptop was asleep (anacron or `Persistent=true` behaviour).
  Done when: with the machine off across a scheduled slot, the next boot runs the job once, and `fm triggers history` marks it "catch-up".

- **Render one trigger spec to systemd, launchd and Task Scheduler** — FEATURE — value 4 — effort M — risk med — category: installs
  Why: the mission says "installs (timers, units) queued for one yes". The pack lists a grant queue but only a Linux timer. Assumption: other platforms are unsupported.
  Done when: one spec renders a `.timer`/`.service` pair and a launchd plist, and `fm install --diff` shows the exact files before the one yes.

- **Watch issues and drafts into the capture inbox** — FEATURE — value 5 — effort M — risk med — category: issue watcher
  Why: the mission names issue watchers, and `fm ci-watch` exists but no issue equivalent is shown. Issue text must be fenced as untrusted input.
  Done when: a new issue labelled `fm` appears as a capture with its text fenced, and an injected instruction inside it does not change the lane brief in a test.

- **Fire on file and git events with debounce and idempotency keys** — FEATURE — value 4 — effort M — risk med — category: file triggers
  Why: the mission names file triggers. Examples: a lockfile change starts a dependency audit, and post-merge starts a docs-drift check. Assumption: the only event source today is the clock plus CI.
  Done when: ten rapid saves of a watched file produce one lane, and replaying the same event id fires nothing.

- **Watch dependency and advisory feeds for the repo's lockfiles** — FEATURE — value 4 — effort M — risk low — category: watchers
  Why: Renovate, Dependabot and OSV scanning are the standard in this space. The pack shows supply-chain items only as deferred (T-0791).
  Done when: a planted vulnerable pin in a fixture repo produces a queued fix lane with the advisory id.

- **Resume parked lanes when the usage window reopens** — FEATURE — value 5 — effort S — risk low — category: resume
  Why: the steers say real usage limits are waited out and resumed where stopped (2026-11-01). Assumption: the resume is a session-time behaviour, not a trigger.
  Done when: a lane stopped by a simulated limit restarts without user input at the reset time and logs "resumed by limit-reset trigger".

- **Dry-run any trigger against its next 7 days** — FEATURE — value 4 — effort S — risk low — category: dry-run
  Why: `fm triggers` has precision numbers but no forecast of what a new trigger would do before the user approves it.
  Done when: `fm triggers plan <id>` lists the fire times and actions for the coming week, and nothing runs.

- **Fire a synthetic event to test a trigger end to end** — FEATURE — value 3 — effort S — risk low — category: testing
  Why: the pack's trigger tests appear to cover the code but not the installed unit. Assumption: no way to exercise the live path without waiting.
  Done when: `fm triggers fire <id> --synthetic` runs the real action in a scratch worktree and reports pass or fail.

- **Ship trigger recipes that are one yes to install** — FEATURE — value 4 — effort M — risk low — category: recipes
  Why: mature tools ship templates (nightly dependency audit, weekly docs drift, stale-branch rebase). The pack's grant queue could carry one card per recipe.
  Done when: `fm triggers recipes` lists at least 5, and accepting one installs its unit and registry row in a single approval.

- **Lease triggers across machines to prevent double fires** — FEATURE — value 3 — effort M — risk med — category: coordination
  Why: assumption: the user has more than one machine (the pack mentions two-machine ideas). Two installed timers could both open the same lane.
  Done when: with two worktrees sharing one remote, a trigger takes a lease ref and the second machine logs "skipped, leased".

- **Chain triggers into conditional flows** — FEATURE — value 3 — effort M — risk med — category: workflows
  Why: n8n, Argo Events and GitHub Actions all let one event's outcome gate the next (red CI on main, then bisect lane, then fix lane). Assumption: only single-step actions exist.
  Done when: a two-step flow runs the second step only if the first fails, with a depth cap enforced in a test.

- **Wild: compile "when X, do Y" sentences into triggers** — FEATURE — value 4 — effort L — risk med — category: natural language
  Why: wild. `fm when "CI fails on main" do "diagnose"` produces a registry row plus the unit, shown as a diff for the one yes.
  Done when: five sample sentences compile to the expected rows, and an ambiguous one asks a single question instead of guessing.

- **Wild: mine the user's repeated manual sequences into proposed triggers** — FEATURE — value 4 — effort M — risk low — category: habits
  Why: wild. The pack keeps the user's "asked" stream and shell habits. A routine like "pull, then run the suite, then check the docs" should be offered as a trigger with its measured precision.
  Done when: a fixture history with a repeated sequence yields a proposal citing its count, and nothing installs without the yes.

- **Wild: wake on silence with a "what is rotting" report** — FEATURE — value 3 — effort S — risk low — category: dead-man
  Why: wild. A dead-man's trigger fires when a repo has had no activity for N days and lists stale branches, red CI and aging deferred tasks (the 28 "Later from T-07xx" bundles).
  Done when: a fixture repo idle past N days produces one digest file, and active repos never get one.
