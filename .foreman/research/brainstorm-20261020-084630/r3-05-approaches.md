# Brainstorm — lens: approaches

- **Make the native todo list the step ledger** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: Long sessions cost about 60% more ($0.095 vs $0.059) because bookkeeping calls and hook notes grow the context faster. Claude already calls TodoWrite on its own, and Foreman asks for a second set of `fm task step` calls. A PostToolUse hook could mirror TodoWrite updates into steps. Assumption: the todo payload is stable and readable in the hook input.
  Done when: a recorded session closes three steps with zero `fm task step` calls, the ledger shows them done, and the long-session bench shows fewer tool calls than the current build.

- **Pre-register each benchmark before it runs** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: The user insists that every claim is measured. They also steered "published whichever way it falls." Committing the case list, model, run count, metric and cap as a hash before a run makes that rule checkable. The results file then records any deviations.
  Done when: `fm bench publish` refuses a results file whose plan hash is missing from an earlier commit, and a deliberate deviation shows on the Benchmarks page as "deviated: <field>".

- **Audit a freshly cloned repo's own Claude config before trusting it** — SECURITY — value 4 — effort M — risk med — category: repo trust
  Why: Foreman runs in bypass mode, and its guard sees Bash commands. A repo's own `.claude/settings.json` hooks, MCP servers, skills and CLAUDE.md can run code or steer the model before the guard matters. The pack shows no scan of these. Assumption: nothing like it exists yet.
  Done when: a fixture repo with a malicious SessionStart hook and a `curl | sh` MCP command is flagged at the first prompt with the file and line, and a clean repo prints nothing.

- **Seal the guard's own wiring** — SECURITY — value 4 — effort S — risk low — category: guard integrity
  Why: Bypass mode with a guard hook means editing `hooks.json`, settings or the guard files is the cheapest way around it. Assumption: some of this is already refused, but the pack shows no per-prompt check of the registration itself.
  Done when: a test that edits the hook registration is refused. A tampered install makes the next prompt print one red line, and `fm doctor` names the changed file.

- **Expose the guard and done-gate as Agent SDK hook callbacks** — FEATURE — value 4 — effort M — risk med — category: surfaces
  Why: The safety result (20 of 24 stopped, 0 of 25 everyday blocked) is Foreman's strongest claim, but it only reaches people who install the whole plugin. SDK apps and `claude -p` pipelines could take it as a few lines of code. This builds on the "extract the guard" and "fm code SDK" ideas but targets Claude's own SDK users.
  Done when: a 10-line SDK script passes `fm guard` as a PreToolUse callback and the 24-command corpus gives the same verdicts as the plugin.

- **Derive the pane palette from the terminal's real background** — FIX — value 3 — effort S — risk low — category: ui
  Why: T-1217: Claude Code paints the docked pane #262626 and Foreman guesses at it. Querying OSC 11 at start (falling back to COLORFGBG) and computing contrast from the answer removes the guess and also fixes light terminals.
  Done when: the pane test with a faked OSC 11 reply of #262626 emits no background escape of its own, and a light reply passes a contrast-ratio check.

- **Backfill a task from a plain session already in flight** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: Users enable Foreman mid-session ("continue, super improve foreman"), and the first-task logic assumes a fresh one-request session. Reading the transcript tail to build a task, criteria and what's already proven gives them the discipline without restarting.
  Done when: `fm adopt --session` on a recorded 30-turn transcript creates one task whose request text matches the last user ask and lists files already edited.

- **Generate pane, web UI and site styles from one token file** — CLEAN — value 3 — effort M — risk low — category: design system
  Why: T-1244 (theme applied after load), T-1217 (pane background) and the "text outside its boxes" report come from three separately hand-styled surfaces. A single `tokens.json` could generate CSS variables and an ANSI palette, and CI could check contrast.
  Done when: changing one token alters the pane, web UI and site, and a CI check fails on any pair below 4.5:1 contrast.

- **Ship hook code as a zipapp run with `python -S -I`** — PERFORMANCE — value 3 — effort M — risk med — category: hook latency
  Why: `bench_hooks.py` gates hook time, and `plugin/lib` has 74 files imported on every hook. Assumption: import and path-scan cost is a measurable share of hook time.
  Done when: `bench_hooks.py --runs 20` p50 drops at least 20% on a cold HOME, and the zipapp is rebuilt automatically by the release step.

- **Run every `fm <verb> --help` example in CI** — CLEAN — value 2 — effort S — risk low — category: developer experience
  Why: Tiers and aliases keep changing (HELP_TIERS conflicts, guessed verbs). Stale help is only caught when a user hits it. Assumption: help text includes runnable example lines.
  Done when: CI executes each example in a scratch repo and fails with the verb and line for any non-zero exit.

- **Wild: Run the real guard in the visitor's browser** — FEATURE — value 4 — effort M — risk low — category: site
  Why: wild. "Every claim must be measured" is stronger if the reader can reproduce it. Pyodide would run the actual guard module on the Benchmarks page with the 24 dangerous and 25 everyday commands as clickable presets and free-text input. Assumption: the guard is pure stdlib Python.
  Done when: the page shows the same 20/24 and 0/25 as `fm guard try` over the corpus, with no network call after load.

- **Wild: Score your own session in the browser** — FEATURE — value 4 — effort L — risk med — category: trust
  Why: wild. A visitor drops a Claude Code transcript onto the page. In-browser code reports compaction count, tool calls and tokens spent on bookkeeping, plus which commands the guard would have stopped. The transcript never leaves the machine, which fits the local-first constraint and shows value without a benchmark.
  Done when: a fixture transcript gives the same numbers in the page as `fm usage` does, and the browser's network log shows no upload.

- **Wild: Give approvals a physical key** — FEATURE — value 2 — effort M — risk high — category: devices
  Why: wild. `fm ask` approvals are bound to the asking Claude Code process so nothing can self-grant them. A USB macro pad or Stream Deck could approve through an authenticated local socket and give the same assurance as a keypress. Risk: it must never be reachable by the agent.
  Done when: a fake key device approves a pending ask, and the same request from a process the agent can spawn is refused.
