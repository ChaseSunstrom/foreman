# Brainstorm — lens: bold bets

- **Make fm code a persistent supervisor daemon with the TUI as a thin client** — FEATURE — value 5 — effort L — risk med — category: architecture
  Why: the user's nixie run "isn't doing anything" and quitting orphaned the planner; T-1326 patches kills, but a daemon owning runs (process group per run, journal, lease table) makes closing the terminal, SSH drops and the lid irrelevant. Assumption: Unix socket under foreman_home is acceptable.
  Done when: start a run, kill the TUI with SIGKILL, reopen `fm code`: the run is still progressing and the TUI reattaches to its live event stream; `fm code stop` leaves zero child processes.

- **Add a runner "audition" that races all detected CLIs on a user's real repo and writes a routing table** — FEATURE — value 5 — effort L — risk med — category: routing
  Why: user wants ANY CLI/model managed; T-1328 only finds runners. Bench exists (`fm code bench`) but isn't tied to the user's own repo or to per-kind routing. Assumption: a throwaway worktree plus a spend cap makes this safe.
  Done when: `fm code audition` runs a seeded fix/feature/question on each detected runner in a worktree, prints a pass/cost/time table, and subsequent runs of each request kind pick the winner, with the reason shown.

- **Detect and collapse duplicate Foreman by a lineage marker in the process environment** — FIX — value 5 — effort M — risk low — category: dedupe
  Why: user explicitly asked "no duplicate Foreman when it runs Claude Code as a worker"; the 66k–133k token startup tax comes from nested plugin/hook/rule loading. Assumption: an env var like FM_PARENT_RUN set by fm code is inherited by the worker.
  Done when: a worker Claude started by fm code, with the plugin installed, loads zero Foreman hooks/rules (asserted from its stream-json init event), and a bare nested `fm` call reports "inside run R-x" instead of starting a second harness.

- **Run a silence watchdog that classifies why a run is quiet and acts** — FIX — value 5 — effort M — risk low — category: reliability
  Why: "just isn't doing anything" for minutes; no visible progress from the planner. T-1329 adds heartbeat but not diagnosis. Assumption: process state (CPU, children, open sockets, last stream byte) is readable from /proc and ps on macOS.
  Done when: with a fake runner that hangs, a rate-limited runner and a runner loading 100k tokens of context, each yields a distinct named line within 15s ("waiting on API 429", "loading plugins", "no output, process idle"), and the third offers a slim-profile retry.

- **Make friction detection a built-in hook that opens a brainstorm task with a receipt** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: user said twice they shouldn't have to ask; an open ask (the "notices on its own" request) already exists but isn't shown delivered. Assumption: the existing intake hook sees user prompts.
  Done when: feeding the prompt "it just isn't doing anything" in a session with a fm code area produces a captured task and a one-line receipt "friction → brainstorm T-xxxx", and unrelated prompts produce none (tested over a corpus of 30 phrases).

- **Ship an MCP/ACP server so Claude Code, Zed and Cursor can call fm code as a tool** — FEATURE — value 4 — effort L — risk med — category: integration
  Why: user wants fm code to manage everything and also coexist as a Claude plugin; being callable removes the duplicate problem by making Foreman the one harness. Assumption: stdlib JSON-RPC over stdio is enough.
  Done when: a scripted MCP client lists tools, calls `fm_code_run` with a request in a temp repo, and receives a streamed result with the closed task id and proof summary.

- **Add a cross-project scheduler with runner quotas, fairness and fallback on classified failure** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: multiple projects is a stated goal; T-1330 only runs one chosen task. Overnight queues across projects need rate-limit awareness. Assumption: failures can be classified (429, auth, crash, timeout) from runner output.
  Done when: with 3 projects queued and a fake runner returning 429 for the first, the scheduler moves to the fallback runner, never exceeds the per-runner concurrency cap, and the morning digest lists every outcome.

- **Wild: Resolve the project and runner from a sentence typed on the home screen** — FEATURE — value 4 — effort M — risk med — category: UX
  Why: assumption: home screen lists projects; "fix the flaky test in nixie" should need no `cd`. wild
  Done when: typing that sentence on a home screen with two projects previews "nixie · claude · fix" and Enter starts the run in the nixie directory.

- **Wild: Adopt a live interactive Claude Code session into fm code through a pty** — FEATURE — value 3 — effort L — risk high — category: supervision
  Why: assumption: users start in plain Claude and want the discipline mid-session. wild
  Done when: `fm code adopt` attached to a pty-run CLI shows its tool calls as stations in the TUI and a guard refusal is injected into that session.

- **Wild: Nightly self-dogfood canary that runs every request kind on every runner and files regressions** — TEST-as-FEATURE (FEATURE) — value 4 — effort M — risk low — category: quality
  Why: only 7/7 for claude; T-0336 live-verify on codex/gemini/opencode is blocked; this makes that continuous. wild
  Done when: a scheduled `fm code canary` produces a matrix, and a deliberately broken fake runner opens a task naming the runner and kind.

- **Add a one-line `fm code why` plus a shareable diagnostic bundle** — FEATURE — value 4 — effort S — risk low — category: support
  Why: first-minute failures (fm not on PATH, nixie stall) were found by hand; a single command answering "is it doing anything and what's installed" cuts that. Assumption: events log and process list are enough.
  Done when: on a hung fake run, `fm code why` prints runner, last event age, child processes and a recommended action in under 2s; the bundle contains no secrets (tested with a planted key).

- **Layer config as global, project and env with `fm code config explain` and last-good fallback** — FEATURE — value 4 — effort M — risk low — category: config
  Why: user asked for better config/setup; models.json is resolved in two places. Assumption: TOML-like or JSON stdlib parsing.
  Done when: `fm code config explain default_runner` prints the winning value and its source file:line; a corrupt project file falls back to last-good with a visible warning.
