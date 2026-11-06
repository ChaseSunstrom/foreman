# Brainstorm — lens: simplicity

- **Claim tasks by atomic rename, not leases** — CLEAN — value 4 — effort M — risk med — category: state
  Why: the 1.2.44 "worker leases fixed" commit and the cross-project home screen (several app instances over many projects) both depend on locks. A task is a file, and moving it between `queue/`, `active/` and `done/` with `os.rename` is the claim, so there is no lease file, heartbeat or stale-owner recovery. Assumption: all state is on one filesystem.
  Done when: two processes race `fm code --task T-x`, exactly one wins, and `kill -9` on the winner leaves the file in `active/` with a mtime-based reclaim that a test exercises.

- **Feed every runner consumer from one probe result** — CLEAN — value 4 — effort S — risk low — category: runners
  Why: runner detection serves `fm code runners`, the home screen, `fm code bench`, `fm doctor` and the "no setup" default. Assumption: these call sites have drifted, since each was added in a separate task. One cached `probe()` returns a list of dicts, and each surface renders that list.
  Done when: grep finds a single function that spawns `--version` or `--help` on a runner CLI, and adding a fake runner to `$FOREMAN_HOME/code.toml` appears in all four surfaces in one test.

- **Make a run a directory of three files** — FEATURE — value 5 — effort M — risk low — category: run state
  Why: the round-1 slate lists durable runs, reopen, follow-ups, undo, PR, hand-off and `fm code why` as separate briefs. Each is a view of the same `plan.json` + `events.jsonl` + `result.json`. Build the directory contract first and the seven features become small readers. Assumption: the existing `--events FILE` replay format can be extended without breaking T-1363.
  Done when: `fm code why RUN` and `fm code --resume RUN` both work from the directory alone, with the original process killed and the TUI never started.

- **Accept one upstream shape: a folder with a markdown file** — FEATURE — value 5 — effort M — risk med — category: integration
  Why: the six repos are skills (SKILL.md), plugins (command/agent markdown plus hooks), cookbook patterns, and a tutorial. The first three share markdown with frontmatter, and the tutorial and cookbook are reading material. One loader parses the frontmatter and passes the body through unexecuted, and anything with a script goes through the guard.
  Done when: a SKILL.md from anthropics/skills, an agent file from a claude-code plugin, and a hand-written folder all load through the same function in a fixture, and a script in any of them is refused unless the guard allows it.

- **Make "automatically" a weekly diff, never a silent install** — FEATURE — value 4 — effort S — risk low — category: integration
  Why: the user wants Foreman to "find, adopt and keep up with" the six repos, and the constraints say third-party code runs nothing unguarded. `fm scout` already watches Claude Code releases. Extending it to write one page per week (new, renamed, changed assets, licence class) satisfies "automatic" without trust risk. Assumption: a text diff is enough to decide adoption.
  Done when: running scout against two fixture snapshots of marketplace.json prints exactly the added and renamed plugins and changes no installed file.

- **Replace the models.json / code.toml split with one rule: a runner is a command line** — CLEAN — value 3 — effort M — risk med — category: config
  Why: runners today come from a CLI registry, `models.json` endpoints and the user's `code.toml`. An endpoint becomes `fm-http URL MODEL` (a small built-in command), so everything is a command and everything shares the lean-profile and stall-watch path. Assumption: the endpoint path doesn't need in-process state.
  Done when: an OpenAI-compatible endpoint configured as a command line runs a full fm code task, and a test shows endpoint and CLI runners emit the same stalled/heartbeat events.

- **Finish the half-built before starting anything new** — CLEAN — value 4 — effort M — risk low — category: scope
  Why: 29 round-1 briefs are "planned but not built", while the queue also holds the blocked trio (T-0335–0337), T-1207 and about ten deferred "Later from" clusters. Mark each brief as a reader of the run directory, a UI item, or cut. Anything that depends on nothing buildable gets deleted from the queue with a one-line reason.
  Done when: the 29 are partitioned into at most 6 live briefs plus a list of deletions, and `fm task ls` shows no open FEATURE older than this round without a dependency.

- **Show one status line that reuses the stall classifier** — FEATURE — value 3 — effort S — risk low — category: TUI
  Why: the user's complaint was "it just isn't doing anything", and T-1336 already classifies stalls. One bottom line, "alive: last tool use 4s ago" or "silent 130s: likely a permission prompt", is shared by the TUI, `--plain` and `fm doctor`, so that complaint can't recur unseen.
  Done when: the same string is produced by a TUI snapshot, a `--plain` run and `fm code why` for a fake runner that goes silent.

- **Wild: Treat "etc." as a counted budget** — FEATURE — value 4 — effort S — risk low — category: mandate
  Why: the user repeats "etc.", "recursive until dry" and "don't stop until complete". Read that as one round of N items chosen by the user's own repeated verbs, ending with a "dry" receipt that lists what was left out and why. Assumption: a visible stop condition satisfies "don't stop" better than an open loop.
  Done when: a mandate containing "etc." produces a run that stops at the budget, writes `dry.md` naming the unbuilt items, and a second invocation continues from that file.

- **Wild: Give the home screen a mail-style inbox of runs, not cards** — FEATURE — value 3 — effort M — risk low — category: TUI
  Why: tasks, runs, blocked items and asks across projects are all "things waiting for me". A single list, newest first, with unread = changed since last seen, handles 90% of the home screen with the Maildir layout from the first idea. Assumption: the project-deck design would add a second mental model.
  Done when: the home screen is one sorted list whose rows come from the run directories, and marking a row read persists across restarts.

- **Wild: Ship the whole harness as a one-file `fm.pyz` that is also its own docs** — FEATURE — value 3 — effort M — risk med — category: packaging
  Why: "work with anything" includes machines without the plugin; the stdlib-only constraint makes a zipapp realistic. `fm.pyz --help` reads the same registry that tests check, so the docs and the artifact can't drift.
  Done when: copying only `fm.pyz` to a clean directory and running `python3 fm.pyz code runners` works with no plugin installed.

- **Wild: Make the guard's verdict the only thing a third-party asset can set** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: adopted skills and plugins must run nothing unguarded. Rather than auditing each asset, every asset runs as a "hand" that only emits requested actions, and the guard decides each one. Assumption: assets that need arbitrary shell simply get refused and flagged.
  Done when: a fixture plugin that runs `curl | sh` in a hook is loaded, its action is refused and logged, and a benign formatter hook passes through the same path.
