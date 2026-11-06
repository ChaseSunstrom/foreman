# Brainstorm — lens: capability map

- **Diagnose silent runs and say why** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the nixie run "just isn't doing anything" for minutes with no output, and the planner then kept running orphaned. T-1329 shows progress when a CLI streams, but nothing says why a run is quiet. A watchdog would read the child's process tree, CPU, last stream event and token count, then name one cause (loading plugins, waiting on the API, rate limited, hung tool, dead pid). It would show that cause in the Activity lane and offer a one-key retry on a leaner launch.
  Done when: a fake runner that sleeps 60 s makes `fm code` print "waiting on runner, no events for 20 s, pid alive, cause: …" within 25 s, and a hung one offers retry.

- **Detect duplicate Foreman installs and fix them** — FIX — value 5 — effort M — risk med — category: setup
  Why: the user asked to "prevent duplicate things when FM is installed as a claude plugin", and `fm` was missing from their shell because the plugin lives only inside Claude Code. T-1327 covers nested sessions, not install-time duplication. `fm doctor` would find hooks present both via the plugin and in `settings.json`, several `fm` copies on PATH, and two plugin versions. It would print a one-line `fm doctor --fix` that leaves one owner.
  Done when: a fixture HOME with hooks registered twice makes `fm doctor` report "duplicate hooks" and `--fix` leaves exactly one, checked by a test.

- **Measure and cap the worker launch tax** — PERFORMANCE — value 5 — effort M — risk low — category: performance
  Why: nested Claude calls cost 66k–133k input tokens each because they load every plugin, hook and rule. Each runner gets a lean launch profile (settings sources limited, no plugins, strict MCP config). `fm code bench` and `fm doctor` then report "tokens before the first user word" per runner and fail past a ratchet.
  Done when: `fm code doctor` prints a launch-tax number per runner, and a test fails if the claude worker's number exceeds the pinned budget.

- **Probe every runner into a capability matrix** — FEATURE — value 4 — effort M — risk low — category: runners
  Why: the request is to manage ANY CLI or model, and T-0335/0336/0337 are blocked on unverified codex, gemini and opencode behaviour. `fm code runners --probe` would run a canned micro-task on each runner and record whether it streams, has a plan mode, reports cost, resumes sessions, honors a read-only flag, and how long it took. The result is cached as the runner's profile and drives routing.
  Done when: with two fake CLIs of different abilities, the probe writes a matrix that differs between them, and a worker without a read-only flag is refused as a planner.

- **Layer config with an explainer and a first-run wizard** — FEATURE — value 4 — effort M — risk low — category: config
  Why: the user wants "better config/setup"; `models.json` is resolved at two call sites and a model must be picked by hand with `m`. A single `fm config` would merge flag > env > project > user > default, validate with line-accurate errors, and have `fm config explain KEY` name the winning layer. First launch auto-picks a default from the detected runners and writes nothing without consent.
  Done when: a key set at two layers reports the winner and its file via `explain`, and a bad value fails with file:line.

- **Route steps across runners by role, cost and failure** — FEATURE — value 4 — effort L — risk med — category: routing
  Why: aider-style architect/editor splits and cost routing are standard. The pack shows one runner per run. Plan on a strong model, fill checked JSON slots on a local one, and escalate a step to the stronger runner after two red verifies. On a rate-limit or quota error, fall back to the next runner in the chain. Assumption: the harness already knows which step failed.
  Done when: a scripted run with a failing cheap runner escalates exactly one step to the second runner and the receipt names both.

- **Schedule the cross-project queue with caps and fairness** — FEATURE — value 4 — effort L — risk med — category: multi-project
  Why: T-1330 gives a home screen that can start one run. A real manager also needs a project registry (`fm projects scan/add`), per-project default runner, a global concurrency cap, per-runner rate limits and a dollar budget per night, so "run everything queued" is safe.
  Done when: with 3 projects × 2 tasks and a cap of 2, never more than 2 runs are active and all 6 finish, asserted from the event log.

- **Run each lane in its own git worktree** — FEATURE — value 4 — effort M — risk med — category: isolation
  Why: parallel runs in one project would collide, and the guard and leases already show that shared state is risky. A worktree per run lets two runners work one project, and the result lands as a branch or PR (`gh` if present) only after the checks are green.
  Done when: two concurrent runs on one repo edit the same file path without conflict, and each closes on its own branch.

- **Serve fm code as an editor agent over ACP and MCP** — FEATURE — value 3 — effort L — risk med — category: surfaces
  Why: the surfaces named are only the web UI and the terminal. Speaking the Agent Client Protocol (Zed and similar editors) and exposing `fm_run`, `fm_status` and `fm_queue` as MCP tools would let other CLIs, including Claude Code, delegate to the harness. Assumption: a stdlib JSON-RPC server is small enough.
  Done when: a scripted JSON-RPC client starts a run, receives streamed events and gets the closing receipt.

- **File a task automatically from a stalled or failed run** — FEATURE — value 4 — effort S — risk low — category: self-improvement
  Why: the user said "I shouldn't even need to ask", and the nixie stall only reached Foreman because they complained. A run that hits the watchdog, is killed, or dies on a runner error would capture a redacted run bundle (events, process tree, runner profile) and open a FIX task with it attached.
  Done when: killing a fake hung run creates a task whose body references a bundle containing the last 50 events.

- **Wild: Resolve the project from the request** — FEATURE — value 3 — effort M — risk med — category: multi-project
  Why: wild. Running `fm code "fix the login bug in nixie"` from any directory matches "nixie" against the project registry, shows the chosen path and runner, and starts after one Enter (or a flag to skip). It removes the `cd`, which is the step that went wrong on the nixie run.
  Done when: from `/tmp`, a request naming a registered project resolves to that path, and an ambiguous name lists candidates instead of guessing.

- **Wild: Race two runners on one task and keep the cheaper green one** — FEATURE — value 3 — effort L — risk med — category: runners
  Why: wild. Using the worktrees idea above, run the same task on two runners. The harness lands the first whose checks pass the fail-first and pass-after proofs, ties broken by cost, and logs the loser. Over time this produces real per-runner win rates.
  Done when: with one fake runner that fails and one that passes, the passing one's commit lands and the receipt lists both costs.

- **Wild: Learn the default runner per kind of request** — FEATURE — value 3 — effort M — risk low — category: routing
  Why: wild. Bench grades and past run history already exist as data. The auto-default would stop being "first CLI found" and become "the runner that has closed docs tasks cheapest here", with `fm code why-runner` printing the evidence. Assumption: enough history exists per request kind.
  Done when: seeded history makes `fm code why-runner docs` pick the runner with the best held-rate and print the numbers behind it.
