# Brainstorm — lens: simplicity

- **Run drive, run, serve, night and session on one scheduler** — CLEAN — value 5 — effort L — risk high — category: architecture
  Why: the commands list shows five separate ways to keep working the queue. The drive is the Stop hook, `fm run` is headless, `fm serve` is Remote Control, `fm night` is budgeted background work and `fm session` is detached starts. Recent asks ("drive: long-lived jobs and an empty queue never leave a session idle", "offer queued work during background jobs") are the same idle-handling bug being fixed in one runner at a time. Assumption: they share little code today.
  Done when: one engine module owns "pick next unblocked task, budget it, run it, stop condition", the five commands are thin trigger adapters, and an idle-queue test passes through every adapter.

- **Make the fm CLI an implementation detail behind typed MCP tools** — FEATURE — value 4 — effort M — risk med — category: interface
  Why: guard refusals keep coming from fm invoked through bash, such as `fm focus T-0278 …; sed -i …` refused twice and `fm task new --focus && <edit>` dropped as YAGNI. `fm mcp` already exists, but it is read-only. Assumption: write tools can carry their own authorization, so the guard doesn't parse shell for them.
  Done when: focus, capture, checkpoint and task-done work as MCP calls in a Claude session, and the guard never sees an fm shell string in a replay of the session.

- **Require a sunset contract on every FEATURE brief** — FEATURE — value 4 — effort M — risk low — category: governance
  Why: there are 70+ commands, 72 skills, and open work that keeps adding more (T-0034, T-0035, T-0214, T-0217). Nothing says when a feature earns its place or goes. Assumption: `fm usage` is reliable enough to measure use.
  Done when: `fm task done` for a FEATURE is refused without "measure: X, remove if below Y by DATE", and `fm tidy` lists features past their date with their measured use.

- **Show a surface-cost estimate in every plan** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: the user pays for complexity in injected tokens, commands, settings and gate seconds. The plan step shows none of them. Assumption: the diff can be classified into those four buckets cheaply.
  Done when: a plan for a task that adds a command and a setting prints "+1 command, +1 setting, +N injected tokens, +S s gate" and the done card repeats the actual numbers.

- **Run a deprecation pipeline for commands and settings** — FEATURE — value 4 — effort M — risk low — category: lifecycle
  Why: "Collapse the command tree" and "prune unused surface" are open ideas with no safe way to remove a verb. Cryptic names (oracle, second, tour, surprise) also can't be renamed without breaking users and JARVIS-style downstream projects.
  Done when: `fm sunset <verb> --into <verb>` makes the old name an alias that warns for N releases and is then deleted, and `fm doctor` flags downstream projects still calling it.

- **Minimize the guard by replay delta-debugging** — CLEAN — value 4 — effort M — risk med — category: guard
  Why: the guard has grown by a patch per incident (T-0414, T-0421, T-0422, T-0275), and a 5000-command replay and real-bash differential tests already exist. Assumption: the rules are separable enough to disable one at a time.
  Done when: a script disables each rule in turn against the replay and differential corpus, lists the rules whose removal changes no verdict, and a merged PR removes at least one with an unchanged corpus result.

- **Gate module layering with an import graph** — CLEAN — value 3 — effort S — risk low — category: architecture
  Why: `plugin/lib` has 35 modules, and T-0166 shows a UI file stuck because its stateful helpers are tangled. Assumption: there are cycles or upward imports today.
  Done when: `fm check` fails on an import that crosses a declared layer or forms a cycle, and the current violations are fixed or baselined.

- **Prove install and uninstall are a byte-identical round trip** — FIX — value 3 — effort S — risk low — category: install
  Why: `install-user` and `uninstall-user` work from a manifest, and the installer touches `~/.claude`, plugins and a mod. A trust claim that uninstall leaves no trace should be tested, not asserted.
  Done when: a sandbox-HOME test hashes the tree before install, then installs and uninstalls, and the trees are identical, including with `--no-mod` and `--apply-conflicts`.

- **Add `fm wiring`, an X-ray of what is active right now** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: hooks, a mod, settings, standing grants, vetoes and per-harness adapters all shape a session, and "was it Foreman?" is hard to answer. Assumption: the user can't currently list all of them in one place.
  Done when: one command prints each active hook, grant, veto, plugin and adapter with its source file and the install step that put it there.

- **Wild: Reveal commands by use, so `fm help` shows only what you'd touch** — FEATURE — value 3 — effort M — risk low — category: progressive disclosure
  Why: assumption: a new user sees about 70 verbs and uses about 10. Help tiers already exist, but they are static.
  Done when: `fm help` lists the user's top-used verbs plus the next likely one for the current state, and `fm help --all` still shows everything.

- **Wild: Ablate whole subsystems against the user's own live work** — FEATURE — value 4 — effort L — risk med — category: evidence
  Why: `fm evolve` ablates instruction files on bench cases, but nobody tests whether a subsystem such as the night run, the court or the second read earns its cost in real use. Assumption: ledger outcomes are comparable across weeks.
  Done when: `fm ablate <subsystem> --weeks 2` turns it off for a window, compares first-pass rate, rework and cost against the prior window, and recommends keep or delete with the numbers.

- **Wild: Give Foreman a "monastery mode" that runs only guard, resume and done-gate** — FEATURE — value 3 — effort S — risk low — category: profile
  Why: assumption: those three are the core promise of the README, and the rest is optional. A named floor makes it easy to say what is optional.
  Done when: one setting disables everything else, the doctor confirms the core three still pass their tests in that profile, and the injected context drops measurably.
