# Brainstorm — lens: bold bets

- **Preflight every runner before its first real call** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the nixie run sat silent while each planner call carried 66k–133k input tokens from a nested Claude loading every plugin and hook; nothing measured or warned about it.
  Done when: `fm code doctor` sends a one-token prompt through each discovered runner and prints latency, input tokens and an ok/slow/over-budget verdict, and a test with a fake CLI that emits 100k tokens gets "over budget" with the lean-mode fix named.

- **Add a silence watchdog that diagnoses and acts** — FEATURE — value 5 — effort M — risk med — category: observability
  Why: "it just isn't doing anything" was the complaint. T-1329 adds a heartbeat but doesn't say why a run is quiet or do anything about it.
  Done when: a fake runner that prints nothing for N seconds makes the run state "quiet: planner waiting 94s, 0 bytes, child pid alive", then restarts it once in lean mode, and the event log records both steps.

- **Detect duplicate Foreman installs and name the live one** — FIX — value 4 — effort S — risk low — category: setup
  Why: the user asked for "no duplicate things when FM is installed as a claude plugin"; the pack shows a plugin copy, a `~/.local/bin` link, and a nested Claude that would load its own Foreman. assumption: the plugin cache can hold a different version from the CLI on PATH.
  Done when: `fm doctor` lists every Foreman copy found (PATH, plugin cache, marketplace) with versions, flags a mismatch, and a nested worker run shows exactly one set of hooks firing in a test.

- **Route tasks to the cheapest runner that has passed that kind** — FEATURE — value 5 — effort L — risk med — category: runners
  Why: `fm code bench` already grades models and CLIs on seeded tasks, but nothing uses the grades. "Manage ANY CLI/model" needs a choice rule, not a picker.
  Done when: with bench grades for a local model and claude, a `docs` task goes to the local model, and a forced failure escalates to claude, with the reason in the run log.

- **Run a supervisor daemon so the TUI is only a client** — FEATURE — value 4 — effort L — risk high — category: architecture
  Why: stopping the TUI currently kills the CLIs (T-1326), and runs can't continue across projects unattended. The user wants full-auto and "don't stop until complete". assumption: the event log can be the only interface between daemon and viewers.
  Done when: `fm code serve` runs a queued task, the TUI is closed and reopened, and the reopened TUI shows the same live run with no restart; `fm code stop` still kills the children.

- **Reap orphans and offer to resume interrupted runs** — FIX — value 4 — effort M — risk low — category: reliability
  Why: after the user quit, the planner kept running orphaned; T-1326 stops this going forward but doesn't clean up what's already left behind.
  Done when: after `kill -9` on a run, the next `fm code` finds the stale process group and kills it, and the home screen lists "interrupted in nixie, step 3: resume / discard".

- **Teach Foreman an unknown CLI by probing it** — FEATURE — value 4 — effort M — risk med — category: runners
  Why: the user said "ANY CLI", and the `CMD {prompt}` template needs hand-writing. assumption: most CLIs have a recognizable non-interactive flag in `--help`.
  Done when: `fm code runner add <cmd>` reads `--help`, tries candidate invocations on a canary task in a scratch directory, and saves the first template that makes a harness-judged edit, with a test against a stub CLI.

- **Show effective config and where each value came from** — FEATURE — value 4 — effort S — risk low — category: config
  Why: "better config/setup" is in the request, and config is now spread over `models.json`, task settings and the runner default.
  Done when: `fm code config` prints each setting with its value and source (default / global / project / env / flag), and `fm code config --fix` rewrites an invalid line with the validator's message.

- **Wild: Offer fm code as an MCP tool that other agents call** — FEATURE — value 4 — effort L — risk med — category: integration — wild
  Why: assumption: Claude Code, Codex and others can call MCP tools, so a harness-proved "do this small change, checked" call lets a big agent delegate to a cheap local model.
  Done when: Claude Code calls the `foreman_code` tool with a request and gets back a commit id plus the passed checks, in an end-to-end test.

- **Wild: Race two runners in worktrees and keep the first green** — FEATURE — value 3 — effort L — risk med — category: runners — wild
  Why: the harness already judges every turn with checks that fail first, so "which runner wins" is mechanical and needs no model opinion.
  Done when: `fm code --race claude,codex "…"` runs both in separate worktrees, merges the first whose checks pass, kills the other, and prints a time/cost comparison.

- **Wild: Let Foreman dogfood itself nightly across all runners** — FEATURE — value 4 — effort M — risk med — category: self-improvement — wild
  Why: the user wants Foreman to notice what needs improving without being asked; the 7/7 request-kind runs only happened once by hand.
  Done when: a scheduled job runs the seven request kinds on each installed runner in scratch repos and files a task with the failing frame/log for any kind that regressed, and a seeded regression produces that task.

- **Wild: Open the home screen on "what needs you", ranked across projects** — FEATURE — value 4 — effort M — risk low — category: user value — wild
  Why: T-1330 lists queue/inbox/blocked per project; with many projects the user wants one ordered answer ("approve publish in foreman; nixie's planner is stuck"), not tables.
  Done when: with three seeded projects in different states, `fm code` opens with a ranked list whose first item is the blocked one, and pressing Enter jumps into that project's run.
