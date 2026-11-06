# Brainstorm — lens: grid

- **Add a shell `command_not_found` hook that files a gap** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Cell: CLI × user × missing. Why: assumption: the user's own terminal hits "command not found" far more often than the agent logs it, and none of the existing gap records see those moments. The hook (bash/zsh/fish, opt-in, installed by `install.sh`) prints one line, "Sampo can find or build this: `sampo need NAME`", and writes a gap record only after a local check shows the name isn't a typo.
  Done when: typing an unknown command in a test shell prints the hint and appends exactly one gap row; `SAMPO_NOHOOK=1` produces nothing.

- **Expose `need(capability)` as one MCP tool any harness can call** — FEATURE — value 5 — effort M — risk med — category: interop
  Cell: other agents × missing. Why: the shelf and manifest are host-neutral on paper, but the pack shows no entry point that Codex, Gemini or opencode can call when they hit a gap. The tool returns one of three answers: a ready tool path with its passport, a queued build ticket, or a grant request card.
  Done when: a scripted MCP client with no Sampo hooks asks for a capability on the shelf and gets the path and passport; for an unknown one it gets a ticket id.

- **Strip project detail from outbound tool searches** — SECURITY — value 4 — effort M — risk low — category: privacy
  Cell: unattended × any × unsafe (privacy). Why: searching GitHub, registries or MCP directories with raw error strings, file names or package names leaks the user's project. Searches should be rewritten into generic capability terms by a local model or a rule table, with the sent query logged, and a "local index only" setting.
  Done when: a seeded private token in a gap never appears in a recorded outbound query in the test harness, and the egress log lists each sent query.

- **Diff a tool's declared egress against a static scan of its source** — SECURITY — value 4 — effort S — risk low — category: safety
  Cell: agent × forged tool × unsafe. Why: the passport lists what a tool may touch, but nothing in the pack checks the code against it. Quarantine greps for sockets, URLs, `subprocess` and env reads, and fails the promotion if any exceed the declared set.
  Done when: a fixture tool with an undeclared `urllib` call fails quarantine with the offending line quoted.

- **Guard against shelf names that shadow system binaries** — FIX — value 4 — effort S — risk low — category: safety
  Cell: agent × CLI × wrong. Why: a forged tool called `ls2` is harmless but one called `rg` or `jq` earlier on PATH changes what every later command means. Shelf tools live in a namespaced dir (`sampo tool NAME`), and any bare PATH exposure is refused when the name collides with an existing binary.
  Done when: forging a tool named after an installed binary is rejected, and the shelf dir never precedes system dirs in PATH.

- **Import golden outputs recorded on another machine as the oracle for a stdlib clone** — FEATURE — value 3 — effort M — risk med — category: correctness
  Cell: unattended × forged tool × wrong. Why: a stdlib stand-in for a missing tool (the shellcheck case in the dropped list) passes its own tests while being wrong. The user may own a machine that does have the real tool, and Sampo installs nothing. A data-only corpus of inputs and expected outputs, recorded there once and copied over, gives an independent judge. Assumption: such a machine exists for at least some tools.
  Done when: a clone is scored against an imported corpus, and a deliberately wrong clone scores visibly lower.

- **Put the shelf lookup under the hook latency bench** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Cell: hook × agent × slow. Why: the "resolve a tool before a Bash call" ideas add work to a path that `bench_hooks.py` already guards, and the pack doesn't show the shelf lookup being measured there. The shelf gets a flat index file read lazily, a p95 budget row in the bench, and a failing gate if it is exceeded.
  Done when: `bench_hooks.py` prints a shelf-lookup row, and inflating the shelf to 5,000 entries stays within budget.

- **Approve a grant from the phone with a reply code tied to the manifest hash** — FEATURE — value 3 — effort M — risk med — category: devices
  Cell: unattended × user × slow. Why: queued install grants stall overnight work until the user sits at the terminal. A push or mail message carries the one-screen grant card and a code derived from the manifest hash, so a reply can only approve exactly what was shown. Assumption: the user already has some push channel; the setting is opt-in and local-network or self-hosted only.
  Done when: a reply with the right code releases the grant for that manifest, a stale or wrong code does nothing, and any edit to the manifest invalidates the code.

- **Add a `/need` command to the Smith TUI** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Cell: Smith TUI × user × unclear. Why: the user's first-time path to the tool shelf is unclear on that surface. The user types a plain-language need and gets the ladder (find, build stdlib-only, ask a grant) with a one-line cost estimate before anything runs.
  Done when: `/need "convert svg to png"` in a TUI test run prints the three rungs and the estimate and takes no action until confirmed.

- **Wild: Teach a tool by doing it once.** — FEATURE — value 4 — effort L — risk med — category: developer experience
  Cell: CLI × user × missing. Why (wild): the user does the task by hand under `sampo teach start` and `stop`. Sampo records commands and outputs and forges a script from them. It verifies by replaying against a scratch copy and asking the user for the failing case before it is shelved. The demonstration becomes the spec and the test, so the small model has less to guess.
  Done when: a recorded 3-step session produces a tool whose replay matches the recorded outputs, and an altered input gives a clear failure.

- **Wild: Chaos-remove a binary and see whether the agent notices.** — FEATURE — value 3 — effort M — risk low — category: gap detection
  Cell: unattended × agent × unclear. Why (wild): the long-horizon tier plants faults, but none removes a tool the task needs. A nightly lane hides one binary (via a PATH shim, never touching the install) and the pass condition is that the gap is logged, a rung is chosen and the task still finishes. This measures gap detection with no real breakage.
  Done when: a scenario with `jq` hidden produces a gap record and a completed task; one with silent failure fails the scenario.

- **Wild: A tool shelf page with a seven-second cast per tool.** — FEATURE — value 3 — effort M — risk low — category: web UI, site
  Cell: web UI × user × unclear. Why (wild): the forged tools' value is invisible to the user unless something shows what each one replaced. Each shelf entry gets a replayable terminal cast recorded from its own test, "last used" and "calls saved", and a retire button, all from data the quarantine test already produces.
  Done when: the web UI shelf page renders a cast for every shelved tool without running the tool, and a tool without a cast shows "unproven".

Cells left empty: site × other agents, because the site is read-only for them and the MCP tool covers the real need; Smith TUI × unattended, because the TUI isn't a surface for unattended runs; "slow" for the user at the CLI, because the existing batching ideas already cover it; "unsafe" for the user at the web UI, because grants already have a card with a world-diff.

Next question: which gaps does the user hit in their own terminal, outside any agent session, and does the ledger see them at all?
Next question: when a grant is refused or ignored for a week, does the gap close, recur, or get quietly worked around, and what should the shelf do in each case?
