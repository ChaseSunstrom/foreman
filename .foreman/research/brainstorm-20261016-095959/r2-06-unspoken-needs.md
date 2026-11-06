# Brainstorm — lens: unspoken needs

- **Lint briefs for false premises at capture** — FEATURE — value 5 — effort S — risk low — category: reliability
  Why: Four dropped ideas say "premise false", and T-1208 and the steered note show a criterion naming a test module that doesn't exist. Checking claims before building is the habit the user keeps enforcing by hand. `fm brief lint` would resolve every named file, test module, function and flag, and refuse or flag the brief when one is missing.
  Done when: capturing a brief whose criterion names `test_lease` (which doesn't exist) prints the missing module, and the same brief with `test_claims` passes.

- **Remember dropped and steered ideas at capture** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: The same ideas come back as brainstorm output (deletion briefs, "Later from" parking, regex-compile cost) after the user has rejected them. Capture and brainstorm would match new briefs against dropped ones and demand new evidence before queueing them.
  Done when: capturing a near-duplicate of a dropped brief without `--evidence` is held with the drop reason shown; with evidence it queues.

- **Track a live parity scoreboard against Claude Code** — FEATURE — value 4 — effort M — risk low — category: product
  Why: The ask is "even better than CC", but nothing says when that's true. A checked list of CC capabilities (plan mode, subagents, hooks, MCP, resume, rewind, permissions, IDE, headless) would be marked have, half or lacking by running a probe per row. assumption: a stable capability list can be maintained.
  Done when: `fm code parity` prints each row with a verdict from a probe that ran, and a row flips to "lacking" when its probe is broken.

- **Replay recorded codex, gemini and opencode sessions to unblock the blocked trio** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: T-0335, T-0336 and T-0337 are blocked because those CLIs aren't installed here. Recorded hook payloads and transcripts from their documented protocols would let `fm agents` be tested without live binaries, and stay honest about what is still unverified live.
  Done when: a test replays a recorded codex payload and a gemini AfterAgent payload through the guard and gets the expected allow or deny, and `fm agents status` labels them "replay-verified, not live".

- **Normalise tool names so one guard corpus covers every harness** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: `guard_cases.jsonl` is written in Claude Code's tool vocabulary, while codex, gemini and opencode call shell and edit tools by other names. A normaliser maps each to the guard's names, so every labelled case runs against every worker's payload shape and `fm code` shares it.
  Done when: the same labelled "refuse" case, expressed as a codex shell call and a gemini run_shell_command call, is denied by `fm replay` for both.

- **Let `fm code` borrow the user's existing login through `claude -p`** — FEATURE — value 4 — effort M — risk med — category: provider
  Why: The user already drives lanes with `claude -p`. A provider that wraps the installed CLI, with no API key, makes `fm code` usable on day one. assumption: the user has a subscription rather than API credit, and the terms allow wrapping their own CLI.
  Done when: `fm code --provider claude-cli` completes a fixture task with no `ANTHROPIC_API_KEY` set.

- **Import Claude Code settings in one step** — FEATURE — value 4 — effort S — risk low — category: migration
  Why: Switching harnesses is costly if CLAUDE.md, permissions, hooks and MCP config must be redone. `fm code --import-cc` reads and translates them, and lists what couldn't be mapped. assumption: the user wants an easy way back as well as out.
  Done when: on a fixture with a CLAUDE.md, an MCP entry and an allow rule, `fm code --import-cc` produces the equivalent config and a list of skipped items.

- **Fall back to Claude Code when `fm code` fails a task** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: A new loop will be worse than CC at first, and the user can't afford a queue stalled by it. `--harness auto` would try `fm code`, and on a provider error or a stuck breaker reroute the same brief to a `claude -p` lane with a note.
  Done when: with a fake provider that always errors, the brief finishes through the fallback worker and the ledger records the reroute and the reason.

- **Keep a human-only inbox with copy-paste commands** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: Mission pillar 7 says what only the user can do goes in the final report, and T-0325 and T-0418 wait on a sudo install and a mod update. One inbox page would list each step with the exact command, the check that proves it done, and the task it unblocks, and auto-clear when the check passes.
  Done when: marking `libappindicator` as installed (fake `pacman -Q` succeeds) removes the item and moves T-0325 back into the queue.

- **Show spend and remaining budget before a lane starts** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: The run shows a hard USD budget ($25) and the user prefers the cheapest model that can. Each lane would show an estimate range up front and a running meter, and refuse to start when the estimate exceeds what's left.
  Done when: a lane whose estimate is above the remaining budget is refused with both numbers shown.

- **Wild: Turn Claude Code's release notes into capability-gap briefs** — FEATURE — value 3 — effort M — risk low — category: watch
  Why: "Better than CC" is a moving target. A scheduled job reads CC's changelog and the other CLIs' releases, and captures a brief for each new capability the parity scoreboard marks lacking (wild). assumption: release notes are fetchable, and the user opts in to network access.
  Done when: given a saved changelog fixture, `fm watch` captures one brief per new feature, with none duplicated on a second run.

- **Wild: Publish a live model leaderboard on the GitHub Pages site** — FEATURE — value 3 — effort M — risk low — category: website
  Why: The user asked for a modern Pages site and for small local models to be "super good". Published pass rates per model on Foreman's own task corpus, with the slot profile used, would be the site's strongest proof (wild). assumption: the conformance suite and task corpus exist by then.
  Done when: `fm site build` renders a table from the stored per-model results, and a model with no results shows "not measured" and not a number.

- **Wild: Write a morning digest of what changed overnight** — DELIGHT-style FEATURE — value 3 — effort S — risk low — category: report
  Why: Unattended runs and parallel lanes are central to the mission, but the user returns to ledgers. A one-screen digest would give merged, failed, waiting-on-you and spent, with one-click diffs, in the web UI and as plain text (wild).
  Done when: after a fixture run with one merged, one failed and one blocked task, `fm digest` lists all three with a reason for each and the total spend.
