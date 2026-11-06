# Brainstorm — lens: approaches

- **Run workers in a lean, isolated profile** — PERFORMANCE — value 5 — effort M — risk med — category: workers
  Why: the nixie planner spent 66k–133k input tokens per call because nested Claude Code loads every plugin, Foreman's hooks and its rules. T-1327 only drops Foreman's own context. Giving each worker a throwaway config dir (credentials linked, no other plugins, hooks or MCP servers, only the guard and leases re-added) cuts the whole tax, not just Foreman's share.
  Done when: a test runs one planner call through the lean profile and a default profile on the same fixture and asserts the lean input-token count is under half; `fm code bench` reports tokens per call and fails if it rises.

- **Diagnose stalls and offer a fix** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: "it just isn't doing anything" is the user's actual complaint. T-1329's heartbeat shows the run is alive, but nothing says why it is slow or what to do. When no tool call or token arrives within a deadline, show cause, elapsed time and tokens (for example "planner 3m, 133k in, no output: heavy profile"). Offer one-key retry on the lean profile, a switch of runner, or abort.
  Done when: a fake runner that goes silent triggers the diagnosis after the deadline, and each offered action works in a pty test.

- **Probe each runner before the first real request** — FEATURE — value 4 — effort S — risk low — category: setup
  Why: assumption: a 1-token "reply ok" call costs seconds and tells the user whether a runner works, how slow it is and how many tokens a bare call costs, before minutes of silent planning. This also makes "works with no setup" (T-1328) checkable. Results are cached per runner version.
  Done when: `fm code doctor` prints a latency, token and pass/fail line per detected runner, and a broken runner is skipped by the auto-default with a reason.

- **Reap orphans after a hard kill** — FIX — value 4 — effort M — risk med — category: reliability
  Why: the nixie planner kept running after quit. T-1326 handles clean stop, but `kill -9`, a closed laptop or a crash can't run handlers. Combine a process group per run, `PR_SET_PDEATHSIG` via ctypes on Linux, and a pidfile sweep at the next launch (with a macOS fallback) so the other cases are covered.
  Done when: a test SIGKILLs the parent mid-run and no child is alive within 2 s on Linux; the next launch reaps a stale pidfile's children.

- **Make bare `fm` open the app and `fm setup` fix PATH** — FEATURE — value 4 — effort S — risk low — category: launch
  Why: `fm` wasn't a command in the user's shell and needed a manual ~/.local/bin link. They want to launch it "like claude". Doing less is a valid approach: `fm` with no args opens the same home screen as `fm code`, and `fm setup` creates the link, checks PATH, and prints the one line to add if needed.
  Done when: in a clean HOME, `fm setup` followed by `command -v fm` succeeds, and a pty test of bare `fm` shows the home screen.

- **Show where every config value came from** — FEATURE — value 4 — effort S — risk low — category: config
  Why: "better config/setup" is asked, and models.json is already read in two places. One `fm code config` command prints the effective runner, model and default with its source (env, project, user, auto-detected) and flags unknown keys.
  Done when: setting a value at two layers prints the winning layer, and a typo'd key reports its line.

- **Schedule runs across projects with runner quotas and fallback** — FEATURE — value 4 — effort L — risk med — category: scheduler
  Why: assumption: with many projects and many CLIs, rate limits and costs differ. The scheduler caps concurrent runs per runner, and on a limit error or timeout it moves a queued task to the next runner that passes the probe. T-1330 runs a task but doesn't choose where.
  Done when: with two fake runners, one returning 429, three queued tasks across two projects all close, and the log names the fallback.

- **Run a nightly canary of the request kinds on every runner** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the user wants Foreman to notice problems without being asked. It already has 7 request kinds proved on the claude CLI and a bench. A scheduled canary runs them on each detected runner and files a task when pass rate, tokens or time regress. That turns "it isn't doing anything" into a task before the user sees it.
  Done when: an injected slowdown in a fake runner produces a filed task naming the runner and the metric.

- **Expose the harness as an MCP server** — FEATURE — value 3 — effort M — risk med — category: integration
  Why: a different approach to "any CLI": instead of Foreman wrapping each CLI, any MCP-capable CLI calls tools such as `fm_plan`, `fm_check` and `fm_close` and gets the discipline from inside. This also sidesteps the duplicate-Foreman problem. Trade-off: the model drives, so the harness enforces less. Assumption: the target CLIs support MCP.
  Done when: a stdio client lists the tools and walks a fake task from plan to close with the guard still refusing a banned command.

- **Discover projects on its own** — FEATURE — value 3 — effort S — risk low — category: projects
  Why: the home screen (T-1330) needs a project list. Scanning ~/projects, recent git roots and Foreman state folders means there is nothing to register. Local only, and a project can be hidden.
  Done when: in a temp HOME with three repos (one with Foreman state), the home screen lists them without any config.

- **Learn a runner from its own `--help`** — FEATURE — value 4 — effort M — risk med — category: runners — wild
  Why: assumption: unknown CLIs appear faster than adapters get written. Parse `--help` for a non-interactive flag and output format, build a `CMD {prompt}` template, and keep it only if the probe passes. Trade-off: it only covers CLIs with sane flags.
  Done when: a fake CLI with a non-obvious prompt flag gets a working template with no adapter code.

- **Race two runners on the plan and keep the better one** — FEATURE — value 3 — effort L — risk med — category: quality — wild
  Why: the harness already checks plans against fail-first criteria. Two runners in separate worktrees each produce a plan, the harness scores them (criteria verifiable, steps small), and only the winner executes. Trade-off: it doubles planning cost, so it is opt-in.
  Done when: two fake planners, one with an unverifiable criterion, always lose to the other, and the choice is logged.

- **Supervise a human-driven interactive CLI through a pty** — FEATURE — value 3 — effort L — risk high — category: workers — wild
  Why: assumption: some CLIs have no headless mode. Foreman sits on a pty, lets the human type, and applies the guard and checks to each turn's file changes. This reaches any CLI at all. Trade-off: the screen scraping is brittle.
  Done when: a scripted pty fake CLI edits a file the guard refuses, and Foreman reverts it and notes it.

- **Speak Agent Client Protocol to agent CLIs** — FEATURE — value 3 — effort L — risk high — category: runners
  Why: assumption: ACP is the emerging standard for driving agents with structured events. One client could replace several per-CLI adapters and give live progress for free. Trade-off: not every CLI speaks it yet, so the adapters stay as fallback.
  Done when: a fake ACP server streams events into Activity, and an `fm code` run closes against it.
